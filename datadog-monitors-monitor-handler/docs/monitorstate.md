# Datadog::Monitors::Monitor MonitorState

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#monitorid" title="MonitorID">MonitorID</a>" : <i>String</i>,
    "<a href="#overallstate" title="OverallState">OverallState</a>" : <i>String</i>,
    "<a href="#groups" title="Groups">Groups</a>" : <i><a href="monitorstate-groups.md">Groups</a></i>
}
</pre>

### YAML

<pre>
<a href="#monitorid" title="MonitorID">MonitorID</a>: <i>String</i>
<a href="#overallstate" title="OverallState">OverallState</a>: <i>String</i>
<a href="#groups" title="Groups">Groups</a>: <i><a href="monitorstate-groups.md">Groups</a></i>
</pre>

## Properties

#### MonitorID

ID of the monitor

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### OverallState

_Required_: No

_Type_: String

_Allowed Values_: <code>Alert</code> | <code>Ignored</code> | <code>No Data</code> | <code>OK</code> | <code>Skipped</code> | <code>Unknown</code> | <code>Warn</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Groups

State of each monitor group

_Required_: No

_Type_: <a href="monitorstate-groups.md">Groups</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

