# Datadog::SLOs::SLO Threshold

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#target" title="Target">Target</a>" : <i>Double</i>,
    "<a href="#targetdisplay" title="TargetDisplay">TargetDisplay</a>" : <i>String</i>,
    "<a href="#timeframe" title="Timeframe">Timeframe</a>" : <i>String</i>,
    "<a href="#warning" title="Warning">Warning</a>" : <i>Double</i>,
    "<a href="#warningdisplay" title="WarningDisplay">WarningDisplay</a>" : <i>String</i>
}
</pre>

### YAML

<pre>
<a href="#target" title="Target">Target</a>: <i>Double</i>
<a href="#targetdisplay" title="TargetDisplay">TargetDisplay</a>: <i>String</i>
<a href="#timeframe" title="Timeframe">Timeframe</a>: <i>String</i>
<a href="#warning" title="Warning">Warning</a>: <i>Double</i>
<a href="#warningdisplay" title="WarningDisplay">WarningDisplay</a>: <i>String</i>
</pre>

## Properties

#### Target

The target value for the service level indicator within the corresponding timeframe.

_Required_: No

_Type_: Double

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### TargetDisplay

A string representation of the target that indicates its precision.(e.g. 98.00)

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Timeframe

The SLO time window options. Allowed enum values: 7d,30d,90d

_Required_: No

_Type_: String

_Allowed Values_: <code>7d</code> | <code>30d</code> | <code>90d</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Warning

The warning value for the service level objective.

_Required_: No

_Type_: Double

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### WarningDisplay

A string representation of the warning target.(e.g. 98.00)

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

