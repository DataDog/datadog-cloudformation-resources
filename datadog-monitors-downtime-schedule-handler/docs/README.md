# Datadog::Monitors::DowntimeSchedule

Datadog Downtime Schedule 0.0.1

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "Datadog::Monitors::DowntimeSchedule",
    "Properties" : {
        "<a href="#displaytimezone" title="DisplayTimezone">DisplayTimezone</a>" : <i>String</i>,
        "<a href="#message" title="Message">Message</a>" : <i>String</i>,
        "<a href="#mutefirstrecoverynotification" title="MuteFirstRecoveryNotification">MuteFirstRecoveryNotification</a>" : <i>Boolean</i>,
        "<a href="#scope" title="Scope">Scope</a>" : <i>String</i>,
        "<a href="#notifyendstates" title="NotifyEndStates">NotifyEndStates</a>" : <i>[ String, ... ]</i>,
        "<a href="#notifyendtypes" title="NotifyEndTypes">NotifyEndTypes</a>" : <i>[ String, ... ]</i>,
        "<a href="#monitoridentifier" title="MonitorIdentifier">MonitorIdentifier</a>" : <i><a href="monitorid.md">MonitorId</a>, <a href="monitortags.md">MonitorTags</a></i>,
        "<a href="#schedule" title="Schedule">Schedule</a>" : <i>Map, <a href="recurringschedule.md">RecurringSchedule</a>, <a href="onetimeschedule.md">OneTimeSchedule</a></i>
    }
}
</pre>

### YAML

<pre>
Type: Datadog::Monitors::DowntimeSchedule
Properties:
    <a href="#displaytimezone" title="DisplayTimezone">DisplayTimezone</a>: <i>String</i>
    <a href="#message" title="Message">Message</a>: <i>String</i>
    <a href="#mutefirstrecoverynotification" title="MuteFirstRecoveryNotification">MuteFirstRecoveryNotification</a>: <i>Boolean</i>
    <a href="#scope" title="Scope">Scope</a>: <i>String</i>
    <a href="#notifyendstates" title="NotifyEndStates">NotifyEndStates</a>: <i>
      - String</i>
    <a href="#notifyendtypes" title="NotifyEndTypes">NotifyEndTypes</a>: <i>
      - String</i>
    <a href="#monitoridentifier" title="MonitorIdentifier">MonitorIdentifier</a>: <i><a href="monitorid.md">MonitorId</a>, <a href="monitortags.md">MonitorTags</a></i>
    <a href="#schedule" title="Schedule">Schedule</a>: <i>Map, <a href="recurringschedule.md">RecurringSchedule</a>, <a href="onetimeschedule.md">OneTimeSchedule</a></i>
</pre>

## Properties

#### DisplayTimezone

The timezone in which to display the downtime's start and end times in Datadog applications. This is not used as an offset for scheduling.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Message

A message to include with notifications for this downtime. Email notifications can be sent to specific users by using the same `@username` notation as events.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### MuteFirstRecoveryNotification

If the first recovery notification during a downtime should be muted.

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Scope

The scope to which the downtime applies. Must follow the [common search syntax](https://docs.datadoghq.com/logs/explorer/search_syntax/).

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### NotifyEndStates

States that will trigger a monitor notification when the `notify_end_types` action occurs.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### NotifyEndTypes

Actions that will trigger a monitor notification if the downtime is in the `notify_end_types` state.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### MonitorIdentifier

_Required_: Yes

_Type_: <a href="monitorid.md">MonitorId</a>, <a href="monitortags.md">MonitorTags</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Schedule

The schedule that defines when the monitor starts, stops, and recurs. There are two types of schedules: one-time and recurring. Recurring schedules may have up to five RRULE-based recurrences. If no schedules are provided, the downtime will begin immediately and never end.

_Required_: No

_Type_: Map, <a href="recurringschedule.md">RecurringSchedule</a>, <a href="onetimeschedule.md">OneTimeSchedule</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the Id.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### Id

ID of the downtime.

