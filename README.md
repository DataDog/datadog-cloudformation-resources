# Datadog-AWS CloudFormation

## Overview
​
[AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/GettingStarted.html) gives you a template to describe, configure, and provision all of the AWS resources in your environment at once. Datadog provides a way for you to monitor these resources.

## Setup

To build a CloudFormation resource and connect it to Datadog:

1. Build [datadog-api-client-java](https://github.com/DataDog/datadog-api-client-java):

    ```
    git clone git@github.com:DataDog/datadog-api-client-java.git
    cd datadog-api-client-java

    # This installs the client into ~/.m2/repository
    mvn install -Dmaven.test.skip=true
    ```
2. Build `datadog-cloudformation-common`:
​
    ```
    # This installs the common package into ~/.m2/repository
    mvn -f datadog-cloudformation-common/pom.xml -Dmaven.test.skip=true install
    ```
3. Install [cfn-cli]()

    **Note**: the tests use `DD_TEST_CF_API_KEY` and `DD_TEST_CF_APP_KEY` from environment variables.

## Resources Available

Now that Datadog-AWS Cloudformation is set up, use it to manipulate Datadog resources:

| Resource                | Description                                                                                                                                                    |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Datadog-AWS integration | [Manage your Datadog-Amazon Web Service integration](https://github.com/DataDog/datadog-cloudformation-resources/tree/master/datadog-integrations-aws-handler) |
| Monitors                | [Create a general Datadog monitor](https://github.com/DataDog/datadog-cloudformation-resources/tree/master/datadog-monitors-monitor-handler).                  |
| ​Downtimes                | [Set downtimes for your monitor](https://github.com/DataDog/datadog-cloudformation-resources/tree/master/datadog-monitors-downtime-handler).                   |
| User                    | [ Create and manage Datadog users](https://github.com/DataDog/datadog-cloudformation-resources/tree/master/ddatadog-iam-user-handler).                         |

## Development
​
This repository contains:

* All resources currently implemented for AWS CloudFormation.
* A package with common functionality shared among the Resources - `datadog-cloudformation-common`

### Run tests

1. Follow the steps in [Setup](#setup).
2. `cd` into the directory of the resource to be tested.
3.  Run `mvn test` inside the directory to run the test suite for that resource.

### Development Tips

* The `Create` and `Update` handlers of your resource should call the `Read` handler (when the create/update is successful) to return a fully populated model.
* On failure, a handler should return an error message. A success does not return a message. For example:
​
    ```
    return ProgressEvent.<ResourceModel, CallbackContext>builder()
        .resourceModel(model)
        .status(OperationStatus.FAILED)
        .message("Failed to read monitor 12345")
        .build();
    ```

* Primary Identifiers should all be based on required fields. Having optional fields make up this property causes errors on stack creation. These will also be displayed when `Fn:Ref` is called on this resource.
* Using the built in `logger` in the resource displays logs in CloudWatch to help debug any issues.

## Troubleshooting

Need help? Contact [Datadog support](https://docs.datadoghq.com/help/).
