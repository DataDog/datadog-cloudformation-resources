# Datadog::Monitors::Downtime

This resource represents a Datadog Monitor Downtime and is used to create and manage these downtimes. More information about Downtimes can be found in the [Downtime documentation](https://docs.datadoghq.com/monitors/downtimes/).

## Example Usage

This example stack creates a downtime on the monitor `12345` until `1569628800`.

```
Resources:
  DatadogTestDowntimeUntilDate:
    Type: 'Datadog::Monitors::Downtime'
    Properties:
      Message: "Setting downtime on this monitor during regular maintenance"
      MonitorId: 12345
      Scope: ["*"]
      Start: 1569614400
      End: 1569628800
      Timezone: "EST"
      DatadogCredentials:
        ApiURL: https://api.datadoghq.com
        ApiKey: <DD_API_KEY>
        ApplicationKey: <DD_APP_KEY>
```

## Property Reference:

For a list of available properties and their descriptions and examples, see the [JSON Schema for this resource](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-monitors-downtime-handler/datadog-monitors-downtime.json).
