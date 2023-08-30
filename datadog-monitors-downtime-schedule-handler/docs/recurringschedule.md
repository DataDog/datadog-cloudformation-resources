# Datadog::Monitors::DowntimeSchedule RecurringSchedule

A recurring downtime schedule definition.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#timezone" title="Timezone">Timezone</a>" : <i>String</i>,
    "<a href="#recurrences" title="Recurrences">Recurrences</a>" : <i>[ <a href="recurringschedule.md">RecurringSchedule</a>, ... ]</i>
}
</pre>

### YAML

<pre>
<a href="#timezone" title="Timezone">Timezone</a>: <i>String</i>
<a href="#recurrences" title="Recurrences">Recurrences</a>: <i>
      - <a href="recurringschedule.md">RecurringSchedule</a></i>
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

_Type_: List of <a href="recurringschedule.md">RecurringSchedule</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

