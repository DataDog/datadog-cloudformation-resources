# Datadog::Integrations::AWS

# Datadog::Users::User

This resource represents the Datadog AWS Integration, and is used to create and manage this integration.

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
      DatadogCredentials:
        ApiKey: <DD_API_KEY>
        ApplicationKey: <DD_APP_KEY>
```

## Property Reference:

For a list of available properties and their descriptions and examples, see the [JSON Schema for this resource](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-integrations-aws-handler/datadog-integrations-aws.json).
