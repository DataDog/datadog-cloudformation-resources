# Datadog::Monitors::DowntimeSchedule Schedule

A recurring downtime schedule definition.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#timezone" title="Timezone">Timezone</a>" : <i>String</i>,
    "<a href="#recurrences" title="Recurrences">Recurrences</a>" : <i>[ <a href="schedule.md">Schedule</a>, ... ]</i>,
    "<a href="#start" title="Start">Start</a>" : <i>String</i>,
    "<a href="#end" title="End">End</a>" : <i>String</i>
}
</pre>

### YAML

<pre>
<a href="#timezone" title="Timezone">Timezone</a>: <i>String</i>
<a href="#recurrences" title="Recurrences">Recurrences</a>: <i>
      - <a href="schedule.md">Schedule</a></i>
<a href="#start" title="Start">Start</a>: <i>String</i>
<a href="#end" title="End">End</a>: <i>String</i>
</pre>

## Properties

#### Timezone

The timezone in which to schedule the downtime.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Recurrences

A list of downtime recurrences.

_Required_: Yes

_Type_: List of <a href="schedule.md">Schedule</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Start

ISO-8601 Datetime to start the downtime. Must include a UTC offset of zero. If not provided, the downtime starts the moment it is created.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### End

 ISO-8601 Datetime to end the downtime. Must include a UTC offset of zero. If not provided, the downtime continues forever.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

