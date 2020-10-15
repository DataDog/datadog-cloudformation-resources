# Datadog::Monitors::Monitor MonitorStateGroup

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#name" title="Name">Name</a>" : <i>String</i>,
    "<a href="#lasttriggeredts" title="LastTriggeredTS">LastTriggeredTS</a>" : <i>Integer</i>,
    "<a href="#lastnotifiedts" title="LastNotifiedTS">LastNotifiedTS</a>" : <i>Integer</i>,
    "<a href="#status" title="Status">Status</a>" : <i>String</i>,
    "<a href="#lastresolvedts" title="LastResolvedTS">LastResolvedTS</a>" : <i>Integer</i>,
    "<a href="#lastnodatats" title="LastNodataTS">LastNodataTS</a>" : <i>Integer</i>
}
</pre>

### YAML

<pre>
<a href="#name" title="Name">Name</a>: <i>String</i>
<a href="#lasttriggeredts" title="LastTriggeredTS">LastTriggeredTS</a>: <i>Integer</i>
<a href="#lastnotifiedts" title="LastNotifiedTS">LastNotifiedTS</a>: <i>Integer</i>
<a href="#status" title="Status">Status</a>: <i>String</i>
<a href="#lastresolvedts" title="LastResolvedTS">LastResolvedTS</a>: <i>Integer</i>
<a href="#lastnodatats" title="LastNodataTS">LastNodataTS</a>: <i>Integer</i>
</pre>

## Properties

#### Name

Name of the group. This is a CSV of tags and filters

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### LastTriggeredTS

Timestamp when the group was last triggered

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### LastNotifiedTS

Timestamp when the group last notified

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Status

_Required_: No

_Type_: String

_Allowed Values_: <code>Alert</code> | <code>Ignored</code> | <code>No Data</code> | <code>OK</code> | <code>Skipped</code> | <code>Unknown</code> | <code>Warn</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### LastResolvedTS

Timestamp when the group was last resolved

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### LastNodataTS

Timestamp when the group was last getting no data

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

