# Datadog::Integrations::AWSAccount

Datadog AWS Account Integration 0.0.1

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "Datadog::Integrations::AWSAccount",
    "Properties" : {
        "<a href="#accountid" title="AccountID">AccountID</a>" : <i>String</i>,
        "<a href="#awspartition" title="AWSPartition">AWSPartition</a>" : <i>String</i>,
        "<a href="#authconfig" title="AuthConfig">AuthConfig</a>" : <i><a href="authconfig.md">AuthConfig</a></i>,
        "<a href="#awsregions" title="AWSRegions">AWSRegions</a>" : <i><a href="awsregions.md">AWSRegions</a></i>,
        "<a href="#metricsconfig" title="MetricsConfig">MetricsConfig</a>" : <i><a href="metricsconfig.md">MetricsConfig</a></i>,
        "<a href="#accounttags" title="AccountTags">AccountTags</a>" : <i>[ String, ... ]</i>,
        "<a href="#resourcesconfig" title="ResourcesConfig">ResourcesConfig</a>" : <i><a href="resourcesconfig.md">ResourcesConfig</a></i>,
        "<a href="#logsconfig" title="LogsConfig">LogsConfig</a>" : <i><a href="logsconfig.md">LogsConfig</a></i>,
        "<a href="#tracesconfig" title="TracesConfig">TracesConfig</a>" : <i><a href="tracesconfig.md">TracesConfig</a></i>,
        "<a href="#externalidsecretname" title="ExternalIDSecretName">ExternalIDSecretName</a>" : <i>String</i>
    }
}
</pre>

### YAML

<pre>
Type: Datadog::Integrations::AWSAccount
Properties:
    <a href="#accountid" title="AccountID">AccountID</a>: <i>String</i>
    <a href="#awspartition" title="AWSPartition">AWSPartition</a>: <i>String</i>
    <a href="#authconfig" title="AuthConfig">AuthConfig</a>: <i><a href="authconfig.md">AuthConfig</a></i>
    <a href="#awsregions" title="AWSRegions">AWSRegions</a>: <i><a href="awsregions.md">AWSRegions</a></i>
    <a href="#metricsconfig" title="MetricsConfig">MetricsConfig</a>: <i><a href="metricsconfig.md">MetricsConfig</a></i>
    <a href="#accounttags" title="AccountTags">AccountTags</a>: <i>
      - String</i>
    <a href="#resourcesconfig" title="ResourcesConfig">ResourcesConfig</a>: <i><a href="resourcesconfig.md">ResourcesConfig</a></i>
    <a href="#logsconfig" title="LogsConfig">LogsConfig</a>: <i><a href="logsconfig.md">LogsConfig</a></i>
    <a href="#tracesconfig" title="TracesConfig">TracesConfig</a>: <i><a href="tracesconfig.md">TracesConfig</a></i>
    <a href="#externalidsecretname" title="ExternalIDSecretName">ExternalIDSecretName</a>: <i>String</i>
</pre>

## Properties

#### AccountID

Your AWS Account ID without dashes.

_Required_: No

_Type_: String

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### AWSPartition

The AWS partition to use. This should be set to 'aws' for commercial accounts, 'aws-us-gov' for GovCloud accounts, and 'aws-cn' for China accounts.

_Required_: No

_Type_: String

_Allowed Values_: <code>aws</code> | <code>aws-us-gov</code> | <code>aws-cn</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### AuthConfig

The configuration for the AWS role delegation.

_Required_: No

_Type_: <a href="authconfig.md">AuthConfig</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### AWSRegions

The configuration for which regions to collect data from.

_Required_: No

_Type_: <a href="awsregions.md">AWSRegions</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### MetricsConfig

The configuration for ingesting AWS Metrics into Datadog.

_Required_: No

_Type_: <a href="metricsconfig.md">MetricsConfig</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### AccountTags

Array of tags (in the form key:value) to add to all hosts and metrics reporting through this integration.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### ResourcesConfig

The configuration for ingesting AWS Resources into Datadog.

_Required_: No

_Type_: <a href="resourcesconfig.md">ResourcesConfig</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### LogsConfig

The configuration for ingesting AWS Logs into Datadog.

_Required_: No

_Type_: <a href="logsconfig.md">LogsConfig</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### TracesConfig

The configuration for ingesting AWS Traces into Datadog.

_Required_: No

_Type_: <a href="tracesconfig.md">TracesConfig</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### ExternalIDSecretName

The name of the AWS SecretsManager secret created in your account to hold this integration's `external_id`. Defaults to `DatadogIntegrationExternalID`. Cannot be referenced from created resource.

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

An identification value that represents this integration object. Combines the AccountID and RoleName. This shouldn't be set in a stack.

