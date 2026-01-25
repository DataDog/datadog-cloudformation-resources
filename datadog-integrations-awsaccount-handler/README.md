# Datadog::Integrations::AWSAccount

This resource represents the Datadog AWS Integration, and is used to create and manage this integration. More information about the Datadog AWS Integration can be found in the [AWS Integration documentation](https://docs.datadoghq.com/integrations/amazon_web_services/).

## Example Usage

```
Resources:
  DatadogAWSIntegration:
    Type: Datadog::Integrations::AWSAccount
    Properties:
      AccountID: 123456789101
      AWSPartition: aws
      AuthConfig:
        RoleName: DatadogAWSAcctRoleName
      ResourcesConfig:
        CSPMResourceCollection: true
```

**Note** The AccountID, and RoleName, cannot be updated. To update these fields, you must delete and recreate the stack.

## Property Reference:

For a list of available properties and their descriptions and examples, see the [JSON Schema for this resource](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-integrations-awsaccount-handler/datadog-integrations-awsaccount.json).
