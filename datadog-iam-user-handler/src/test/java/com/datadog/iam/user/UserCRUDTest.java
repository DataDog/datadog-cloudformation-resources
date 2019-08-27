package com.datadog.iam.user;

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
public class UserCRUDTest {

    private final String testingAccessRole = "st";
    private final String testingHandle = "nobody@datadoghq.com";
    private final String testingName = "Nobody";
    private final DatadogCredentials datadogCredentials = new DatadogCredentials(System.getenv("DD_TEST_CF_API_KEY"), System.getenv("DD_TEST_CF_APP_KEY"));

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
    public void deleteUser() {
        final DeleteHandler handler = new DeleteHandler();
        final ResourceModel model = ResourceModel.builder().build();
        model.setHandle(testingHandle);
        model.setDatadogCredentials(datadogCredentials);
        final ResourceHandlerRequest<ResourceModel> request = ResourceHandlerRequest.<ResourceModel>builder()
            .desiredResourceState(model)
            .build();
        final ProgressEvent<ResourceModel, CallbackContext> response
            = handler.handleRequest(proxy, request, null, logger);
    }

    @Test
    public void testUserCRUD() {
        final CreateHandler createHandler = new CreateHandler();
        final UpdateHandler updateHandler = new UpdateHandler();

        final ResourceModel model = ResourceModel.builder().build();
        model.setAccessRole(testingAccessRole);
        model.setHandle(testingHandle);
        model.setName(testingName);
        model.setEmail(testingHandle);
        model.setDatadogCredentials(datadogCredentials);

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
        assertThat(read.getAccessRole()).isEqualTo(testingAccessRole);
        assertThat(read.getDisabled()).isEqualTo(true);
        assertThat(read.getEmail()).isEqualTo(testingHandle);
        assertThat(read.getHandle()).isEqualTo(testingHandle);
        assertThat(read.getName()).isEqualTo(testingName);
        assertThat(read.getVerified()).isEqualTo(false);

        model.setDisabled(false);
        model.setName("New name");

        final ResourceHandlerRequest<ResourceModel> updateRequest = ResourceHandlerRequest.<ResourceModel>builder()
            .desiredResourceState(model)
            .build();

        final ProgressEvent<ResourceModel, CallbackContext> updateResponse
            = updateHandler.handleRequest(proxy, updateRequest, null, logger);

        ResourceModel updateRead = updateResponse.getResourceModel();
        assertThat(read.getAccessRole()).isEqualTo(testingAccessRole);
        assertThat(read.getDisabled()).isEqualTo(false);
        assertThat(read.getEmail()).isEqualTo(testingHandle);
        assertThat(read.getHandle()).isEqualTo(testingHandle);
        assertThat(read.getName()).isEqualTo("New name");
        assertThat(read.getVerified()).isEqualTo(false);
    }
}
