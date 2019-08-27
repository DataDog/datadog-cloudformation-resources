# Datadog Resources for AWS CloudFormation

This repository contains:

* All resources currently implemented for AWS CloudFormation
* A package with common functionality shared among the Resources - `datadog-cloudformation-common`

## Local Development

To build and run tests for a given resource:

* Build [datadog-api-client-java](https://github.com/DataDog/datadog-api-client-java):

    ```
    git clone git@github.com:DataDog/datadog-api-client-java.git
    cd datadog-api-client-java
    # this will install the client into ~/.m2/repository
    mvn install -Dmaven.test.skip=true
    ```

* Build `datadog-cloudformation-common` from this repository:

    ```
    # this will install the common package into ~/.m2/repository
    mvn -f datadog-cloudformation-common/pom.xml -Dmaven.test.skip=true install
    ```

* Install cfn-cli
* Do note that for now, the tests use `DD_TEST_CF_API_KEY` and `DD_TEST_CF_APP_KEY` from environment variables.
* `cd` into the directory of the resource you want to work with
* Run `mvn test` inside the directory to 

## Development Tips

* Create and Update handlers of your resource should call the Read handler (when the create/update is successful) to return a fully populated model.
* On failure, a handler should return an error message (messages are not displayed on success). For example:

    ```
    return ProgressEvent.<ResourceModel, CallbackContext>builder()
        .resourceModel(model)
        .status(OperationStatus.FAILED)
        .message("Failed to read monitor 12345")
        .build();
    ```
