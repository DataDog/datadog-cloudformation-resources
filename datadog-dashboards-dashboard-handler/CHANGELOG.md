# Changelog

## 2.0.2 / 2021-09-27

* [Fixed] Properly pass raw JSON payload to API. See [#167](https://github.com/DataDog/datadog-cloudformation-resources/pull/167).

## 2.0.1 / 2021-09-23

* [Fixed] Pass dashboard JSON payload to API directly, unmodified. See [#165](https://github.com/DataDog/datadog-cloudformation-resources/pull/165).
* Link to Resource: `s3://datadog-cloudformation-resources/datadog-dashboards-dashboard/datadog-dashboards-dashboard-2.0.1.zip`

## 2.0.0 / 2021-06-28

* [Added] Upgrade datadog-cloudformation-common-python version. See [#138](https://github.com/DataDog/datadog-cloudformation-resources/pull/138). Thanks [iwt-dennyschaefer](https://github.com/iwt-dennyschaefer).
* [Fixed] Update Datadog::Dashboards::Dashboard UPDATE handler to check/convert types of sub-models. See [#130](https://github.com/DataDog/datadog-cloudformation-resources/pull/130).
* [Changed]  Add Type Configuration to specify Datadog credentials instead of passing them in templates. See [#142](https://github.com/DataDog/datadog-cloudformation-resources/pull/142).
* Link to Resource: `s3://datadog-cloudformation-resources/datadog-dashboards-dashboard/datadog-dashboards-dashboard-2.0.0.zip`

## 1.0.0 / 2021-02-16

* [Fixed] Bump common-python dependencies in all resources. See [#117](https://github.com/DataDog/datadog-cloudformation-resources/pull/117).

## 1.0.0b2 / 2020-11-20

* [Fixed] Cleanup old java files and bump common-python dep in all resources. See [#105](https://github.com/DataDog/datadog-cloudformation-resources/pull/105).
* [Fixed] Bump plugin and add new build deps. See [#101](https://github.com/DataDog/datadog-cloudformation-resources/pull/101).

## 1.0.0b1 / 2020-10-30

* [Added] Add dashboard resource. See [#93](https://github.com/DataDog/datadog-cloudformation-resources/pull/93).
