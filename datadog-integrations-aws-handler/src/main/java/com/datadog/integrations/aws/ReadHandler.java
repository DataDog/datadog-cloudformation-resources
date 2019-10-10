package com.datadog.integrations.aws;

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

public class ReadHandler extends BaseHandler<CallbackContext> {

    @Override
    public ProgressEvent<ResourceModel, CallbackContext> handleRequest(
        final AmazonWebServicesClientProxy proxy,
        final ResourceHandlerRequest<ResourceModel> request,
        final CallbackContext callbackContext,
        final Logger logger) {

        final ResourceModel model = request.getDesiredResourceState();

        logger.log("Starting the AWS Integration Resource Read Handler");

        ApiClient apiClient = ApiClients.V1Client(
            model.getDatadogCredentials().getApiKey(),
            model.getDatadogCredentials().getApplicationKey()
        );
        AwsIntegrationApi awsApi = new AwsIntegrationApi(apiClient);


        AWSAccount awsAccount = null;
        try {
            awsAccount = awsApi.getAllAWSAccounts(model.getAccountID(), model.getRoleName(), model.getAccessKeyID()).get("accounts").get(0);
        } catch (ApiException e) {
            String err = "Failed to read AWS Integration Account: " + e.toString();
            logger.log(err);

            return ProgressEvent.<ResourceModel, CallbackContext>builder()
                .resourceModel(model)
                .status(OperationStatus.FAILED)
                .message(err)
                .build();
        }

        model.setAccountID(awsAccount.getAccountId());
        model.setRoleName(awsAccount.getRoleName());
        model.setAccessKeyID(awsAccount.getAccessKeyId());
        model.setHostTags(awsAccount.getHostTags());
        model.setFilterTags(awsAccount.getFilterTags());
        model.setAccountSpecificNamespaceRules(awsAccount.getAccountSpecificNamespaceRules());

        return ProgressEvent.<ResourceModel, CallbackContext>builder()
            .resourceModel(model)
            .status(OperationStatus.SUCCESS)
            .build();
    }
}
