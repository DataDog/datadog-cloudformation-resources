# Changelog

## 2.4.0 / 2023-04-06

* [Added] Add errors handler to all resources. See [#258](https://github.com/DataDog/datadog-cloudformation-resources/pull/258).
* [Added] Bump common package in all resources. See [#255](https://github.com/DataDog/datadog-cloudformation-resources/pull/255).
* [Added] Add support for ExcludedRegions. See [#243](https://github.com/DataDog/datadog-cloudformation-resources/pull/243).
* [Added] Fix AWS resource metric fields setting in state. See [#244](https://github.com/DataDog/datadog-cloudformation-resources/pull/244).
* [Added] Use custom exports for AWS contract tests. See [#181](https://github.com/DataDog/datadog-cloudformation-resources/pull/181).
* [Changed] Bump python version to `3.9` in all resources. See [#252](https://github.com/DataDog/datadog-cloudformation-resources/pull/252).

## 2.3.0 / 2021-12-02

* Same as previous release 2.2.1 See version [2.2.1](#221--2021-11-30).

## 2.2.1 / 2021-11-30

* [Added] Use custom exports for AWS contract tests. See [#181](https://github.com/DataDog/datadog-cloudformation-resources/pull/181).
* Link to Resource: `s3://datadog-cloudformation-resources/datadog-integrations-aws/datadog-integrations-aws-2.2.1.zip`

## 2.2.0 / 2021-11-23

* [Added] Update common version. See [#176](https://github.com/DataDog/datadog-cloudformation-resources/pull/176).
* [Added] Support additional params for AWS resource. See [#173](https://github.com/DataDog/datadog-cloudformation-resources/pull/173).
* Link to Resource: `s3://datadog-cloudformation-resources/datadog-integrations-aws/datadog-integrations-aws-2.2.0.zip`

## 2.1.0 / 2021-08-26

* [Added] Store returned `external_id` secret in AWS SecretsManager. See [#161](https://github.com/DataDog/datadog-cloudformation-resources/pull/161).
* [Fixed] Fix read handler not finding integration. See [#143](https://github.com/DataDog/datadog-cloudformation-resources/pull/143).
* Link to Resource: `s3://datadog-cloudformation-resources/datadog-integrations-aws/datadog-integrations-aws-2.1.0.zip`

## 2.0.0 / 2021-06-28

* [Added] Upgrade datadog-cloudformation-common-python version. See [#138](https://github.com/DataDog/datadog-cloudformation-resources/pull/138). Thanks [iwt-dennyschaefer](https://github.com/iwt-dennyschaefer).
* [Changed] Add Type Configuration to specify Datadog credentials instead of passing them in templates. See [#142](https://github.com/DataDog/datadog-cloudformation-resources/pull/142).

## 1.2.0 / 2021-02-16

* [Fixed] Bump common-python dependencies in all resources. See [#117](https://github.com/DataDog/datadog-cloudformation-resources/pull/117).

## 1.2.0b1 / 2020-11-20

* [Fixed] Cleanup old java files and bump common-python dep in all resources. See [#105](https://github.com/DataDog/datadog-cloudformation-resources/pull/105).
* [Fixed] Bump plugin and add new build deps. See [#101](https://github.com/DataDog/datadog-cloudformation-resources/pull/101).
* [Changed] Migrate Datadog::Integrations::AWS resource to python. See [#95](https://github.com/DataDog/datadog-cloudformation-resources/pull/95).

## 1.1.0 / 2020-08-04

* Link to Resource: `s3://datadog-cloudformation-resources/datadog-integrations-aws/datadog-integrations-aws-1.1.0.zip`
* Rebuilt with aws-cloudformation-rpdk-java-plugin 2.0.1.

## 1.0.1

Released on 2019-11-19

* Link to Resource: `s3://datadog-cloudformation-resources/datadog-integrations-aws/datadog-integrations-aws-1.0.1.zip`
* [FEATURE] Add ApiURL property to allow managing resource in EU accounts

## 1.0.0

Released on 2019-11-18

* Link to Resource: `s3://datadog-cloudformation-resources/datadog-integrations-aws/datadog-integrations-aws-1.0.0.zip`
* Initial release of the Datadog AWS integration resource for AWS CloudFormation.
