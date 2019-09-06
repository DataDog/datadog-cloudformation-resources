package com.datadog.monitors.downtime;

import com.amazonaws.cloudformation.proxy.AmazonWebServicesClientProxy;
import com.amazonaws.cloudformation.proxy.Logger;
import com.amazonaws.cloudformation.proxy.OperationStatus;
import com.amazonaws.cloudformation.proxy.ProgressEvent;
import com.amazonaws.cloudformation.proxy.ResourceHandlerRequest;
import com.datadog.api.client.v1.ApiClient;
import com.datadog.api.client.v1.ApiException;
import com.datadog.api.client.v1.api.DowntimesApi;
import com.datadog.api.client.v1.model.Downtime;
import com.datadog.cloudformation.common.clients.ApiClients;

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
            .message(model.getMessage())
            .monitorId(model.getMonitorId())
            .monitorTags(model.getMonitorTags())
            .scope(model.getScope())
            .timezone(model.getTimezone());

        if (model.getStart() != null) {
            downtime.setStart(model.getStart().longValue());
        }
        if (model.getEnd() != null) {
            downtime.setEnd(model.getEnd().longValue());
        }

        if (model.getEnd() != null) {
            downtime.setEnd(model.getEnd().longValue());
        }

        //Convert to proper type.recurrence(model.getRecurrence())
        if (model.getRecurrence() != null) {
            DowntimeRecurrence downtimeRecurrenceModel = model.getRecurrence();
            com.datadog.api.client.v1.model.DowntimeRecurrence downtimeRecurrenceApi = new com.datadog.api.client.v1.model.DowntimeRecurrence();
            downtimeRecurrenceApi.setPeriod(downtimeRecurrenceModel.getPeriod());
            downtimeRecurrenceApi.setType(downtimeRecurrenceModel.getType());
            if (downtimeRecurrenceModel.getUntilDate() != null) {
                downtimeRecurrenceApi.setUntilDate(downtimeRecurrenceModel.getUntilDate().longValue());
            }
            downtimeRecurrenceApi.setUntilOccurrences(downtimeRecurrenceModel.getUntilOccurrences());
            downtimeRecurrenceApi.setWeekDays(downtimeRecurrenceModel.getWeekDays());
            downtime.recurrence(downtimeRecurrenceApi);
        }

        Downtime createdDowntime;
        try {
            createdDowntime = downtimesApi.createDowntime(downtime);
        } catch (ApiException e) {
            String err = "Failed to create downtime: " + e.toString();
            logger.log(err);

            return ProgressEvent.<ResourceModel, CallbackContext>builder()
                .resourceModel(model)
                .status(OperationStatus.FAILED)
                .message(err)
                .build();
        }

        // Set ID of the returned monitor, so that the read handler can request it
        model.setId((int) (long) createdDowntime.getId());
        return new ReadHandler().handleRequest(proxy, request, callbackContext, logger);
    }
}
