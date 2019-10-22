# Datadog-AWS CloudFormation
​
[AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/GettingStarted.html) gives you templates to describe, configure, and provision all of the AWS resources in your environment at once. The Datadog-AWS CloudFormation provider allows you to interact with the supported Datadog resources. To get started:

1. In your terminal, use the [aws-cli tool](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/) to register a Datadog resource.

    ```shell
    aws cloudformation register-type \
        --region <REGION> \
        --type RESOURCE \
        --type-name "<DATADOG_RESOURCE_NAME>" \
        --schema-handler-package <LINK_TO_S3_OR_GITHUB_RELEASE>
    ```

    With the following placeholders:
    * `<REGION>`: Your AWS region.
    * `<DATADOG_RESOURCE_NAME>`: The name of the resource to register, refer to the table below to see the supported resources.
    * `<LINK_TO_S3_OR_GITHUB_RELEASE>`: Link to the S3 or Github release for the resource.
      * S3 link: `s3://datadog-cloudformation-resources/<RESOURCE_FOLDER>/<RESOURCE_FOLDER>-1.0.0.zip`

2. In your AWS account, [create your AWS stack](https://console.aws.amazon.com/cloudformation/home) that includes any of the registered Datadog resources.

## Resources available

The following Datadog resources can be registered within your AWS account, refer to their specific documentation to see how to configure them:

| Resource                | Name                          | Description                                                                                                                                                    |
|-------------------------|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Datadog-AWS integration | `Datadog::Integrations::AWS`  | [Manage your Datadog-Amazon Web Service integration](https://github.com/DataDog/datadog-cloudformation-resources/tree/master/datadog-integrations-aws-handler) |
| Monitors                | `Datadog::Monitors::Monitor`  | [Create, update, and delete Datadog monitors](https://github.com/DataDog/datadog-cloudformation-resources/tree/master/datadog-monitors-monitor-handler).       |
| ​Downtimes                | `Datadog::Monitors::Downtime` | [Enable or Disable downtimes for your monitors](https://github.com/DataDog/datadog-cloudformation-resources/tree/master/datadog-monitors-downtime-handler).    |
| User                    | `Datadog::IAM::User`          | [ Create and manage Datadog users](https://github.com/DataDog/datadog-cloudformation-resources/tree/master/ddatadog-iam-user-handler).                         |

## Development

The `Datadog/datadog-cloudformation-resources` repository contains:

* All resources currently implemented for AWS CloudFormation.
* A package with common functionality shared among the Resources - `datadog-cloudformation-common`

### Setup

To set up the Datadog-AWS CloudFormation provider, follow the instructions below:

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
3. Install `cfn-cli`.

### Run tests

1. Follow the steps in [Setup](#setup).
2. `cd` into the directory of the resource to be tested.
3.  Run `mvn test` inside the directory to run the test suite for that resource.

**Note**: the tests use `DD_TEST_CF_API_KEY` and `DD_TEST_CF_APP_KEY` from environment variables.

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
