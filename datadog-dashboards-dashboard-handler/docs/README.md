# Datadog::Dashboards::Dashboard

Datadog Dashboard 2.1.0 - backward compatible with 1.0.0

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "Datadog::Dashboards::Dashboard",
    "Properties" : {
        "<a href="#datadogcredentials" title="DatadogCredentials">DatadogCredentials</a>" : <i><a href="datadogcredentials.md">DatadogCredentials</a></i>,
        "<a href="#dashboarddefinition" title="DashboardDefinition">DashboardDefinition</a>" : <i>String</i>
    }
}
</pre>

### YAML

<pre>
Type: Datadog::Dashboards::Dashboard
Properties:
    <a href="#datadogcredentials" title="DatadogCredentials">DatadogCredentials</a>: <i><a href="datadogcredentials.md">DatadogCredentials</a></i>
    <a href="#dashboarddefinition" title="DashboardDefinition">DashboardDefinition</a>: <i>String</i>
</pre>

## Properties

#### DatadogCredentials

Credentials for the Datadog API

_Required_: No

_Type_: <a href="datadogcredentials.md">DatadogCredentials</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### DashboardDefinition

JSON string of the dashboard definition

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the Id.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### Id

ID of the dashboard

#### Url

Url of the dashboard

