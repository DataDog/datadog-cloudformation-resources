# Datadog::Monitors::Monitor

This resource represents a Datadog Monitor, and is used to create and manage Datadog Monitors. More information about Datadog Monitors can be found in the [Monitors documentation](https://docs.datadoghq.com/monitors/monitor_types/).

## Example Usage

```
Resources:
  DatadogTestMonitor:
    Type: 'Datadog::Monitors::Monitor'
    Properties:
      Type: query alert
      Query: 'avg(last_1h):sum:system.cpu.system{host:host0} > 100'
      Name: Test Monitor
      Options:
        Thresholds:
          Critical: 100
          Warning: 80
          Ok: 90
        NotifyNoData: true
        EvaluationDelay: 60
      DatadogCredentials:
        ApiKey: <DD_API_KEY>
        ApplicationKey: <DD_APP_KEY>
```

## Property Reference:

For a list of available properties and their descriptions and examples, see the [JSON Schema for this resource](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-monitors-monitor-handler/datadog-monitors-monitor.json).
