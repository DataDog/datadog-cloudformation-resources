# Datadog::Monitors::Monitor State

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#monitorid" title="MonitorID">MonitorID</a>" : <i>Double</i>,
    "<a href="#groups" title="Groups">Groups</a>" : <i><a href="state-groups.md">Groups</a></i>
}
</pre>

### YAML

<pre>
<a href="#monitorid" title="MonitorID">MonitorID</a>: <i>Double</i>
<a href="#groups" title="Groups">Groups</a>: <i><a href="state-groups.md">Groups</a></i>
</pre>

## Properties

#### MonitorID

ID of the monitor

_Required_: No

_Type_: Double

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Groups

State of each monitor group

_Required_: No

_Type_: <a href="state-groups.md">Groups</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

