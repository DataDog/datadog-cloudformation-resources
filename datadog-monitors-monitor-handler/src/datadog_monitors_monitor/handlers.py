import logging
from time import sleep
from typing import List, Any, MutableMapping, Optional

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
from datadog_api_client.v1.model.monitor_renotify_status_type import MonitorRenotifyStatusType
from datadog_api_client.v1.model.monitor_threshold_window_options import (
    MonitorThresholdWindowOptions as ApiMonitorThresholdWindows,
)
from datadog_api_client.v1.model.monitor_options_scheduling_options import (
    MonitorOptionsSchedulingOptions as ApiMonitorOptionsSchedulingOptions,
)
from datadog_api_client.v1.model.monitor_options_scheduling_options_evaluation_window import (
    MonitorOptionsSchedulingOptionsEvaluationWindow as ApiMonitorOptionsSchedulingOptionsEvaluationWindow,
)
from datadog_api_client.v1.model.monitor_thresholds import MonitorThresholds as ApiMonitorThresholds
from datadog_api_client.v1.model.monitor_type import MonitorType as ApiMonitorType
from datadog_api_client.v1.model.monitor_update_request import MonitorUpdateRequest as ApiMonitorUpdateRequest
from datadog_api_client.v1.model.query_sort_order import QuerySortOrder as ApiMonitorQuerySortOrder
from datadog_api_client.v1.model.monitor_formula_and_function_event_query_definition import (
    MonitorFormulaAndFunctionEventQueryDefinition as ApiMonitorMonitorFormulaAndFunctionEventQueryDefinition,
)
from datadog_api_client.v1.model.monitor_formula_and_function_events_data_source import (
    MonitorFormulaAndFunctionEventsDataSource as ApiMonitorMonitorFormulaAndFunctionEventsDataSource,
)
from datadog_api_client.v1.model.on_missing_data_option import OnMissingDataOption as ApiOnMissingDataOption
from datadog_api_client.v1.model.monitor_options_notification_presets import (
    MonitorOptionsNotificationPresets as ApiMonitorOptionsNotificationPresets,
)
from datadog_api_client.v1.model.monitor_formula_and_function_event_query_definition_compute import (
    MonitorFormulaAndFunctionEventQueryDefinitionCompute as ApiMonitorMonitorFormulaAndFunctionEventQueryDefinitionCompute,
)
from datadog_api_client.v1.model.monitor_formula_and_function_event_aggregation import (
    MonitorFormulaAndFunctionEventAggregation as ApiMonitorMonitorFormulaAndFunctionEventAggregation,
)
from datadog_api_client.v1.model.monitor_formula_and_function_event_query_definition_search import (
    MonitorFormulaAndFunctionEventQueryDefinitionSearch as ApiMonitorMonitorFormulaAndFunctionEventQueryDefinitionSearch,
)
from datadog_api_client.v1.model.monitor_formula_and_function_event_query_group_by import (
    MonitorFormulaAndFunctionEventQueryGroupBy as ApiMonitorMonitorFormulaAndFunctionEventQueryGroupBy,
)
from datadog_api_client.v1.model.monitor_formula_and_function_event_query_group_by_sort import (
    MonitorFormulaAndFunctionEventQueryGroupBySort as ApiMonitorMonitorFormulaAndFunctionEventQueryGroupBySort,
)
from datadog_api_client.v1.model.monitor_formula_and_function_query_definition import (
    MonitorFormulaAndFunctionQueryDefinition as ApiMonitorMonitorFormulaAndFunctionQueryDefinition,
)

# Data Quality Query imports (available after API client is updated)
try:
    from datadog_api_client.v1.model.monitor_formula_and_function_data_quality_query_definition import (
        MonitorFormulaAndFunctionDataQualityQueryDefinition as ApiMonitorFormulaAndFunctionDataQualityQueryDefinition,
    )
    from datadog_api_client.v1.model.monitor_formula_and_function_data_quality_data_source import (
        MonitorFormulaAndFunctionDataQualityDataSource as ApiMonitorFormulaAndFunctionDataQualityDataSource,
    )

    # Note: Measure is now a plain string (not an enum) to allow extensibility
    from datadog_api_client.v1.model.monitor_formula_and_function_data_quality_monitor_options import (
        MonitorFormulaAndFunctionDataQualityMonitorOptions as ApiMonitorFormulaAndFunctionDataQualityMonitorOptions,
    )
    from datadog_api_client.v1.model.monitor_formula_and_function_data_quality_model_type_override import (
        MonitorFormulaAndFunctionDataQualityModelTypeOverride as ApiMonitorFormulaAndFunctionDataQualityModelTypeOverride,
    )

    HAS_DATA_QUALITY_SUPPORT = True
except ImportError:
    HAS_DATA_QUALITY_SUPPORT = False

from datadog_cloudformation_common.api_clients import client
from datadog_cloudformation_common.utils import errors_handler, http_to_handler_error_code

from .models import (
    Creator,
    MonitorOptions,
    MonitorSchedulingOptions,
    MonitorSchedulingOptionsEvaluationWindow,
    MonitorThresholdWindows,
    MonitorThresholds,
    ResourceHandlerRequest,
    ResourceModel,
    MonitorFormulaAndFunctionEventQueryDefinition,
    MonitorFormulaAndFunctionEventQueryGroupBy,
    MonitorFormulaAndFunctionDataQualityQueryDefinition,
    MonitorFormulaAndFunctionDataQualityMonitorOptions,
    Sort,
    Compute,
    Search,
    TypeConfigurationModel,
)
from .version import __version__

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "Datadog::Monitors::Monitor"
TELEMETRY_TYPE_NAME = "monitors-monitor"
MAX_RETRY_COUNT = 5
RETRY_SLEEP_INTERVAL = 5

resource = Resource(TYPE_NAME, ResourceModel, TypeConfigurationModel)
test_entrypoint = resource.test_entrypoint


@resource.handler(Action.READ)
@errors_handler
def read_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    LOG.info("Starting %s Read Handler", TYPE_NAME)
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration

    with client(
        type_configuration.DatadogCredentials.ApiKey,
        type_configuration.DatadogCredentials.ApplicationKey,
        type_configuration.DatadogCredentials.ApiURL,
        TELEMETRY_TYPE_NAME,
        __version__,
    ) as api_client:
        api_instance = MonitorsApi(api_client)
        monitor_id = model.Id
        if monitor_id is None:
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message="Error getting monitor: monitor does not exist",
                errorCode=HandlerErrorCode.NotFound,
            )

        retry_count = 0
        monitor = api_exception = None
        while retry_count < MAX_RETRY_COUNT:
            retry_count += 1
            try:
                monitor = api_instance.get_monitor(monitor_id)
                api_exception = None
                break
            except ApiException as e:
                api_exception = e
                if e.status == 404:
                    sleep(RETRY_SLEEP_INTERVAL)
                    continue
                else:
                    break

        if api_exception is not None:
            LOG.exception("Exception when calling MonitorsApi->get_monitor: %s\n", api_exception)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error getting monitor: {api_exception}",
                errorCode=http_to_handler_error_code(api_exception.status),
            )

    model.Created = monitor.created.isoformat()
    model.Modified = monitor.modified.isoformat()
    model.Message = monitor.message
    model.Name = monitor.name
    model.Tags = monitor.tags
    model.Priority = monitor.priority
    model.Query = monitor.query
    model.Multi = monitor.multi
    model.RestrictedRoles = monitor.restricted_roles
    if monitor.deleted:
        model.Deleted = monitor.deleted.isoformat()
    if not (
        (model.Type == "query alert" and monitor.type.value == "metric alert")
        or (model.Type == "metric alert" and monitor.type.value == "query alert")
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
            EnableSamples=options.enable_samples if hasattr(options, "enable_samples") else None,
            EnableLogsSample=options.enable_logs_sample if hasattr(options, "enable_logs_sample") else None,
            EscalationMessage=options.escalation_message if hasattr(options, "escalation_message") else None,
            EvaluationDelay=options.evaluation_delay if hasattr(options, "evaluation_delay") else None,
            GroupRetentionDuration=options.group_retention_duration
            if hasattr(options, "group_retention_duration")
            else None,
            IncludeTags=options.include_tags if hasattr(options, "include_tags") else None,
            Locked=options.locked if hasattr(options, "locked") else None,
            MinLocationFailed=options.min_location_failed if hasattr(options, "min_location_failed") else None,
            NewHostDelay=options.new_host_delay if hasattr(options, "new_host_delay") else None,
            NoDataTimeframe=options.no_data_timeframe if hasattr(options, "no_data_timeframe") else None,
            NotifyAudit=options.notify_audit if hasattr(options, "notify_audit") else None,
            NotifyBy=[str(notify) for notify in options.notify_by] if hasattr(options, "notify_by") else None,
            NotifyNoData=options.notify_no_data if hasattr(options, "notify_no_data") else None,
            NotificationPresetName=str(options.notification_preset_name)
            if hasattr(options, "notification_preset_name")
            else None,
            OnMissingData=str(options.on_missing_data) if hasattr(options, "on_missing_data") else None,
            RenotifyInterval=options.renotify_interval if hasattr(options, "renotify_interval") else None,
            RequireFullWindow=options.require_full_window if hasattr(options, "require_full_window") else None,
            SchedulingOptions=None,
            SyntheticsCheckID=options.synthetics_check_id if hasattr(options, "synthetics_check_id") else None,
            Thresholds=None,
            ThresholdWindows=None,
            TimeoutH=options.timeout_h if hasattr(options, "timeout_h") else None,
            RenotifyOccurrences=options.renotify_occurrences if hasattr(options, "renotify_occurrences") else None,
            RenotifyStatuses=[str(status) for status in options.renotify_statuses]
            if hasattr(options, "renotify_statuses")
            else None,
            MinFailureDuration=options.min_failure_duration if hasattr(options, "min_failure_duration") else None,
            NewGroupDelay=options.new_group_delay if hasattr(options, "new_group_delay") else None,
            Variables=None,
        )

        scheduling_options = options.scheduling_options if hasattr(options, "scheduling_options") else None
        if scheduling_options:
            evaluation_window = getattr(scheduling_options, "evaluation_window", None)
            if evaluation_window:
                model.Options.SchedulingOptions = MonitorSchedulingOptions(
                    EvaluationWindow=MonitorSchedulingOptionsEvaluationWindow(
                        DayStarts=evaluation_window.day_starts if hasattr(evaluation_window, "day_starts") else None,
                        MonthStarts=evaluation_window.month_starts
                        if hasattr(evaluation_window, "month_starts")
                        else None,
                        HourStarts=evaluation_window.hour_starts if hasattr(evaluation_window, "hour_starts") else None,
                    )
                )

        variables = getattr(options, "variables", None)
        if variables:
            model.Options.Variables = build_cf_variables(variables)

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

    # Remove write only fields
    model.CloudformationOptions = None

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )


@resource.handler(Action.UPDATE)
@errors_handler
def update_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    LOG.info("Starting %s Update Handler", TYPE_NAME)
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration

    monitor = ApiMonitorUpdateRequest()
    monitor.query = model.Query
    if model.CloudformationOptions is not None:
        if model.CloudformationOptions.LowercaseQuery:
            monitor.query = model.Query.lower()
    monitor.type = ApiMonitorType(model.Type)
    if model.Message is not None:
        monitor.message = model.Message
    if model.Name is not None:
        monitor.name = model.Name
    if model.Tags is not None:
        monitor.tags = model.Tags
    if model.Priority is not None:
        monitor.priority = model.Priority
    if model.RestrictedRoles is not None:
        monitor.restricted_roles = model.RestrictedRoles
    options = build_monitor_options_from_model(model)
    if options:
        monitor.options = options

    with client(
        type_configuration.DatadogCredentials.ApiKey,
        type_configuration.DatadogCredentials.ApplicationKey,
        type_configuration.DatadogCredentials.ApiURL,
        TELEMETRY_TYPE_NAME,
        __version__,
    ) as api_client:
        api_instance = MonitorsApi(api_client)
        try:
            api_instance.update_monitor(model.Id, monitor)
        except ApiException as e:
            LOG.exception("Exception when calling MonitorsApi->update_monitor: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error updating monitor: {e}",
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
    LOG.info("Starting %s Delete Handler", TYPE_NAME)
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration

    with client(
        type_configuration.DatadogCredentials.ApiKey,
        type_configuration.DatadogCredentials.ApplicationKey,
        type_configuration.DatadogCredentials.ApiURL,
        TELEMETRY_TYPE_NAME,
        __version__,
    ) as api_client:
        api_instance = MonitorsApi(api_client)
        try:
            api_instance.delete_monitor(model.Id)
        except ApiException as e:
            LOG.exception("Exception when calling MonitorsApi->delete_monitor: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error deleting monitor: {e}",
                errorCode=http_to_handler_error_code(e.status),
            )

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=None,
    )


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

    query = model.Query
    if model.CloudformationOptions is not None:
        if model.CloudformationOptions.LowercaseQuery:
            query = query.lower()

    monitor = ApiMonitor(query, ApiMonitorType(model.Type))
    if model.Message is not None:
        monitor.message = model.Message
    if model.Name is not None:
        monitor.name = model.Name
    if model.Tags is not None:
        monitor.tags = model.Tags
    if model.Priority is not None:
        monitor.priority = model.Priority
    if model.RestrictedRoles is not None:
        monitor.restricted_roles = model.RestrictedRoles
    options = build_monitor_options_from_model(model)
    if options:
        monitor.options = options

    with client(
        type_configuration.DatadogCredentials.ApiKey,
        type_configuration.DatadogCredentials.ApplicationKey,
        type_configuration.DatadogCredentials.ApiURL,
        TELEMETRY_TYPE_NAME,
        __version__,
    ) as api_client:
        api_instance = MonitorsApi(api_client)
        try:
            monitor_resp = api_instance.create_monitor(monitor)
        except ApiException as e:
            LOG.exception("Exception when calling MonitorsApi->create_monitor: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error creating monitor: {e}",
                errorCode=http_to_handler_error_code(e.status),
            )

    model.Id = monitor_resp.id
    return read_handler(session, request, callback_context)


def build_api_variable_from_model(variable):
    """
    Convert a variable (dict or model instance) to the appropriate Datadog API variable type.
    Variables can come in as raw dicts from CloudFormation deserialization or as model instances.
    """
    # Normalize: if it's a dict, extract values using dict access; otherwise use attribute access
    if isinstance(variable, dict):
        data_source = variable.get("DataSource")
        name = variable.get("Name")
        compute = variable.get("Compute")
        search = variable.get("Search")
        indexes = variable.get("Indexes")
        group_by = variable.get("GroupBy")
        # Data quality specific fields
        measure = variable.get("Measure")
        filter_val = variable.get("Filter")
        schema_version = variable.get("SchemaVersion")
        scope = variable.get("Scope")
        monitor_options = variable.get("MonitorOptions")
    else:
        data_source = getattr(variable, "DataSource", None)
        name = getattr(variable, "Name", None)
        compute = getattr(variable, "Compute", None)
        search = getattr(variable, "Search", None)
        indexes = getattr(variable, "Indexes", None)
        group_by = getattr(variable, "GroupBy", None)
        # Data quality specific fields
        measure = getattr(variable, "Measure", None)
        filter_val = getattr(variable, "Filter", None)
        schema_version = getattr(variable, "SchemaVersion", None)
        scope = getattr(variable, "Scope", None)
        monitor_options = getattr(variable, "MonitorOptions", None)

    # Determine type based on data source or presence of specific fields
    # Event query types have DataSource like "rum", "logs", "spans", etc.
    # Data quality queries have DataSource "data_quality" and require "Measure" and "Filter"
    is_data_quality = data_source == "data_quality" or (measure is not None and filter_val is not None)

    if is_data_quality and HAS_DATA_QUALITY_SUPPORT:
        datadog_variable = ApiMonitorFormulaAndFunctionDataQualityQueryDefinition(
            data_source=ApiMonitorFormulaAndFunctionDataQualityDataSource(data_source),
            name=name,
            measure=measure,
            filter=filter_val,
        )
        if schema_version is not None:
            datadog_variable.schema_version = schema_version
        if scope is not None:
            datadog_variable.scope = scope
        if group_by is not None:
            datadog_variable.group_by = group_by
        if monitor_options is not None:
            datadog_variable.monitor_options = ApiMonitorFormulaAndFunctionDataQualityMonitorOptions()
            if isinstance(monitor_options, dict):
                custom_sql = monitor_options.get("CustomSql")
                custom_where = monitor_options.get("CustomWhere")
                group_by_columns = monitor_options.get("GroupByColumns")
                crontab_override = monitor_options.get("CrontabOverride")
                model_type_override = monitor_options.get("ModelTypeOverride")
            else:
                custom_sql = getattr(monitor_options, "CustomSql", None)
                custom_where = getattr(monitor_options, "CustomWhere", None)
                group_by_columns = getattr(monitor_options, "GroupByColumns", None)
                crontab_override = getattr(monitor_options, "CrontabOverride", None)
                model_type_override = getattr(monitor_options, "ModelTypeOverride", None)

            if custom_sql is not None:
                datadog_variable.monitor_options.custom_sql = custom_sql
            if custom_where is not None:
                datadog_variable.monitor_options.custom_where = custom_where
            if group_by_columns is not None:
                datadog_variable.monitor_options.group_by_columns = group_by_columns
            if crontab_override is not None:
                datadog_variable.monitor_options.crontab_override = crontab_override
            if model_type_override is not None:
                datadog_variable.monitor_options.model_type_override = (
                    ApiMonitorFormulaAndFunctionDataQualityModelTypeOverride(model_type_override)
                )
        return datadog_variable
    elif compute is not None:
        # Event query type (has Compute field)
        if isinstance(compute, dict):
            aggregation = compute.get("Aggregation")
            interval = compute.get("Interval")
            metric = compute.get("Metric")
        else:
            aggregation = getattr(compute, "Aggregation", None)
            interval = getattr(compute, "Interval", None)
            metric = getattr(compute, "Metric", None)

        datadog_variable = ApiMonitorMonitorFormulaAndFunctionEventQueryDefinition(
            data_source=ApiMonitorMonitorFormulaAndFunctionEventsDataSource(data_source),
            name=name,
            compute=ApiMonitorMonitorFormulaAndFunctionEventQueryDefinitionCompute(
                aggregation=ApiMonitorMonitorFormulaAndFunctionEventAggregation(aggregation),
            ),
        )
        if interval is not None:
            datadog_variable.compute.interval = interval
        if metric is not None:
            datadog_variable.compute.metric = metric

        if search is not None:
            if isinstance(search, dict):
                query = search.get("Query")
            else:
                query = getattr(search, "Query", None)
            datadog_variable.search = ApiMonitorMonitorFormulaAndFunctionEventQueryDefinitionSearch(query=query)

        if indexes is not None:
            datadog_variable.indexes = indexes

        datadog_variable.group_by = []
        if group_by is not None:
            for group in group_by:
                if isinstance(group, dict):
                    facet = group.get("Facet")
                    sort = group.get("Sort")
                    limit = group.get("Limit")
                else:
                    facet = getattr(group, "Facet", None)
                    sort = getattr(group, "Sort", None)
                    limit = getattr(group, "Limit", None)

                datadog_group = ApiMonitorMonitorFormulaAndFunctionEventQueryGroupBy(facet)
                if sort is not None:
                    if isinstance(sort, dict):
                        sort_agg = sort.get("Aggregation")
                        sort_metric = sort.get("Metric")
                        sort_order = sort.get("Order")
                    else:
                        sort_agg = getattr(sort, "Aggregation", None)
                        sort_metric = getattr(sort, "Metric", None)
                        sort_order = getattr(sort, "Order", None)

                    datadog_group.sort = ApiMonitorMonitorFormulaAndFunctionEventQueryGroupBySort(sort_agg)
                    if sort_metric is not None:
                        datadog_group.sort.metric = sort_metric
                    if sort_order is not None:
                        datadog_group.sort.order = ApiMonitorQuerySortOrder(sort_order)
                if limit is not None:
                    datadog_group.limit = limit
                datadog_variable.group_by.append(datadog_group)
        return datadog_variable

    # Unknown variable type
    LOG.warning("Unknown variable type, skipping: %s", variable)
    return None


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
        options.renotify_occurrences = model.Options.RenotifyOccurrences
        options.min_failure_duration = model.Options.MinFailureDuration
        options.new_group_delay = model.Options.NewGroupDelay

        # Non nullable
        if model.Options.RenotifyStatuses is not None:
            options.renotify_statuses = (
                [MonitorRenotifyStatusType(status) for status in model.Options.RenotifyStatuses]
                if model.Options.RenotifyStatuses is not None
                else None
            )
        if model.Options.EnableSamples is not None:
            options.enable_samples = model.Options.EnableSamples
        if model.Options.EnableLogsSample is not None:
            options.enable_logs_sample = model.Options.EnableLogsSample
        if model.Options.EscalationMessage is not None:
            options.escalation_message = model.Options.EscalationMessage
        if model.Options.GroupRetentionDuration is not None:
            options.group_retention_duration = model.Options.GroupRetentionDuration
        if model.Options.IncludeTags is not None:
            options.include_tags = model.Options.IncludeTags
        if model.Options.Locked is not None:
            options.locked = model.Options.Locked
        if model.Options.NotificationPresetName is not None:
            options.notification_preset_name = ApiMonitorOptionsNotificationPresets(
                str(model.Options.NotificationPresetName)
            )
        if model.Options.NotifyAudit is not None:
            options.notify_audit = model.Options.NotifyAudit
        if model.Options.NotifyBy is not None:
            options.notify_by = [str(notify) for notify in model.Options.NotifyBy]
        if model.Options.NotifyNoData is not None:
            options.notify_no_data = model.Options.NotifyNoData
        if model.Options.OnMissingData is not None:
            options.on_missing_data = ApiOnMissingDataOption(str(model.Options.OnMissingData))
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
        if model.Options.SchedulingOptions is not None:
            options.scheduling_options = ApiMonitorOptionsSchedulingOptions()
            if model.Options.SchedulingOptions.EvaluationWindow is not None:
                options.scheduling_options.evaluation_window = ApiMonitorOptionsSchedulingOptionsEvaluationWindow()
                if model.Options.SchedulingOptions.EvaluationWindow.DayStarts is not None:
                    options.scheduling_options.evaluation_window.day_starts = (
                        model.Options.SchedulingOptions.EvaluationWindow.DayStarts
                    )
                if model.Options.SchedulingOptions.EvaluationWindow.HourStarts is not None:
                    options.scheduling_options.evaluation_window.hour_starts = (
                        model.Options.SchedulingOptions.EvaluationWindow.HourStarts
                    )
                if model.Options.SchedulingOptions.EvaluationWindow.MonthStarts is not None:
                    options.scheduling_options.evaluation_window.month_starts = (
                        model.Options.SchedulingOptions.EvaluationWindow.MonthStarts
                    )

        if model.Options.ThresholdWindows is not None:
            options.threshold_windows = ApiMonitorThresholdWindows()
            options.threshold_windows.trigger_window = model.Options.ThresholdWindows.TriggerWindow
            options.threshold_windows.recovery_window = model.Options.ThresholdWindows.RecoveryWindow

        if model.Options.Variables is not None:
            options.variables = []
            for variable in model.Options.Variables:
                datadog_variable = build_api_variable_from_model(variable)
                if datadog_variable is not None:
                    options.variables.append(datadog_variable)

    return options


def build_cf_variables(variables: List[ApiMonitorMonitorFormulaAndFunctionQueryDefinition]):
    cf_variables = []
    for variable in variables:
        oneof_instance = variable.get_oneof_instance()
        if type(oneof_instance) == ApiMonitorMonitorFormulaAndFunctionEventQueryDefinition:
            cf_variable = MonitorFormulaAndFunctionEventQueryDefinition(
                DataSource=variable.data_source.value,
                Name=variable.name,
                Compute=Compute(
                    Aggregation=variable.compute.aggregation.value,
                    Interval=variable.compute.interval if hasattr(variable.compute, "interval") else None,
                    Metric=variable.compute.metric if hasattr(variable.compute, "metric") else None,
                ),
                Search=Search(Query=variable.search.query) if hasattr(variable, "search") else None,
                Indexes=variable.indexes if hasattr(variable, "indexes") else None,
                GroupBy=None,
            )

            if hasattr(variable, "group_by"):
                cf_variable.GroupBy = []
                for group in variable.group_by:
                    cf_group = MonitorFormulaAndFunctionEventQueryGroupBy(
                        Facet=group.facet,
                        Sort=None,
                        Limit=group.limit if hasattr(group, "limit") else None,
                    )
                    if hasattr(group, "sort"):
                        cf_group.Sort = Sort(
                            Aggregation=group.sort.aggregation.value,
                            Metric=group.sort.metric if hasattr(group.sort, "metric") else None,
                            Order=group.sort.order.value if hasattr(group.sort, "order") else None,
                        )
                    cf_variable.GroupBy.append(cf_group)
            cf_variables.append(cf_variable)
        elif HAS_DATA_QUALITY_SUPPORT:
            try:
                if type(oneof_instance) == ApiMonitorFormulaAndFunctionDataQualityQueryDefinition:
                    cf_monitor_options = None
                    if hasattr(variable, "monitor_options") and variable.monitor_options is not None:
                        opts = variable.monitor_options
                        cf_monitor_options = MonitorFormulaAndFunctionDataQualityMonitorOptions(
                            CustomSql=opts.custom_sql if hasattr(opts, "custom_sql") else None,
                            CustomWhere=opts.custom_where if hasattr(opts, "custom_where") else None,
                            GroupByColumns=opts.group_by_columns if hasattr(opts, "group_by_columns") else None,
                            CrontabOverride=opts.crontab_override if hasattr(opts, "crontab_override") else None,
                            ModelTypeOverride=opts.model_type_override.value
                            if hasattr(opts, "model_type_override") and opts.model_type_override
                            else None,
                        )
                    cf_variable = MonitorFormulaAndFunctionDataQualityQueryDefinition(
                        DataSource=variable.data_source.value if hasattr(variable, "data_source") else None,
                        Name=variable.name if hasattr(variable, "name") else None,
                        Measure=variable.measure if hasattr(variable, "measure") else None,
                        Filter=variable.filter if hasattr(variable, "filter") else None,
                        Scope=variable.scope if hasattr(variable, "scope") else None,
                        SchemaVersion=variable.schema_version if hasattr(variable, "schema_version") else None,
                        GroupBy=variable.group_by if hasattr(variable, "group_by") else None,
                        MonitorOptions=cf_monitor_options,
                    )
                    cf_variables.append(cf_variable)
            except Exception:
                # Skip if data quality types are not fully supported
                pass
    return cf_variables
