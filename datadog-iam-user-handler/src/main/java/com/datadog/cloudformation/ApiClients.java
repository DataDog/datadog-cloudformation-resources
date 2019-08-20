package com.datadog.cloudformation;

import com.datadog.api.client.v1.ApiClient;
import com.datadog.api.client.v1.Configuration;
import com.datadog.api.client.v1.auth.ApiKeyAuth;

public class ApiClients {
    public static ApiClient V1Client() {
        ApiClient defaultClient = Configuration.getDefaultApiClient();

        // Configure API key authorization: apiKeyAuth
        String apiKey = System.getenv("DATADOG_API_KEY");
        ApiKeyAuth apiKeyAuth = (ApiKeyAuth) defaultClient.getAuthentication("apiKeyAuth");
        apiKeyAuth.setApiKey(apiKey);

        // Configure API key authorization: appKeyAuth
        String appKey = System.getenv("DATADOG_APP_KEY");
        ApiKeyAuth appKeyAuth = (ApiKeyAuth) defaultClient.getAuthentication("appKeyAuth");
        appKeyAuth.setApiKey(appKey);

        return defaultClient;
    }
}