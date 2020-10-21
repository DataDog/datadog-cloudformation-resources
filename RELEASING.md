# Releasing

This document summarizes the process of doing a new release of this project.
Release can only be performed by Datadog maintainers of this repository.

## Schedule
This project does not have a strict release schedule. However, we would make a release at least every 2 months.
  - No release will be done if no changes got merged to the `master` branch during the above mentioned window.
  - Releases may be done more frequently than the above mentioned window.

## Make Sure Everything Works

* Make sure tests are passing.
* Build locally the datadog-cloudformation-common and datadog-api-client-java maven projects locally (e.g. `maven install` from the each project's root)
* Build the resource locally (e.g. `cd <resource_folder>; cfn-cli submit --dry-run --no-role`), Submit this to an AWS account to run manual tests against

## Update Changelog

### Prerequisite

- Install [datadog_checks_dev](https://datadog-checks-base.readthedocs.io/en/latest/datadog_checks_dev.cli.html#installation) using Python 3
- Install [CloudFormation CLI Java Plugin](https://github.com/aws-cloudformation/cloudformation-cli-java-plugin/releases)

### Commands

- See changes ready for release by running `ddev release show changes . --tag-prefix <RESOURCE_TAG_PREFIX>` (where `<RESOURCE_TAG_PREFIX>` is e.g. `datadog-iam-user-`) at the root of this project. Add any missing labels to PRs if needed.
- Run `ddev release changelog . <NEW_VERSION> --tag-prefix <RESOURCE_TAG_PREFIX> -o <RESOURCE_DIRECTORY>/CHANGELOG.md` to update the `CHANGELOG.md` file at the directory belonging to the specific resource.
- Ensure that the resource changelog contains only relevant entries (currently the tooling generates changelog entries from all PRs merged for all resources) and update the root CHANGELOG.md following the existing format.
- Commit the changes to the repository in a release branch and get it approved/merged.

## Release

Note that once the release process is started, nobody should be merging/pushing anything. This process applies for each resource you'd like to release

Our team will trigger the release pipeline.

* (If you're releasing a Java resource) Bump the versions in the pom.xml, e.g. User resource pom.xml
* Update the `description` field in the resources json schema to include the version of the resource.
* If you bumped the datadog-cloudformation-common version, update the dependency in the resource you are releasing.
* If you're releasing a resource using the Java runtime (This step isn't needed for python resources):
  * Go into the resource folder and build the JAR: `mvn package` (this will also execute tests)
* Generate the zip file `cfn-cli submit --dry-run --no-role` (or use the one created during testing) and upload it to the s3 bucket.
* Create a github release for this version, and attach the generated zip file.
