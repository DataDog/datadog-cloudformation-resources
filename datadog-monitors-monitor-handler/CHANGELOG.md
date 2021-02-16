# Changelog

## 3.0.0 / 2021-02-16

* [Fixed] Bump common-python dependencies in all resources. See [#117](https://github.com/DataDog/datadog-cloudformation-resources/pull/117).
* [Fixed] Bump datadog-api-client version. See [#114](https://github.com/DataDog/datadog-cloudformation-resources/pull/114).
* [Fixed] Bump cloudformation-cli-python-plugin version. See [#111](https://github.com/DataDog/datadog-cloudformation-resources/pull/111).
* [Fixed] Fix the user agent header when using the python common package. See [#109](https://github.com/DataDog/datadog-cloudformation-resources/pull/109).

## 3.0.0b2 / 2020-11-20

* [Fixed] Cleanup old java files and bump common-python dep in all resources. See [#105](https://github.com/DataDog/datadog-cloudformation-resources/pull/105).
* [Fixed] Bump plugin and add new build deps. See [#101](https://github.com/DataDog/datadog-cloudformation-resources/pull/101).

## 3.0.0b1 / 2020-10-30

* [Changed] Migrate monitor resource to python. See [#89](https://github.com/DataDog/datadog-cloudformation-resources/pull/89).


## 2.1.0 / 2020-08-04

* Link to Resource: `s3://datadog-cloudformation-resources/datadog-monitors-monitor/datadog-monitors-monitor-2.1.0.zip`
* Rebuilt with aws-cloudformation-rpdk-java-plugin 2.0.1.

## 2.0.0

Released on 2020-06-11

* Link to Resource: `s3://datadog-cloudformation-resources/datadog-monitors-monitor/datadog-monitors-monitor-2.0.0.zip`
* [BUGFIX] Don't try to set monitor id in the ReadHandler.
* [CHANGED] Removed attributes considered unused/unstable on the API side:
  * `MonitorOptions.Aggregation`
  * `MonitorOptions.DeviceIDs`
  * `MonitorStageGroup.LastDataTS`
  * `MonitorStateGroup.Message`
  * `MonitorStateGroup.TriggeringValue` (which was a reference to an also removed type `MonitorStateGroupValue`)

## 1.0.2

Released on 2019-11-21

* Link to Resource: `s3://datadog-cloudformation-resources/datadog-monitors-monitor/datadog-monitors-monitor-1.0.2.zip`
* [BUGFIX] Use `Double` for all previously `Float` values to get sufficient precision for high thresholds.

## 1.0.1

Released on 2019-11-19

* Link to Resource: `s3://datadog-cloudformation-resources/datadog-monitors-monitor/datadog-monitors-monitor-1.0.1.zip`
* [FEATURE] Add ApiURL property to allow managing resource in EU accounts

## 1.0.0

Released on 2019-11-18

* Link to Resource: `s3://datadog-cloudformation-resources/datadog-monitors-monitor/datadog-monitors-monitor-1.0.0.zip`
Initial release of the Datadog monitor resource for AWS CloudFormation.
