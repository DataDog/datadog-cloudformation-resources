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
from datadog_api_client.v1 import ApiException
from datadog_api_client.v1.api.dashboards_api import DashboardsApi
from datadog_cloudformation_common.api_clients import client
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

    try:
        json_payload = json.loads(model.DashboardDefinition)
    except ValueError as e:
        LOG.exception("Exception parsing dashboard payload: %s\n", e)
        return ProgressEvent(
            status=OperationStatus.FAILED,
            resourceModel=model,
            message=f"Error parsing dashboard payload: {e}",
            errorCode=HandlerErrorCode.InternalFailure,
        )

    with client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
            {"preload_content": False, "check_input_type": False}
    ) as api_client:
        api_instance = DashboardsApi(api_client)
        try:
            # Get raw http response with _preload_content False
            resp = api_instance.create_dashboard(json_payload)
            json_dict = json.loads(resp.data)
            model.Id = json_dict["id"]
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
                errorCode=http_to_handler_error_code(e.status),
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

    try:
        json_payload = json.loads(model.DashboardDefinition)
    except ValueError as e:
        LOG.exception("Exception parsing dashboard payload: %s\n", e)
        return ProgressEvent(
            status=OperationStatus.FAILED,
            resourceModel=model,
            message=f"Error parsing dashboard payload: {e}",
            errorCode=HandlerErrorCode.InternalFailure,
        )

    dashboard_id = model.Id

    with client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
            {"preload_content": False, "check_input_type": False}
    ) as api_client:
        api_instance = DashboardsApi(api_client)
        try:
            # Get raw http response with _preload_content False
            api_instance.update_dashboard(dashboard_id, json_payload)
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
                errorCode=http_to_handler_error_code(e.status),
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

    with client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
            {"preload_content": False}
    ) as api_client:
        api_instance = DashboardsApi(api_client)
        try:
            # Get raw http response with _preload_content False
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

    with client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
            {"preload_content": False}
    ) as api_client:
        api_instance = DashboardsApi(api_client)
        try:
            # Get raw http response with _preload_content  set to False
            resp = api_instance.get_dashboard(dashboard_id)
            json_dict = json.loads(resp.data)
            model.Url = json_dict["url"]
            for k in ["author_handle", "id", "created_at", "modified_at", "url", "author_name"]:
                try:
                    del json_dict[k]
                except KeyError:
                    pass
            model.DashboardDefinition = json.dumps(json_dict, sort_keys=True)
        except ApiException as e:
            LOG.exception("Exception when calling DashboardsApi->get_dashboard: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error getting dashboard: {e}",
                errorCode=http_to_handler_error_code(e.status),
            )
    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )
