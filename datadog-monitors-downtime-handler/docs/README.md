# Datadog::Monitors::Downtime

Datadog Monitors Downtime 2.0.0.dev

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "Datadog::Monitors::Downtime",
    "Properties" : {
        "<a href="#datadogcredentials" title="DatadogCredentials">DatadogCredentials</a>" : <i><a href="datadogcredentials.md">DatadogCredentials</a></i>,
        "<a href="#disabled" title="Disabled">Disabled</a>" : <i>Boolean</i>,
        "<a href="#end" title="End">End</a>" : <i>Integer</i>,
        "<a href="#message" title="Message">Message</a>" : <i>String</i>,
        "<a href="#monitorid" title="MonitorId">MonitorId</a>" : <i>Integer</i>,
        "<a href="#monitortags" title="MonitorTags">MonitorTags</a>" : <i>[ String, ... ]</i>,
        "<a href="#scope" title="Scope">Scope</a>" : <i>[ String, ... ]</i>,
        "<a href="#start" title="Start">Start</a>" : <i>Integer</i>,
        "<a href="#timezone" title="Timezone">Timezone</a>" : <i>String</i>,
    }
}
</pre>

### YAML

<pre>
Type: Datadog::Monitors::Downtime
Properties:
    <a href="#datadogcredentials" title="DatadogCredentials">DatadogCredentials</a>: <i><a href="datadogcredentials.md">DatadogCredentials</a></i>
    <a href="#disabled" title="Disabled">Disabled</a>: <i>Boolean</i>
    <a href="#end" title="End">End</a>: <i>Integer</i>
    <a href="#message" title="Message">Message</a>: <i>String</i>
    <a href="#monitorid" title="MonitorId">MonitorId</a>: <i>Integer</i>
    <a href="#monitortags" title="MonitorTags">MonitorTags</a>: <i>
      - String</i>
    <a href="#scope" title="Scope">Scope</a>: <i>
      - String</i>
    <a href="#start" title="Start">Start</a>: <i>Integer</i>
    <a href="#timezone" title="Timezone">Timezone</a>: <i>String</i>
</pre>

## Properties

#### DatadogCredentials

Credentials for the Datadog API

_Required_: Yes

_Type_: <a href="datadogcredentials.md">DatadogCredentials</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Disabled

Whether or not this downtime is disabled

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### End

POSIX timestamp to end the downtime. If not provided, the downtime is in effect indefinitely (i.e. until you cancel it).

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Message

Message on the downtime

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### MonitorId

A single monitor to which the downtime applies. If not provided, the downtime applies to all monitors.

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### MonitorTags

A comma-separated list of monitor tags, to which the downtime applies. The resulting downtime applies to monitors that match ALL provided monitor tags.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Scope

The scope(s) to which the downtime applies

_Required_: Yes

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Start

POSIX timestamp to start the downtime. If not provided, the downtime starts the moment it is created.

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Timezone

The timezone for the downtime

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the Id.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### Active

Whether or not this downtime is currently active

#### Canceled

POSIX Timestamp of cancellation of this downtime (null if not canceled)

#### CreatorId

Id of the user who created this downtime

#### DowntimeType

Type of this downtime

#### Id

Id of this downtime

#### ParentId

The ID of the parent downtime to this one

#### UpdaterId

Id of the user who updated this downtime

