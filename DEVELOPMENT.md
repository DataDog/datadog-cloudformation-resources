# Development

The `Datadog/datadog-cloudformation-resources` repository contains:

* All resources currently implemented for AWS CloudFormation.
* A package with common functionality shared among the Resources - `datadog-cloudformation-common`

## Prerequisites:

- [CloudFormation CLI](https://github.com/aws-cloudformation/cloudformation-cli) 0.2.13
- [cloudformation-cli-python-plugin ](https://github.com/aws-cloudformation/cloudformation-cli-python-plugin) 2.1.4
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

### Development Tips

* The `Create` and `Update` handlers of your resource should call the `Read` handler (when the create/update is successful) to return a fully populated model.
  * On failure, a handler should return an error message. A success does not return a message. For example:

   ```
    return ProgressEvent(
        status=OperationStatus.FAILED,
        resourceModel=model,
        message=f"Error getting monitor: 12345",
        errorCode=http_to_handler_error_code(e.status)
    )
   ```

* Primary Identifiers should all be based on required fields. Having optional fields make up this property causes errors on stack creation. These will also be displayed when `Fn:Ref` is called on this resource.
* Using the built in `logger` in the resource displays logs in CloudWatch to help debug any issues.

### Testing the resource manually in AWS

1. Install the prerequisites in [Prerequisites](#Prerequisites:).
2. `cd` into the directory of the resource to be tested.
3. Run `cfn generate` to generate code based on the project and resource type schema.
4. Run `cfn submit --set-default` to register the extension with CloudFormation and set it as the default version.
5. Create a stack in AWS with the submitted resource.


### Local testing using contract tests

AWS Cloudformation CLI provides tests to ensure resource type is behaving as expected during each event in the resource lifecycle.
AWS requires all contracts tests to pass for resource to be registered.

1. Install the prerequisites in [Prerequisites](#Prerequisites:).
2. `cd` into the directory of the resource to be tested.
3. Run `cfn generate` to generate code based on the project and resource type schema.
4. Run `cfn submit --dry-run`. This will generate a zip file and place it in your current directory.
5. Start a local AWS Lambda endpoint `sam local start-lambda`
6. Run the contract tests `cfn test`

### Local testing using lifecycle events

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
