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
from datadog_api_client.v1.model.monitor_options import MonitorOptions as ApiMonitorOptions
from datadog_api_client.v1.model.monitor_threshold_window_options import \
    MonitorThresholdWindowOptions as ApiMonitorThresholdWindows
from datadog_api_client.v1.model.monitor_thresholds import MonitorThresholds as ApiMonitorThresholds
from datadog_api_client.v1.model.monitor_type import MonitorType as ApiMonitorType
from datadog_api_client.v1.model.monitor_update_request import MonitorUpdateRequest as ApiMonitorUpdateRequest
from datadog_cloudformation_common.api_clients import v1_client

from .models import Creator, MonitorOptions, MonitorThresholdWindows, \
    MonitorThresholds, \
    ResourceHandlerRequest, \
    ResourceModel
from .version import __version__

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "Datadog::Monitors::Monitor"
TELEMETRY_TYPE_NAME = "monitors-monitor"

resource = Resource(TYPE_NAME, ResourceModel)
test_entrypoint = resource.test_entrypoint


@resource.handler(Action.READ)
def read_handler(
        session: Optional[SessionProxy],
        request: ResourceHandlerRequest,
        callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    LOG.info("Starting %s Read Handler", TYPE_NAME)
    model = request.desiredResourceState
    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL or "https://api.datadoghq.com",
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = MonitorsApi(api_client)
        monitor_id = model.Id
        try:
            monitor = api_instance.get_monitor(monitor_id)
        except ApiException as e:
            LOG.error("Exception when calling MonitorsApi->get_monitor: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED, resourceModel=model, message=f"Error getting monitor: {e}"
            )

    model.Created = monitor.created.isoformat()
    model.Modified = monitor.modified.isoformat()
    model.Message = monitor.message
    model.Name = monitor.name
    model.Tags = monitor.tags
    model.Query = monitor.query
    model.Multi = monitor.multi
    if monitor.deleted:
        model.Deleted = monitor.deleted.isoformat()
    if not (
            (model.Type == "query alert" and monitor.type.value == "metric alert") or
            (model.Type == "metric alert" and monitor.type.value == "query alert")
    ):
        # metric alert and query alert are interchangeable, so don't update from one to the other
        model.Type = monitor.type.value
    if monitor.creator:
        model.Creator = Creator(Name=monitor.creator.name, Email=monitor.creator.email, Handle=monitor.creator.handle)

    # Add hasattr checks for options since not all of them are applicable to all monitor types, so some attributes
    # might not always be present
    options = monitor.options if hasattr(monitor, "options") else None
    if options:
        model.Options = MonitorOptions(
            EnableLogsSample=options.enable_logs_sample if hasattr(options, "enable_logs_sample") else None,
            EscalationMessage=options.escalation_message if hasattr(options, "escalation_message") else None,
            EvaluationDelay=options.evaluation_delay if hasattr(options, "evaluation_delay") else None,
            IncludeTags=options.include_tags if hasattr(options, "include_tags") else None,
            Locked=options.locked if hasattr(options, "locked") else None,
            MinLocationFailed=options.min_location_failed if hasattr(options, "min_location_failed") else None,
            NewHostDelay=options.new_host_delay if hasattr(options, "new_host_delay") else None,
            NoDataTimeframe=options.no_data_timeframe if hasattr(options, "no_data_timeframe") else None,
            NotifyAudit=options.notify_audit if hasattr(options, "notify_audit") else None,
            NotifyNoData=options.notify_no_data if hasattr(options, "notify_no_data") else None,
            RenotifyInterval=options.renotify_interval if hasattr(options, "renotify_interval") else None,
            RequireFullWindow=options.require_full_window if hasattr(options, "require_full_window") else None,
            SyntheticsCheckID=options.synthetics_check_id if hasattr(options, "synthetics_check_id") else None,
            Thresholds=None,
            ThresholdWindows=None,
            TimeoutH=options.timeout_h if hasattr(options, "timeout_h") else None,
        )
        thresholds = options.thresholds if hasattr(options, "thresholds") else None
        if thresholds:
            model.Options.Thresholds = MonitorThresholds(
                Critical=thresholds.critical if hasattr(thresholds, "critical") else None,
                CriticalRecovery=thresholds.critical_recovery if hasattr(thresholds, "critical_recovery") else None,
                Warning=thresholds.warning if hasattr(thresholds, "warning") else None,
                WarningRecovery=thresholds.warning_recovery if hasattr(thresholds, "warning_recovery") else None,
                OK=thresholds.ok if hasattr(thresholds, "ok") else None,
            )
        tw = options.threshold_windows if hasattr(options, "threshold_windows") else None
        if tw:
            model.Options.ThresholdWindows = MonitorThresholdWindows(
                TriggerWindow=tw.trigger_window if hasattr(tw, "trigger_window") else None,
                RecoveryWindow=tw.recovery_window if hasattr(tw, "recovery_window") else None,
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
    LOG.info("Starting %s Update Handler", TYPE_NAME)
    model = request.desiredResourceState

    monitor = ApiMonitorUpdateRequest()
    monitor.query = model.Query
    monitor.type = ApiMonitorType(model.Type)
    if model.Message is not None:
        monitor.message = model.Message
    if model.Name is not None:
        monitor.name = model.Name
    if model.Tags is not None:
        monitor.tags = model.Tags
    options = build_monitor_options_from_model(model)
    if options:
        monitor.options = options

    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL or "https://api.datadoghq.com",
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = MonitorsApi(api_client)
        try:
            api_instance.update_monitor(model.Id, monitor)
        except ApiException as e:
            LOG.error("Exception when calling MonitorsApi->update_monitor: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED, resourceModel=model, message=f"Error updating monitor: {e}"
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

    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL or "https://api.datadoghq.com",
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = MonitorsApi(api_client)
        try:
            api_instance.delete_monitor(model.Id)
        except ApiException as e:
            LOG.error("Exception when calling MonitorsApi->delete_monitor: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED, resourceModel=model, message=f"Error deleting monitor: {e}"
            )

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
    LOG.info("Starting %s Create Handler", TYPE_NAME)
    model = request.desiredResourceState

    monitor = ApiMonitor()
    monitor.query = model.Query
    monitor.type = ApiMonitorType(model.Type)
    if model.Message is not None:
        monitor.message = model.Message
    if model.Name is not None:
        monitor.name = model.Name
    if model.Tags is not None:
        monitor.tags = model.Tags
    options = build_monitor_options_from_model(model)
    if options:
        monitor.options = options

    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL or "https://api.datadoghq.com",
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = MonitorsApi(api_client)
        try:
            monitor_resp = api_instance.create_monitor(monitor)
        except ApiException as e:
            LOG.error("Exception when calling MonitorsApi->create_monitor: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED, resourceModel=model, message=f"Error creating monitor: {e}"
            )

    model.Id = monitor_resp.id
    return read_handler(session, request, callback_context)


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
        options = ApiMonitorOptions()

        # Nullable attributes
        options.evaluation_delay = model.Options.EvaluationDelay
        options.min_location_failed = model.Options.MinLocationFailed
        options.new_host_delay = model.Options.NewHostDelay
        options.no_data_timeframe = model.Options.NoDataTimeframe
        options.synthetics_check_id = model.Options.SyntheticsCheckID
        options.timeout_h = model.Options.TimeoutH
        options.renotify_interval = model.Options.RenotifyInterval

        # Non nullable
        if model.Options.EnableLogsSample is not None:
            options.enable_logs_sample = model.Options.EnableLogsSample
        if model.Options.EscalationMessage is not None:
            options.escalation_message = model.Options.EscalationMessage
        if model.Options.IncludeTags is not None:
            options.include_tags = model.Options.IncludeTags
        if model.Options.Locked is not None:
            options.locked = model.Options.Locked
        if model.Options.NotifyAudit is not None:
            options.notify_audit = model.Options.NotifyAudit
        if model.Options.NotifyNoData is not None:
            options.notify_no_data = model.Options.NotifyNoData
        if model.Options.RequireFullWindow is not None:
            options.require_full_window = model.Options.RequireFullWindow
        if model.Options.Thresholds is not None:
            options.thresholds = ApiMonitorThresholds()
            if model.Options.Thresholds.Critical is not None:
                options.thresholds.critical = model.Options.Thresholds.Critical
            if model.Options.Thresholds.CriticalRecovery is not None:
                options.thresholds.critical_recovery = model.Options.Thresholds.CriticalRecovery
            if model.Options.Thresholds.Warning is not None:
                options.thresholds.warning = model.Options.Thresholds.Warning
            if model.Options.Thresholds.WarningRecovery is not None:
                options.thresholds.warning_recovery = model.Options.Thresholds.WarningRecovery
            if model.Options.Thresholds.OK is not None:
                options.thresholds.ok = model.Options.Thresholds.OK

        if model.Options.ThresholdWindows is not None:
            options.threshold_windows = ApiMonitorThresholdWindows()
            options.threshold_windows.trigger_window = model.Options.ThresholdWindows.TriggerWindow
            options.threshold_windows.recovery_window = model.Options.ThresholdWindows.RecoveryWindow

    return options
