package com.datadog.iam.user;

import com.amazonaws.cloudformation.proxy.AmazonWebServicesClientProxy;
import com.amazonaws.cloudformation.proxy.Logger;
import com.amazonaws.cloudformation.proxy.ProgressEvent;
import com.amazonaws.cloudformation.proxy.OperationStatus;
import com.amazonaws.cloudformation.proxy.ResourceHandlerRequest;

import com.datadog.cloudformation.common.clients.ApiClients;

import com.datadog.api.client.v1.ApiClient;
import com.datadog.api.client.v1.ApiException;
import com.datadog.api.client.v1.api.UsersApi;
import com.datadog.api.client.v1.model.User;
import com.datadog.api.client.v1.model.UserUpdatePayload;
import com.datadog.api.client.v1.model.UserUpdateResponse;

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
        UsersApi usersApi = new UsersApi(apiClient);

        UserUpdatePayload userUpdatePayload = new UserUpdatePayload()
            .accessRole(UserUpdatePayload.AccessRoleEnum.fromValue(model.getAccessRole()))
            .disabled(model.getDisabled())
            .email(model.getEmail())
            .name(model.getName());

        try {
            usersApi.updateUser(model.getHandle(), userUpdatePayload);
        } catch (ApiException e) {
            String err = "Failed to update user: " + e.toString();
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