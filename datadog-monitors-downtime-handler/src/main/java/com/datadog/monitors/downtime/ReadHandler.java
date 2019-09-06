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

public class ReadHandler extends BaseHandler<CallbackContext> {

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

        Downtime downtime = null;
        try {
            downtime = downtimesApi.getDowntime(model.getId().longValue());
        } catch (ApiException e) {
            String err = "Failed to read downtime: " + e.toString();
            logger.log(err);

            return ProgressEvent.<ResourceModel, CallbackContext>builder()
                .resourceModel(model)
                .status(OperationStatus.FAILED)
                .message(err)
                .build();
        }

        model.setId((int) (long) downtime.getId());
        model.setEnd((int) (long) downtime.getEnd());
        model.setMessage(downtime.getMessage());
        model.setMonitorId(downtime.getMonitorId());
        model.setMonitorTags(downtime.getMonitorTags());
        model.setScope(downtime.getScope());
        model.setStart((int) (long) downtime.getStart());
        model.setTimezone(downtime.getTimezone());

        if (downtime.getRecurrence() != null) {
            //Convert to proper type.recurrence(model.getRecurrence())
            DowntimeRecurrence downtimeRecurrenceModel = model.getRecurrence();
            com.datadog.api.client.v1.model.DowntimeRecurrence downtimeRecurrenceApi = downtime.getRecurrence();
            downtimeRecurrenceModel.setPeriod(downtimeRecurrenceApi.getPeriod());
            downtimeRecurrenceModel.setType(downtimeRecurrenceApi.getType());
            if (downtimeRecurrenceApi.getUntilDate() != null) {
                downtimeRecurrenceModel.setUntilDate((int) (long) downtimeRecurrenceApi.getUntilDate());
            }
            downtimeRecurrenceModel.setUntilOccurrences(downtimeRecurrenceApi.getUntilOccurrences());
            downtimeRecurrenceModel.setWeekDays(downtimeRecurrenceApi.getWeekDays());
            model.setRecurrence(downtimeRecurrenceModel);
        }

        return ProgressEvent.<ResourceModel, CallbackContext>builder()
            .resourceModel(model)
            .status(OperationStatus.SUCCESS)
            .build();
    }
}
