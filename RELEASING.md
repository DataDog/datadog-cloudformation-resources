# Releasing

This document summarizes the process of doing a new release of this project.
Release can only be performed by Datadog maintainers of this repository.

## Schedule
This project does not have a strict release schedule. However, we would make a release at least every 2 months.
  - No release will be done if no changes got merged to the `master` branch during the above mentioned window.
  - Releases may be done more frequently than the above mentioned window.
  - Create a pager duty schedule corresponding to this.
  - Create a google calendar schedule corresponding to this.

## Make Sure Everything Works

* Make sure tests are passing.
* Build locally the datadog-cloudformation-common and datadog-api-client-java maven projects locally (e.g. `maven install` from the each project's root)
* Build the resource locally (e.g. `cd <resource_folder>; cfn-cli submit --dry-run --no-role`), Submit this to an AWS account to run manual tests against

## Update Changelog

### Prerequisite

- Install [datadog_checks_dev](https://datadog-checks-base.readthedocs.io/en/latest/datadog_checks_dev.cli.html#installation) using Python 3
- Install [CloudFormation CLI Java Plugin](https://github.com/aws-cloudformation/cloudformation-cli-java-plugin/releases)

### Commands

- See changes ready for release by running `ddev release show changes .` at the root of this project. Add any missing labels to PRs if needed.
- Run `ddev release changelog . <NEW_VERSION>` to update the `CHANGELOG.md` file at the root of this repository
- Manually move each changelog item to the resource folder's CHANGELOG.md file to which it belongs and update the root CHANGELOG.md following the existing format.
- Commit the changes to the repository in a release branch and get it approved/merged.

## Release

Note that once the release process is started, nobody should be merging/pushing anything. This process applies for each resource you'd like to release

Our team will trigger the release pipeline.

* Bump the versions in the pom.xml, e.g. User resource pom.xml
* If you bumped the datadog-cloudformation-common version, update the dependency in the resource you are releasing.
* Go into the resource folder and build the JAR: `mvn package` (this will also execute tests)
* Generate the zip file `cfn-cli submit --dry-run --no-role` (or use the one created during testing) and upload it to the s3 bucket.
* Create a github release for this version, and attach the generated zip file.
