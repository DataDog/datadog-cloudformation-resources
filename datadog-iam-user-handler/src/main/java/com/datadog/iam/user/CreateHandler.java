package com.datadog.iam.user;

import software.amazon.cloudformation.proxy.AmazonWebServicesClientProxy;
import software.amazon.cloudformation.proxy.Logger;
import software.amazon.cloudformation.proxy.ProgressEvent;
import software.amazon.cloudformation.proxy.OperationStatus;
import software.amazon.cloudformation.proxy.ResourceHandlerRequest;

import com.datadog.cloudformation.common.clients.ApiClients;

import com.datadog.api.v1.client.ApiClient;
import com.datadog.api.v1.client.ApiException;
import com.datadog.api.v1.client.api.UsersApi;
import com.datadog.api.v1.client.model.User;

public class CreateHandler extends BaseHandler<CallbackContext> {

    @Override
    public ProgressEvent<ResourceModel, CallbackContext> handleRequest(
        final AmazonWebServicesClientProxy proxy,
        final ResourceHandlerRequest<ResourceModel> request,
        final CallbackContext callbackContext,
        final Logger logger) {
        final ResourceModel model = request.getDesiredResourceState();

        logger.log("Starting the User Resource Create Handler");

        ApiClient apiClient = ApiClients.V1Client(
            model.getDatadogCredentials().getApiKey(),
            model.getDatadogCredentials().getApplicationKey()
        );
        UsersApi usersApi = new UsersApi(apiClient);

        User userCreatePayload = new User()
            .accessRole(User.AccessRoleEnum.fromValue(model.getAccessRole()))
            .email(model.getEmail())
            .name(model.getName())
            .handle(model.getHandle());

        try {
            usersApi.createUser(userCreatePayload);
        } catch (ApiException e) {
            String err = "Failed to create user: " + e.toString();
            logger.log(err);

            return ProgressEvent.<ResourceModel, CallbackContext>builder()
                .resourceModel(model)
                .status(OperationStatus.FAILED)
                .message(err)
                .build();
        }

        return new ReadHandler().handleRequest(proxy, request, callbackContext, logger);
    }
}
