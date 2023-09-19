# Datadog::Monitors::DowntimeSchedule

This resource represents a Datadog Monitor Downtime and is used to create and manage these downtimes. More information about Downtimes can be found in the [Downtime documentation](https://docs.datadoghq.com/monitors/downtimes/).

## Example Usage

This example stack creates a downtime on scope `env:(staging OR dev)`.

```
Resources:
  DatadogTestDowntimeOnetime:
    Type: 'Datadog::Monitors::DowntimeSchedule'
    Properties:
      Message: "Setting downtime on this monitor during regular maintenance"
      Scope: "env:(staging OR prod)"
      Timezone: "EST"
      NotifyEndStates: ["warn"]
      NotifyEndTypes: ["expired"]
      MonitorIdentifier:
        MonitorTags: ["cat:hatcf1234"]
      Schedule:
        Start: "2050-01-02T03:04:05+00:00"
```

## Property Reference:

For a list of available properties and their descriptions and examples, see the [JSON Schema for this resource](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-monitors-downtimeschedule-handler/datadog-monitors-downtimeschedule.json).