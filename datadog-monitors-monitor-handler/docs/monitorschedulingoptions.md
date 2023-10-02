# Datadog::Monitors::Monitor MonitorSchedulingOptions

Configuration options for scheduling.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#evaluationwindow" title="EvaluationWindow">EvaluationWindow</a>" : <i><a href="monitorschedulingoptionsevaluationwindow.md">MonitorSchedulingOptionsEvaluationWindow</a></i>
}
</pre>

### YAML

<pre>
<a href="#evaluationwindow" title="EvaluationWindow">EvaluationWindow</a>: <i><a href="monitorschedulingoptionsevaluationwindow.md">MonitorSchedulingOptionsEvaluationWindow</a></i>
</pre>

## Properties

#### EvaluationWindow

Configuration options for the evaluation window. If `hour_starts` is set, no other fields may be set. Otherwise, `day_starts` and `month_starts` must be set together.

_Required_: No

_Type_: <a href="monitorschedulingoptionsevaluationwindow.md">MonitorSchedulingOptionsEvaluationWindow</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

