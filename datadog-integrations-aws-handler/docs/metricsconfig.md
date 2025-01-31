# Datadog::Integrations::AWS MetricsConfig

The configuration for ingesting AWS Metrics into Datadog.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#enabled" title="Enabled">Enabled</a>" : <i>Boolean</i>,
    "<a href="#automuteenabled" title="AutomuteEnabled">AutomuteEnabled</a>" : <i>Boolean</i>,
    "<a href="#collectcloudwatchalarms" title="CollectCloudwatchAlarms">CollectCloudwatchAlarms</a>" : <i>Boolean</i>,
    "<a href="#collectcustommetrics" title="CollectCustomMetrics">CollectCustomMetrics</a>" : <i>Boolean</i>,
    "<a href="#tagfilters" title="TagFilters">TagFilters</a>" : <i>[ <a href="metricsconfig.md">MetricsConfig</a>, ... ]</i>,
    "<a href="#namespacefilters" title="NamespaceFilters">NamespaceFilters</a>" : <i><a href="metricsconfig.md">MetricsConfig</a></i>
}
</pre>

### YAML

<pre>
<a href="#enabled" title="Enabled">Enabled</a>: <i>Boolean</i>
<a href="#automuteenabled" title="AutomuteEnabled">AutomuteEnabled</a>: <i>Boolean</i>
<a href="#collectcloudwatchalarms" title="CollectCloudwatchAlarms">CollectCloudwatchAlarms</a>: <i>Boolean</i>
<a href="#collectcustommetrics" title="CollectCustomMetrics">CollectCustomMetrics</a>: <i>Boolean</i>
<a href="#tagfilters" title="TagFilters">TagFilters</a>: <i>
      - <a href="metricsconfig.md">MetricsConfig</a></i>
<a href="#namespacefilters" title="NamespaceFilters">NamespaceFilters</a>: <i><a href="metricsconfig.md">MetricsConfig</a></i>
</pre>

## Properties

#### Enabled

Enable the infrastructure monitoring Datadog product for this AWS Account. This will enable collecting all AWS metrics in your account.

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### AutomuteEnabled

Enable EC2 automute for AWS metrics

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### CollectCloudwatchAlarms

Enable CloudWatch alarms collection

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### CollectCustomMetrics

Enable custom metrics collection

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### TagFilters

The array of EC2 tags (in the form key:value) defines a filter that Datadog uses when collecting metrics from EC2.

_Required_: No

_Type_: List of <a href="metricsconfig.md">MetricsConfig</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### NamespaceFilters

_Required_: No

_Type_: <a href="metricsconfig.md">MetricsConfig</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

