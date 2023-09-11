# Datadog::Monitors::Monitor MonitorOptions

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#aggregation" title="Aggregation">Aggregation</a>" : <i><a href="monitoraggregation.md">MonitorAggregation</a></i>,
    "<a href="#enablelogssample" title="EnableLogsSample">EnableLogsSample</a>" : <i>Boolean</i>,
    "<a href="#enablesamples" title="EnableSamples">EnableSamples</a>" : <i>Boolean</i>,
    "<a href="#escalationmessage" title="EscalationMessage">EscalationMessage</a>" : <i>String</i>,
    "<a href="#evaluationdelay" title="EvaluationDelay">EvaluationDelay</a>" : <i>Integer</i>,
    "<a href="#groupretentionduration" title="GroupRetentionDuration">GroupRetentionDuration</a>" : <i>String</i>,
    "<a href="#includetags" title="IncludeTags">IncludeTags</a>" : <i>Boolean</i>,
    "<a href="#locked" title="Locked">Locked</a>" : <i>Boolean</i>,
    "<a href="#minlocationfailed" title="MinLocationFailed">MinLocationFailed</a>" : <i>Integer</i>,
    "<a href="#newhostdelay" title="NewHostDelay">NewHostDelay</a>" : <i>Integer</i>,
    "<a href="#nodatatimeframe" title="NoDataTimeframe">NoDataTimeframe</a>" : <i>Integer</i>,
    "<a href="#notifyaudit" title="NotifyAudit">NotifyAudit</a>" : <i>Boolean</i>,
    "<a href="#notifyby" title="NotifyBy">NotifyBy</a>" : <i>[ String, ... ]</i>,
    "<a href="#notifynodata" title="NotifyNoData">NotifyNoData</a>" : <i>Boolean</i>,
    "<a href="#notificationpresetname" title="NotificationPresetName">NotificationPresetName</a>" : <i>String</i>,
    "<a href="#onmissingdata" title="OnMissingData">OnMissingData</a>" : <i>String</i>,
    "<a href="#renotifyinterval" title="RenotifyInterval">RenotifyInterval</a>" : <i>Integer</i>,
    "<a href="#requirefullwindow" title="RequireFullWindow">RequireFullWindow</a>" : <i>Boolean</i>,
    "<a href="#schedulingoptions" title="SchedulingOptions">SchedulingOptions</a>" : <i><a href="monitorschedulingoptions.md">MonitorSchedulingOptions</a></i>,
    "<a href="#syntheticscheckid" title="SyntheticsCheckID">SyntheticsCheckID</a>" : <i>Integer</i>,
    "<a href="#thresholds" title="Thresholds">Thresholds</a>" : <i><a href="monitorthresholds.md">MonitorThresholds</a></i>,
    "<a href="#thresholdwindows" title="ThresholdWindows">ThresholdWindows</a>" : <i><a href="monitorthresholdwindows.md">MonitorThresholdWindows</a></i>,
    "<a href="#timeouth" title="TimeoutH">TimeoutH</a>" : <i>Integer</i>,
    "<a href="#renotifyoccurrences" title="RenotifyOccurrences">RenotifyOccurrences</a>" : <i>Integer</i>,
    "<a href="#renotifystatuses" title="RenotifyStatuses">RenotifyStatuses</a>" : <i>[ String, ... ]</i>,
    "<a href="#minfailureduration" title="MinFailureDuration">MinFailureDuration</a>" : <i>Integer</i>,
    "<a href="#newgroupdelay" title="NewGroupDelay">NewGroupDelay</a>" : <i>Integer</i>,
    "<a href="#variables" title="Variables">Variables</a>" : <i>[ <a href="monitorformulaandfunctioneventquerydefinition.md">MonitorFormulaAndFunctionEventQueryDefinition</a>, ... ]</i>
}
</pre>

### YAML

<pre>
<a href="#aggregation" title="Aggregation">Aggregation</a>: <i><a href="monitoraggregation.md">MonitorAggregation</a></i>
<a href="#enablelogssample" title="EnableLogsSample">EnableLogsSample</a>: <i>Boolean</i>
<a href="#enablesamples" title="EnableSamples">EnableSamples</a>: <i>Boolean</i>
<a href="#escalationmessage" title="EscalationMessage">EscalationMessage</a>: <i>String</i>
<a href="#evaluationdelay" title="EvaluationDelay">EvaluationDelay</a>: <i>Integer</i>
<a href="#groupretentionduration" title="GroupRetentionDuration">GroupRetentionDuration</a>: <i>String</i>
<a href="#includetags" title="IncludeTags">IncludeTags</a>: <i>Boolean</i>
<a href="#locked" title="Locked">Locked</a>: <i>Boolean</i>
<a href="#minlocationfailed" title="MinLocationFailed">MinLocationFailed</a>: <i>Integer</i>
<a href="#newhostdelay" title="NewHostDelay">NewHostDelay</a>: <i>Integer</i>
<a href="#nodatatimeframe" title="NoDataTimeframe">NoDataTimeframe</a>: <i>Integer</i>
<a href="#notifyaudit" title="NotifyAudit">NotifyAudit</a>: <i>Boolean</i>
<a href="#notifyby" title="NotifyBy">NotifyBy</a>: <i>
      - String</i>
<a href="#notifynodata" title="NotifyNoData">NotifyNoData</a>: <i>Boolean</i>
<a href="#notificationpresetname" title="NotificationPresetName">NotificationPresetName</a>: <i>String</i>
<a href="#onmissingdata" title="OnMissingData">OnMissingData</a>: <i>String</i>
<a href="#renotifyinterval" title="RenotifyInterval">RenotifyInterval</a>: <i>Integer</i>
<a href="#requirefullwindow" title="RequireFullWindow">RequireFullWindow</a>: <i>Boolean</i>
<a href="#schedulingoptions" title="SchedulingOptions">SchedulingOptions</a>: <i><a href="monitorschedulingoptions.md">MonitorSchedulingOptions</a></i>
<a href="#syntheticscheckid" title="SyntheticsCheckID">SyntheticsCheckID</a>: <i>Integer</i>
<a href="#thresholds" title="Thresholds">Thresholds</a>: <i><a href="monitorthresholds.md">MonitorThresholds</a></i>
<a href="#thresholdwindows" title="ThresholdWindows">ThresholdWindows</a>: <i><a href="monitorthresholdwindows.md">MonitorThresholdWindows</a></i>
<a href="#timeouth" title="TimeoutH">TimeoutH</a>: <i>Integer</i>
<a href="#renotifyoccurrences" title="RenotifyOccurrences">RenotifyOccurrences</a>: <i>Integer</i>
<a href="#renotifystatuses" title="RenotifyStatuses">RenotifyStatuses</a>: <i>
      - String</i>
<a href="#minfailureduration" title="MinFailureDuration">MinFailureDuration</a>: <i>Integer</i>
<a href="#newgroupdelay" title="NewGroupDelay">NewGroupDelay</a>: <i>Integer</i>
<a href="#variables" title="Variables">Variables</a>: <i>
      - <a href="monitorformulaandfunctioneventquerydefinition.md">MonitorFormulaAndFunctionEventQueryDefinition</a></i>
</pre>

## Properties

#### Aggregation

Type of aggregation performed in the monitor query.

_Required_: No

_Type_: <a href="monitoraggregation.md">MonitorAggregation</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### EnableLogsSample

Whether or not to include a sample of the logs

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### EnableSamples

Whether or not to send a list of samples when the monitor triggers. This is only used by CI Test and Pipeline monitors.

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### EscalationMessage

Message to include with a re-notification when renotify_interval is set

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### EvaluationDelay

Time in seconds to delay evaluation

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### GroupRetentionDuration

The time span after which groups with missing data are dropped from the monitor state.
The minimum value is one hour, and the maximum value is 72 hours.
Example values are: "60m", "1h", and "2d".
This option is only available for APM Trace Analytics, Audit Trail, CI, Error Tracking, Event, Logs, and RUM monitors.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### IncludeTags

Whether or not to include triggering tags into notification title

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Locked

Whether or not changes to this monitor should be restricted to the creator or admins

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### MinLocationFailed

Number of locations allowed to fail before triggering alert

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### NewHostDelay

Time in seconds to allow a host to start reporting data before starting the evaluation of monitor results

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### NoDataTimeframe

Number of minutes data stopped reporting before notifying

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### NotifyAudit

Whether or not to notify tagged users when changes are made to the monitor

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### NotifyBy

Controls what granularity a monitor alerts on. Only available for monitors with groupings.
For instance, a monitor grouped by `cluster`, `namespace`, and `pod` can be configured to only notify on each new `cluster` violating the alert conditions by setting `notify_by` to `["cluster"]`.
Tags mentioned in `notify_by` must be a subset of the grouping tags in the query.
For example, a query grouped by `cluster` and `namespace` cannot notify on `region`.
Setting `notify_by` to `[*]` configures the monitor to notify as a simple-alert.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### NotifyNoData

Whether or not to notify when data stops reporting

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### NotificationPresetName

Toggles the display of additional content sent in the monitor notification.

_Required_: No

_Type_: String

_Allowed Values_: <code>show_all</code> | <code>hide_query</code> | <code>hide_handles</code> | <code>hide_all</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### OnMissingData

Controls how groups or monitors are treated if an evaluation does not return any data points.
The default option results in different behavior depending on the monitor query type.
For monitors using Count queries, an empty monitor evaluation is treated as 0 and is compared to the threshold conditions.
For monitors using any query type other than Count, for example Gauge, Measure, or Rate, the monitor shows the last known status.
This option is only available for APM Trace Analytics, Audit Trail, CI, Error Tracking, Event, Logs, and RUM monitors.

_Required_: No

_Type_: String

_Allowed Values_: <code>default</code> | <code>show_no_data</code> | <code>show_and_notify_no_data</code> | <code>resolve</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### RenotifyInterval

Number of minutes after the last notification before the monitor re-notifies on the current status

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### RequireFullWindow

Whether or not the monitor requires a full window of data before it is evaluated

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### SchedulingOptions

Configuration options for scheduling.

_Required_: No

_Type_: <a href="monitorschedulingoptions.md">MonitorSchedulingOptions</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### SyntheticsCheckID

ID of the corresponding synthetics check

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Thresholds

_Required_: No

_Type_: <a href="monitorthresholds.md">MonitorThresholds</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### ThresholdWindows

_Required_: No

_Type_: <a href="monitorthresholdwindows.md">MonitorThresholdWindows</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### TimeoutH

Number of hours of the monitor not reporting data before it automatically resolves

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### RenotifyOccurrences

The number of times re-notification messages should be sent on the current status at the provided re-notification interval.

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### RenotifyStatuses

The types of monitor statuses for which re-notification messages are sent.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### MinFailureDuration

How long the test should be in failure before alerting (integer, number of seconds, max 7200).

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### NewGroupDelay

Time (in seconds) to skip evaluations for new groups. For example, this option can be used to skip evaluations for new hosts while they initialize. Must be a non negative integer.

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Variables

List of requests that can be used in the monitor query.

_Required_: No

_Type_: List of <a href="monitorformulaandfunctioneventquerydefinition.md">MonitorFormulaAndFunctionEventQueryDefinition</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

