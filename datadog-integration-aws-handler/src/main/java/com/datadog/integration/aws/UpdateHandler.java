package com.datadog.integration.aws;

import java.util.HashMap;
import java.util.Map;

import com.amazonaws.cloudformation.proxy.AmazonWebServicesClientProxy;
import com.amazonaws.cloudformation.proxy.Logger;
import com.amazonaws.cloudformation.proxy.ProgressEvent;
import com.amazonaws.cloudformation.proxy.OperationStatus;
import com.amazonaws.cloudformation.proxy.ResourceHandlerRequest;

import com.datadog.cloudformation.common.clients.ApiClients;

import com.datadog.api.client.v1.ApiClient;
import com.datadog.api.client.v1.ApiException;
import com.datadog.api.client.v1.api.AwsIntegrationApi;
import com.datadog.api.client.v1.model.AWSAccount;

public class UpdateHandler extends BaseHandler<CallbackContext> {

    @Override
    public ProgressEvent<ResourceModel, CallbackContext> handleRequest(
        final AmazonWebServicesClientProxy proxy,
        final ResourceHandlerRequest<ResourceModel> request,
        final CallbackContext callbackContext,
        final Logger logger) {

        final ResourceModel model = request.getDesiredResourceState();

        ApiClient apiClient = ApiClients.V1Client(
            model.getDatadogCredentials().getApiKey(),
            model.getDatadogCredentials().getApplicationKey()
        );
        AwsIntegrationApi awsApi = new AwsIntegrationApi(apiClient);

        // Convert the model's accountSpecificNameSpaceRules to expected object type
        Map<String, Boolean> accountSpecificNamespaceRules = new HashMap<String, Boolean>((Map)model.getAccountSpecificNamespaceRules());

        AWSAccount awsCreatePayload = new AWSAccount()
            .accountId(model.getAccountID())
            .roleName(model.getRoleName())
            .accessKeyId(model.getAccessKeyID())
            .hostTags(model.getHostTags())
            .filterTags(model.getFilterTags())
            .accountSpecificNamespaceRules(accountSpecificNamespaceRules);

            try {
                awsApi.updateAWSAccount(awsCreatePayload, model.getAccountID(), model.getRoleName(), model.getAccessKeyID());
            } catch (ApiException e) {
                String err = "Failed to update AWS Integration: " + e.toString();
                logger.log(err);

                return ProgressEvent.<ResourceModel, CallbackContext>builder()
                    .resourceModel(model)
                    .status(OperationStatus.FAILED)
                    .message(err)
                    .build();
            }

        return ProgressEvent.<ResourceModel, CallbackContext>builder()
            .resourceModel(model)
            .status(OperationStatus.SUCCESS)
            .build();
    }
}
