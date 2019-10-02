package com.datadog.monitors.downtime;

import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.time.ZoneId;
import java.util.ArrayList;
import java.util.List;
import java.util.TimeZone;

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
import static org.mockito.Mockito.mock;

@ExtendWith(MockitoExtension.class)
public class DowntimeCRUDTest {

    private final DatadogCredentials datadogCredentials = new DatadogCredentials(System.getenv("DD_TEST_CF_API_KEY"), System.getenv("DD_TEST_CF_APP_KEY"));

    private Integer downtimeID;
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
    public void disableDowntime() {
        final DeleteHandler handler = new DeleteHandler();
        final ResourceModel model = ResourceModel.builder().build();
        model.setId(downtimeID);
        model.setDatadogCredentials(datadogCredentials);
        final ResourceHandlerRequest<ResourceModel> request = ResourceHandlerRequest.<ResourceModel>builder()
            .desiredResourceState(model)
            .build();
        handler.handleRequest(proxy, request, null, logger);
    }

    @Test
    public void testDowntimeCRUD() {
        final CreateHandler createHandler = new CreateHandler();
        final UpdateHandler updateHandler = new UpdateHandler();
        final ResourceModel model = ResourceModel.builder().build();
        model.setDatadogCredentials(datadogCredentials);

        final String initialMessage = "Test Downtime Message";
        List<String> monitorTags = new ArrayList<String>();
        monitorTags.add("test:monitor");
        List<String> monitorScope = new ArrayList<String>();
        monitorScope.add("test:monitors");
        Clock offsetClock = Clock.offset(Clock.systemUTC(), Duration.ofHours(-5));
        long instant = Instant.now(offsetClock).getEpochSecond() + 1000000;

        model.setEnd((int) (long) instant);
        model.setMessage(initialMessage);
        model.setMonitorTags(monitorTags);

        model.setScope(monitorScope);
        model.setTimezone("UTC");

        // Not currently supported properly
        // //Convert to proper type.recurrence(model.getRecurrence())
        // DowntimeRecurrence downtimeRecurrenceModel = new DowntimeRecurrence();
        // downtimeRecurrenceModel.setPeriod(2);
        // downtimeRecurrenceModel.setType("days");
        // downtimeRecurrenceModel.setUntilOccurrences(4);
        // List<String> weekDays = new ArrayList<String>();
        // weekDays.add("Thursday");
        // downtimeRecurrenceModel.setWeekDays(weekDays);
        // model.setRecurrence(downtimeRecurrenceModel);

        final ResourceHandlerRequest<ResourceModel> request = ResourceHandlerRequest.<ResourceModel>builder()
            .desiredResourceState(model)
            .build();

        final ProgressEvent<ResourceModel, CallbackContext> response
            = createHandler.handleRequest(proxy, request, null, logger);

        assertThat(response).isNotNull();
        assertThat(response.getStatus()).isEqualTo(OperationStatus.SUCCESS);
        assertThat(response.getCallbackContext()).isNull();
        assertThat(response.getCallbackDelaySeconds()).isEqualTo(0);
        assertThat(response.getResourceModel()).isEqualTo(request.getDesiredResourceState());
        assertThat(response.getResourceModels()).isNull();
        assertThat(response.getMessage()).isNull();
        assertThat(response.getErrorCode()).isNull();

        ResourceModel read = response.getResourceModel();
        // Used to delete the downtime after this test is over
        downtimeID = read.getId();
        assertThat(read.getEnd()).isEqualTo(instant);
        assertThat(read.getMessage()).isEqualTo(initialMessage);
        assertThat(read.getMonitorTags()).isEqualTo(monitorTags);
        assertThat(read.getScope()).isEqualTo(monitorScope);
        assertThat(read.getTimezone()).isEqualTo("UTC");

        // Not currently supported properly
        // DowntimeRecurrence readRecurrence = read.getRecurrence();
        // assertThat(readRecurrence.getPeriod()).isEqualTo(2);
        // assertThat(readRecurrence.getType()).isEqualTo("days");
        // assertThat(readRecurrence.getUntilOccurrences()).isEqualTo(4);
        // assertThat(readRecurrence.getWeekDays()).isEqualTo(weekDays);

        //Update model with new values
        String newMessage = "Updated Message Value";
        model.setMessage(newMessage);

        // Not currently supported properly
        // downtimeRecurrenceModel.setType("weeks");
        // model.setRecurrence(downtimeRecurrenceModel);

        final ResourceHandlerRequest<ResourceModel> updateRequest = ResourceHandlerRequest.<ResourceModel>builder()
            .desiredResourceState(model)
            .build();

        final ProgressEvent<ResourceModel, CallbackContext> updateResponse
            = updateHandler.handleRequest(proxy, updateRequest, null, logger);

        ResourceModel updateRead = updateResponse.getResourceModel();
        assertThat(updateRead.getMessage()).isEqualTo(newMessage);

        // Not currently supported properly
        // assertThat(updateRead.getRecurrence().getType()).isEqualTo("weeks");

        //Assert original field that we didn't update
        assertThat(updateRead.getEnd()).isEqualTo((int) (long) instant);
    }
}
