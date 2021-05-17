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
from datadog_api_client.v1.api import downtimes_api
from datadog_api_client.v1.model.downtime import Downtime
from datadog_cloudformation_common.api_clients import v1_client
from datadog_cloudformation_common.utils import http_to_handler_error_code

from .models import ResourceHandlerRequest, ResourceModel, TypeConfigurationModel
from .version import __version__

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
TYPE_NAME = "Datadog::Monitors::Downtime"
TELEMETRY_TYPE_NAME = "monitors-downtime"

resource = Resource(TYPE_NAME, ResourceModel, TypeConfigurationModel)
test_entrypoint = resource.test_entrypoint


def build_downtime_struct(model):
    downtime = Downtime(
        end=model.End,
        monitor_id=model.MonitorId
    )

    # Non Nullable attributes
    if model.Message:
        downtime.message = model.Message
    if model.MonitorTags:
        downtime.monitor_tags = model.MonitorTags
    if model.Scope:
        downtime.scope = model.Scope
    if model.Timezone:
        downtime.timezone = model.Timezone
    if model.Start:
        downtime.start = model.Start
    return downtime


@resource.handler(Action.CREATE)
def create_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration
    LOG.info(f"Starting the {TYPE_NAME} Create Handler")

    downtime_body = build_downtime_struct(model)

    with v1_client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = downtimes_api.DowntimesApi(api_client)
        try:
            api_resp = api_instance.create_downtime(downtime_body)
            model.Id = api_resp.id
        except ApiException as e:
            LOG.error("Exception when calling DowntimeApi->create_downtime: %s\n" % e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=e.body,
                errorCode=http_to_handler_error_code(e.status)
            )

    return read_handler(session, request, callback_context)


@resource.handler(Action.UPDATE)
def update_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration

    LOG.info(f"Starting the {TYPE_NAME} Update Handler")

    downtime_body = build_downtime_struct(model)

    with v1_client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = downtimes_api.DowntimesApi(api_client)
        try:
            api_instance.update_downtime(model.Id, downtime_body)
        except ApiException as e:
            LOG.error("Exception when calling DowntimeApi->update_downtime: %s\n" % e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=e.body,
                errorCode=http_to_handler_error_code(e.status)
            )

    return read_handler(session, request, callback_context)


@resource.handler(Action.DELETE)
def delete_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration
    LOG.info(f"Starting the {TYPE_NAME} Delete Handler")

    with v1_client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = downtimes_api.DowntimesApi(api_client)
        # First get the downtime to check if it's disabled (mostly a hack to make a contract_delete_delete test pass)
        try:
            api_resp = api_instance.get_downtime(model.Id)
            if api_resp.disabled:
                # Return a 404 to indicate the downtime was already deleted
                return ProgressEvent(
                    status=OperationStatus.FAILED,
                    resourceModel=None,
                    message="Downtime {model.Id} already disabled",
                    errorCode=HandlerErrorCode.NotFound
                )
        except ApiException as e:
            # Log error but continue in case of failure to get, this should not prevent the next call to delete
            LOG.error("Exception when calling DowntimeApi->get_downtime: %s\n" % e)
        try:
            api_instance.cancel_downtime(model.Id)
        except ApiException as e:
            LOG.error("Exception when calling DowntimeApi->cancel_downtime: %s\n" % e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=e.body,
                errorCode=http_to_handler_error_code(e.status)
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
    type_configuration = request.typeConfiguration
    LOG.info(f"Starting the {TYPE_NAME} Read Handler")

    if model.Id is None:
        return ProgressEvent(
            status=OperationStatus.FAILED,
            resourceModel=model,
            message="No downtime ID in model",
            errorCode=HandlerErrorCode.NotFound
        )
    with v1_client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = downtimes_api.DowntimesApi(api_client)
        try:
            api_resp = api_instance.get_downtime(model.Id)
        except ApiException as e:
            LOG.error("Exception when calling DowntimeApi->get_downtime: %s\n" % e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=e.body,
                errorCode=http_to_handler_error_code(e.status)
            )

    LOG.info(f"Success retrieving downtime {api_resp}")

    # If downtime is disabled, return a NotFound error code to indicate so
    if api_resp.disabled:
        return ProgressEvent(
            status=OperationStatus.FAILED,
            resourceModel=model,
            message=f"downtime {model.Id} is disabled",
            errorCode=HandlerErrorCode.NotFound
        )

    # Add hasattr checks for non-nullable fields to ensure they're available to be set
    # Currently in datadog-api-client-python, accessing fields that don't exist return an AttributeError
    if hasattr(api_resp, 'message'):
        model.Message = api_resp.message
    if hasattr(api_resp, 'monitor_tags'):
        model.MonitorTags = api_resp.monitor_tags
    if hasattr(api_resp, 'scope'):
        model.Scope = api_resp.scope
    if hasattr(api_resp, 'timezone'):
        model.Timezone = api_resp.timezone
    if hasattr(api_resp, 'start'):
        model.Start = api_resp.start

    # Nullable fields, these should be None or set as a value
    if api_resp.end:
        model.End = api_resp.end
    if api_resp.monitor_id:
        model.MonitorId = api_resp.monitor_id

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )
