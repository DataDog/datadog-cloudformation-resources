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
from datadog_api_client.v2 import OpenApiException

from datadog_api_client.v2.model.aws_account_create_request import AWSAccountCreateRequest
from datadog_api_client.v2.model.aws_account_update_request import AWSAccountUpdateRequest
from datadog_api_client.v2.model.aws_account_create_request_data import AWSAccountCreateRequestAttributes
from datadog_api_client.v2.model.aws_account_create_request_data import AWSAccountCreateRequestData
from datadog_api_client.v2.model.aws_account_update_request_data import AWSAccountUpdateRequestAttributes
from datadog_api_client.v2.model.aws_auth_config import AWSAuthConfig
from datadog_api_client.v2.model.aws_account_partition import AWSAccountPartition
from datadog_api_client.v2.model.aws_regions import AWSRegions
from datadog_api_client.v2.model.aws_logs_config import AWSLogsConfig
from datadog_api_client.v2.model.aws_metrics_config import AWSMetricsConfig
from datadog_api_client.v2.model.aws_resource_config import AWSResourcesConfig #TODO: check if this is the right import
from datadog_api_client.v2.model.aws_traces_config import AWSTracesConfig
from datadog_api_client.v2.model.aws_auth_config_keys import AWSAuthConfigKeys
from datadog_api_client.v2.model.aws_auth_config_role import AWSAuthConfigRole
from datadog_api_client.v2.model.aws_regions_include_all import AWSRegionsIncludeAll
from datadog_api_client.v2.model.aws_regions_include_only import AWSRegionsIncludeOnly
from datadog_api_client.v2.model.aws_namespace_filters_exclude_only import AWSNamespaceFiltersExcludeOnly
from datadog_api_client.v2.model.aws_namespace_filters_include_only import AWSNamespaceFiltersIncludeOnly
from datadog_api_client.v2.model.aws_namespace_tag_filter import AWSNamespaceTagFilter
from datadog_api_client.v2.model.aws_lambda_forwarder_config import AWSLambdaForwarderConfig
from datadog_api_client.v2.model.x_ray_services_list import XRayServicesList
from datadog_api_client.v2.model.x_ray_services_include_all import XRayServicesIncludeAll
from datadog_api_client.v2.model.x_ray_services_include_only import XRayServicesIncludeOnly
from datadog_api_client.v2.model.aws_account_update_request_data import AWSAccountUpdateRequestData
from datadog_api_client.v2.model.aws_account_response_attributes import AWSAccountResponseAttributes

from datadog_api_client.v2.api.aws_integration_api import AWSIntegrationApi
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

resource = Resource(TYPE_NAME, ResourceModel, TypeConfigurationModel)
test_entrypoint = resource.test_entrypoint


def build_aws_account_from_model(
        api_request_data: AWSAccountCreateRequestAttributes | AWSAccountUpdateRequestAttributes, 
        desired_state_model: ResourceModel) -> AWSAccountCreateRequestAttributes | AWSAccountUpdateRequestAttributes:
    if desired_state_model.AccountID is not None:
        api_request_data.aws_account_id = desired_state_model.AccountID

    if desired_state_model.AWSPartition is not None:
        api_request_data.aws_partition = AWSAccountPartition(partition=desired_state_model.AWSPartition)

    if desired_state_model.RoleName is not None:
        api_request_data.auth_config = AWSAuthConfigRole(
            role=AWSAuthConfigRole(
                role_name=desired_state_model.RoleName,
            )
        )

    if desired_state_model.AccountTags is not None:
        api_request_data.account_tags = list(desired_state_model.AccountTags)

    if desired_state_model.IncludedRegions is not None:
        api_request_data.aws_regions = AWSRegionsIncludeOnly(
                include_only=desired_state_model.IncludedRegions
        )

    api_request_data.metrics_config = AWSMetricsConfig()
    new_metrics_config = AWSMetricsConfig()
    metrics_config_updated = False
    if desired_state_model.MetricsCollection is not None:
        new_metrics_config.enabled = desired_state_model.MetricsCollection
        metrics_config_updated = True

    if desired_state_model.CollectCustomMetrics is not None:
        new_metrics_config.custom_metrics = desired_state_model.CollectCustomMetrics
        metrics_config_updated = True

    if desired_state_model.AutomuteEnabled is not None: 
        new_metrics_config.automute_enabled = desired_state_model.AutomuteEnabled
        metrics_config_updated = True

    if desired_state_model.CollectCloudwatchAllarms is not None:
        new_metrics_config.collect_cloudwatch_alarms = desired_state_model.CollectCloudwatchAllarms
        metrics_config_updated = True

    if desired_state_model.FilterTags is not None:
        api_request_tag_filters = []
        for namespace, tag_filter_str in desired_state_model.FilterTags:
            api_request_tag_filters.append(AWSNamespaceTagFilter(
                namespace=namespace,
                tags=tag_filter_str
            ))
        new_metrics_config.tag_filters = api_request_tag_filters
        metrics_config_updated = True

    if desired_state_model.IncludeListedNamespaces is not None:
        if desired_state_model.FilterNamespaces is not None:
            if desired_state_model.IncludeListedNamespaces:
                new_metrics_config.namespace_filters = AWSNamespaceFiltersIncludeOnly(
                    include_only=desired_state_model.FilterNamespaces
                )
            else:
                new_metrics_config.namespace_filters = AWSNamespaceFiltersExcludeOnly(
                    exclude_only=desired_state_model.FilterNamespaces
                )
            metrics_config_updated = True

    if metrics_config_updated:
        api_request_data.metrics_config = new_metrics_config
    
    logs_config = AWSLogsConfig(lambda_forwarder_config=AWSLambdaForwarderConfig())
    if desired_state_model.LogForwarderLambdas is not None:
        logs_config.lambda_forwarder_config.lambda_forwarder.lambdas = desired_state_model.Lambdas
        api_request_data.logs_config = logs_config
    if desired_state_model.LogForwarderSources is not None:
        logs_config.lambda_forwarder_config.lambda_forwarder.sources = desired_state_model.LogForwarderSources
        api_request_data.logs_config = logs_config

    resources_config = AWSResourcesConfig()
    if desired_state_model.CSPMResourceCollection is not None:
        resources_config.cloud_security_posture_management_collection = desired_state_model.CSPMResourceCollection
        api_request_data.resources_config = resources_config
    if desired_state_model.ExtendedResourceCollection is not None:
        api_request_data.resources_config.extended_collection = desired_state_model.ExtendedResourceCollection
        api_request_data.resources_config = resources_config

    return api_request_data

def build_model_from_aws_account(aws_account: AWSAccountResponseAttributes) -> ResourceModel:
    
    model = ResourceModel()

    if aws_account.aws_account_id is not None:
        model.AccountID = aws_account.aws_account_id

    if aws_account.auth_config is not None:
        if aws_account.auth_config.role is not None:
            model.RoleName = aws_account.auth_config.role.role_name
            model.ExternalIDSecretName = aws_account.auth_config.role.external_id

    if aws_account.account_tags is not None:
        model.AccountTags = aws_account.account_tags

    if aws_account.aws_regions is not None:
        if aws_account.aws_regions.include_only is not None:
            model.IncludedRegions = aws_account.aws_regions.include_only

    if aws_account.metrics_config is not None:
        if aws_account.metrics_config.enabled is not None:
            model.MetricsCollection = aws_account.metrics_config.enabled
        if aws_account.metrics_config.custom_metrics is not None:
            model.CollectCustomMetrics = aws_account.metrics_config.custom_metrics
        if aws_account.metrics_config.automute_enabled is not None:
            model.AutomuteEnabled = aws_account.metrics_config.automute_enabled
        if aws_account.metrics_config.collect_cloudwatch_alarms is not None:
            model.CollectCloudwatchAllarms = aws_account.metrics_config.collect_cloudwatch_alarms
        if aws_account.metrics_config.tag_filters is not None:
            model.FilterTags = {}
            for tag_filter in aws_account.metrics_config.tag_filters:
                model.FilterTags[tag_filter.namespace] = tag_filter.tags
        if aws_account.metrics_config.namespace_filters is not None:
            if aws_account.metrics_config.namespace_filters.include_only is not None:
                model.IncludeListedNamespaces = True
                model.FilterNamespaces = aws_account.metrics_config.namespace_filters.include_only
            elif aws_account.metrics_config.namespace_filters.exclude_only is not None:
                model.IncludeListedNamespaces = False
                model.FilterNamespaces = aws_account.metrics_config.namespace_filters.exclude_only
    
    if aws_account.logs_config is not None:
        if aws_account.logs_config.lambda_forwarder_config is not None:
            if aws_account.logs_config.lambda_forwarder_config.lambda_forwarder.lambdas is not None:
                model.LogForwarderLambdas = aws_account.logs_config.lambda_forwarder_config.lambda_forwarder.lambdas
            if aws_account.logs_config.lambda_forwarder_config.lambda_forwarder.sources is not None:
                model.LogForwarderSources = aws_account.logs_config.lambda_forwarder_config.lambda_forwarder.sources

    if aws_account.resources_config is not None:
        if aws_account.resources_config.cloud_security_posture_management_collection is not None:
            model.CSPMResourceCollection = aws_account.resources_config.cloud_security_posture_management_collection
        if aws_account.resources_config.extended_collection is not None:
            model.ExtendedResourceCollection = aws_account.resources_config.extended_collection

    return model


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

    aws_account_request_attributes = build_aws_account_from_model(AWSAccountCreateRequestAttributes(), model)
    with client(
        type_configuration.DatadogCredentials.ApiKey,
        type_configuration.DatadogCredentials.ApplicationKey,
        type_configuration.DatadogCredentials.ApiURL,
        TELEMETRY_TYPE_NAME,
        __version__,
    ) as api_client:
        api_instance = AWSIntegrationApi(api_client)
        try:
            response = api_instance.create_aws_account(AWSAccountCreateRequest(data=AWSAccountCreateRequestData(attributes=aws_account_request_attributes)))
        except OpenApiException as e:
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
    response_external_id = response.data.attributes.auth_config.role.external_id
    boto_client = session.client("secretsmanager")
    boto_client.create_secret(
        Description="The external_id associated with your Datadog AWS Integration.",
        Name=secret_name,
        SecretString='{"external_id":"%s"}' % response_external_id,
    )

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

    aws_account_request_attributes = build_aws_account_from_model(AWSAccountUpdateRequestAttributes(), model)
    if not model.UUID:
        LOG.error("Cannot update non existent resource")
        return ProgressEvent(
            status=OperationStatus.FAILED,
            resourceModel=model,
            message="Cannot update non existent resource",
            errorCode=HandlerErrorCode.NotFound,
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
            api_instance.update_aws_account(model.UUID, AWSAccountUpdateRequest(data=AWSAccountUpdateRequestData(attributes=aws_account_request_attributes)))
        except OpenApiException as e:
            LOG.exception("Exception when calling AWSIntegrationApi->update_aws_account: %s\n", e)
            error_code = http_to_handler_error_code(e.status)
            if e.status == 400 and "errors" in e.body and any("does not exist" in s for s in e.body["errors"]):
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
        kwargs = {
            "aws_account_config_id": model.AccountID
        }
        with client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
        ) as api_client:
            api_instance = AWSIntegrationApi(api_client)
            try:
                api_instance.delete_aws_account(**kwargs)
            except OpenApiException as e:
                LOG.exception("Exception when calling AWSIntegrationApi->delete_aws_account: %s\n", e)
                error_code = http_to_handler_error_code(e.status)
                if e.status == 400 and "errors" in e.body and any("does not exist" in s for s in e.body["errors"]):
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
        try:
            if model.AWSAccountID is None:
                return ProgressEvent(
                    status=OperationStatus.FAILED,
                    resourceModel=model,
                    message="No AWSAccountID set, resource never created",
                    errorCode=HandlerErrorCode.NotFound,
                )
            kwargs = {
                "aws_account_id": model.AWSAccountID
            }
            aws_account = api_instance.list_aws_accounts(**kwargs).data[0]
        except OpenApiException as e:
            LOG.exception("Exception when calling AWSIntegrationApi->list_aws_accounts: %s\n", e)
            error_code = http_to_handler_error_code(e.status)
            if e.status == 400 and "errors" in e.body and any("does not exist" in s for s in e.body["errors"]):
                error_code = HandlerErrorCode.NotFound
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error getting AWS account: {e}",
                errorCode=error_code,
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
                f"Was it updated outside of AWS CloudFormation ?",
                errorCode=HandlerErrorCode.NotFound,
            )
        
    model = build_model_from_aws_account(aws_account.attributes)
    model.UUID = aws_account.id

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )
