# Datadog::Users::User

This resource represents a Datadog App User. This can be used to create and manage Datadog Users

## Example Usage

```
Resources:
  DatadogTestUser:
    Type: 'Datadog::IAM::User'
    Properties:
      AccessRole: st
      Email: test@example.com
      Handle: test@example.com
      Name: Test LastName
      DatadogCredentials:
        ApiKey: <DD_API_KEY>
        ApplicationKey: <DD_APP_KEY>
```

## Property Reference:
Please reference the [JSON Schema for this resource](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-iam-user-handler/datadog-iam-user.json) for a list of available properties and their descriptions/examples.
