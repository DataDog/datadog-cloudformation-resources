// Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
// This product includes software developed at Datadog (https://www.datadoghq.com/).
// Copyright 2019-Present Datadog, Inc.
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

public class CreateHandler extends BaseHandler<CallbackContext> {

    @Override
    public ProgressEvent<ResourceModel, CallbackContext> handleRequest(
        final AmazonWebServicesClientProxy proxy,
        final ResourceHandlerRequest<ResourceModel> request,
        final CallbackContext callbackContext,
        final Logger logger) {

        final ResourceModel model = request.getDesiredResourceState();

        logger.log("Starting the Downtime Resource Create Handler");

        ApiClient apiClient = ApiClients.V1Client(
            model.getDatadogCredentials().getApiKey(),
            model.getDatadogCredentials().getApplicationKey(),
            model.getDatadogCredentials().getApiURL()
        );
        DowntimesApi downtimesApi = new DowntimesApi(apiClient);

        Downtime downtime = new Downtime()
            .message(model.getMessage())
            .monitorTags(model.getMonitorTags())
            .scope(model.getScope())
            .timezone(model.getTimezone());

        if (model.getMonitorId() != null)
            downtime.monitorId(model.getMonitorId().longValue());

        if (model.getStart() != null) {
            downtime.setStart(model.getStart().longValue());
        }
        if (model.getEnd() != null) {
            downtime.setEnd(model.getEnd().longValue());
        }

        if (model.getEnd() != null) {
            downtime.setEnd(model.getEnd().longValue());
        }

        // Not currently supported properly
        // Convert to proper type.recurrence(model.getRecurrence())
        // if (model.getRecurrence() != null) {
        //     DowntimeRecurrence downtimeRecurrenceModel = model.getRecurrence();
        //     com.datadog.api.v1.client.model.DowntimeRecurrence downtimeRecurrenceApi = new com.datadog.api.v1.client.model.DowntimeRecurrence();
        //     downtimeRecurrenceApi.setPeriod(downtimeRecurrenceModel.getPeriod());
        //     downtimeRecurrenceApi.setType(downtimeRecurrenceModel.getType());
        //     if (downtimeRecurrenceModel.getUntilDate() != null) {
        //         downtimeRecurrenceApi.setUntilDate(downtimeRecurrenceModel.getUntilDate().longValue());
        //     }
        //     downtimeRecurrenceApi.setUntilOccurrences(downtimeRecurrenceModel.getUntilOccurrences());
        //     downtimeRecurrenceApi.setWeekDays(downtimeRecurrenceModel.getWeekDays());
        //     downtime.recurrence(downtimeRecurrenceApi);
        // }

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
        model.setId(createdDowntime.getId().intValue());
        return new ReadHandler().handleRequest(proxy, request, callbackContext, logger);
    }
}
