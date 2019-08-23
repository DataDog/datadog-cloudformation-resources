package com.datadog.cloudformation.utils;

import com.datadog.api.client.v1.ApiClient;
import com.datadog.api.client.v1.Configuration;
import com.datadog.api.client.v1.auth.ApiKeyAuth;

import java.util.Map;

public class ApiClients {
    public static ApiClient V1Client(String apiKey, String applicationKey){
        ApiClient defaultClient = Configuration.getDefaultApiClient();

        // Configure API key authorization: apiKeyAuth
        ApiKeyAuth apiKeyAuth = (ApiKeyAuth) defaultClient.getAuthentication("apiKeyAuth");
        apiKeyAuth.setApiKey(apiKey);

        // Configure API key authorization: appKeyAuth
        ApiKeyAuth appKeyAuth = (ApiKeyAuth) defaultClient.getAuthentication("appKeyAuth");
        appKeyAuth.setApiKey(applicationKey);

        return defaultClient;
    }

    public static ApiClient V1ClientFromEnv() throws CredentialsMissingException {
        String apiKey = System.getenv("DATADOG_API_KEY");
        String applicationKey = System.getenv("DATADOG_APP_KEY");

        if (apiKey == null) {
            throw new CredentialsMissingException("DATADOG_API_KEY not present in environment");
        }
        if (applicationKey == null) {
            throw new CredentialsMissingException("DATADOG_APP_KEY not present in environment");
        }

        return V1Client(apiKey, applicationKey);
    }
}