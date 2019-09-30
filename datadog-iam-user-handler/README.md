# Datadog::Users::User

This resource represents a Datadog application user, and is used to create and manage Datadog users. More information about Datadog Users can be found in the [Users documentation](https://docs.datadoghq.com/api/?lang=python#users).

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

For a list of available properties and their descriptions and examples, see the [JSON Schema for this resource](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-iam-user-handler/datadog-iam-user.json).
