# Datadog::Monitors::Monitor MonitorOptions

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#enablelogssample" title="EnableLogsSample">EnableLogsSample</a>" : <i>Boolean</i>,
    "<a href="#escalationmessage" title="EscalationMessage">EscalationMessage</a>" : <i>String</i>,
    "<a href="#evaluationdelay" title="EvaluationDelay">EvaluationDelay</a>" : <i>Double</i>,
    "<a href="#includetags" title="IncludeTags">IncludeTags</a>" : <i>Boolean</i>,
    "<a href="#locked" title="Locked">Locked</a>" : <i>Boolean</i>,
    "<a href="#minlocationfailed" title="MinLocationFailed">MinLocationFailed</a>" : <i>Double</i>,
    "<a href="#newhostdelay" title="NewHostDelay">NewHostDelay</a>" : <i>Double</i>,
    "<a href="#nodatatimeframe" title="NoDataTimeframe">NoDataTimeframe</a>" : <i>Double</i>,
    "<a href="#notifyaudit" title="NotifyAudit">NotifyAudit</a>" : <i>Boolean</i>,
    "<a href="#notifynodata" title="NotifyNoData">NotifyNoData</a>" : <i>Boolean</i>,
    "<a href="#renotifyinterval" title="RenotifyInterval">RenotifyInterval</a>" : <i>Double</i>,
    "<a href="#requirefullwindow" title="RequireFullWindow">RequireFullWindow</a>" : <i>Boolean</i>,
    "<a href="#syntheticscheckid" title="SyntheticsCheckID">SyntheticsCheckID</a>" : <i>Double</i>,
    "<a href="#thresholds" title="Thresholds">Thresholds</a>" : <i><a href="monitorthresholds.md">MonitorThresholds</a></i>,
    "<a href="#thresholdwindows" title="ThresholdWindows">ThresholdWindows</a>" : <i><a href="monitorthresholdwindows.md">MonitorThresholdWindows</a></i>,
    "<a href="#timeouth" title="TimeoutH">TimeoutH</a>" : <i>Double</i>
}
</pre>

### YAML

<pre>
<a href="#enablelogssample" title="EnableLogsSample">EnableLogsSample</a>: <i>Boolean</i>
<a href="#escalationmessage" title="EscalationMessage">EscalationMessage</a>: <i>String</i>
<a href="#evaluationdelay" title="EvaluationDelay">EvaluationDelay</a>: <i>Double</i>
<a href="#includetags" title="IncludeTags">IncludeTags</a>: <i>Boolean</i>
<a href="#locked" title="Locked">Locked</a>: <i>Boolean</i>
<a href="#minlocationfailed" title="MinLocationFailed">MinLocationFailed</a>: <i>Double</i>
<a href="#newhostdelay" title="NewHostDelay">NewHostDelay</a>: <i>Double</i>
<a href="#nodatatimeframe" title="NoDataTimeframe">NoDataTimeframe</a>: <i>Double</i>
<a href="#notifyaudit" title="NotifyAudit">NotifyAudit</a>: <i>Boolean</i>
<a href="#notifynodata" title="NotifyNoData">NotifyNoData</a>: <i>Boolean</i>
<a href="#renotifyinterval" title="RenotifyInterval">RenotifyInterval</a>: <i>Double</i>
<a href="#requirefullwindow" title="RequireFullWindow">RequireFullWindow</a>: <i>Boolean</i>
<a href="#syntheticscheckid" title="SyntheticsCheckID">SyntheticsCheckID</a>: <i>Double</i>
<a href="#thresholds" title="Thresholds">Thresholds</a>: <i><a href="monitorthresholds.md">MonitorThresholds</a></i>
<a href="#thresholdwindows" title="ThresholdWindows">ThresholdWindows</a>: <i><a href="monitorthresholdwindows.md">MonitorThresholdWindows</a></i>
<a href="#timeouth" title="TimeoutH">TimeoutH</a>: <i>Double</i>
</pre>

## Properties

#### EnableLogsSample

Whether or not to include a sample of the logs

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

_Type_: Double

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

_Type_: Double

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### NewHostDelay

Time in seconds to allow a host to start reporting data before starting the evaluation of monitor results

_Required_: No

_Type_: Double

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### NoDataTimeframe

Number of minutes data stopped reporting before notifying

_Required_: No

_Type_: Double

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### NotifyAudit

Whether or not to notify tagged users when changes are made to the monitor

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### NotifyNoData

Whether or not to notify when data stops reporting

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### RenotifyInterval

Number of minutes after the last notification before the monitor re-notifies on the current status

_Required_: No

_Type_: Double

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### RequireFullWindow

Whether or not the monitor requires a full window of data before it is evaluated

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### SyntheticsCheckID

ID of the corresponding synthetics check

_Required_: No

_Type_: Double

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

_Type_: Double

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

