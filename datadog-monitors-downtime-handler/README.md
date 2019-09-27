# Datadog::Monitors::Downtime

This resource represents a Datadog Monitor Downtime and is used to create and manage these downtimes. More information about Downtimes can be found in the [Dowintime documentation](https://docs.datadoghq.com/monitors/downtimes/).

## Example Usage

This example stack creates a downtime on the monitor `12345` over all groups every `Monday` and `Friday` until `1448387217`. Each day the downtime is active from 4-8pm EST.

```
Resources:
  DatadogTestDowntimeUntilDate:
    Type: 'Datadog::Monitors::Downtime'
    Properties:
      Recurrence:
        Type: "weeks"
        WeekDays: ["Monday", "Friday]
        UntilDate: 1448387217
      Message: "Setting downtime on this monitor during regular maintenance"
      MonitorId: 12345
      Scope: ["*"]
      Start: 1569614400
      End: 1569628800
      Timezone: "EST"
      DatadogCredentials:
        ApiKey: <DD_API_KEY>
        ApplicationKey: <DD_APP_KEY>
```

This example stack creates a downtime on monitors with the tag `maintanence:scheduled` over all groups every `3 days` until. Each day the downtime is active from 4-8pm UTC.

```
Resources:
  DatadogTestDowntimeUntilOccurrences:
    Type: 'Datadog::Monitors::Downtime'
    Properties:
      Recurrence:
        Period: 3
        Type: days
      Message: Muting monitors periodically for maintenance
      MonitorTags: ["maintanence:scheduled"]
      Scope: ["*"]
      Start: 1569614400
      End: 1569628800
      Timezone: UTC
      DatadogCredentials:
        ApiKey: <DD_API_KEY>
        ApplicationKey: <DD_APP_KEY>
```

## Property Reference:

For a list of available properties and their descriptions and examples, see the [JSON Schema for this resource](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-monitors-downtime-handler/datadog-monitors-downtime.json).
