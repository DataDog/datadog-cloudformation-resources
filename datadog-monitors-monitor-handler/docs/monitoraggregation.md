# Datadog::Monitors::Monitor MonitorAggregation

Type of aggregation performed in the monitor query.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#metric" title="Metric">Metric</a>" : <i>String</i>,
    "<a href="#type" title="Type">Type</a>" : <i>String</i>,
    "<a href="#groupby" title="GroupBy">GroupBy</a>" : <i>String</i>
}
</pre>

### YAML

<pre>
<a href="#metric" title="Metric">Metric</a>: <i>String</i>
<a href="#type" title="Type">Type</a>: <i>String</i>
<a href="#groupby" title="GroupBy">GroupBy</a>: <i>String</i>
</pre>

## Properties

#### Metric

Metric name used in the monitor.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Type

Metric type used in the monitor.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### GroupBy

Group to break down the monitor on.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

