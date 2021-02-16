# Datadog::IAM::User

Datadog Application User 1.2.0

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "Datadog::IAM::User",
    "Properties" : {
        "<a href="#datadogcredentials" title="DatadogCredentials">DatadogCredentials</a>" : <i><a href="datadogcredentials.md">DatadogCredentials</a></i>,
        "<a href="#accessrole" title="AccessRole">AccessRole</a>" : <i>String</i>,
        "<a href="#email" title="Email">Email</a>" : <i>String</i>,
        "<a href="#handle" title="Handle">Handle</a>" : <i>String</i>,
        "<a href="#name" title="Name">Name</a>" : <i>String</i>,
    }
}
</pre>

### YAML

<pre>
Type: Datadog::IAM::User
Properties:
    <a href="#datadogcredentials" title="DatadogCredentials">DatadogCredentials</a>: <i><a href="datadogcredentials.md">DatadogCredentials</a></i>
    <a href="#accessrole" title="AccessRole">AccessRole</a>: <i>String</i>
    <a href="#email" title="Email">Email</a>: <i>String</i>
    <a href="#handle" title="Handle">Handle</a>: <i>String</i>
    <a href="#name" title="Name">Name</a>: <i>String</i>
</pre>

## Properties

#### DatadogCredentials

Credentials for the Datadog API

_Required_: Yes

_Type_: <a href="datadogcredentials.md">DatadogCredentials</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### AccessRole

The role of the user

_Required_: No

_Type_: String

_Allowed Values_: <code>adm</code> | <code>ro</code> | <code>st</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Email

User email

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Handle

User handle (a valid email)

_Required_: Yes

_Type_: String

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### Name

User name

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the Handle.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### Disabled

Wheter or not the user is disabled

#### Verified

Whether or not the user is verified

