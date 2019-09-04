package com.datadog.monitors.monitor;

import java.util.stream.Collectors;

import com.amazonaws.cloudformation.proxy.AmazonWebServicesClientProxy;
import com.amazonaws.cloudformation.proxy.Logger;
import com.amazonaws.cloudformation.proxy.ProgressEvent;
import com.amazonaws.cloudformation.proxy.OperationStatus;
import com.amazonaws.cloudformation.proxy.ResourceHandlerRequest;

import com.datadog.cloudformation.common.clients.ApiClients;

import com.datadog.api.client.v1.model.MonitorOptions;
import com.datadog.api.client.v1.model.MonitorThresholds;
import com.datadog.api.client.v1.model.MonitorThresholdWindows;

import com.datadog.api.client.v1.ApiClient;
import com.datadog.api.client.v1.ApiException;
import com.datadog.api.client.v1.api.MonitorsApi;
import com.datadog.api.client.v1.model.Monitor;

public class CreateHandler extends BaseHandler<CallbackContext> {

    @Override
    public ProgressEvent<ResourceModel, CallbackContext> handleRequest(final AmazonWebServicesClientProxy proxy,
            final ResourceHandlerRequest<ResourceModel> request, final CallbackContext callbackContext,
            final Logger logger) {

        final ResourceModel model = request.getDesiredResourceState();

        ApiClient apiClient = ApiClients.V1Client(
            model.getDatadogCredentials().getApiKey(),
            model.getDatadogCredentials().getApplicationKey()
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
                    thresholds.critical(model.getOptions().getThresholds().getCritical().floatValue());
                if(model.getOptions().getThresholds().getCriticalRecovery() != null)
                    thresholds.criticalRecovery(model.getOptions().getThresholds().getCriticalRecovery().floatValue());
                if(model.getOptions().getThresholds().getOK() != null)
                    thresholds.ok(model.getOptions().getThresholds().getOK().floatValue());
                if(model.getOptions().getThresholds().getWarning() != null)
                    thresholds.warning(model.getOptions().getThresholds().getWarning().floatValue());
                if(model.getOptions().getThresholds().getWarningRecovery() != null)
                    thresholds.warningRecovery(model.getOptions().getThresholds().getWarningRecovery().floatValue());
            }
            options.thresholds(thresholds);

            MonitorThresholdWindows thresholdWindows = null;
            if (model.getOptions().getThresholdWindows() != null) {
                thresholdWindows = new MonitorThresholdWindows()
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
        model.setID(createdMonitor.getId().doubleValue());

        return new ReadHandler().handleRequest(proxy, request, callbackContext, logger);
    }
}
