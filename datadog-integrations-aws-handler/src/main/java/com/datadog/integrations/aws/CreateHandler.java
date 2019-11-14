package com.datadog.integrations.aws;

import com.amazonaws.cloudformation.proxy.AmazonWebServicesClientProxy;
import com.amazonaws.cloudformation.proxy.Logger;
import com.amazonaws.cloudformation.proxy.OperationStatus;
import com.amazonaws.cloudformation.proxy.ProgressEvent;
import com.amazonaws.cloudformation.proxy.ResourceHandlerRequest;
import com.datadog.api.v1.client.ApiClient;
import com.datadog.api.v1.client.ApiException;
import com.datadog.api.v1.client.api.AwsIntegrationApi;
import com.datadog.api.v1.client.model.AWSAccount;
import com.datadog.cloudformation.common.clients.ApiClients;


public class CreateHandler extends BaseHandler<CallbackContext> {

    @Override
    public ProgressEvent<ResourceModel, CallbackContext> handleRequest(
        final AmazonWebServicesClientProxy proxy,
        final ResourceHandlerRequest<ResourceModel> request,
        final CallbackContext callbackContext,
        final Logger logger) {

        final ResourceModel model = request.getDesiredResourceState();

        logger.log("Starting the AWS Integration Resource Create Handler");

        ApiClient apiClient = ApiClients.V1Client(
            model.getDatadogCredentials().getApiKey(),
            model.getDatadogCredentials().getApplicationKey()
        );
        AwsIntegrationApi awsApi = new AwsIntegrationApi(apiClient);

        AWSAccount awsCreatePayload = new AWSAccount()
            .accountId(model.getAccountID())
            .roleName(model.getRoleName())
            .accessKeyId(model.getAccessKeyID())
            .hostTags(model.getHostTags())
            .filterTags(model.getFilterTags())
            .accountSpecificNamespaceRules(model.getAccountSpecificNamespaceRules());

        try {
            awsApi.createAWSAccount(awsCreatePayload);
        } catch (ApiException e) {
            String err = "Failed to create AWS Account Integration: " + e.toString();
            logger.log(err);

            return ProgressEvent.<ResourceModel, CallbackContext>builder()
                .resourceModel(model)
                .status(OperationStatus.FAILED)
                .message(err)
                .build();
        }

        String integrationID = model.getAccountID() + ":" + model.getRoleName() + ":" + model.getAccessKeyID();
        model.setIntegrationID(integrationID);

        return new ReadHandler().handleRequest(proxy, request, callbackContext, logger);
    }
}
