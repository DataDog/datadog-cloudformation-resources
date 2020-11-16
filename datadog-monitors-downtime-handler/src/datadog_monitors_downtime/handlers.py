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
from datadog_api_client.v1.api import downtimes_api
from datadog_api_client.v1.model.downtime import Downtime
from datadog_cloudformation_common.api_clients import v1_client

from .models import ResourceHandlerRequest, ResourceModel
from .version import __version__

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
TYPE_NAME = "Datadog::Monitors::Downtime"
TELEMETRY_TYPE_NAME = "monitors-downtime"

resource = Resource(TYPE_NAME, ResourceModel)
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
        downtime.monitorTags = model.MonitorTags
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
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )
    LOG.info(f"Starting the {TYPE_NAME} Create Handler")

    downtime_body = build_downtime_struct(model)

    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = downtimes_api.DowntimesApi(api_client)
        try:
            api_resp = api_instance.create_downtime(downtime_body)
            model.Id = api_resp.id
        except ApiException as e:
            LOG.error("Exception when calling DowntimeApi->create_downtime: %s\n" % e)
            return ProgressEvent(status=OperationStatus.FAILED, resourceModel=model, message=e.body)

    return read_handler(session, request, callback_context)


@resource.handler(Action.UPDATE)
def update_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )

    LOG.info(f"Starting the {TYPE_NAME} Update Handler")

    downtime_body = build_downtime_struct(model)

    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = downtimes_api.DowntimesApi(api_client)
        try:
            api_instance.update_downtime(model.Id, downtime_body)
        except ApiException as e:
            LOG.error("Exception when calling DowntimeApi->update_downtime: %s\n" % e)
            return ProgressEvent(status=OperationStatus.FAILED, resourceModel=model, message=e.body)

    return read_handler(session, request, callback_context)


@resource.handler(Action.DELETE)
def delete_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )
    LOG.info(f"Starting the {TYPE_NAME} Delete Handler")

    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = downtimes_api.DowntimesApi(api_client)
        try:
            api_instance.cancel_downtime(model.Id)
        except ApiException as e:
            LOG.error("Exception when calling DowntimeApi->cancel_downtime: %s\n" % e)
            return ProgressEvent(status=OperationStatus.FAILED, resourceModel=model, message=e.body)

    return read_handler(session, request, callback_context)


@resource.handler(Action.READ)
def read_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    LOG.info(f"Starting the {TYPE_NAME} Read Handler")

    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = downtimes_api.DowntimesApi(api_client)
        try:
            api_resp = api_instance.get_downtime(model.Id)
        except ApiException as e:
            LOG.error("Exception when calling DowntimeApi->get_downtime: %s\n" % e)
            return ProgressEvent(status=OperationStatus.FAILED, resourceModel=model, message=e.body)

    LOG.info(f"Success retrieving downtime {api_resp}")

    # Not Nullable attributes
    model.Message = api_resp.message
    model.MonitorTags = api_resp.monitor_tags
    model.Scope = api_resp.scope
    model.Timezone = api_resp.timezone
    model.Start = api_resp.start

    # Nullable attributes
    if api_resp.end:
        model.End = api_resp.end
    if api_resp.monitor_id:
        model.MonitorId = api_resp.monitor_id

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
