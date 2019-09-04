package com.datadog.monitors.monitor;

import com.amazonaws.cloudformation.proxy.AmazonWebServicesClientProxy;
import com.amazonaws.cloudformation.proxy.Logger;
import com.amazonaws.cloudformation.proxy.OperationStatus;
import com.amazonaws.cloudformation.proxy.ProgressEvent;
import com.amazonaws.cloudformation.proxy.ResourceHandlerRequest;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;


import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.within;
import static org.mockito.Mockito.mock;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@ExtendWith(MockitoExtension.class)
public class MonitorCRUDTest {

    private final List<String> testTagsUpdated = new ArrayList<String>(
        Arrays.asList("app:UpdatedCF")
    );
    private final List<String> testTags = new ArrayList<String>(
        Arrays.asList("app:CF", "key2:val2")
    );
    private final DatadogCredentials datadogCredentials = new DatadogCredentials(System.getenv("DD_TEST_CF_API_KEY"), System.getenv("DD_TEST_CF_APP_KEY"));

    private double id;

    @Mock
    private AmazonWebServicesClientProxy proxy;

    @Mock
    private Logger logger;

    @BeforeEach
    public void setup() {
        proxy = mock(AmazonWebServicesClientProxy.class);
        logger = mock(Logger.class);
    }

    @AfterEach
    public void deleteMonitor() {
        final DeleteHandler deleteHandler = new DeleteHandler();
        final ResourceModel model = ResourceModel.builder().build();
        model.setID(id);
        model.setDatadogCredentials(datadogCredentials);

        final ResourceHandlerRequest<ResourceModel> request = ResourceHandlerRequest.<ResourceModel>builder()
            .desiredResourceState(model)
            .build();
        final ProgressEvent<ResourceModel, CallbackContext> response = deleteHandler.handleRequest(proxy, request, null, logger);
        assertThat(response.getStatus()).isEqualTo(OperationStatus.SUCCESS);
    }

    @Test
    public void testMonitorCRUD() {
        final CreateHandler createHandler = new CreateHandler();
        final UpdateHandler updateHandler = new UpdateHandler();

        final ResourceModel model = ResourceModel.builder().build();
        model.setTags(testTags);
        model.setDatadogCredentials(datadogCredentials);
        model.setType("service check");
        model.setQuery("\"ntp.in_sync\".over(\"*\").last(2).count_by_status()");
        MonitorOptions options = new MonitorOptions();
        MonitorThresholds thresholds = new MonitorThresholds();
        thresholds.setCritical(3.);
        thresholds.setOK(2.);
        options.setThresholds(thresholds);
        model.setOptions(options);

        final ResourceHandlerRequest<ResourceModel> request = ResourceHandlerRequest.<ResourceModel>builder()
            .desiredResourceState(model)
            .build();

        final ProgressEvent<ResourceModel, CallbackContext> response
            = createHandler.handleRequest(proxy, request, null, logger);

        logger.log("Response is: %v" + response);

        assertThat(response).isNotNull();
        assertThat(response.getStatus()).isEqualTo(OperationStatus.SUCCESS);
        assertThat(response.getCallbackContext()).isNull();
        assertThat(response.getCallbackDelaySeconds()).isEqualTo(0);
        assertThat(response.getResourceModel()).isEqualTo(request.getDesiredResourceState());
        assertThat(response.getResourceModels()).isNull();
        assertThat(response.getMessage()).isNull();
        assertThat(response.getErrorCode()).isNull();

        ResourceModel read = response.getResourceModel();
        assertThat(read.getTags()).isEqualTo(testTags);
        assertThat(read.getOptions().getThresholds().getCritical()).isEqualTo(3.);
        assertThat(read.getOptions().getThresholds().getOK()).isEqualTo(2.);
        id = read.getID();

        // Update the resource
        options = new MonitorOptions();
        options.setAggregation("in total");
        options.setEnableLogsSample(true);
        options.setEscalationMessage("escalation message");
        options.setIncludeTags(false);
        options.setLocked(true);
        options.setNotifyAudit(true);
        options.setNotifyNoData(true);
        options.setRequireFullWindow(false);
        options.setTimeoutH(10);
        options.setEvaluationDelay(300.);
        options.setMinLocationFailed(2.);
        options.setNewHostDelay(10.);
        options.setNoDataTimeframe(20.);
        options.setRenotifyInterval(10.);

        thresholds = new MonitorThresholds();
        thresholds.setCritical(.1);
        thresholds.setCriticalRecovery(.09);
        thresholds.setOK(.02);
        thresholds.setWarning(.05);
        thresholds.setWarningRecovery(.04);
        options.setThresholds(thresholds);

        MonitorThresholdWindows thresholdWindows = new MonitorThresholdWindows();
        thresholdWindows.setRecoveryWindow("last_30m");
        thresholdWindows.setTriggerWindow("last_30m");
        options.setThresholdWindows(thresholdWindows);

        model.setOptions(options);
        model.setTags(testTagsUpdated);
        String updatedQuery = "avg(last_4h):anomalies(avg:datadog.estimated_usage.containers{*}, 'basic', 2, direction='both', alert_window='last_30m', interval=60, count_default_zero='true') >= 0.1";
        model.setQuery(updatedQuery);
        model.setType("metric alert");
        model.setMessage("updated message");
        model.setName("updated name");

        final ResourceHandlerRequest<ResourceModel> updateRequest = ResourceHandlerRequest.<ResourceModel>builder()
            .desiredResourceState(model)
            .build();

        final ProgressEvent<ResourceModel, CallbackContext> updateResponse
            = updateHandler.handleRequest(proxy, updateRequest, null, logger);
        assertThat(updateResponse.getStatus()).isEqualTo(OperationStatus.SUCCESS);

        ResourceModel updateRead = updateResponse.getResourceModel();
        assertThat(updateRead.getTags()).isEqualTo(testTagsUpdated);
        assertThat(updateRead.getQuery()).isEqualTo(updatedQuery);
        assertThat(updateRead.getMessage()).isEqualTo("updated message");
        assertThat(updateRead.getName()).isEqualTo("updated name");
        assertThat(updateRead.getType()).isEqualTo("metric alert");
        assertThat(updateRead.getOptions().getAggregation()).isEqualTo("in total");
        assertThat(updateRead.getOptions().getEnableLogsSample()).isTrue();
        assertThat(updateRead.getOptions().getEscalationMessage()).isEqualTo("escalation message");
        assertThat(updateRead.getOptions().getIncludeTags()).isFalse();
        assertThat(updateRead.getOptions().getLocked()).isTrue();
        assertThat(updateRead.getOptions().getNotifyAudit()).isTrue();
        assertThat(updateRead.getOptions().getNotifyNoData()).isTrue();
        assertThat(updateRead.getOptions().getRequireFullWindow()).isFalse();
        assertThat(updateRead.getOptions().getTimeoutH()).isEqualTo(10);
        assertThat(updateRead.getOptions().getEvaluationDelay()).isEqualTo(300.);
        assertThat(updateRead.getOptions().getMinLocationFailed()).isEqualTo(2.);
        assertThat(updateRead.getOptions().getNewHostDelay()).isEqualTo(10.);
        assertThat(updateRead.getOptions().getNoDataTimeframe()).isEqualTo(20.);
        assertThat(updateRead.getOptions().getRenotifyInterval()).isEqualTo(10.);
        assertThat(updateRead.getOptions().getThresholds().getCritical()).isEqualTo(.1, within(.00001));
        assertThat(updateRead.getOptions().getThresholds().getCriticalRecovery()).isEqualTo(.09, within(.00001));
        assertThat(updateRead.getOptions().getThresholds().getOK()).isEqualTo(.02, within(.00001));
        assertThat(updateRead.getOptions().getThresholds().getWarning()).isEqualTo(.05, within(.00001));
        assertThat(updateRead.getOptions().getThresholds().getWarningRecovery()).isEqualTo(.04, within(.00001));
        assertThat(updateRead.getOptions().getThresholdWindows().getTriggerWindow()).isEqualTo("last_30m");
        assertThat(updateRead.getOptions().getThresholdWindows().getRecoveryWindow()).isEqualTo("last_30m");
    }
}
