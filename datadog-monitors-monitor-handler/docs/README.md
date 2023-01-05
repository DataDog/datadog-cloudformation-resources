# Datadog::Monitors::Monitor

Datadog Monitor 4.5.0

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "Datadog::Monitors::Monitor",
    "Properties" : {
        "<a href="#message" title="Message">Message</a>" : <i>String</i>,
        "<a href="#name" title="Name">Name</a>" : <i>String</i>,
        "<a href="#tags" title="Tags">Tags</a>" : <i>[ String, ... ]</i>,
        "<a href="#priority" title="Priority">Priority</a>" : <i>Integer</i>,
        "<a href="#options" title="Options">Options</a>" : <i><a href="monitoroptions.md">MonitorOptions</a></i>,
        "<a href="#query" title="Query">Query</a>" : <i>String</i>,
        "<a href="#type" title="Type">Type</a>" : <i>String</i>,
        "<a href="#multi" title="Multi">Multi</a>" : <i>Boolean</i>,
        "<a href="#restrictedroles" title="RestrictedRoles">RestrictedRoles</a>" : <i>[ String, ... ]</i>
    }
}
</pre>

### YAML

<pre>
Type: Datadog::Monitors::Monitor
Properties:
    <a href="#message" title="Message">Message</a>: <i>String</i>
    <a href="#name" title="Name">Name</a>: <i>String</i>
    <a href="#tags" title="Tags">Tags</a>: <i>
      - String</i>
    <a href="#priority" title="Priority">Priority</a>: <i>Integer</i>
    <a href="#options" title="Options">Options</a>: <i><a href="monitoroptions.md">MonitorOptions</a></i>
    <a href="#query" title="Query">Query</a>: <i>String</i>
    <a href="#type" title="Type">Type</a>: <i>String</i>
    <a href="#multi" title="Multi">Multi</a>: <i>Boolean</i>
    <a href="#restrictedroles" title="RestrictedRoles">RestrictedRoles</a>: <i>
      - String</i>
</pre>

## Properties

#### Message

A message to include with notifications for the monitor

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Name

Name of the monitor

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Tags

Tags associated with the monitor

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Priority

Integer from 1 (high) to 5 (low) indicating alert severity.

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Options

_Required_: No

_Type_: <a href="monitoroptions.md">MonitorOptions</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Query

The monitor query

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Type

The type of the monitor

_Required_: Yes

_Type_: String

_Allowed Values_: <code>audit alert</code> | <code>composite</code> | <code>event alert</code> | <code>event-v2 alert</code> | <code>log alert</code> | <code>metric alert</code> | <code>process alert</code> | <code>query alert</code> | <code>service check</code> | <code>synthetics alert</code> | <code>trace-analytics alert</code> | <code>slo alert</code> | <code>rum alert</code> | <code>ci-pipelines alert</code> | <code>error-tracking alert</code> | <code>ci-tests alert</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Multi

Whether or not the monitor is multi alert

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### RestrictedRoles

A list of unique role identifiers to define which roles are allowed to edit the monitor. The unique identifiers for all roles can be pulled from the [Roles API](https://docs.datadoghq.com/api/latest/roles/#list-roles) and are located in the `data.id` field. Editing a monitor includes any updates to the monitor configuration, monitor deletion, and muting of the monitor for any amount of time. `restricted_roles` is the successor of `locked`. For more information about `locked` and `restricted_roles`, see the [monitor options docs](https://docs.datadoghq.com/monitors/guide/monitor_api_options/#permissions-options).

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the Id.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### Modified

Date of modification of the monitor

#### Id

ID of the monitor

#### Deleted

Date of deletion of the monitor

#### State

Returns the <code>State</code> value.

#### OverallState

Returns the <code>OverallState</code> value.

#### Creator

Returns the <code>Creator</code> value.

#### Created

Date of creation of the monitor

