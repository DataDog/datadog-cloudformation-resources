import json
import logging
from typing import Any, MutableMapping, Optional

from cloudformation_cli_python_lib import (
    Action,
    HandlerErrorCode,
    OperationStatus,
    ProgressEvent,
    Resource,
    SessionProxy,
)
from datadog_api_client.v1 import ApiClient, ApiException
from datadog_api_client.v1.api.dashboards_api import DashboardsApi
from datadog_api_client.v1.model.dashboard import Dashboard
from datadog_api_client.v1.model_utils import validate_and_convert_types
from datadog_cloudformation_common.api_clients import v1_client
from datadog_cloudformation_common.utils import http_to_handler_error_code

from .models import ResourceHandlerRequest, ResourceModel, TypeConfigurationModel
from .version import __version__

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "Datadog::Dashboards::Dashboard"
TELEMETRY_TYPE_NAME = "dashboards-dashboard"

resource = Resource(TYPE_NAME, ResourceModel, TypeConfigurationModel)
test_entrypoint = resource.test_entrypoint


@resource.handler(Action.CREATE)
def create_handler(
        session: Optional[SessionProxy],
        request: ResourceHandlerRequest,
        callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    LOG.info("Starting %s Create Handler", TYPE_NAME)
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration

    json_payload = model.DashboardDefinition
    with v1_client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = DashboardsApi(api_client)
        try:
            # Call the deserialization function of the python client.
            # It expects the loaded JSON payload, the python client type of the model,
            # some path to the data (not sure what this one does),
            # whether or not the payload is a server payload, so true in our case,
            # whether or not to do type conversion, true in our case too
            # and importantly the api_client configuration, needed to perform the type conversions
            dashboard = validate_and_convert_types(
                json_payload, (Dashboard,), ["resource_data"], True, True, configuration=api_client.configuration
            )
            res = api_instance.create_dashboard(dashboard)
            model.Id = res.id
        except TypeError as e:
            LOG.exception("Exception when deserializing the Dashboard payload definition: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error deserializing dashboard: {e}",
                errorCode=HandlerErrorCode.InternalFailure,
            )
        except ApiException as e:
            LOG.exception("Exception when calling DashboardsApi->create_dashboard: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error creating dashboard: {e}",
                errorCode=http_to_handler_error_code(e.status)
            )
    return read_handler(session, request, callback_context)


@resource.handler(Action.UPDATE)
def update_handler(
        session: Optional[SessionProxy],
        request: ResourceHandlerRequest,
        callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    LOG.info("Starting %s Update Handler", TYPE_NAME)
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration

    json_payload = model.DashboardDefinition
    dashboard_id = model.Id

    with v1_client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = DashboardsApi(api_client)
        try:
            # Call the deserialization function of the python client.
            # It expects the loaded JSON payload, the python client type of the model,
            # some path to the data (not sure what this one does),
            # whether or not the payload is a server payload, so true in our case,
            # whether or not to do type conversion, true in our case too
            # and importantly the api_client configuration, needed to perform the type conversions
            dashboard = validate_and_convert_types(
                json_payload, (Dashboard,), ["resource_data"], True, True, configuration=api_client.configuration
            )
            api_instance.update_dashboard(dashboard_id, dashboard)
        except TypeError as e:
            LOG.exception("Exception when deserializing the Dashboard payload definition: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error deserializing dashboard: {e}",
                errorCode=HandlerErrorCode.InternalFailure,
            )
        except ApiException as e:
            LOG.exception("Exception when calling DashboardsApi->update_dashboard: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error updating dashboard: {e}",
                errorCode=http_to_handler_error_code(e.status)
            )
    return read_handler(session, request, callback_context)


@resource.handler(Action.DELETE)
def delete_handler(
        session: Optional[SessionProxy],
        request: ResourceHandlerRequest,
        callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    LOG.info("Starting %s Delete Handler", TYPE_NAME)
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration

    dashboard_id = model.Id

    with v1_client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = DashboardsApi(api_client)
        try:
            api_instance.delete_dashboard(dashboard_id)
        except ApiException as e:
            LOG.exception("Exception when calling DashboardsApi->delete_dashboard: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error deleting dashboard: {e}",
                errorCode=http_to_handler_error_code(e.status),
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
    LOG.info("Starting %s Read Handler", TYPE_NAME)
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration

    dashboard_id = model.Id

    with v1_client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = DashboardsApi(api_client)
        try:
            dash = api_instance.get_dashboard(dashboard_id)
            json_dict = ApiClient.sanitize_for_serialization(dash)
            model.Url = json_dict["url"]
            for k in ["author_handle", "id", "created_at", "modified_at", "url"]:
                del json_dict[k]
            model.DashboardDefinition = json_dict
        except ApiException as e:
            LOG.exception("Exception when calling DashboardsApi->get_dashboard: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error getting dashboard: {e}",
                errorCode=http_to_handler_error_code(e.status)
            )
    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )
