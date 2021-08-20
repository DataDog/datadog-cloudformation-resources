# Datadog::Integrations::AWS

Datadog AWS Integration 2.0.0

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "Datadog::Integrations::AWS",
    "Properties" : {
        "<a href="#accountid" title="AccountID">AccountID</a>" : <i>String</i>,
        "<a href="#rolename" title="RoleName">RoleName</a>" : <i>String</i>,
        "<a href="#accesskeyid" title="AccessKeyID">AccessKeyID</a>" : <i>String</i>,
        "<a href="#filtertags" title="FilterTags">FilterTags</a>" : <i>[ String, ... ]</i>,
        "<a href="#hosttags" title="HostTags">HostTags</a>" : <i>[ String, ... ]</i>,
        "<a href="#accountspecificnamespacerules" title="AccountSpecificNamespaceRules">AccountSpecificNamespaceRules</a>" : <i><a href="accountspecificnamespacerules.md">AccountSpecificNamespaceRules</a></i>,
        "<a href="#externalidsecretname" title="ExternalIDSecretName">ExternalIDSecretName</a>" : <i>String</i>
    }
}
</pre>

### YAML

<pre>
Type: Datadog::Integrations::AWS
Properties:
    <a href="#accountid" title="AccountID">AccountID</a>: <i>String</i>
    <a href="#rolename" title="RoleName">RoleName</a>: <i>String</i>
    <a href="#accesskeyid" title="AccessKeyID">AccessKeyID</a>: <i>String</i>
    <a href="#filtertags" title="FilterTags">FilterTags</a>: <i>
      - String</i>
    <a href="#hosttags" title="HostTags">HostTags</a>: <i>
      - String</i>
    <a href="#accountspecificnamespacerules" title="AccountSpecificNamespaceRules">AccountSpecificNamespaceRules</a>: <i><a href="accountspecificnamespacerules.md">AccountSpecificNamespaceRules</a></i>
    <a href="#externalidsecretname" title="ExternalIDSecretName">ExternalIDSecretName</a>: <i>String</i>
</pre>

## Properties

#### AccountID

Your AWS Account ID without dashes.

_Required_: No

_Type_: String

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### RoleName

Your Datadog role delegation name.

_Required_: No

_Type_: String

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### AccessKeyID

If your AWS account is a GovCloud or China account, enter the corresponding Access Key ID.

_Required_: No

_Type_: String

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### FilterTags

The array of EC2 tags (in the form key:value) defines a filter that Datadog uses when collecting metrics from EC2.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### HostTags

Array of tags (in the form key:value) to add to all hosts and metrics reporting through this integration.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### AccountSpecificNamespaceRules

An object (in the form {"namespace1":true/false, "namespace2":true/false}) that enables or disables metric collection for specific AWS namespaces for this AWS account only.

_Required_: No

_Type_: <a href="accountspecificnamespacerules.md">AccountSpecificNamespaceRules</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### ExternalIDSecretName

The name of the AWS SecretsManager secret we create in your account to hold this integration's external_id.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the IntegrationID.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### IntegrationID

An identification value that represents this integration object. Combines the AccountID, RoleName, and AccessKeyID. This shouldn't be set in a stack.

