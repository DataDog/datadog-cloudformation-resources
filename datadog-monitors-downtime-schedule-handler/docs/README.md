# Datadog::Monitors::DowntimeSchedule

Datadog Downtime Schedule 0.0.1

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "Datadog::Monitors::DowntimeSchedule",
    "Properties" : {
        "<a href="#tpscode" title="TPSCode">TPSCode</a>" : <i>String</i>
    }
}
</pre>

### YAML

<pre>
Type: Datadog::Monitors::DowntimeSchedule
Properties:
    <a href="#tpscode" title="TPSCode">TPSCode</a>: <i>String</i>
</pre>

## Properties

#### TPSCode

A TPS Code is automatically generated on creation and assigned as the unique identifier.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the Id.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### Id

Returns the <code>Id</code> value.

