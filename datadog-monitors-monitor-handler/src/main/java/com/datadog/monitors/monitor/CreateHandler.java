// Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
// This product includes software developed at Datadog (https://www.datadoghq.com/).
// Copyright 2019-Present Datadog, Inc.
package com.datadog.monitors.monitor;

import java.util.stream.Collectors;

import software.amazon.cloudformation.proxy.AmazonWebServicesClientProxy;
import software.amazon.cloudformation.proxy.Logger;
import software.amazon.cloudformation.proxy.ProgressEvent;
import software.amazon.cloudformation.proxy.OperationStatus;
import software.amazon.cloudformation.proxy.ResourceHandlerRequest;

import com.datadog.cloudformation.common.clients.ApiClients;

import com.datadog.api.v1.client.model.MonitorOptions;
import com.datadog.api.v1.client.model.MonitorThresholds;
import com.datadog.api.v1.client.model.MonitorThresholdWindowOptions;

import com.datadog.api.v1.client.ApiClient;
import com.datadog.api.v1.client.ApiException;
import com.datadog.api.v1.client.api.MonitorsApi;
import com.datadog.api.v1.client.model.Monitor;

public class CreateHandler extends BaseHandler<CallbackContext> {

    // TEST
    @Override
    public ProgressEvent<ResourceModel, CallbackContext> handleRequest(final AmazonWebServicesClientProxy proxy,
            final ResourceHandlerRequest<ResourceModel> request, final CallbackContext callbackContext,
            final Logger logger) {

        final ResourceModel model = request.getDesiredResourceState();

        logger.log("Starting the Monitor Resource Create Handler");

        ApiClient apiClient = ApiClients.V1Client(
            model.getDatadogCredentials().getApiKey(),
            model.getDatadogCredentials().getApplicationKey(),
            model.getDatadogCredentials().getApiURL()
        );
        MonitorOptions options = null;
        if (model.getOptions() != null) {
            options = new MonitorOptions()
                .aggregation(model.getOptions().getAggregation())
                .enableLogsSample(model.getOptions().getEnableLogsSample())
                .escalationMessage(model.getOptions().getEscalationMessage())
                .includeTags(model.getOptions().getIncludeTags())
                .locked(model.getOptions().getLocked())
                .notifyAudit(model.getOptions().getNotifyAudit())
                .notifyNoData(model.getOptions().getNotifyNoData())
                .requireFullWindow(model.getOptions().getRequireFullWindow())
                .timeoutH(model.getOptions().getTimeoutH());
            if(model.getOptions().getSyntheticsCheckID() != null)
                options.syntheticsCheckId(model.getOptions().getSyntheticsCheckID().longValue());
            if(model.getOptions().getEvaluationDelay() != null)
                options.evaluationDelay(model.getOptions().getEvaluationDelay().longValue());
            if(model.getOptions().getMinLocationFailed() != null)
                options.minLocationFailed(model.getOptions().getMinLocationFailed().longValue());
            if(model.getOptions().getNewHostDelay() != null)
                options.newHostDelay(model.getOptions().getNewHostDelay().longValue());
            if(model.getOptions().getNoDataTimeframe() != null)
                options.noDataTimeframe(model.getOptions().getNoDataTimeframe().longValue());
            if(model.getOptions().getRenotifyInterval() != null)
                options.renotifyInterval(model.getOptions().getRenotifyInterval().longValue());

            MonitorThresholds thresholds = null;
            if (model.getOptions().getThresholds() != null) {
                thresholds = new MonitorThresholds();
                if(model.getOptions().getThresholds().getCritical() != null)
                    thresholds.critical(model.getOptions().getThresholds().getCritical());
                if(model.getOptions().getThresholds().getCriticalRecovery() != null)
                    thresholds.criticalRecovery(model.getOptions().getThresholds().getCriticalRecovery());
                if(model.getOptions().getThresholds().getOK() != null)
                    thresholds.ok(model.getOptions().getThresholds().getOK());
                if(model.getOptions().getThresholds().getWarning() != null)
                    thresholds.warning(model.getOptions().getThresholds().getWarning());
                if(model.getOptions().getThresholds().getWarningRecovery() != null)
                    thresholds.warningRecovery(model.getOptions().getThresholds().getWarningRecovery());
            }
            options.thresholds(thresholds);

            MonitorThresholdWindowOptions thresholdWindows = null;
            if (model.getOptions().getThresholdWindows() != null) {
                thresholdWindows = new MonitorThresholdWindowOptions()
                    .recoveryWindow(model.getOptions().getThresholdWindows().getRecoveryWindow())
                    .triggerWindow(model.getOptions().getThresholdWindows().getTriggerWindow());
            }
            options.thresholdWindows(thresholdWindows);

            if (model.getOptions().getDeviceIDs() != null) {
                options.deviceIds(
                    model.getOptions().getDeviceIDs().stream()
                        .map(d -> MonitorOptions.DeviceIdsEnum.fromValue(d))
                        .collect(Collectors.toList())
                );
            }
        }

        MonitorsApi monitorsApi = new MonitorsApi(apiClient);
        Monitor monitor = new Monitor()
            .message(model.getMessage())
            .name(model.getName())
            .tags(model.getTags())
            .options(options)
            .query(model.getQuery())
            .type(Monitor.TypeEnum.fromValue(model.getType()))
            .multi(model.getMulti());

        Monitor createdMonitor = null;
        try {
            createdMonitor = monitorsApi.createMonitor(monitor);
        } catch (ApiException e) {
            String err = "Failed to create monitor: " + e.toString();
            logger.log(err);

            return ProgressEvent.<ResourceModel, CallbackContext>builder()
                .resourceModel(model)
                .status(OperationStatus.FAILED)
                .message(err)
                .build();
        }

        // Set ID of the returned monitor, so that the read handler can request it
        model.setId(createdMonitor.getId().doubleValue());
        return new ReadHandler().handleRequest(proxy, request, callbackContext, logger);
    }
}
