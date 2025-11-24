# Datadog::Integrations::AWS

> **⚠️ DEPRECATION NOTICE**: This resource (`Datadog::Integrations::AWS`) is deprecated and uses the legacy v1 Datadog API.
>
> **Please use the new [`Datadog::Integrations::AWSAccount`](../datadog-integrations-awsaccount-handler/README.md) resource instead**, which uses the v2 API and provides enhanced features including:
> - More granular control over metrics, logs, traces, and resources collection
> - Support for AWS partitions (commercial, GovCloud, China)
> - Better regional configuration options
> - Improved namespace and tag filtering
>
> This resource will continue to work but may be removed in a future release when v1 API support is discontinued.

This resource represents the Datadog AWS Integration, and is used to create and manage this integration. More information about the Datadog AWS Integration can be found in the [AWS Integration documentation](https://docs.datadoghq.com/integrations/amazon_web_services/).

## Example Usage

```
Resources:
  DatadogTestAWSAccount:
    Type: 'Datadog::Integrations::AWS'
    Properties:
      AccountID: 123456
      RoleName: DatadogAWSAcctRoleName
      FilterTags: ["filter:thisTag"]
      HostTags: ["env:staging", "account:123456"]
      AccountSpecificNamespaceRules: {"api_gateway": true, "route53": false}
```

**Note** The AccountID, RoleName, and AccessKeyID cannot be updated. To update these fields, you must delete and recreate the stack.

## Property Reference:

For a list of available properties and their descriptions and examples, see the [JSON Schema for this resource](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-integrations-aws-handler/datadog-integrations-aws.json).
