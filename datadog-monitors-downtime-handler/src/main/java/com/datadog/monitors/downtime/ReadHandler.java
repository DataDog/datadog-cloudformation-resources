package com.datadog.monitors.downtime;

import software.amazon.cloudformation.proxy.AmazonWebServicesClientProxy;
import software.amazon.cloudformation.proxy.Logger;
import software.amazon.cloudformation.proxy.OperationStatus;
import software.amazon.cloudformation.proxy.ProgressEvent;
import software.amazon.cloudformation.proxy.ResourceHandlerRequest;
import com.datadog.api.v1.client.ApiClient;
import com.datadog.api.v1.client.ApiException;
import com.datadog.api.v1.client.api.DowntimesApi;
import com.datadog.api.v1.client.model.Downtime;
import com.datadog.cloudformation.common.clients.ApiClients;

public class ReadHandler extends BaseHandler<CallbackContext> {

    @Override
    public ProgressEvent<ResourceModel, CallbackContext> handleRequest(
        final AmazonWebServicesClientProxy proxy,
        final ResourceHandlerRequest<ResourceModel> request,
        final CallbackContext callbackContext,
        final Logger logger) {

        final ResourceModel model = request.getDesiredResourceState();

        logger.log("Starting the Downtime Resource Read Handler");

        ApiClient apiClient = ApiClients.V1Client(
            model.getDatadogCredentials().getApiKey(),
            model.getDatadogCredentials().getApplicationKey(),
            model.getDatadogCredentials().getApiURL()
        );
        DowntimesApi downtimesApi = new DowntimesApi(apiClient);

        Downtime downtime = null;
        try {
            downtime = downtimesApi.getDowntime(model.getId().longValue(), null);
        } catch (ApiException e) {
            String err = "Failed to read downtime: " + e.toString();
            logger.log(err);

            return ProgressEvent.<ResourceModel, CallbackContext>builder()
                .resourceModel(model)
                .status(OperationStatus.FAILED)
                .message(err)
                .build();
        }

        model.setId(downtime.getId().intValue());
        if(downtime.getEnd() != null)
            model.setEnd(downtime.getEnd().intValue());
        model.setMessage(downtime.getMessage());
        if (downtime.getMonitorId() != null)
            model.setMonitorId(downtime.getMonitorId().doubleValue());
        model.setMonitorTags(downtime.getMonitorTags());
        model.setScope(downtime.getScope());
        if(downtime.getStart() != null)
            model.setStart(downtime.getStart().intValue());
        model.setTimezone(downtime.getTimezone());

        // Not currently supported properly
        // if (downtime.getRecurrence() != null) {
        //     // Convert to proper type.recurrence(model.getRecurrence())
        //     DowntimeRecurrence downtimeRecurrenceModel = model.getRecurrence();
        //     com.datadog.api.v1.client.model.DowntimeRecurrence downtimeRecurrenceApi = downtime.getRecurrence();
        //     downtimeRecurrenceModel.setPeriod(downtimeRecurrenceApi.getPeriod());
        //     downtimeRecurrenceModel.setType(downtimeRecurrenceApi.getType());
        //     if (downtimeRecurrenceApi.getUntilDate() != null) {
        //         downtimeRecurrenceModel.setUntilDate(downtimeRecurrenceApi.getUntilDate().intValue());
        //     }
        //     downtimeRecurrenceModel.setUntilOccurrences(downtimeRecurrenceApi.getUntilOccurrences());
        //     downtimeRecurrenceModel.setWeekDays(downtimeRecurrenceApi.getWeekDays());
        //     model.setRecurrence(downtimeRecurrenceModel);
        // }

        return ProgressEvent.<ResourceModel, CallbackContext>builder()
            .resourceModel(model)
            .status(OperationStatus.SUCCESS)
            .build();
    }
}
