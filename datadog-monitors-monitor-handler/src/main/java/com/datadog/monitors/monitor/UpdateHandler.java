package com.datadog.monitors.monitor;

import java.util.stream.Collectors;

import software.amazon.cloudformation.proxy.AmazonWebServicesClientProxy;
import software.amazon.cloudformation.proxy.Logger;
import software.amazon.cloudformation.proxy.ProgressEvent;
import software.amazon.cloudformation.proxy.OperationStatus;
import software.amazon.cloudformation.proxy.ResourceHandlerRequest;

import com.datadog.api.v1.client.ApiClient;
import com.datadog.api.v1.client.ApiException;
import com.datadog.api.v1.client.api.MonitorsApi;
import com.datadog.api.v1.client.model.Monitor;
import com.datadog.api.v1.client.model.MonitorOptions;
import com.datadog.api.v1.client.model.MonitorThresholds;
import com.datadog.api.v1.client.model.MonitorThresholdWindowOptions;

import com.datadog.cloudformation.common.clients.ApiClients;

public class UpdateHandler extends BaseHandler<CallbackContext> {

    @Override
    public ProgressEvent<ResourceModel, CallbackContext> handleRequest(
        final AmazonWebServicesClientProxy proxy,
        final ResourceHandlerRequest<ResourceModel> request,
        final CallbackContext callbackContext,
        final Logger logger) {

        final ResourceModel model = request.getDesiredResourceState();

        logger.log("Starting the Monitor Resource Update Handler");

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
                    thresholds.setCritical(model.getOptions().getThresholds().getCritical());
                if(model.getOptions().getThresholds().getCriticalRecovery() != null)
                    thresholds.setCriticalRecovery(model.getOptions().getThresholds().getCriticalRecovery());
                if(model.getOptions().getThresholds().getWarning() != null)
                    thresholds.setWarning(model.getOptions().getThresholds().getWarning());
                if(model.getOptions().getThresholds().getWarningRecovery() != null)
                    thresholds.setWarningRecovery(model.getOptions().getThresholds().getWarningRecovery());
                if(model.getOptions().getThresholds().getOK() != null)
                    thresholds.setOk(model.getOptions().getThresholds().getOK());
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

        try {
            monitorsApi.editMonitor(model.getId().longValue(), monitor);
        } catch(ApiException e) {
            String err = "Failed to update monitor: " + e.toString();
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
