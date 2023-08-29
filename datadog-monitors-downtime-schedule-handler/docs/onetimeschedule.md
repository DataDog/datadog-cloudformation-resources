# Datadog::Monitors::DowntimeSchedule OneTimeSchedule

A recurring downtime schedule definition.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#start" title="Start">Start</a>" : <i>String</i>,
    "<a href="#end" title="End">End</a>" : <i>String</i>
}
</pre>

### YAML

<pre>
<a href="#start" title="Start">Start</a>: <i>String</i>
<a href="#end" title="End">End</a>: <i>String</i>
</pre>

## Properties

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

