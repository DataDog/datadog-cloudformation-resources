# Datadog::Monitors::Monitor DatadogCredentials

Credentials for the Datadog API

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#apikey" title="ApiKey">ApiKey</a>" : <i>String</i>,
    "<a href="#applicationkey" title="ApplicationKey">ApplicationKey</a>" : <i>String</i>,
    "<a href="#apiurl" title="ApiURL">ApiURL</a>" : <i>String</i>
}
</pre>

### YAML

<pre>
<a href="#apikey" title="ApiKey">ApiKey</a>: <i>String</i>
<a href="#applicationkey" title="ApplicationKey">ApplicationKey</a>: <i>String</i>
<a href="#apiurl" title="ApiURL">ApiURL</a>: <i>String</i>
</pre>

## Properties

#### ApiKey

Datadog API key

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### ApplicationKey

Datadog application key

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### ApiURL

Datadog API URL (defaults to https://api.datadoghq.com) Use https://api.datadoghq.eu for EU accounts.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

