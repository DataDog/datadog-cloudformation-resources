package com.datadog.monitors.downtime;

import com.amazonaws.cloudformation.proxy.AmazonWebServicesClientProxy;
import com.amazonaws.cloudformation.proxy.Logger;
import com.amazonaws.cloudformation.proxy.ProgressEvent;
import com.amazonaws.cloudformation.proxy.OperationStatus;
import com.amazonaws.cloudformation.proxy.ResourceHandlerRequest;

import com.datadog.cloudformation.common.clients.ApiClients;

import com.datadog.api.client.v1.ApiClient;
import com.datadog.api.client.v1.ApiException;
import com.datadog.api.client.v1.api.DowntimesApi;
import com.datadog.api.client.v1.model.Downtime;

public class CreateHandler extends BaseHandler<CallbackContext> {

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
        DowntimesApi downtimesApi = new DowntimesApi(apiClient);

        Downtime downtime = new Downtime()
            .end(model.getEnd().longValue())
            .message(model.getMessage())
            .monitorId(model.getMonitorId())
            .monitorTags(model.getMonitorTags())
            .scope(model.getScope())
            .start(model.getStart().longValue())
            .timezone(model.getTimezone());

        //Convert to proper type.recurrence(model.getRecurrence())
        DowntimeRecurrence downtimeRecurrenceModel = model.getRecurrence();
        com.datadog.api.client.v1.model.DowntimeRecurrence downtimeApi = new DowntimeRecurrence();

        downtimeApi.setPeriod(downtimeRecurrenceModel.getPeriod());

        downtime.recurrence(downtimeApi);

        try {
            downtimesApi.createDowntime(downtime);
        } catch (ApiException e) {
            String err = "Failed to create downtime: " + e.toString();
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
