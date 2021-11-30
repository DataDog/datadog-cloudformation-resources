# Datadog::SLOs::SLO

Datadog SLO 1.0.1

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "Datadog::SLOs::SLO",
    "Properties" : {
        "<a href="#description" title="Description">Description</a>" : <i>String</i>,
        "<a href="#groups" title="Groups">Groups</a>" : <i>[ String, ... ]</i>,
        "<a href="#monitorids" title="MonitorIds">MonitorIds</a>" : <i>[ Integer, ... ]</i>,
        "<a href="#name" title="Name">Name</a>" : <i>String</i>,
        "<a href="#query" title="Query">Query</a>" : <i><a href="query.md">Query</a></i>,
        "<a href="#tags" title="Tags">Tags</a>" : <i>[ String, ... ]</i>,
        "<a href="#thresholds" title="Thresholds">Thresholds</a>" : <i>[ <a href="threshold.md">Threshold</a>, ... ]</i>,
        "<a href="#type" title="Type">Type</a>" : <i>String</i>,
    }
}
</pre>

### YAML

<pre>
Type: Datadog::SLOs::SLO
Properties:
    <a href="#description" title="Description">Description</a>: <i>String</i>
    <a href="#groups" title="Groups">Groups</a>: <i>
      - String</i>
    <a href="#monitorids" title="MonitorIds">MonitorIds</a>: <i>
      - Integer</i>
    <a href="#name" title="Name">Name</a>: <i>String</i>
    <a href="#query" title="Query">Query</a>: <i><a href="query.md">Query</a></i>
    <a href="#tags" title="Tags">Tags</a>: <i>
      - String</i>
    <a href="#thresholds" title="Thresholds">Thresholds</a>: <i>
      - <a href="threshold.md">Threshold</a></i>
    <a href="#type" title="Type">Type</a>: <i>String</i>
</pre>

## Properties

#### Description

Description of the slo

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Groups

A list of (up to 20) monitor groups that narrow the scope of a monitor service level objective.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### MonitorIds

A list of monitor ids that defines the scope of a monitor service level objective. Required if type is monitor.

_Required_: No

_Type_: List of Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Name

Name of the slo

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Query

_Required_: No

_Type_: <a href="query.md">Query</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Tags

Tags associated with the slo

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Thresholds

_Required_: Yes

_Type_: List of <a href="threshold.md">Threshold</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Type

The type of the slo

_Required_: Yes

_Type_: String

_Allowed Values_: <code>monitor</code> | <code>metric</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the Id.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### Modified

Date of modification of the slo

#### Id

ID of the slo

#### Deleted

Date of deletion of the slo

#### State

Returns the <code>State</code> value.

#### OverallState

Returns the <code>OverallState</code> value.

#### Creator

Returns the <code>Creator</code> value.

#### Created

Date of creation of the slo

