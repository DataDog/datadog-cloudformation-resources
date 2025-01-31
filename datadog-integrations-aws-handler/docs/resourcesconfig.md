# Datadog::Integrations::AWS ResourcesConfig

The configuration for ingesting AWS Resources into Datadog.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#cspmresourcecollection" title="CSPMResourceCollection">CSPMResourceCollection</a>" : <i>Boolean</i>,
    "<a href="#extendedresourcecollection" title="ExtendedResourceCollection">ExtendedResourceCollection</a>" : <i>Boolean</i>
}
</pre>

### YAML

<pre>
<a href="#cspmresourcecollection" title="CSPMResourceCollection">CSPMResourceCollection</a>: <i>Boolean</i>
<a href="#extendedresourcecollection" title="ExtendedResourceCollection">ExtendedResourceCollection</a>: <i>Boolean</i>
</pre>

## Properties

#### CSPMResourceCollection

Enable the compliance and security posture management Datadog product. This will enable collecting information on your AWS resources and providing security validation.

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### ExtendedResourceCollection

Enable collecting information on your AWS resources for use in Datadog products such as Network Process Monitoring.

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

