# Datadog::Integrations::AWS

Datadog AWS Integration 2.4.0

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "Datadog::Integrations::AWS",
    "Properties" : {
        "<a href="#accountid" title="AccountID">AccountID</a>" : <i>String</i>,
        "<a href="#awspartition" title="AWSPartition">AWSPartition</a>" : <i>String</i>,
        "<a href="#rolename" title="RoleName">RoleName</a>" : <i>String</i>,
        "<a href="#includedregions" title="IncludedRegions">IncludedRegions</a>" : <i>[ String, ... ]</i>,
        "<a href="#accounttags" title="AccountTags">AccountTags</a>" : <i>[ String, ... ]</i>,
        "<a href="#metricscollection" title="MetricsCollection">MetricsCollection</a>" : <i>Boolean</i>,
        "<a href="#automuteenabled" title="AutomuteEnabled">AutomuteEnabled</a>" : <i>Boolean</i>,
        "<a href="#collectcloudwatchallarms" title="CollectCloudwatchAllarms">CollectCloudwatchAllarms</a>" : <i>Boolean</i>,
        "<a href="#collectcustommetrics" title="CollectCustomMetrics">CollectCustomMetrics</a>" : <i>Boolean</i>,
        "<a href="#filtertags" title="FilterTags">FilterTags</a>" : <i><a href="filtertags.md">FilterTags</a></i>,
        "<a href="#includelistednamespaces" title="IncludeListedNamespaces">IncludeListedNamespaces</a>" : <i>Boolean</i>,
        "<a href="#filternamespaces" title="FilterNamespaces">FilterNamespaces</a>" : <i>[ String, ... ]</i>,
        "<a href="#logforwarderlambdas" title="LogForwarderLambdas">LogForwarderLambdas</a>" : <i>[ String, ... ]</i>,
        "<a href="#logforwardersources" title="LogForwarderSources">LogForwarderSources</a>" : <i>[ String, ... ]</i>,
        "<a href="#cspmresourcecollection" title="CSPMResourceCollection">CSPMResourceCollection</a>" : <i>Boolean</i>,
        "<a href="#extendedresourcecollection" title="ExtendedResourceCollection">ExtendedResourceCollection</a>" : <i>Boolean</i>,
        "<a href="#externalidsecretname" title="ExternalIDSecretName">ExternalIDSecretName</a>" : <i>String</i>,
        "<a href="#uuid" title="UUID">UUID</a>" : <i>String</i>
    }
}
</pre>

### YAML

<pre>
Type: Datadog::Integrations::AWS
Properties:
    <a href="#accountid" title="AccountID">AccountID</a>: <i>String</i>
    <a href="#awspartition" title="AWSPartition">AWSPartition</a>: <i>String</i>
    <a href="#rolename" title="RoleName">RoleName</a>: <i>String</i>
    <a href="#includedregions" title="IncludedRegions">IncludedRegions</a>: <i>
      - String</i>
    <a href="#accounttags" title="AccountTags">AccountTags</a>: <i>
      - String</i>
    <a href="#metricscollection" title="MetricsCollection">MetricsCollection</a>: <i>Boolean</i>
    <a href="#automuteenabled" title="AutomuteEnabled">AutomuteEnabled</a>: <i>Boolean</i>
    <a href="#collectcloudwatchallarms" title="CollectCloudwatchAllarms">CollectCloudwatchAllarms</a>: <i>Boolean</i>
    <a href="#collectcustommetrics" title="CollectCustomMetrics">CollectCustomMetrics</a>: <i>Boolean</i>
    <a href="#filtertags" title="FilterTags">FilterTags</a>: <i><a href="filtertags.md">FilterTags</a></i>
    <a href="#includelistednamespaces" title="IncludeListedNamespaces">IncludeListedNamespaces</a>: <i>Boolean</i>
    <a href="#filternamespaces" title="FilterNamespaces">FilterNamespaces</a>: <i>
      - String</i>
    <a href="#logforwarderlambdas" title="LogForwarderLambdas">LogForwarderLambdas</a>: <i>
      - String</i>
    <a href="#logforwardersources" title="LogForwarderSources">LogForwarderSources</a>: <i>
      - String</i>
    <a href="#cspmresourcecollection" title="CSPMResourceCollection">CSPMResourceCollection</a>: <i>Boolean</i>
    <a href="#extendedresourcecollection" title="ExtendedResourceCollection">ExtendedResourceCollection</a>: <i>Boolean</i>
    <a href="#externalidsecretname" title="ExternalIDSecretName">ExternalIDSecretName</a>: <i>String</i>
    <a href="#uuid" title="UUID">UUID</a>: <i>String</i>
</pre>

## Properties

#### AccountID

Your AWS Account ID without dashes.

_Required_: No

_Type_: String

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### AWSPartition

The AWS partition to use. Defaults to 'aws'.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### RoleName

Your Datadog role delegation name.

_Required_: No

_Type_: String

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### IncludedRegions

Array of AWS regions in which to collect data. If left empty, all regions will be collected

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### AccountTags

Array of tags (in the form key:value) to add to all hosts and metrics reporting through this integration.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### MetricsCollection

Enable the infrastructure monitoring Datadog product for this AWS Account. This will enable collecting all AWS metrics in your account.

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### AutomuteEnabled

Enable EC2 automute for AWS metrics

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### CollectCloudwatchAllarms

Enable CloudWatch alarms collection

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### CollectCustomMetrics

Enable custom metrics collection

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### FilterTags

An object (in the form {"namespace1":"key:value,key2:value:2", "namespace2": "!key:value"}) that filters the metrics collected for specific AWS namespaces based on attached tags.

_Required_: No

_Type_: <a href="filtertags.md">FilterTags</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### IncludeListedNamespaces

Whether to include or exclude the namespaces listed in the Namespaces property. Defaults to false, so the listed namespaces will be excluded.

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### FilterNamespaces

A list of AWS namespaces to collect metrics from. If IncludeListedNamespaces is true, only these namespaces will be collected. If false, these namespaces will be excluded.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### LogForwarderLambdas

List of Datadog Lambda Log Forwarder ARNs

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### LogForwarderSources

List of AWS services that will send logs to the Datadog Lambda Log Forwarder.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### CSPMResourceCollection

Enable the compliance and security posture management Datadog product. This will enable collecting information on your AWS resources and providing security validation.

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### ExtendedResourceCollection

Whether Datadog collects additional attributes and configuration information about the resources in your AWS account. Required for CSPMResourceCollection.

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### ExternalIDSecretName

The name of the AWS SecretsManager secret created in your account to hold this integration's `external_id`. Defaults to `DatadogIntegrationExternalID`. Cannot be referenced from created resource.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### UUID

The Datadog unique identifier for the integrated AWS account. Cannot be referenced from created resource.

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

Returns the <code>IntegrationID</code> value.

