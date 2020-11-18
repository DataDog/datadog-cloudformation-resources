import logging
from typing import Any, MutableMapping, Optional

from cloudformation_cli_python_lib import (
    Action,
    OperationStatus,
    ProgressEvent,
    Resource,
    SessionProxy,
)
from datadog_api_client.v1 import ApiException
from datadog_api_client.v1.api.aws_integration_api import AWSIntegrationApi
from datadog_api_client.v1.model.aws_account import AWSAccount
from datadog_cloudformation_common.api_clients import v1_client

from .models import ResourceHandlerRequest, ResourceModel
from .version import __version__

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "Datadog::Integrations::AWS"
TELEMETRY_TYPE_NAME = "integrations-aws"

resource = Resource(TYPE_NAME, ResourceModel)
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
    return aws_account


@resource.handler(Action.CREATE)
def create_handler(
        session: Optional[SessionProxy],
        request: ResourceHandlerRequest,
        callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    LOG.info("Starting %s Create Handler", TYPE_NAME)
    model = request.desiredResourceState

    aws_account = build_aws_account_from_model(model)
    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = AWSIntegrationApi(api_client)
        try:
            api_instance.create_aws_account(aws_account)
        except ApiException as e:
            LOG.error("Exception when calling AWSIntegrationApi->create_aws_account: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED, resourceModel=model, message=f"Error creating AWS account: {e}"
            )

    model.IntegrationID = get_integration_id(model.AccountID, model.RoleName, model.AccessKeyID)

    return read_handler(session, request, callback_context)


@resource.handler(Action.UPDATE)
def update_handler(
        session: Optional[SessionProxy],
        request: ResourceHandlerRequest,
        callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    LOG.info("Starting %s Update Handler", TYPE_NAME)
    model = request.desiredResourceState

    aws_account = build_aws_account_from_model(model)
    if get_integration_id(model.AccountID, model.RoleName, model.AccessKeyID) != model.IntegrationID:
        LOG.error(
            f"Cannot update `account_id`, `role_name` or `access_key_id` using this resource. "
            f"Please delete it and create a new one instead."
        )
        return ProgressEvent(
            status=OperationStatus.FAILED,
            resourceModel=model,
            message=f"Cannot update `account_id`, `role_name` or `access_key_id` using this resource. "
                    f"Please delete it and create a new one instead."
        )
    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = AWSIntegrationApi(api_client)
        try:
            api_instance.update_aws_account(
                aws_account,
                account_id=model.AccountID,
                role_name=model.RoleName,
                access_key_id=model.AccessKeyID,
            )
        except ApiException as e:
            LOG.error("Exception when calling AWSIntegrationApi->update_aws_account: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED, resourceModel=model, message=f"Error updating AWS account: {e}"
            )

    return read_handler(session, request, callback_context)


@resource.handler(Action.DELETE)
def delete_handler(
        session: Optional[SessionProxy],
        request: ResourceHandlerRequest,
        callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState

    aws_account = build_aws_account_from_model(model)

    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = AWSIntegrationApi(api_client)
        try:
            api_instance.delete_aws_account(aws_account)
        except ApiException as e:
            LOG.error("Exception when calling AWSIntegrationApi->delete_aws_account: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED, resourceModel=model, message=f"Error deleting AWS account: {e}"
            )

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=None,
    )


@resource.handler(Action.READ)
def read_handler(
        session: Optional[SessionProxy],
        request: ResourceHandlerRequest,
        callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState

    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = AWSIntegrationApi(api_client)
        try:
            aws_account = api_instance.list_aws_accounts(
                account_id=model.AccountID,
                role_name=model.RoleName,
                access_key_id=model.AccessKeyID
            ).accounts[0]
        except ApiException as e:
            LOG.error("Exception when calling AWSIntegrationApi->list_aws_accounts: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED, resourceModel=model, message=f"Error getting AWS account: {e}"
            )
        except IndexError:
            LOG.error(
                f"Account with integration ID '{model.IntegrationID}' not found. "
                f"Was it updated outside of AWS CloudFormation ?"
            )
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Account with integration ID '{model.IntegrationID}' not found. "
                        f"Was it updated outside of AWS CloudFormation ?"
            )

    model.HostTags = aws_account.host_tags
    model.FilterTags = aws_account.filter_tags
    model.AccountSpecificNamespaceRules = aws_account.account_specific_namespace_rules

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )


@resource.handler(Action.LIST)
def list_handler(
        session: Optional[SessionProxy],
        request: ResourceHandlerRequest,
        callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    # TODO: put code here
    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModels=[],
    )


def get_integration_id(account_id, role_name, access_key_id):
    return f"{account_id}:{role_name}:{access_key_id}"
