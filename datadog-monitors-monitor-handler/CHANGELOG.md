# Changelog

## 4.7.0 / 2023-09-18

* [Added] Bump common package to `0.0.19` in monitors resource. See [#280](https://github.com/DataDog/datadog-cloudformation-resources/pull/280).
* [Added] Add missing monitor options. See [#276](https://github.com/DataDog/datadog-cloudformation-resources/pull/276).
* [Added] Add support for CI monitor option `EnableSamples`. See [#274](https://github.com/DataDog/datadog-cloudformation-resources/pull/274).
* [Added] Bump datadog-api-client and cloudformation-cli-python packages. See [#268](https://github.com/DataDog/datadog-cloudformation-resources/pull/268).

* Link to Resource: `s3://datadog-cloudformation-resources/datadog-monitors-monitor/datadog-monitors-monitor-4.7.0.zip`

## 4.6.0 / 2023-04-10

* [Added] Add errors handler to all resources. See [#258](https://github.com/DataDog/datadog-cloudformation-resources/pull/258).
* [Added] Bump common package in all resources. See [#255](https://github.com/DataDog/datadog-cloudformation-resources/pull/255).
* [Changed] Bump python version to `3.9` in all resources. See [#252](https://github.com/DataDog/datadog-cloudformation-resources/pull/252).

* Link to Resource: `s3://datadog-cloudformation-resources/datadog-monitors-monitor/datadog-monitors-monitor-4.6.0.zip`

## 4.5.0 / 2023-01-05

* [Added] support for variables option. See [#237](https://github.com/DataDog/datadog-cloudformation-resources/pull/237).
* [Added] Bump common package to 0.0.12. See [#237](https://github.com/DataDog/datadog-cloudformation-resources/pull/237).
* Link to Resource: `s3://datadog-cloudformation-resources/datadog-monitors-monitor/datadog-monitors-monitor-4.5.0.zip`

## 4.4.0 / 2022-06-13

* [Added] Add missing monitor type and bump common package version. See [#221](https://github.com/DataDog/datadog-cloudformation-resources/pull/221).
* [Added] Add missing monitor fields. See [#216](https://github.com/DataDog/datadog-cloudformation-resources/pull/216). Thanks [huyngogia1997](https://github.com/huyngogia1997)
* Link to Resource: `s3://datadog-cloudformation-resources/datadog-monitors-monitor/datadog-monitors-monitor-4.4.0.zip`

## 4.3.0 / 2022-05-19

* [Added] Add missing monitors alert types and bump common package in all resources. See [#207](https://github.com/DataDog/datadog-cloudformation-resources/pull/207).
* Link to Resource: `s3://datadog-cloudformation-resources/datadog-monitors-monitor/datadog-monitors-monitor-4.3.0.zip`

## 4.2.0 / 2022-02-07

* [Added] Bump common package in all resources. See [#197](https://github.com/DataDog/datadog-cloudformation-resources/pull/197).
* [Added] Add support for `ci-pipelines alert` monitor type. See [#196](https://github.com/DataDog/datadog-cloudformation-resources/pull/196).
* [Added] Add support for RUM monitors. See [#191](https://github.com/DataDog/datadog-cloudformation-resources/pull/191).
* Link to Resource: `s3://datadog-cloudformation-resources/datadog-monitors-monitor/datadog-monitors-monitor-4.2.0.zip`

## 4.1.0 / 2021-11-23

* [Added] Update common version. See [#176](https://github.com/DataDog/datadog-cloudformation-resources/pull/176).
* [Added] Set priority on monitor creation/update. See [#170](https://github.com/DataDog/datadog-cloudformation-resources/pull/170). Thanks [bencrinkle](https://github.com/bencrinkle).
* Link to Resource: `s3://datadog-cloudformation-resources/datadog-monitors-monitor/datadog-monitors-monitor-4.1.0.zip`

## 4.0.0 / 2021-06-28

* [Added] Upgrade datadog-cloudformation-common-python version. See [#138](https://github.com/DataDog/datadog-cloudformation-resources/pull/138). Thanks [iwt-dennyschaefer](https://github.com/iwt-dennyschaefer).
* [Changed] Add Type Configuration to specify Datadog credentials instead of passing them in templates. See [#142](https://github.com/DataDog/datadog-cloudformation-resources/pull/142).
* Link to resource `s3://datadog-cloudformation-resources/datadog-monitors-monitor/datadog-monitors-monitor-4.0.0.zip`

## 3.0.0 / 2021-02-16

* [Fixed] Bump common-python dependencies in all resources. See [#117](https://github.com/DataDog/datadog-cloudformation-resources/pull/117).

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
