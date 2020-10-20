# Datadog::Monitors::Monitor MonitorThresholds

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#critical" title="Critical">Critical</a>" : <i>Double</i>,
    "<a href="#criticalrecovery" title="CriticalRecovery">CriticalRecovery</a>" : <i>Double</i>,
    "<a href="#ok" title="OK">OK</a>" : <i>Double</i>,
    "<a href="#warning" title="Warning">Warning</a>" : <i>Double</i>,
    "<a href="#warningrecovery" title="WarningRecovery">WarningRecovery</a>" : <i>Double</i>
}
</pre>

### YAML

<pre>
<a href="#critical" title="Critical">Critical</a>: <i>Double</i>
<a href="#criticalrecovery" title="CriticalRecovery">CriticalRecovery</a>: <i>Double</i>
<a href="#ok" title="OK">OK</a>: <i>Double</i>
<a href="#warning" title="Warning">Warning</a>: <i>Double</i>
<a href="#warningrecovery" title="WarningRecovery">WarningRecovery</a>: <i>Double</i>
</pre>

## Properties

#### Critical

Threshold value for triggering an alert

_Required_: No

_Type_: Double

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### CriticalRecovery

Threshold value for recovering from an alert state

_Required_: No

_Type_: Double

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### OK

Threshold value for recovering from an alert state

_Required_: No

_Type_: Double

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Warning

Threshold value for triggering a warning

_Required_: No

_Type_: Double

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### WarningRecovery

Threshold value for recovering from a warning state

_Required_: No

_Type_: Double

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

