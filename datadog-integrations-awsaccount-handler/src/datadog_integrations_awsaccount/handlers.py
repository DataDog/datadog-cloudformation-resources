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
from datadog_cloudformation_common.api_clients import client
from datadog_cloudformation_common.utils import (
    errors_handler,
    http_to_handler_error_code,
)

from .models import (
    ResourceHandlerRequest,
    ResourceModel,
    TypeConfigurationModel,
    MetricsConfig,
    TagFilters,
    LogsConfig,
    ResourcesConfig,
    LambdaForwarder,
    AWSRegions,
    NamespaceFilters,
    TracesConfig,
    XRayServices,
    AuthConfig,
)
from .version import __version__

from datadog_api_client.v2.model.aws_account_partition import AWSAccountPartition
from datadog_api_client.v2.model.aws_logs_config import AWSLogsConfig
from datadog_api_client.v2.model.aws_metrics_config import AWSMetricsConfig
from datadog_api_client.v2.model.aws_resources_config import AWSResourcesConfig
from datadog_api_client.v2.model.aws_auth_config_role import AWSAuthConfigRole
from datadog_api_client.v2.model.aws_regions_include_only import AWSRegionsIncludeOnly
from datadog_api_client.v2.model.aws_regions_include_all import AWSRegionsIncludeAll
from datadog_api_client.v2.model.aws_namespace_tag_filter import AWSNamespaceTagFilter
from datadog_api_client.v2.model.x_ray_services_include_all import (
    XRayServicesIncludeAll,
)
from datadog_api_client.v2.model.x_ray_services_include_only import (
    XRayServicesIncludeOnly,
)
from datadog_api_client.v2.model.aws_namespace_filters_include_only import (
    AWSNamespaceFiltersIncludeOnly,
)
from datadog_api_client.v2.model.aws_namespace_filters_exclude_only import (
    AWSNamespaceFiltersExcludeOnly,
)
from datadog_api_client.v2.model.aws_lambda_forwarder_config import (
    AWSLambdaForwarderConfig,
)
from datadog_api_client.v2.model.aws_traces_config import AWSTracesConfig

from datadog_api_client.v2.model.aws_account_create_request import (
    AWSAccountCreateRequest,
)
from datadog_api_client.v2.model.aws_account_create_request_data import (
    AWSAccountCreateRequestData,
)
from datadog_api_client.v2.model.aws_account_create_request_attributes import (
    AWSAccountCreateRequestAttributes,
)

from datadog_api_client.v2.model.aws_account_update_request import (
    AWSAccountUpdateRequest,
)
from datadog_api_client.v2.model.aws_account_update_request_data import (
    AWSAccountUpdateRequestData,
)
from datadog_api_client.v2.model.aws_account_update_request_attributes import (
    AWSAccountUpdateRequestAttributes,
)


from datadog_api_client.v2.api.aws_integration_api import (
    AWSIntegrationApi as V2AWSIntegrationApi,
)

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "Datadog::Integrations::AWSAccount"
TELEMETRY_TYPE_NAME = "integrations-awsaccount"
DEFAULT_SECRET_NAME = "ExternalIDSecretName"
MAX_DELETE_SECRET_RETRIES = 30
DELETE_SECRET_CALLBACK_INTERVAL = 2

resource = Resource(TYPE_NAME, ResourceModel, TypeConfigurationModel)
test_entrypoint = resource.test_entrypoint


def build_api_request_from_model(api_request_data_generator, desired_state_model):
    new_aws_regions = None
    if desired_state_model.AWSRegions is not None:
        desired_aws_regions = desired_state_model.AWSRegions
        if desired_aws_regions.IncludeAll:
            new_aws_regions = AWSRegionsIncludeAll(include_all=True)
        if desired_aws_regions.IncludeOnly is not None:
            new_aws_regions = AWSRegionsIncludeOnly(include_only=desired_aws_regions.IncludeOnly)

    new_metrics_config = None
    if desired_state_model.MetricsConfig is not None:
        desired_metrics_config = desired_state_model.MetricsConfig
        new_tag_filters = None
        if desired_metrics_config.TagFilters is not None:
            new_tag_filters = []
            for tag_filter in desired_metrics_config.TagFilters:
                new_tag_filters.append(AWSNamespaceTagFilter(namespace=tag_filter.Namespace, tags=tag_filter.Tags))

        new_namespace_filters = None
        if desired_metrics_config.NamespaceFilters is not None:
            if desired_metrics_config.NamespaceFilters.IncludeOnly is not None:
                new_namespace_filters = AWSNamespaceFiltersIncludeOnly(
                    include_only=desired_metrics_config.NamespaceFilters.IncludeOnly
                )
            if desired_metrics_config.NamespaceFilters.ExcludeOnly is not None:
                new_namespace_filters = AWSNamespaceFiltersExcludeOnly(
                    exclude_only=desired_metrics_config.NamespaceFilters.ExcludeOnly
                )

        new_metrics_config = AWSMetricsConfig(
            enabled=desired_metrics_config.Enabled,
            automute_enabled=desired_metrics_config.AutomuteEnabled,
            collect_custom_metrics=desired_metrics_config.CollectCustomMetrics,
            collect_cloudwatch_alarms=desired_metrics_config.CollectCloudwatchAlarms,
            tag_filters=new_tag_filters,
            namespace_filters=new_namespace_filters,
        )

    new_logs_config = None
    if desired_state_model.LogsConfig is not None:
        new_lambda_forwarder_config = None
        if desired_state_model.LogsConfig.LambdaForwarder is not None:
            forwarder_desired_config = desired_state_model.LogsConfig.LambdaForwarder
            new_lambda_forwarder_config = AWSLambdaForwarderConfig(
                lambdas=forwarder_desired_config.Lambdas,
                sources=forwarder_desired_config.Sources,
            )
        new_logs_config = AWSLogsConfig(lambda_forwarder=new_lambda_forwarder_config)

    new_resources_config = None
    if desired_state_model.ResourcesConfig is not None:
        resources_desired_config = desired_state_model.ResourcesConfig
        new_resources_config = AWSResourcesConfig(
            cloud_security_posture_management_collection=resources_desired_config.CSPMResourceCollection,
            extended_collection=resources_desired_config.ExtendedResourceCollection,
        )

    new_traces_config = None
    if desired_state_model.TracesConfig is not None:
        traces_desired_config = desired_state_model.TracesConfig
        new_xray_services = None
        if traces_desired_config.XRayServices is not None:
            xray_services_desired_config = traces_desired_config.XRayServices
            if xray_services_desired_config.IncludeAll:
                new_xray_services = XRayServicesIncludeAll(True)
            if xray_services_desired_config.IncludeOnly is not None:
                new_xray_services = XRayServicesIncludeOnly(xray_services_desired_config.IncludeOnly)
        new_traces_config = AWSTracesConfig(
            xray_services=new_xray_services,
        )

    return api_request_data_generator(
        aws_account_id=desired_state_model.AccountID,
        aws_partition=AWSAccountPartition(desired_state_model.AWSPartition),
        auth_config=AWSAuthConfigRole(
            role_name=desired_state_model.AuthConfig.RoleName,
        ),
        account_tags=desired_state_model.AccountTags,
        aws_regions=new_aws_regions,
        metrics_config=new_metrics_config,
        logs_config=new_logs_config,
        resources_config=new_resources_config,
        traces_config=new_traces_config,
    )


def build_model_from_api_response(model, aws_account):
    model.AccountTags = aws_account.account_tags
    model.AuthConfig = AuthConfig(
        aws_account.auth_config.role_name,
    )
    if aws_account.get("aws_regions"):
        model.AWSRegions = AWSRegions(
            aws_account.aws_regions.get("include_only"),
            aws_account.aws_regions.get("include_all"),
        )
    if aws_account.get("metrics_config"):
        model.MetricsConfig = MetricsConfig(None, None, None, None, None, None)
        model.MetricsConfig.Enabled = aws_account.metrics_config.get("enabled")
        model.MetricsConfig.AutomuteEnabled = aws_account.metrics_config.get("automute_enabled")
        model.MetricsConfig.CollectCustomMetrics = aws_account.metrics_config.get("custom_metrics")
        model.MetricsConfig.CollectCloudwatchAlarms = aws_account.metrics_config.get("collect_cloudwatch_alarms")
        model.MetricsConfig.TagFilters = []
        if aws_account.metrics_config.get("tag_filters"):
            for tag_filter in aws_account.metrics_config.tag_filters:
                filter_tags = TagFilters(tag_filter.namespace, tag_filter.tags)
                model.MetricsConfig.TagFilters.append(filter_tags)
        if aws_account.metrics_config.get("namespace_filters", {}):
            model.MetricsConfig.NamespaceFilters = NamespaceFilters(
                aws_account.metrics_config.namespace_filters.get("include_only"),
                aws_account.metrics_config.namespace_filters.get("exclude_only"),
            )

    if aws_account.get("resources_config"):
        model.ResourcesConfig = ResourcesConfig(
            aws_account.resources_config.get("cloud_security_posture_management_collection"),
            aws_account.resources_config.get("extended_collection"),
        )
    if aws_account.get("logs_config"):
        model.LogsConfig = LogsConfig(None)
        if aws_account.logs_config.get("lambda_forwarder"):
            model.LogsConfig.LambdaForwarder = LambdaForwarder(
                aws_account.logs_config.lambda_forwarder.get("lambdas"),
                aws_account.logs_config.lambda_forwarder.get("sources"),
            )
    if aws_account.get("traces_config"):
        model.TracesConfig = TracesConfig(None)
        if aws_account.traces_config.get("xray_services"):
            model.TracesConfig.XRayServices = XRayServices(
                aws_account.traces_config.xray_services.get("include_only"),
                aws_account.traces_config.xray_services.get("include_all"),
            )

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

    aws_account = build_api_request_from_model(AWSAccountCreateRequestAttributes, model)

    with client(
        type_configuration.DatadogCredentials.ApiKey,
        type_configuration.DatadogCredentials.ApplicationKey,
        type_configuration.DatadogCredentials.ApiURL,
        TELEMETRY_TYPE_NAME,
        __version__,
        unstable_operations={"create_aws_account": True},
    ) as api_client:
        try:
            api_instance = V2AWSIntegrationApi(api_client)
            response = api_instance.create_aws_account(
                AWSAccountCreateRequest(data=AWSAccountCreateRequestData(attributes=aws_account, type="account"))
            )
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

    external_id = response["data"]["attributes"]["auth_config"]["external_id"]
    boto_client = session.client("secretsmanager")
    boto_client.create_secret(
        Description="The external_id associated with your Datadog AWS Integration.",
        Name=secret_name,
        SecretString='{"external_id":"%s"}' % external_id,
    )

    model.Id = response["data"]["id"]

    return read_handler(session, request, callback_context)


@resource.handler(Action.UPDATE)
@errors_handler
def update_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    LOG.info("Starting %s Update Handler", TYPE_NAME)
    previousState = request.previousResourceState
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration

    if not model.Id:
        LOG.error("Cannot update non existent resource")
        return ProgressEvent(
            status=OperationStatus.FAILED,
            resourceModel=model,
            message="Cannot update non existent resource",
            errorCode=HandlerErrorCode.NotFound,
        )

    # Check if createOnly fields are being updated
    if previousState.AccountID != model.AccountID:
        return ProgressEvent(
            status=OperationStatus.FAILED,
            resourceModel=model,
            message="Cannot update `AccountID`. Please delete it and create a new one instead.",
            errorCode=HandlerErrorCode.NotUpdatable,
        )
    if previousState.AuthConfig.RoleName != model.AuthConfig.RoleName:
        return ProgressEvent(
            status=OperationStatus.FAILED,
            resourceModel=model,
            message="Cannot update `AuthConfig.RoleName`. Please delete it and create a new one instead.",
            errorCode=HandlerErrorCode.NotUpdatable,
        )

    aws_account = build_api_request_from_model(AWSAccountUpdateRequestAttributes, model)

    with client(
        type_configuration.DatadogCredentials.ApiKey,
        type_configuration.DatadogCredentials.ApplicationKey,
        type_configuration.DatadogCredentials.ApiURL,
        TELEMETRY_TYPE_NAME,
        __version__,
        unstable_operations={"update_aws_account": True},
    ) as api_client:
        try:
            api_instance = V2AWSIntegrationApi(api_client)
            api_instance.update_aws_account(
                aws_account_config_id=model.Id,
                body=AWSAccountUpdateRequest(data=AWSAccountUpdateRequestData(attributes=aws_account, type="account")),
            )
        except ApiException as e:
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
            status=OperationStatus.FAILED,
            message=f"Error deleting AWS Account: failed to delete secret {secret_name}",
        )
    else:
        with client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
            unstable_operations={"delete_aws_account": True},
        ) as api_client:
            try:
                api_instance = V2AWSIntegrationApi(api_client)
                api_instance.delete_aws_account(model.Id)
            except ApiException as e:
                LOG.exception(
                    "Exception when calling AWSIntegrationApi->delete_aws_account: %s\n",
                    e,
                )
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
        unstable_operations={"get_aws_account": True},
    ) as api_client:
        api_instance = V2AWSIntegrationApi(api_client)
        try:
            if model.Id is None:
                return ProgressEvent(
                    status=OperationStatus.FAILED,
                    resourceModel=model,
                    message="No Id set, resource never created",
                    errorCode=HandlerErrorCode.NotFound,
                )
            aws_account = api_instance.get_aws_account(aws_account_config_id=model.Id)["data"]["attributes"]
        except ApiException as e:
            LOG.exception("Exception when calling AWSIntegrationApi->get_aws_account: %s\n", e)
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
            LOG.error(f"Account with ID '{model.Id}' not found. " f"Was it updated outside of AWS CloudFormation ?")
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Account with ID '{model.Id}' not found. " f"Was it updated outside of AWS CloudFormation ?",
                errorCode=HandlerErrorCode.NotFound,
            )

    model = build_model_from_api_response(model, aws_account)

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )
