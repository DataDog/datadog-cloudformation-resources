import logging
from typing import Any, MutableMapping, Optional
from cloudformation_cli_python_lib import (
    Action,
    HandlerErrorCode,
    OperationStatus,
    ProgressEvent,
    Resource,
    SessionProxy,
    exceptions,
    identifier_utils,
)

from datadog_api_client.v2 import ApiException
from datadog_api_client.v2.api.downtimes_api import DowntimesApi
from datadog_api_client.v2.model.downtime_create_request import DowntimeCreateRequest as DDDowntimeCreateRequest
from datadog_api_client.v2.model.downtime_create_request_attributes import DowntimeCreateRequestAttributes as DDDowntimeCreateRequestAttributes
from datadog_api_client.v2.model.downtime_create_request_data import DowntimeCreateRequestData as DDDowntimeCreateRequestData
from datadog_api_client.v2.model.downtime_monitor_identifier import DowntimeMonitorIdentifier as DDDowntimeMonitorIdentifier
from datadog_api_client.v2.model.downtime_monitor_identifier_id import DowntimeMonitorIdentifierId as DDDowntimeMonitorIdentifierId
from datadog_api_client.v2.model.downtime_monitor_identifier_tags import DowntimeMonitorIdentifierTags as DDDowntimeMonitorIdentifierTags
from datadog_api_client.v2.model.downtime_resource_type import DowntimeResourceType as DDDowntimeResourceType
from datadog_api_client.v2.model.downtime_schedule_create_request import DowntimeScheduleCreateRequest as DDDowntimeScheduleCreateRequest
from datadog_api_client.v2.model.downtime_schedule_one_time_response import DowntimeScheduleOneTimeResponse as DDDowntimeScheduleOneTimeResponse
from datadog_api_client.v2.model.downtime_schedule_recurrence_create_update_request import DowntimeScheduleRecurrenceCreateUpdateRequest as DDDowntimeScheduleRecurrenceCreateUpdateRequest
from datadog_api_client.v2.model.downtime_schedule_recurrences_response import DowntimeScheduleRecurrencesResponse as DDDowntimeScheduleRecurrencesResponse
from datadog_api_client.v2.model.downtime_schedule_update_request import DowntimeScheduleUpdateRequest as DDDowntimeScheduleUpdateRequest
from datadog_api_client.v2.model.downtime_update_request import DowntimeUpdateRequest as DDDowntimeUpdateRequest
from datadog_api_client.v2.model.downtime_update_request_attributes import DowntimeUpdateRequestAttributes as DDDowntimeUpdateRequestData
from datadog_api_client.v2.model.downtime_update_request_data import DowntimeUpdateRequestData as DDDowntimeUpdateRequestData

from datadog_cloudformation_common.utils import errors_handler, http_to_handler_error_code
from .version import __version__
from datadog_cloudformation_common.api_clients import client
from .models import MonitorId, MonitorTags, OneTimeSchedule, Recurrences, RecurringSchedule, ResourceHandlerRequest, ResourceModel

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "Datadog::Monitors::DowntimeSchedule"
TELEMETRY_TYPE_NAME = "monitors-downtime-schedule"

resource = Resource(TYPE_NAME, ResourceModel)
test_entrypoint = resource.test_entrypoint


@resource.handler(Action.CREATE)
@errors_handler
def create_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration

    downtime = build_downtime_create_from_model(model)
    with client(
        type_configuration.DatadogCredentials.ApiKey,
        type_configuration.DatadogCredentials.ApplicationKey,
        type_configuration.DatadogCredentials.ApiURL,
        TELEMETRY_TYPE_NAME,
        __version__,
    ) as api_client:
        api_instance = DowntimesApi(api_client)
        try:
            resp = api_instance.create_downtime(downtime)
        except ApiException as e:
            LOG.exception("Exception when calling DowntimesApi->create_downtime: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error creating downtime: {e}",
                errorCode=http_to_handler_error_code(e.status),
            )

    model.Id = resp.data.id
    return read_handler(session, request, callback_context)


@resource.handler(Action.UPDATE)
@errors_handler
def update_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration

    downtime = build_downtime_update_from_model(model)
    with client(
        type_configuration.DatadogCredentials.ApiKey,
        type_configuration.DatadogCredentials.ApplicationKey,
        type_configuration.DatadogCredentials.ApiURL,
        TELEMETRY_TYPE_NAME,
        __version__,
    ) as api_client:
        api_instance = DowntimesApi(api_client)
        try:
            resp = api_instance.update_downtime(model.Id, downtime)
        except ApiException as e:
            LOG.exception("Exception when calling DowntimesApi->update_downtime: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error updating downtime: {e}",
                errorCode=http_to_handler_error_code(e.status),
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

    with client(
        type_configuration.DatadogCredentials.ApiKey,
        type_configuration.DatadogCredentials.ApplicationKey,
        type_configuration.DatadogCredentials.ApiURL,
        TELEMETRY_TYPE_NAME,
        __version__,
    ) as api_client:
        api_instance = DowntimesApi(api_client)
        try:
            api_instance.cancel_downtime(model.Id)
        except ApiException as e:
            LOG.exception("Exception when calling DowntimesApi->cancel_downtime: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error canceling downtime: {e}",
                errorCode=http_to_handler_error_code(e.status),
            )

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=None,
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
        api_instance = DowntimesApi(api_client)
        if model.Id is None:
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error getting downtime: downtime does not exist",
                errorCode=HandlerErrorCode.NotFound,
            )
        try:
            resp = api_instance.get_downtime(model.Id)
        except ApiException as e:
            LOG.exception("Exception when calling DowntimesApi->get_downtime: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error getting downtime: {e}",
                errorCode=http_to_handler_error_code(e.status),
            )

        attributes = resp.data.attributes
        
        model.Id = resp.data.id
        model.Scope = attributes.scope
        model.DisplayTimezone = getattr(attributes, "display_timezone", None)
        model.Message = getattr(attributes, "message", None)
        model.MuteFirstRecoveryNotification = getattr(attributes, "mute_first_recovery_notification", None)
        model.NotifyEndStates = getattr(attributes, "notify_end_states", None)
        model.NotifyEndTypes = getattr(attributes, "notify_end_types", None)
        
        monitor_identifier = attributes.monitor_identifier.get_oneof_instance()
        if isinstance(monitor_identifier, DDDowntimeMonitorIdentifierId):
            model.MonitorIdentifier = MonitorId(MonitorId=monitor_identifier.monitor_id)
        elif type(model.MonitorIdentifier.get_oneof_instance()) == DDDowntimeMonitorIdentifierTags:
            model.MonitorIdentifier = MonitorTags(MonitorTags=monitor_identifier.monitor_tags)
        
        if attributes.schedule:
            schedule = attributes.schedule.get_oneof_instance()
            if isinstance(monitor_identifier, DDDowntimeScheduleOneTimeResponse):
                model.Schedule = OneTimeSchedule(
                    Start=getattr(schedule, "start", None),
                    End=getattr(schedule, "end", None)
                )
            elif type(model.MonitorIdentifier.get_oneof_instance()) == DDDowntimeScheduleRecurrencesResponse:
                recurrences = []
                for r in schedule.recurrences:
                    recurrence = Recurrences(
                        Rrule=getattr(r, "rrule", None),
                        Start=getattr(r, "start", None),
                        Duration=getattr(r, "duration", None),
                    )
                    recurrences.append(r)
                model.Schedule = RecurringSchedule(
                    Timezone=getattr(schedule, "timezone", None),
                    Recurrences=recurrences,
                )
    
    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )


def build_downtime_create_from_model(model: ResourceModel) -> DDDowntimeCreateRequest:
    scope = model.Scope
    if isinstance(model.MonitorIdentifier, MonitorId):
        monitor_identifier = DDDowntimeMonitorIdentifier(monitor_id=model.MonitorIdentifier.MonitorId)
    elif isinstance(model.MonitorIdentifier, MonitorTags):
        monitor_identifier = DDDowntimeMonitorIdentifier(monitor_tags=model.MonitorIdentifier.MonitorTags)
    else:
        LOG.error("Invalid value for MonitorIdentifier")
        raise Exception("Invalid value for MonitorIdentifier")

    attributes = DDDowntimeCreateRequestAttributes(scope=scope, monitor_identifier=monitor_identifier)

    if model.DisplayTimezone is not None:
        attributes.display_timezoe = model.DisplayTimezone
    if model.Message is not None:
        attributes.message = model.Message
    if model.MuteFirstRecoveryNotification is not None:
        attributes.mute_first_recovery_notification = model.MuteFirstRecoveryNotification
    if model.NotifyEndStates is not None:
        attributes.notify_end_states = model.NotifyEndStates
    if model.NotifyEndTypes is not None:
        attributes.notify_end_types = model.NotifyEndTypes
    if model.Schedule is not None:
        schedule = DDDowntimeScheduleCreateRequest()
        if isinstance(model.Schedule, RecurringSchedule):
            recurrences = []
            for r in model.Schedule.Recurrences:
                recurrence = DDDowntimeScheduleRecurrenceCreateUpdateRequest(duration=r.Duration, rrule=r.Rrule)
                if r.Start is not None:
                    recurrence.start = r.Start
                recurrences.append(recurrence)
            schedule.recurrences = recurrences

            if model.Schedule.Timezone is not None:
                schedule.timezone = model.Schedule.Timezone
        elif isinstance(model.Schedule, OneTimeSchedule):
            schedule = DDDowntimeScheduleCreateRequest()
            if model.Schedule.Start is not None:
                schedule.start = model.Schedule.Start
            if model.Schedule.End is not None:
                schedule.end = model.Schedule.End
        attributes.schedule = schedule
    
    return DDDowntimeCreateRequest(
        data=DDDowntimeCreateRequestData(
            attributes=attributes,
            type=DDDowntimeResourceType.DOWNTIME,
        ),
    )


def build_downtime_update_from_model(model: ResourceModel) -> DDDowntimeUpdateRequest:
    scope = model.Scope
    if isinstance(model.MonitorIdentifier, MonitorId):
        monitor_identifier = DDDowntimeMonitorIdentifier(monitor_id=model.MonitorIdentifier.MonitorId)
    elif isinstance(model.MonitorIdentifier, MonitorTags):
        monitor_identifier = DDDowntimeMonitorIdentifier(monitor_tags=model.MonitorIdentifier.MonitorTags)
    else:
        LOG.error("Invalid value for MonitorIdentifier")
        raise Exception("Invalid value for MonitorIdentifier")

    attributes = DDDowntimeUpdateRequestData(scope=scope, monitor_identifier=monitor_identifier)

    if model.DisplayTimezone is not None:
        attributes.display_timezoe = model.DisplayTimezone
    if model.Message is not None:
        attributes.message = model.Message
    if model.MuteFirstRecoveryNotification is not None:
        attributes.mute_first_recovery_notification = model.MuteFirstRecoveryNotification
    if model.NotifyEndStates is not None:
        attributes.notify_end_states = model.NotifyEndStates
    if model.NotifyEndTypes is not None:
        attributes.notify_end_types = model.NotifyEndTypes
    if model.Schedule is not None:
        schedule = DDDowntimeScheduleUpdateRequest()
        if isinstance(model.Schedule, RecurringSchedule):
            recurrences = []
            for r in model.Schedule.Recurrences:
                recurrence = DDDowntimeScheduleRecurrenceCreateUpdateRequest(duration=r.Duration, rrule=r.Rrule)
                if r.Start is not None:
                    recurrence.start = r.Start
                recurrences.append(recurrence)
            schedule.recurrences = recurrences

            if model.Schedule.Timezone is not None:
                schedule.timezone = model.Schedule.Timezone
        elif isinstance(model.Schedule, OneTimeSchedule):
            schedule = DDDowntimeScheduleUpdateRequest()
            if model.Schedule.Start is not None:
                schedule.start = model.Schedule.Start
            if model.Schedule.End is not None:
                schedule.end = model.Schedule.End
        attributes.schedule = schedule
    
    return DDDowntimeUpdateRequest(
        data=DDDowntimeUpdateRequestData(
            attributes=attributes,
            type=DDDowntimeResourceType.DOWNTIME,
            id=model.Id,
        ),
    )
