package com.datadog.integration.aws;

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

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@ExtendWith(MockitoExtension.class)
public class AWSCRUDTest {

    private final String testAccountID = "1234";
    private final String testRoleName = "CF Test Role Name";
    private final List<String> testFilterTags = new ArrayList<String>(
        Arrays.asList("app:CF")
    );
    private final List<String> testFilterTagsUpdated = new ArrayList<String>(
        Arrays.asList("app:UpdatedCF")
    );
    private final List<String> testHostTags = new ArrayList<String>(
        Arrays.asList("key:val", "key2:val2")
    );
    private Map<String, Boolean> testAccountSpecificNamespaceRules = new HashMap<String, Boolean>();
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
    public void deleteAWSAccount() {
        final DeleteHandler deleteHandler = new DeleteHandler();
        final ResourceModel model = ResourceModel.builder().build();
        model.setAccountID(testAccountID);
        model.setRoleName(testRoleName);

        model.setDatadogCredentials(datadogCredentials);
        final ResourceHandlerRequest<ResourceModel> request = ResourceHandlerRequest.<ResourceModel>builder()
            .desiredResourceState(model)
            .build();
        deleteHandler.handleRequest(proxy, request, null, logger);
    }

    @Test
    public void testUserCRUD() {
        final CreateHandler createHandler = new CreateHandler();
        final UpdateHandler updateHandler = new UpdateHandler();

        final ResourceModel model = ResourceModel.builder().build();

        testAccountSpecificNamespaceRules.put("api_gateway", true);
        testAccountSpecificNamespaceRules.put("trusted_advisor", false);
        model.setAccountID(testAccountID);
        model.setRoleName(testRoleName);
        model.setHostTags(testHostTags);
        model.setFilterTags(testFilterTags);
        // Convert the model's accountSpecificNameSpaceRules to expected object type
        Map<String, Object> accountSpecificNamespaceRules = new HashMap<String, Object>((Map)testAccountSpecificNamespaceRules);

        model.setAccountSpecificNamespaceRules(accountSpecificNamespaceRules);

        model.setDatadogCredentials(datadogCredentials);

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
        assertThat(read.getAccountID()).isEqualTo(testAccountID);
        assertThat(read.getRoleName()).isEqualTo(testRoleName);
        assertThat(read.getHostTags()).isEqualTo(testHostTags);
        assertThat(read.getFilterTags()).isEqualTo(testFilterTags);
        assertThat(read.getAccountSpecificNamespaceRules()).isEqualTo(testAccountSpecificNamespaceRules);

        model.setFilterTags(testFilterTagsUpdated);

        final ResourceHandlerRequest<ResourceModel> updateRequest = ResourceHandlerRequest.<ResourceModel>builder()
            .desiredResourceState(model)
            .build();

        final ProgressEvent<ResourceModel, CallbackContext> updateResponse
            = updateHandler.handleRequest(proxy, updateRequest, null, logger);

        ResourceModel updateRead = updateResponse.getResourceModel();
        assertThat(updateRead.getAccountID()).isEqualTo(testAccountID);
        assertThat(updateRead.getRoleName()).isEqualTo(testRoleName);
        assertThat(updateRead.getHostTags()).isEqualTo(testHostTags);
        assertThat(updateRead.getFilterTags()).isEqualTo(testFilterTagsUpdated);
        assertThat(updateRead.getAccountSpecificNamespaceRules()).isEqualTo(testAccountSpecificNamespaceRules);
    }
}
