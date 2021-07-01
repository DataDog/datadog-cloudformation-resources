# Datadog::SLOs::SLO

This resource represents a Datadog SLO, and is used to create and manage Datadog SLOs. More
 information about Datadog SLOs can be found in the [SLOs documentation](https://docs.datadoghq.com
 /monitors/service_level_objectives/).

## Example Usage

```yaml
Resources:
  DatadogTestSLO:
    Type: 'Datadog::SLOs::SLO'
    Properties:
      Type: Metric
      Query:
        Denominator: ''
        Numerator: ''
      Name: Test Metric SLO
      Description: This is a test SLO
      Thresholds:
        Target: 99.9
        Timeframe: '30d'
        TargetDisplay: '99.90'
        Warning: 99.0
        WarningDisplay: '99.0'
```
```yaml
Resources:
  DatadogTestSLO:
    Type: 'Datadog::SLOs::SLO'
    Properties:
      Type: Monitor
      Name: Test Monitor SLO
      Description: This is a test SLO
      MonitorIds: [12251, 1232345]
      Thresholds:
        Target: 99.0
        Timeframe: '30d'
        TargetDisplay: '99.00'
        Warning: 99.5
        WarningDisplay: '99.50'
```
## Property Reference:

For a list of available properties and their descriptions and examples, see the [JSON Schema for
 this resource](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-slos-slo-handler/datadog-slos-slo.json).
