# Datadog::Dashboards::Dashboard

Datadog Dashboard 1.0.0

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "Datadog::Dashboards::Dashboard",
    "Properties" : {
        "<a href="#dashboarddefinition" title="DashboardDefinition">DashboardDefinition</a>" : <i>Map</i>
    }
}
</pre>

### YAML

<pre>
Type: Datadog::Dashboards::Dashboard
Properties:
    <a href="#dashboarddefinition" title="DashboardDefinition">DashboardDefinition</a>: <i>Map</i>
</pre>

## Properties

#### DashboardDefinition

JSON string of the dashboard definition

_Required_: Yes

_Type_: Map

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

