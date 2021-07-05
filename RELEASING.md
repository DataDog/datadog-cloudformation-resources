# Releasing

This document summarizes the process of doing a new release of this project.
Release can only be performed by Datadog maintainers of this repository.

## Schedule
This project does not have a strict release schedule. However, we would make a release at least every 2 months.
  - No release will be done if no changes got merged to the `master` branch during the above mentioned window.
  - Releases may be done more frequently than the above mentioned window.

## Make Sure Everything Works

* Make sure tests are passing.
* Submit the resource to a test AWS account to run manual tests (e.g. `cd <resource_folder>; cfn-cli submit --no-role`).

## Update Changelog

### Prerequisite

- Install [datadog_checks_dev](https://datadog-checks-base.readthedocs.io/en/latest/datadog_checks_dev.cli.html#installation) using Python 3

### Commands

- See changes ready for release by running `ddev release show changes . --tag-prefix <RESOURCE_TAG_PREFIX>` (where `<RESOURCE_TAG_PREFIX>` is e.g. `datadog-iam-user-`) at the root of this project. Add any missing labels to PRs if needed.
- Run `ddev release changelog . <NEW_VERSION> --tag-prefix <RESOURCE_TAG_PREFIX> -o <RESOURCE_DIRECTORY>/CHANGELOG.md` to update the `CHANGELOG.md` file at the directory belonging to the specific resource.
- Ensure that the resource changelog contains only relevant entries (currently the tooling generates changelog entries from all PRs merged for all resources) and update the root CHANGELOG.md following the existing format.
- Add the link to the s3 bucket where the release will be uploaded.
- Commit the changes to the repository in a release branch.

## Release

Note that once the release process is started, nobody should be merging/pushing anything. This process applies for each resource you'd like to release

Our team will trigger the release pipeline.

* Bump the version in `version.py`.
* Bump the version in the `description` field of the resource's JSON schema.
* If you bumped the datadog-cloudformation-common version, update the dependency in the resource you are releasing.
* Merge the release PR.
* Run the `publish` script `./publish -f <RESOURCE_DIRECTORY> -r <REGION> -t <RESOURCE_TYPE_NAME> -v <VERSION>`.
* Upload the generated ZIP file to the s3 bucket `aws s3 cp <ZIP_FILE> s3://datadog-cloudformation-resources/<RESOURCE_NAME>/<RESOURCE_NAME>-<VERSION>.zip`.
* Create a github release for this version, and attach the generated ZIP file.
