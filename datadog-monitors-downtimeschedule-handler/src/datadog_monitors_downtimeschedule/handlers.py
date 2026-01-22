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

from datadog_api_client.v2 import ApiException
from datadog_api_client.v2.api.downtimes_api import DowntimesApi
from datadog_api_client.v2.model.downtime_create_request import DowntimeCreateRequest as DDDowntimeCreateRequest
from datadog_api_client.v2.model.downtime_create_request_attributes import (
    DowntimeCreateRequestAttributes as DDDowntimeCreateRequestAttributes,
)
from datadog_api_client.v2.model.downtime_create_request_data import (
    DowntimeCreateRequestData as DDDowntimeCreateRequestData,
)
from datadog_api_client.v2.model.downtime_monitor_identifier import (
    DowntimeMonitorIdentifier as DDDowntimeMonitorIdentifier,
)
from datadog_api_client.v2.model.downtime_monitor_identifier_id import (
    DowntimeMonitorIdentifierId as DDDowntimeMonitorIdentifierId,
)
from datadog_api_client.v2.model.downtime_monitor_identifier_tags import (
    DowntimeMonitorIdentifierTags as DDDowntimeMonitorIdentifierTags,
)
from datadog_api_client.v2.model.downtime_notify_end_state_actions import (
    DowntimeNotifyEndStateActions as DDDowntimeNotifyEndStateActions,
)
from datadog_api_client.v2.model.downtime_notify_end_state_types import (
    DowntimeNotifyEndStateTypes as DDDowntimeNotifyEndStateTypes,
)
from datadog_api_client.v2.model.downtime_resource_type import DowntimeResourceType as DDDowntimeResourceType
from datadog_api_client.v2.model.downtime_schedule_create_request import (
    DowntimeScheduleCreateRequest as DDDowntimeScheduleCreateRequest,
)
from datadog_api_client.v2.model.downtime_schedule_one_time_create_update_request import (
    DowntimeScheduleOneTimeCreateUpdateRequest as DDDowntimeScheduleOneTimeCreateUpdateRequest,
)
from datadog_api_client.v2.model.downtime_schedule_one_time_response import (
    DowntimeScheduleOneTimeResponse as DDDowntimeScheduleOneTimeResponse,
)
from datadog_api_client.v2.model.downtime_schedule_recurrence_create_update_request import (
    DowntimeScheduleRecurrenceCreateUpdateRequest as DDDowntimeScheduleRecurrenceCreateUpdateRequest,
)
from datadog_api_client.v2.model.downtime_schedule_recurrences_response import (
    DowntimeScheduleRecurrencesResponse as DDDowntimeScheduleRecurrencesResponse,
)
from datadog_api_client.v2.model.downtime_schedule_recurrences_update_request import (
    DowntimeScheduleRecurrencesUpdateRequest as DDDowntimeScheduleRecurrencesUpdateRequest,
)
from datadog_api_client.v2.model.downtime_status import DowntimeStatus as DDDowntimeStatus
from datadog_api_client.v2.model.downtime_update_request import DowntimeUpdateRequest as DDDowntimeUpdateRequest
from datadog_api_client.v2.model.downtime_update_request_attributes import (
    DowntimeUpdateRequestAttributes as DDDowntimeUpdateRequestAttributes,
)
from datadog_api_client.v2.model.downtime_update_request_data import (
    DowntimeUpdateRequestData as DDDowntimeUpdateRequestData,
)

from .version import __version__
from datadog_cloudformation_common.api_clients import client
from datadog_cloudformation_common.utils import errors_handler, http_to_handler_error_code
from .models import (
    MonitorIdentifier,
    Recurrences,
    ResourceHandlerRequest,
    ResourceModel,
    Schedule,
    TypeConfigurationModel,
)

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "Datadog::Monitors::DowntimeSchedule"
TELEMETRY_TYPE_NAME = "monitors-downtime-schedule"

resource = Resource(TYPE_NAME, ResourceModel, TypeConfigurationModel)
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
            model.Id = resp.data.id
        except ApiException as e:
            LOG.exception("Exception when calling DowntimesApi->create_downtime: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error creating downtime: {e}",
                errorCode=http_to_handler_error_code(e.status),
            )

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

        # Check if the downtime exists and is not cancelled before updating
        try:
            resp = api_instance.get_downtime(model.Id)
            if resp.data.attributes.status == DDDowntimeStatus.CANCELED:
                return ProgressEvent(
                    status=OperationStatus.FAILED,
                    resourceModel=model,
                    message=f"Downtime {model.Id} is canceled and cannot be updated",
                    errorCode=HandlerErrorCode.NotFound,
                )
        except ApiException as e:
            LOG.exception("Exception when calling DowntimesApi->get_downtime: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error getting downtime: {e}",
                errorCode=http_to_handler_error_code(e.status),
            )

        try:
            api_instance.update_downtime(model.Id, downtime)
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
            resp = api_instance.get_downtime(model.Id)
            if resp.data.attributes.status == DDDowntimeStatus.CANCELED:
                # Return a 404 to indicate the downtime was already deleted
                return ProgressEvent(
                    status=OperationStatus.FAILED,
                    resourceModel=None,
                    message="Downtime {model.Id} already canceled",
                    errorCode=HandlerErrorCode.NotFound,
                )
        except ApiException as e:
            # Log error but continue in case of failure to get, this should not prevent the next call to delete
            LOG.exception("Exception when calling DowntimeApi->get_downtime: %s\n", e)

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

        # If downtime is disabled, return a NotFound error code to indicate so
        if resp.data.attributes.status == DDDowntimeStatus.CANCELED:
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"downtime {model.Id} is canceled",
                errorCode=HandlerErrorCode.NotFound,
            )

        attributes = resp.data.attributes

        model.Id = resp.data.id
        model.Scope = attributes.scope
        model.DisplayTimezone = getattr(attributes, "display_timezone", None)
        model.Message = getattr(attributes, "message", None)
        model.MuteFirstRecoveryNotification = getattr(attributes, "mute_first_recovery_notification", None)
        model.NotifyEndStates = (
            [str(s) for s in attributes.notify_end_states] if hasattr(attributes, "notify_end_states") else None
        )
        model.NotifyEndTypes = (
            [str(s) for s in attributes.notify_end_types] if hasattr(attributes, "notify_end_types") else None
        )

        monitor_identifier = attributes.monitor_identifier.get_oneof_instance()
        if isinstance(monitor_identifier, DDDowntimeMonitorIdentifierId):
            model.MonitorIdentifier = MonitorIdentifier(MonitorId=monitor_identifier.monitor_id, MonitorTags=None)
        elif isinstance(monitor_identifier, DDDowntimeMonitorIdentifierTags):
            model.MonitorIdentifier = MonitorIdentifier(MonitorId=None, MonitorTags=monitor_identifier.monitor_tags)

        if attributes.schedule:
            schedule = attributes.schedule.get_oneof_instance()
            if isinstance(schedule, DDDowntimeScheduleOneTimeResponse):
                model.Schedule = Schedule(
                    Start=schedule.start.isoformat() if schedule.start else None,
                    End=schedule.end.isoformat() if schedule.end else None,
                    Timezone=None,
                    Recurrences=None,
                )
            elif isinstance(schedule, DDDowntimeScheduleRecurrencesResponse):
                recurrences = []
                for r in schedule.recurrences:
                    recurrence = Recurrences(
                        Rrule=getattr(r, "rrule", None),
                        Start=getattr(r, "start", None),
                        Duration=getattr(r, "duration", None),
                    )
                    recurrences.append(recurrence)
                model.Schedule = Schedule(
                    Start=None,
                    End=None,
                    Timezone=getattr(schedule, "timezone", None),
                    Recurrences=recurrences,
                )

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )


def build_downtime_create_from_model(model: ResourceModel) -> DDDowntimeCreateRequest:
    scope = model.Scope
    if model.MonitorIdentifier.MonitorId is not None:
        monitor_identifier = DDDowntimeMonitorIdentifier(monitor_id=model.MonitorIdentifier.MonitorId)
    elif model.MonitorIdentifier.MonitorTags is not None:
        monitor_identifier = DDDowntimeMonitorIdentifier(monitor_tags=model.MonitorIdentifier.MonitorTags)
    else:
        raise Exception("Invalid value for MonitorIdentifier")

    attributes = DDDowntimeCreateRequestAttributes(scope=scope, monitor_identifier=monitor_identifier)

    if model.DisplayTimezone is not None:
        attributes.display_timezone = model.DisplayTimezone
    if model.Message is not None:
        attributes.message = model.Message
    if model.MuteFirstRecoveryNotification is not None:
        attributes.mute_first_recovery_notification = model.MuteFirstRecoveryNotification
    if model.NotifyEndStates is not None:
        attributes.notify_end_states = [DDDowntimeNotifyEndStateTypes(s) for s in model.NotifyEndStates]
    if model.NotifyEndTypes is not None:
        attributes.notify_end_types = [DDDowntimeNotifyEndStateActions(s) for s in model.NotifyEndTypes]
    if model.Schedule is not None:
        schedule = DDDowntimeScheduleCreateRequest()
        if model.Schedule.Recurrences is not None:
            recurrences = []
            for r in model.Schedule.Recurrences:
                recurrence = DDDowntimeScheduleRecurrenceCreateUpdateRequest(duration=r.Duration, rrule=r.Rrule)
                if r.Start is not None:
                    recurrence.start = r.Start
                recurrences.append(recurrence)
            schedule.recurrences = recurrences

            if model.Schedule.Timezone is not None:
                schedule.timezone = model.Schedule.Timezone
        # We fall back to one time schedule if recurrence(required property is not set)
        else:
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
    if model.MonitorIdentifier.MonitorId is not None:
        monitor_identifier = DDDowntimeMonitorIdentifier(monitor_id=model.MonitorIdentifier.MonitorId)
    elif model.MonitorIdentifier.MonitorTags is not None:
        monitor_identifier = DDDowntimeMonitorIdentifier(monitor_tags=model.MonitorIdentifier.MonitorTags)
    else:
        raise Exception("Invalid value for MonitorIdentifier")

    attributes = DDDowntimeUpdateRequestAttributes(scope=scope, monitor_identifier=monitor_identifier)

    if model.DisplayTimezone is not None:
        attributes.display_timezone = model.DisplayTimezone
    if model.Message is not None:
        attributes.message = model.Message
    if model.MuteFirstRecoveryNotification is not None:
        attributes.mute_first_recovery_notification = model.MuteFirstRecoveryNotification
    if model.NotifyEndStates is not None:
        attributes.notify_end_states = [DDDowntimeNotifyEndStateTypes(s) for s in model.NotifyEndStates]
    if model.NotifyEndTypes is not None:
        attributes.notify_end_types = [DDDowntimeNotifyEndStateActions(s) for s in model.NotifyEndTypes]
    if model.Schedule is not None:
        if model.Schedule.Recurrences is not None:
            schedule = DDDowntimeScheduleRecurrencesUpdateRequest()
            recurrences = []
            for r in model.Schedule.Recurrences:
                recurrence = DDDowntimeScheduleRecurrenceCreateUpdateRequest(duration=r.Duration, rrule=r.Rrule)
                if r.Start is not None:
                    recurrence.start = r.Start
                recurrences.append(recurrence)
            schedule.recurrences = recurrences

            if model.Schedule.Timezone is not None:
                schedule.timezone = model.Schedule.Timezone
        else:
            schedule = DDDowntimeScheduleOneTimeCreateUpdateRequest()
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
