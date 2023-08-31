# Datadog::Monitors::DowntimeSchedule MonitorIdentifier

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#monitorid" title="MonitorId">MonitorId</a>" : <i>Integer</i>,
    "<a href="#monitortags" title="MonitorTags">MonitorTags</a>" : <i>[ String, ... ]</i>
}
</pre>

### YAML

<pre>
<a href="#monitorid" title="MonitorId">MonitorId</a>: <i>Integer</i>
<a href="#monitortags" title="MonitorTags">MonitorTags</a>: <i>
      - String</i>
</pre>

## Properties

#### MonitorId

ID of the monitor to prevent notifications.

_Required_: Yes

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### MonitorTags

A list of monitor tags. For example, tags that are applied directly to monitors, not tags that are used in monitor queries (which are filtered by the scope parameter), to which the downtime applies. The resulting downtime applies to monitors that match **all** provided monitor tags. Setting `monitor_tags` to `[*]` configures the downtime to mute all monitors for the given scope.

_Required_: Yes

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

