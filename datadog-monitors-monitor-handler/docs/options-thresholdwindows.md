# Datadog::Monitors::Monitor Options ThresholdWindows

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#triggerwindow" title="TriggerWindow">TriggerWindow</a>" : <i>String</i>,
    "<a href="#recoverywindow" title="RecoveryWindow">RecoveryWindow</a>" : <i>String</i>
}
</pre>

### YAML

<pre>
<a href="#triggerwindow" title="TriggerWindow">TriggerWindow</a>: <i>String</i>
<a href="#recoverywindow" title="RecoveryWindow">RecoveryWindow</a>: <i>String</i>
</pre>

## Properties

#### TriggerWindow

How long a metric must be anomalous before triggering an alert

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### RecoveryWindow

How long an anomalous metric must be normal before recovering from an alert state

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

