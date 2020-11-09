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

from .models import ResourceHandlerRequest, ResourceModel
from .version import __version__

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
LOG.setLevel(100)
TYPE_NAME = "Datadog::Dashboards::Dashboard"
TELEMETRY_TYPE_NAME = "dashboards-dashboard"

resource = Resource(TYPE_NAME, ResourceModel)
test_entrypoint = resource.test_entrypoint


@resource.handler(Action.CREATE)
def create_handler(
        session: Optional[SessionProxy],
        request: ResourceHandlerRequest,
        callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    LOG.info("Starting %s Create Handler", TYPE_NAME)
    model = request.desiredResourceState

    try:
        json_payload = json.loads(model.DashboardDefinition)
    except json.JSONDecodeError as e:
        LOG.error("Exception when loading the Dashboard JSON definition: %s\n", e)
        return ProgressEvent(
            status=OperationStatus.FAILED, resourceModel=model, message=f"Error loading Dashboard JSON definition: {e}"
        )

    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL,
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
            LOG.error("Exception when deserializing the Dashboard payload definition: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED, resourceModel=model, message=f"Error deserializing dashboard: {e}"
            )
        except ApiException as e:
            LOG.error("Exception when calling DashboardsApi->create_dashboard: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED, resourceModel=model, message=f"Error creating dashboard: {e}"
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

    json_payload = json.loads(model.DashboardDefinition)
    dashboard_id = model.Id

    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL,
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
                json_payload, (Dashboard,), ["resource_data"], True, False, configuration=api_client.configuration
            )
            api_instance.update_dashboard(dashboard_id, dashboard)
        except TypeError as e:
            LOG.error("Exception when deserializing the Dashboard payload definition: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED, resourceModel=model, message=f"Error deserializing dashboard: {e}"
            )
        except ApiException as e:
            LOG.error("Exception when calling DashboardsApi->update_dashboard: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED, resourceModel=model, message=f"Error updating dashboard: {e}"
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

    dashboard_id = model.Id

    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = DashboardsApi(api_client)
        try:
            api_instance.delete_dashboard(dashboard_id)
        except ApiException as e:
            LOG.error("Exception when calling DashboardsApi->delete_dashboard: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED, resourceModel=model, message=f"Error deleting dashboard: {e}"
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

    dashboard_id = model.Id

    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = DashboardsApi(api_client)
        try:
            dash = api_instance.get_dashboard(dashboard_id)
            json_dict = ApiClient.sanitize_for_serialization(dash)
            model.DashboardDefinition = json.dumps(json_dict)
        except ApiException as e:
            LOG.error("Exception when calling DashboardsApi->get_dashboard: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED, resourceModel=model, message=f"Error getting dashboard: {e}"
            )
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
