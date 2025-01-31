# Datadog::Integrations::AWS AWSRegions

The configuration for which regions to collect data from.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#includeonly" title="IncludeOnly">IncludeOnly</a>" : <i>[ String, ... ]</i>,
    "<a href="#includeall" title="IncludeAll">IncludeAll</a>" : <i>Boolean</i>
}
</pre>

### YAML

<pre>
<a href="#includeonly" title="IncludeOnly">IncludeOnly</a>: <i>
      - String</i>
<a href="#includeall" title="IncludeAll">IncludeAll</a>: <i>Boolean</i>
</pre>

## Properties

#### IncludeOnly

Array of AWS regions to include from metrics collection.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### IncludeAll

Collect data for all AWS regions.

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

