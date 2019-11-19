# Datadog::Integrations::AWS

This resource represents the Datadog AWS Integration, and is used to create and manage this integration. More information about the Datadog AWS Integration can be found in the [AWS Integration documentation](https://docs.datadoghq.com/integrations/amazon_web_services/).

## Example Usage

```
Resources:
  DatadogTestAWSAccount:
    Type: 'Datadog::Integrations::AWS'
    Properties:
      ApiURL: https://api.datadoghq.com
      AccountID: 123456
      RoleName: DatadogAWSAcctRoleName
      FilterTags: ["filter:thisTag"]
      HostTags: ["env:staging", "account:123456"]
      AccountSpecificNamespaceRules: {"api_gateway": true, "route53": false}
      DatadogCredentials:
        ApiKey: <DD_API_KEY>
        ApplicationKey: <DD_APP_KEY>
```

**Note** The AccountID, RoleName, and AccessKeyID cannot be updated. To update these fields, you must delete and recreate the stack.

## Property Reference:

For a list of available properties and their descriptions and examples, see the [JSON Schema for this resource](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-integrations-aws-handler/datadog-integrations-aws.json).
