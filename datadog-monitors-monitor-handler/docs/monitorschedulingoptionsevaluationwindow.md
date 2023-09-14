# Datadog::Monitors::Monitor MonitorSchedulingOptionsEvaluationWindow

Configuration options for the evaluation window. If `hour_starts` is set, no other fields may be set. Otherwise, `day_starts` and `month_starts` must be set together.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#daystarts" title="DayStarts">DayStarts</a>" : <i>String</i>,
    "<a href="#monthstarts" title="MonthStarts">MonthStarts</a>" : <i>Integer</i>,
    "<a href="#hourstarts" title="HourStarts">HourStarts</a>" : <i>Integer</i>
}
</pre>

### YAML

<pre>
<a href="#daystarts" title="DayStarts">DayStarts</a>: <i>String</i>
<a href="#monthstarts" title="MonthStarts">MonthStarts</a>: <i>Integer</i>
<a href="#hourstarts" title="HourStarts">HourStarts</a>: <i>Integer</i>
</pre>

## Properties

#### DayStarts

The time of the day at which a one day cumulative evaluation window starts. Must be defined in UTC time in `HH:mm` format.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### MonthStarts

The day of the month at which a one month cumulative evaluation window starts.

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### HourStarts

The minute of the hour at which a one hour cumulative evaluation window starts.

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

