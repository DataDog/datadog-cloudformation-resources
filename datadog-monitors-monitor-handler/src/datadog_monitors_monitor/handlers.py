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
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor import Monitor as ApiMonitor
from datadog_api_client.v1.model.monitor_update_request import MonitorUpdateRequest as ApiMonitorUpdateRequest
from datadog_api_client.v1.model.monitor_type import MonitorType as ApiMonitorType
from datadog_api_client.v1.model.monitor_options import MonitorOptions as ApiMonitorOptions
from datadog_api_client.v1.model.monitor_thresholds import MonitorThresholds as ApiMonitorThresholds
from datadog_api_client.v1.model.monitor_threshold_window_options import MonitorThresholdWindowOptions as ApiMonitorThresholdWindows
from datadog_cloudformation_common.api_clients import v1_client

from .models import Creator, MonitorOptions, MonitorState, MonitorStateGroup, MonitorThresholdWindows, \
    MonitorThresholds, \
    ResourceHandlerRequest, \
    ResourceModel
from .version import __version__

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "Datadog::Monitors::Monitor"

resource = Resource(TYPE_NAME, ResourceModel)
test_entrypoint = resource.test_entrypoint


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
        model.DatadogCredentials.ApiURL or "https://api.datadoghq.com",
        TYPE_NAME,
        __version__,
    ) as api_client:
        api_instance = MonitorsApi(api_client)
        monitor_id = model.Id
        try:
            monitor = api_instance.get_monitor(monitor_id)
        except ApiException as e:
            LOG.error("Exception when calling MonitorsApi->get_monitor: %s\n", e)
            return ProgressEvent.failed(HandlerErrorCode.InternalFailure, f"Error getting monitor: {e}")

    model.Created = monitor.created.isoformat()
    model.Modified = monitor.modified.isoformat()
    if monitor.deleted:
        model.Deleted = monitor.deleted.isoformat()
    model.Message = monitor.message
    model.Name = monitor.name
    model.Tags = monitor.tags
    model.Query = monitor.query
    if not (
            (model.Type == "query alert" and monitor.type.value == "metric alert") or
            (model.Type == "metric alert" and monitor.type.value == "query alert")
    ):
        # metric alert and query alert are interchangeable, so don 't update when is from one to the other
        model.Type = monitor.type
    model.Multi = monitor.multi
    if monitor.creator:
        model.Creator = Creator(Name=monitor.creator.name, Email=monitor.creator.email, Handle=monitor.creator.handle)
    if monitor.options:
        model.Options = MonitorOptions(
            EnableLogsSample=monitor.options.enable_logs_sample,
            EscalationMessage=monitor.options.escalation_message,
            EvaluationDelay=monitor.options.evalutation_delay,
            IncludeTags=monitor.options.include_tags,
            Locked=monitor.options.locked,
            MinLocationFailed=monitor.options.min_location_failed,
            NewHostDelay=monitor.options.new_host_delay,
            NoDataTimeframe=monitor.options.no_data_timeframe,
            NotifyAudit=monitor.options.notify_audit,
            NotifyNoData=monitor.options.notify_no_data,
            RenotifyInterval=monitor.options.renotify_interval,
            RequireFullWindow=monitor.options.require_full_window,
            SyntheticsCheckID=monitor.options.synthetics_check_id,
            Thresholds=None,
            ThresholdWindows=None,
            TimeoutH=monitor.options.timeout_h,
        )
        if monitor.options.thresholds:
            model.Options.Thresholds = MonitorThresholds(
                Critical=monitor.options.thresholds.critical,
                CriticalRecovery=monitor.options.thresholds.critical_recovery,
                Warning=monitor.options.thresholds.warning,
                WarningRecovery=monitor.options.thresholds.warning_recovery,
                OK=monitor.options.thresholds.ok,
            )
        if monitor.options.threshold_windows:
            model.Options.ThresholdWindows = MonitorThresholdWindows(
                TriggerWindow=monitor.options.threshold_windows.trigger_window,
                RecoveryWindow=monitor.options.threshold_windows.recovery_window,
            )
    model.OverallState = monitor.overall_state.value if monitor.overall_state else None
    if monitor.state:
        model.State = MonitorState(
            MonitorID=monitor.id,
            OverallState=monitor.state.overall_state.value if monitor.state.overall_state else None,
            Groups=None,
        )
        if monitor.state.groups:
            model.State.Groups = {}
            for k, v in monitor.state.groups:
                model.State.Groups[k] = MonitorStateGroup(
                    Name=v.name,
                    LastTriggeredTS=v.last_triggered_ts,
                    LastNotifiedTS=v.last_notified_ts,
                    LastResolvedTS=v.last_resolved_ts,
                    LastNodataTS=v.last_nodata_ts,
                    Status=v.status.value if v.status else None,
                )
    model.Id = monitor.id

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )


@resource.handler(Action.UPDATE)
def update_handler(
        session: Optional[SessionProxy],
        request: ResourceHandlerRequest,
        callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState

    monitor = ApiMonitorUpdateRequest(
        message=model.Message,
        name=model.Name,
        tags=model.Tags,
        options=build_monitor_options_from_model(model),
        query=model.Query,
        type=ApiMonitorType(model.Type)
    )

    with v1_client(
        model.DatadogCredentials.ApiKey,
        model.DatadogCredentials.ApplicationKey,
        model.DatadogCredentials.ApiURL or "https://api.datadoghq.com",
        TYPE_NAME,
        __version__,
    ) as api_client:
        api_instance = MonitorsApi(api_client)
        try:
            api_instance.update_monitor(model.Id, monitor)
        except ApiException as e:
            LOG.error("Exception when calling MonitorsApi->update_monitor: %s\n", e)
            return ProgressEvent.failed(HandlerErrorCode.InternalFailure, f"Exception when updating monitor {e}")

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )


@resource.handler(Action.DELETE)
def delete_handler(
        session: Optional[SessionProxy],
        request: ResourceHandlerRequest,
        callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState

    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL or "https://api.datadoghq.com",
            TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = MonitorsApi(api_client)
        try:
            api_instance.delete_monitor(model.Id)
        except ApiException as e:
            LOG.error("Exception when calling MonitorsApi->delete_monitor: %s\n", e)
            return ProgressEvent.failed(HandlerErrorCode.InternalFailure, f"Exception when deleting monitor {e}")

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )


@resource.handler(Action.CREATE)
def create_handler(
        session: Optional[SessionProxy],
        request: ResourceHandlerRequest,
        callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState

    monitor = ApiMonitor(
        message=model.Message,
        name=model.Name,
        tags=model.Tags,
        options=build_monitor_options_from_model(model),
        query=model.Query,
        type=ApiMonitorType(model.Type)
    )

    with v1_client(
        model.DatadogCredentials.ApiKey,
        model.DatadogCredentials.ApplicationKey,
        model.DatadogCredentials.ApiURL or "https://api.datadoghq.com",
        TYPE_NAME,
        __version__,
    ) as api_client:
        api_instance = MonitorsApi(api_client)
        try:
            api_instance.create_monitor(monitor)
        except ApiException as e:
            LOG.error("Exception when calling MonitorsApi->create_monitor: %s\n", e)
            return ProgressEvent.failed(HandlerErrorCode.InternalFailure, f"Exception when creating monitor {e}")

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


def build_monitor_options_from_model(model: ResourceModel) -> ApiMonitorOptions:
    options = None
    if model.Options:
        options = ApiMonitorOptions(
            enable_logs_sample=model.Options.EnableLogsSample,
            escalation_message=model.Options.EscalationMessage,
            include_tags=model.Options.IncludeTags,
            locked=model.Options.Locked,
            notify_audit=model.Options.NotifyAudit,
            notify_no_data=model.Options.NotifyNoData,
            require_full_window=model.Options.RequireFullWindow,
            timeout_h=model.Options.TimeoutH,
            synthetics_check_id=model.Options.SyntheticsCheckID,
            evaluation_delay=model.Options.EvaluationDelay,
            min_location_failed=model.Options.MinLocationFailed,
            new_host_delay=model.Options.NewHostDelay,
            no_data_timeframe=model.Options.NoDataTimeframe,
            renotify_interval=model.Options.RenotifyInterval,
            thresholds=None,
            threshold_windows=None,
        )
        if model.Options.Thresholds:
            options.thresholds = ApiMonitorThresholds(
                critical=model.Options.Thresholds.Critical,
                critical_recovery=model.Options.Thresholds.CriticalRecovery,
                warning=model.Options.Thresholds.Warning,
                warning_recovery=model.Options.Thresholds.WarningRecovery,
                ok=model.Options.Thresholds.OK,
            )
        if model.Options.ThresholdWindows:
            options.threshold_windows = ApiMonitorThresholdWindows(
                trigger_window=model.Options.ThresholdWindows.TriggerWindow,
                recovery_window=model.Options.ThresholdWindows.RecoveryWindow,
            )

    return options