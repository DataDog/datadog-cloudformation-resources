import logging
from typing import Any, MutableMapping, Optional

from cloudformation_cli_python_lib import (
    Action,
    OperationStatus,
    ProgressEvent,
    Resource,
    SessionProxy,
    HandlerErrorCode,
)
from datadog_api_client.v1 import ApiException
from datadog_api_client.v1.api.aws_integration_api import AWSIntegrationApi
from datadog_api_client.v1.model.aws_account import AWSAccount
from datadog_api_client.v1.model.aws_account_delete_request import AWSAccountDeleteRequest
from datadog_cloudformation_common.api_clients import client
from datadog_cloudformation_common.utils import errors_handler, http_to_handler_error_code

from .models import ResourceHandlerRequest, ResourceModel, TypeConfigurationModel
from .version import __version__

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "Datadog::Integrations::AWS"
TELEMETRY_TYPE_NAME = "integrations-aws"
DEFAULT_SECRET_NAME = "DatadogIntegrationExternalID"
MAX_DELETE_SECRET_RETRIES = 30
DELETE_SECRET_CALLBACK_INTERVAL = 2
MAX_RETRY_COUNT = 5
RETRY_SLEEP_INTERVAL = 5

resource = Resource(TYPE_NAME, ResourceModel, TypeConfigurationModel)
test_entrypoint = resource.test_entrypoint


def build_aws_account_from_model(model):
    aws_account = AWSAccount()
    if model.AccountID is not None:
        aws_account.account_id = model.AccountID
    if model.RoleName is not None:
        aws_account.role_name = model.RoleName
    if model.AccessKeyID is not None:
        aws_account.access_key_id = model.AccessKeyID
    if model.HostTags is not None:
        aws_account.host_tags = model.HostTags
    if model.FilterTags is not None:
        aws_account.filter_tags = model.FilterTags
    if model.AccountSpecificNamespaceRules is not None:
        aws_account.account_specific_namespace_rules = model.AccountSpecificNamespaceRules
    if model.MetricsCollection is not None:
        aws_account.metrics_collection_enabled = model.MetricsCollection
    if model.CSPMResourceCollection is not None:
        aws_account.cspm_resource_collection_enabled = model.CSPMResourceCollection
    if model.ResourceCollection is not None:
        aws_account.resource_collection_enabled = model.ResourceCollection
    if model.ExcludedRegions is not None:
        aws_account.excluded_regions = model.ExcludedRegions
    return aws_account


@resource.handler(Action.CREATE)
@errors_handler
def create_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    LOG.info("Starting %s Create Handler", TYPE_NAME)
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration

    aws_account = build_aws_account_from_model(model)
    with client(
        type_configuration.DatadogCredentials.ApiKey,
        type_configuration.DatadogCredentials.ApplicationKey,
        type_configuration.DatadogCredentials.ApiURL,
        TELEMETRY_TYPE_NAME,
        __version__,
    ) as api_client:
        api_instance = AWSIntegrationApi(api_client)
        try:
            response = api_instance.create_aws_account(aws_account)
        except ApiException as e:
            LOG.exception("Exception when calling AWSIntegrationApi->create_aws_account: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error creating AWS account: {e}",
                errorCode=http_to_handler_error_code(e.status),
            )
    if model.ExternalIDSecretName is not None:
        secret_name = model.ExternalIDSecretName
    else:
        secret_name = DEFAULT_SECRET_NAME
    boto_client = session.client("secretsmanager")
    boto_client.create_secret(
        Description="The external_id associated with your Datadog AWS Integration.",
        Name=secret_name,
        SecretString='{"external_id":"%s"}' % response.external_id,
    )

    model.IntegrationID = get_integration_id(model.AccountID, model.RoleName, model.AccessKeyID)

    return read_handler(session, request, callback_context)


@resource.handler(Action.UPDATE)
@errors_handler
def update_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    LOG.info("Starting %s Update Handler", TYPE_NAME)
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration

    aws_account = build_aws_account_from_model(model)
    if not model.IntegrationID:
        LOG.error("Cannot update non existent resource")
        return ProgressEvent(
            status=OperationStatus.FAILED,
            resourceModel=model,
            message="Cannot update non existent resource",
            errorCode=HandlerErrorCode.NotFound,
        )
    if get_integration_id(model.AccountID, model.RoleName, model.AccessKeyID) != model.IntegrationID:
        LOG.error(
            "Cannot update `account_id`, `role_name` or `access_key_id` using this resource. "
            "Please delete it and create a new one instead."
        )
        return ProgressEvent(
            status=OperationStatus.FAILED,
            resourceModel=model,
            message="Cannot update `account_id`, `role_name` or `access_key_id` using this resource. "
            "Please delete it and create a new one instead.",
            errorCode=HandlerErrorCode.NotUpdatable,
        )
    with client(
        type_configuration.DatadogCredentials.ApiKey,
        type_configuration.DatadogCredentials.ApplicationKey,
        type_configuration.DatadogCredentials.ApiURL,
        TELEMETRY_TYPE_NAME,
        __version__,
    ) as api_client:
        api_instance = AWSIntegrationApi(api_client)
        try:
            kwargs = {}
            if model.AccountID is not None:
                kwargs["account_id"] = model.AccountID
            if model.RoleName is not None:
                kwargs["role_name"] = model.RoleName
            if model.AccessKeyID is not None:
                kwargs["access_key_id"] = model.AccessKeyID
            api_instance.update_aws_account(aws_account, **kwargs)
        except ApiException as e:
            LOG.exception("Exception when calling AWSIntegrationApi->update_aws_account: %s\n", e)
            error_code = http_to_handler_error_code(e.status)
            if (
                e.status == 400
                and "errors" in e.body
                and (
                    any("does not exist" in s for s in e.body["errors"])
                    or any("not yet installed" in s for s in e.body["errors"])
                )
            ):
                error_code = HandlerErrorCode.NotFound
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error updating AWS account: {e}",
                errorCode=error_code,
            )

    return read_handler(session, request, callback_context)


@resource.handler(Action.DELETE)
@errors_handler
def delete_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration

    if model.ExternalIDSecretName is not None:
        secret_name = model.ExternalIDSecretName
    else:
        secret_name = DEFAULT_SECRET_NAME
    boto_client = session.client("secretsmanager")
    callback_count = callback_context.get("callback_count", 0)

    if 0 < callback_count <= MAX_DELETE_SECRET_RETRIES:
        LOG.info(f"Checking deletion of secret {secret_name}")
        try:
            boto_client.describe_secret(SecretId=secret_name)
        except boto_client.exceptions.ResourceNotFoundException:
            return ProgressEvent(
                status=OperationStatus.SUCCESS,
                resourceModel=None,
            )
    elif callback_count > MAX_DELETE_SECRET_RETRIES:
        return ProgressEvent(
            status=OperationStatus.FAILED, message=f"Error deleting AWS Account: failed to delete secret {secret_name}"
        )
    else:
        kwargs = {}
        if model.AccountID is not None:
            kwargs["account_id"] = model.AccountID
        if model.RoleName is not None:
            kwargs["role_name"] = model.RoleName
        if model.AccessKeyID is not None:
            kwargs["access_key_id"] = model.AccessKeyID
        delete_request = AWSAccountDeleteRequest(**kwargs)

        with client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
        ) as api_client:
            api_instance = AWSIntegrationApi(api_client)
            try:
                api_instance.delete_aws_account(delete_request)
            except ApiException as e:
                LOG.exception("Exception when calling AWSIntegrationApi->delete_aws_account: %s\n", e)
                error_code = http_to_handler_error_code(e.status)
                if (
                    e.status == 400
                    and "errors" in e.body
                    and (
                        any("does not exist" in s for s in e.body["errors"])
                        or any("not yet installed" in s for s in e.body["errors"])
                    )
                ):
                    error_code = HandlerErrorCode.NotFound
                return ProgressEvent(
                    status=OperationStatus.FAILED,
                    resourceModel=model,
                    message=f"Error deleting AWS account: {e}",
                    errorCode=error_code,
                )

        boto_client.delete_secret(
            SecretId=secret_name,
            ForceDeleteWithoutRecovery=True,
        )

    return ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
        callbackContext={"callback_count": callback_count + 1},
        callbackDelaySeconds=DELETE_SECRET_CALLBACK_INTERVAL,
    )


@resource.handler(Action.READ)
@errors_handler
def read_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration

    with client(
        type_configuration.DatadogCredentials.ApiKey,
        type_configuration.DatadogCredentials.ApplicationKey,
        type_configuration.DatadogCredentials.ApiURL,
        TELEMETRY_TYPE_NAME,
        __version__,
    ) as api_client:
        api_instance = AWSIntegrationApi(api_client)

        if model.IntegrationID is None:
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message="No IntegrationID set, resource never created",
                errorCode=HandlerErrorCode.NotFound,
            )

        account_id, role_name, access_key_id = parse_integration_id(model.IntegrationID)
        kwargs = {}
        if account_id is not None:
            kwargs["account_id"] = account_id
        if role_name is not None:
            kwargs["role_name"] = role_name
        if access_key_id is not None:
            kwargs["access_key_id"] = access_key_id

        retry_count = 0
        aws_account = error_code = exception = None
        while retry_count < MAX_RETRY_COUNT:
            LOG.warning("Retry count %s, err: %s", retry_count, exception)
            retry_count += 1
            try:
                aws_account = api_instance.list_aws_accounts(**kwargs).accounts[0]
                exception = None
                error_code = None
                break
            except ApiException as e:
                exception = e
                if (
                    e.status == 400
                    and "errors" in e.body
                    and (
                        any("does not exist" in s for s in e.body["errors"])
                        or any("not yet installed" in s for s in e.body["errors"])
                    )
                ):
                    error_code = HandlerErrorCode.NotFound
                    continue
                else:
                    break
            except IndexError as e:
                exception = e
                error_code = HandlerErrorCode.NotFound
                continue

        if exception is not None:
            if isinstance(exception, ApiException):
                LOG.error(
                    f"Account with integration ID '{model.IntegrationID}' not found. "
                    f"Was it updated outside of AWS CloudFormation ?"
                )
                return ProgressEvent(
                    status=OperationStatus.FAILED,
                    resourceModel=model,
                    message=f"Account with integration ID '{model.IntegrationID}' not found. "
                    f"Was it updated outside of AWS CloudFormation ?",
                    errorCode=error_code,
                )
            if isinstance(exception, IndexError):
                LOG.error(
                    f"Account with integration ID '{model.IntegrationID}' not found. "
                    f"Was it updated outside of AWS CloudFormation ?"
                )
                return ProgressEvent(
                    status=OperationStatus.FAILED,
                    resourceModel=model,
                    message=f"Account with integration ID '{model.IntegrationID}' not found. "
                    f"Was it updated outside of AWS CloudFormation ?",
                    errorCode=error_code,
                )

    model.HostTags = aws_account.host_tags
    model.FilterTags = aws_account.filter_tags
    model.AccountSpecificNamespaceRules = aws_account.account_specific_namespace_rules
    model.ExcludedRegions = aws_account.excluded_regions
    model.MetricsCollection = aws_account.metrics_collection_enabled
    model.CSPMResourceCollection = aws_account.cspm_resource_collection_enabled
    model.ResourceCollection = aws_account.resource_collection_enabled

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )


def get_integration_id(account_id, role_name, access_key_id):
    return f"{account_id}:{role_name}:{access_key_id}"


def parse_integration_id(integration_id):
    ret = []
    parts = integration_id.split(":")
    for part in parts:
        if part != "None":
            ret.append(part)
        else:
            ret.append(None)
    return ret
