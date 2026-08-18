# Datadog::Integrations::AWS (Deprecated)

**Please use the new [`Datadog::Integrations::AWSAccount`](../datadog-integrations-awsaccount-handler/README.md) resource instead**

This resource represents the Datadog AWS Integration, and is used to create and manage this integration. More information about the Datadog AWS Integration can be found in the [AWS Integration documentation](https://docs.datadoghq.com/integrations/amazon_web_services/).

## Migrating to `Datadog::Integrations::AWSAccount`

> **Do not migrate by removing this resource and adding the new one in its place.** Removing a
> `Datadog::Integrations::AWS` resource invokes its DELETE handler, which deletes the AWS integration in
> Datadog. Recreating it produces a **new external ID**, so metric collection stops until you update the
> trust policy on your IAM role, and settings such as resource collection are reset. Use the retain and
> import procedure below instead, which keeps the integration in place throughout.

### 1. Retain the existing resource

Add `DeletionPolicy` and `UpdateReplacePolicy` to the resource and deploy the stack. Nothing changes in
Datadog.

```yaml
Resources:
  DatadogTestAWSAccount:
    Type: 'Datadog::Integrations::AWS'
    DeletionPolicy: Retain
    UpdateReplacePolicy: Retain
    Properties:
      ...
```

### 2. Remove the resource from the stack

Delete the resource block from your template and deploy. Because of the retain policies, CloudFormation
stops managing the resource without invoking the DELETE handler, so the Datadog integration, its external
ID, and the Secrets Manager secret all survive.

### 3. Look up the account config ID

The new resource is addressed by the account config ID rather than by account ID and role name:

```
GET https://api.datadoghq.com/api/v2/integration/aws/accounts?aws_account_id=<ACCOUNT_ID>
```

Take `data[].id` for the config whose `attributes.auth_config.role_name` matches your role.

### 4. Import the integration under the new type

Add a `Datadog::Integrations::AWSAccount` resource to your template, setting `Id` to the config ID from the
previous step and translating your properties using the table below. Then create and execute an import
change set:

```
aws cloudformation create-change-set --stack-name <STACK> --change-set-type IMPORT \
  --resources-to-import '[{"ResourceType":"Datadog::Integrations::AWSAccount","LogicalResourceId":"DatadogAWSIntegration","ResourceIdentifier":{"Id":"<CONFIG_ID>"}}]' \
  --template-body file://template.yaml --change-set-name import-datadog-aws
```

`AuthConfig` and `AWSPartition` are required, and `AccountID` and `AuthConfig.RoleName` are create-only, so
all of them must match the live configuration or the import is rejected.

### Property mapping

| `Datadog::Integrations::AWS` | `Datadog::Integrations::AWSAccount` |
|---|---|
| `AccountID` | `AccountID` |
| `RoleName` | `AuthConfig.RoleName` |
| `HostTags` | `AccountTags` |
| `FilterTags` | `MetricsConfig.TagFilters`, as `{Namespace, Tags}` entries — v1 filtered EC2 only, so use `Namespace: AWS/EC2` |
| `AccountSpecificNamespaceRules` | `MetricsConfig.NamespaceFilters.IncludeOnly` or `ExcludeOnly`. These take **AWS namespace strings** (`AWS/EC2`), not the legacy Datadog identifiers (`ec2`) this resource used |
| `ExcludedRegions` | `AWSRegions.IncludeOnly`. There is no exclude form, so list the regions you want to keep rather than the ones you dropped |
| `MetricsCollection` | `MetricsConfig.Enabled` |
| `ResourceCollection` | `ResourcesConfig.ExtendedResourceCollection` |
| `CSPMResourceCollection` | `ResourcesConfig.CSPMResourceCollection` |
| `ExternalIDSecretName` | `ExternalIDSecretName`. The two resources have different defaults, so set this explicitly to keep using the same secret |
| `IntegrationID` (read-only) | `Id` (read-only) |
| `AccessKeyID` | Not supported — see below |

### GovCloud and China accounts

`Datadog::Integrations::AWSAccount` supports role-based authentication only; its `AuthConfig` accepts a
`RoleName` and nothing else. If you authenticate with `AccessKeyID`, there is no equivalent configuration on
the new resource, so this migration does not apply to your account. [Contact Datadog
support](https://www.datadoghq.com/support/) to discuss your options.

## Example Usage

```
Resources:
  DatadogTestAWSAccount:
    Type: 'Datadog::Integrations::AWS'
    Properties:
      AccountID: 123456
      RoleName: DatadogAWSAcctRoleName
      FilterTags: ["filter:thisTag"]
      HostTags: ["env:staging", "account:123456"]
      AccountSpecificNamespaceRules: {"api_gateway": true, "route53": false}
```

**Note** The AccountID, RoleName, and AccessKeyID cannot be updated. To update these fields, you must delete and recreate the stack.

## Property Reference:

For a list of available properties and their descriptions and examples, see the [JSON Schema for this resource](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-integrations-aws-handler/datadog-integrations-aws.json).
