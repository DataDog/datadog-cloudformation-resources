# Datadog::Monitors::Monitor MonitorAsset

A monitor asset (for example, a runbook) tied to a monitor to help users take action on alerts.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#category" title="Category">Category</a>" : <i>String</i>,
    "<a href="#name" title="Name">Name</a>" : <i>String</i>,
    "<a href="#url" title="Url">Url</a>" : <i>String</i>,
    "<a href="#resourcekey" title="ResourceKey">ResourceKey</a>" : <i>String</i>,
    "<a href="#resourcetype" title="ResourceType">ResourceType</a>" : <i>String</i>
}
</pre>

### YAML

<pre>
<a href="#category" title="Category">Category</a>: <i>String</i>
<a href="#name" title="Name">Name</a>: <i>String</i>
<a href="#url" title="Url">Url</a>: <i>String</i>
<a href="#resourcekey" title="ResourceKey">ResourceKey</a>: <i>String</i>
<a href="#resourcetype" title="ResourceType">ResourceType</a>: <i>String</i>
</pre>

## Properties

#### Category

Indicates the type of asset this entity represents on a monitor.

_Required_: Yes

_Type_: String

_Allowed Values_: <code>runbook</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Name

Name for the monitor asset.

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Url

URL link for the asset. For internal resource types (notebooks), provide a relative path. For external links, provide the full URL.

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### ResourceKey

Identifier of the internal Datadog resource that this asset represents (for example, a notebook ID). IDs should be passed as strings.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### ResourceType

Type of internal Datadog resource associated with a monitor asset.

_Required_: No

_Type_: String

_Allowed Values_: <code>notebook</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

