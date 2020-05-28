// Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
// This product includes software developed at Datadog (https://www.datadoghq.com/).
// Copyright 2019-Present Datadog, Inc.
package com.datadog.monitors.monitor;

import java.util.HashMap;
import java.util.Map.Entry;
import java.util.stream.Collectors;

import software.amazon.cloudformation.proxy.AmazonWebServicesClientProxy;
import software.amazon.cloudformation.proxy.Logger;
import software.amazon.cloudformation.proxy.ProgressEvent;
import software.amazon.cloudformation.proxy.OperationStatus;
import software.amazon.cloudformation.proxy.ResourceHandlerRequest;

import com.datadog.cloudformation.common.clients.ApiClients;

import com.datadog.api.v1.client.ApiClient;
import com.datadog.api.v1.client.ApiException;
import com.datadog.api.v1.client.api.MonitorsApi;
import com.datadog.api.v1.client.model.Monitor;

public class ReadHandler extends BaseHandler<CallbackContext> {

    @Override
    public ProgressEvent<ResourceModel, CallbackContext> handleRequest(
        final AmazonWebServicesClientProxy proxy,
        final ResourceHandlerRequest<ResourceModel> request,
        final CallbackContext callbackContext,
        final Logger logger) {

        final ResourceModel model = request.getDesiredResourceState();

        logger.log("Starting the Monitor Resource Read Handler");

        ApiClient apiClient = ApiClients.V1Client(
            model.getDatadogCredentials().getApiKey(),
            model.getDatadogCredentials().getApplicationKey(),
            model.getDatadogCredentials().getApiURL()
        );
        MonitorsApi monitorsApi = new MonitorsApi(apiClient);

        Monitor monitor = null;
        try {
            monitor = monitorsApi.getMonitor(model.getId().longValue()).execute();
        } catch(ApiException e) {
            String err = "Failed to get monitor: " + e.toString();
            logger.log(err);

            return ProgressEvent.<ResourceModel, CallbackContext>builder()
                .resourceModel(model)
                .status(OperationStatus.FAILED)
                .message(err)
                .build();
        }

        model.setId(monitor.getId().doubleValue());
        model.setCreated(monitor.getCreated().toString());
        model.setModified(monitor.getCreated().toString());
        if(monitor.getDeleted() != null)
            model.setDeleted(monitor.getDeleted().toString());
        model.setMessage(monitor.getMessage());
        model.setName(monitor.getName());
        model.setTags(monitor.getTags());
        model.setQuery(monitor.getQuery());
        if(
            !(model.getType().equals("query alert") && monitor.getType().getValue().equals("metric alert"))
            && !(model.getType().equals("metric alert") && monitor.getType().getValue().equals("query alert"))
        )
            // metric alert and query alert are interchangeable, so don't update when is from one to the other
            model.setType(monitor.getType().getValue());
        model.setMulti(monitor.getMulti());

        if(monitor.getCreator() != null) {
            Creator creator = new Creator();
            creator.setEmail(monitor.getCreator().getEmail());
            creator.setHandle(monitor.getCreator().getHandle());
            creator.setName(monitor.getCreator().getName());
            model.setCreator(creator);
        }

        if(monitor.getOptions() != null) {
            MonitorOptions monitorOptions = new MonitorOptions();
            monitorOptions.setEnableLogsSample(monitor.getOptions().getEnableLogsSample());
            monitorOptions.setEscalationMessage(monitor.getOptions().getEscalationMessage());
            if(monitor.getOptions().getEvaluationDelay() != null)
                monitorOptions.setEvaluationDelay(monitor.getOptions().getEvaluationDelay().doubleValue());
            monitorOptions.setIncludeTags(monitor.getOptions().getIncludeTags());
            monitorOptions.setLocked(monitor.getOptions().getLocked());
            if(monitor.getOptions().getMinLocationFailed() != null)
                monitorOptions.setMinLocationFailed(monitor.getOptions().getMinLocationFailed().doubleValue());
            if(monitor.getOptions().getNewHostDelay() != null)
                monitorOptions.setNewHostDelay(monitor.getOptions().getNewHostDelay().doubleValue());
            if(monitor.getOptions().getNoDataTimeframe() != null)
                monitorOptions.setNoDataTimeframe(monitor.getOptions().getNoDataTimeframe().doubleValue());
            monitorOptions.setNotifyAudit(monitor.getOptions().getNotifyAudit());
            monitorOptions.setNotifyNoData(monitor.getOptions().getNotifyNoData());
            if(monitor.getOptions().getRenotifyInterval() != null)
                monitorOptions.setRenotifyInterval(monitor.getOptions().getRenotifyInterval().doubleValue());
            monitorOptions.setRequireFullWindow(monitor.getOptions().getRequireFullWindow());
            if(monitor.getOptions().getSyntheticsCheckId() != null)
                monitorOptions.setSyntheticsCheckID(monitor.getOptions().getSyntheticsCheckId().doubleValue());
            if(monitor.getOptions().getThresholds() != null) {
                MonitorThresholds monitorThresholds = new MonitorThresholds();
                if(monitor.getOptions().getThresholds().getCritical() != null)
                    monitorThresholds.setCritical(monitor.getOptions().getThresholds().getCritical().doubleValue());
                if(monitor.getOptions().getThresholds().getCriticalRecovery() != null)
                    monitorThresholds.setCriticalRecovery(monitor.getOptions().getThresholds().getCriticalRecovery().doubleValue());
                if(monitor.getOptions().getThresholds().getWarning() != null)
                    monitorThresholds.setWarning(monitor.getOptions().getThresholds().getWarning().doubleValue());
                if(monitor.getOptions().getThresholds().getWarningRecovery() != null)
                    monitorThresholds.setWarningRecovery(monitor.getOptions().getThresholds().getWarningRecovery().doubleValue());
                if(monitor.getOptions().getThresholds().getOk() != null)
                    monitorThresholds.setOK(monitor.getOptions().getThresholds().getOk().doubleValue());
                monitorOptions.setThresholds(monitorThresholds);
            }
            if(monitor.getOptions().getThresholdWindows() != null) {
                MonitorThresholdWindows monitorThresholdWindows = new MonitorThresholdWindows();
                monitorThresholdWindows.setTriggerWindow(monitor.getOptions().getThresholdWindows().getTriggerWindow());
                monitorThresholdWindows.setRecoveryWindow(monitor.getOptions().getThresholdWindows().getRecoveryWindow());
                monitorOptions.setThresholdWindows(monitorThresholdWindows);
            }
            if (monitor.getOptions().getTimeoutH() != null) {
                monitorOptions.setTimeoutH(monitor.getOptions().getTimeoutH().intValue());
            }
            model.setOptions(monitorOptions);
        }

        if(monitor.getOverallState() != null)
            model.setOverallState(monitor.getOverallState().getValue());

        if(monitor.getState() != null) {
            MonitorState state = new MonitorState();
            state.setMonitorID(monitor.getId().doubleValue());
            if(monitor.getOverallState() != null)
                state.setOverallState(monitor.getOverallState().getValue());
            if(monitor.getState().getGroups() != null) {
                HashMap<String, MonitorStateGroup> groups = new HashMap<>();
                for(Entry<String, com.datadog.api.v1.client.model.MonitorStateGroup> entry: monitor.getState().getGroups().entrySet()) {
                    MonitorStateGroup group = new MonitorStateGroup();
                    group.setName(entry.getValue().getName());
                    if(entry.getValue().getLastTriggeredTs() != null)
                        group.setLastTriggeredTS(entry.getValue().getLastTriggeredTs().doubleValue());
                    if(entry.getValue().getLastNotifiedTs() != null)
                        group.setLastNotifiedTS(entry.getValue().getLastNotifiedTs().doubleValue());
                    if(entry.getValue().getLastResolvedTs() != null)
                        group.setLastResolvedTS(entry.getValue().getLastResolvedTs().doubleValue());
                    if(entry.getValue().getLastNodataTs() != null)
                        group.setLastNodataTS(entry.getValue().getLastNodataTs().doubleValue());

                    if(entry.getValue().getStatus() != null)
                        group.setStatus(entry.getValue().getStatus().getValue());

                    groups.put(entry.getKey(), group);
                }
                state.setGroups(groups);
            }
            model.setState(state);
        }

        return ProgressEvent.<ResourceModel, CallbackContext>builder()
            .resourceModel(model)
            .status(OperationStatus.SUCCESS)
            .build();
    }
}
