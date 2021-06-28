# Datadog::Dashboards::Dashboard

This resource represents a Datadog Dashboard, and is used to create and manage Datadog Dashboards.
More information about the Datadog Dashboards can be found in the [Dashboards documentation](https://docs.datadoghq.com/dashboards/).

## Example Usage

```
Resources:
  DatadogTestDashboard:
    Type: 'Datadog::Dashboards::Dashboard'
    Properties:
      DashboardDefinition: |
        <Put here the JSON string of the dashboard definition. Can be exported directly from the web application>
```

## Property Reference:

For a list of available properties and their descriptions and examples, see the [JSON Schema for this resource](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-dashboards-dashboard-handler/datadog-dashboards-dashboard.json).