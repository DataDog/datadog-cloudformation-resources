# Development

The `Datadog/datadog-cloudformation-resources` repository contains:

* All resources currently implemented for AWS CloudFormation.
* A package with common functionality shared among the Resources - `datadog-cloudformation-common`

## Setup

To set up the Datadog-AWS CloudFormation provider, follow the instructions below:

1. Build [datadog-api-client-java][12]:

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
3. Install [`cfn-cli`](https://github.com/aws-cloudformation/cloudformation-cli).

## Testing

1. Follow the steps in [Setup](#setup).
2. `cd` into the directory of the resource to be tested.
3.  Run `mvn test` inside the directory to run the test suite for that resource.

**Note**: the tests use `DD_TEST_CF_API_KEY`, `DD_TEST_CF_APP_KEY` and optionally also `DD_TEST_CF_API_URL` from environment variables.

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

### Local testing
Before submitting the resource to an AWS account for final testing, you can simulate lifecycle events of a resource locally. 
This allows for quickly iterating and manually testing out changes during development.
A more complete tutorial can be found here - https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/resource-type-walkthrough.html

To simulate local events, create a `sam-tests` directory at the root of the resource. Then create a json file for each lifecycle event. 

Ex:
`datadog-iam-user-handler/sam-tests/create.json`

```json
{
    "credentials": {
      "accessKeyId": "",
      "secretAccessKey": "",
      "sessionToken": ""
    },
    "action": "CREATE",
    "request": {
        "clientRequestToken": "4b90a7e4-b790-456b-a937-0cfdfa211dfe",
        "desiredResourceState": {
          "AccessRole": "st",
          "Email": "cf-test@datadoghq.com",
          "Handle": "cf-test@datadoghq.com",
          "Name": "Test LastName",
          "DatadogCredentials": {
            "ApiURL": "https:api.datadoghq.com",
            "ApiKey": "<API_KEY_FOR_ORG>",
            "ApplicationKey": "<APP_KEY_FOR_ORG>"
          }
        },
        "logicalResourceIdentifier": "Datadog::IAM::User"
    },
    "callbackContext": null
}
```

where:

* `action`: is the lifecycle event; CREATE/UPDATE/DELETE/READ
* `request/clientRequestToken`: is any guid, this can be left as the example
* `request/desiredResourceState`: is the object of the schema you're looking to create

Once done, you can run: `sam local invoke TestEntrypoint --event sam-tests/create.json` from within the resource directory to trigger this event. 
This will make a real request to the Datadog API by running through your handler code.


**NOTE** Any code changes to the resource will require a re-building of the resource before running the `sam` command again. You can re-build with `cfn submit --dry-run`
