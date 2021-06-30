# Datadog::SLOs::SLO Query

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#numerator" title="Numerator">Numerator</a>" : <i>String</i>,
    "<a href="#denominator" title="Denominator">Denominator</a>" : <i>String</i>
}
</pre>

### YAML

<pre>
<a href="#numerator" title="Numerator">Numerator</a>: <i>String</i>
<a href="#denominator" title="Denominator">Denominator</a>: <i>String</i>
</pre>

## Properties

#### Numerator

A Datadog metric query for total (valid) events.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Denominator

A Datadog metric query for good events.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

