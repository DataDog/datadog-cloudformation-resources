package com.datadog.cloudformation.common.clients;

import com.datadog.api.v1.client.ApiClient;
import com.datadog.api.v1.client.auth.ApiKeyAuth;

import com.datadog.cloudformation.common.exceptions.CredentialsMissingException;

public class ApiClients {
    public static ApiClient V1Client(String apiKey, String applicationKey, String apiURL) {
        ApiClient client = new ApiClient();

        if (apiURL != null && !apiURL.equals("")) {
            client.setBasePath(apiURL);
        }

        // Configure API key authorization: apiKeyAuth
        ApiKeyAuth apiKeyAuth = (ApiKeyAuth) client.getAuthentication("apiKeyAuth");
        apiKeyAuth.setApiKey(apiKey);

        // Configure API key authorization: appKeyAuth
        ApiKeyAuth appKeyAuth = (ApiKeyAuth) client.getAuthentication("appKeyAuth");
        appKeyAuth.setApiKey(applicationKey);

        return client;
    }

    public static ApiClient V1ClientFromEnv() throws CredentialsMissingException {
        String apiKey = System.getenv("DATADOG_API_KEY");
        String applicationKey = System.getenv("DATADOG_APP_KEY");
        String apiURL = System.getenv("DATADOG_API_URL");

        if (apiKey == null) {
            throw new CredentialsMissingException("DATADOG_API_KEY not present in environment");
        }
        if (applicationKey == null) {
            throw new CredentialsMissingException("DATADOG_APP_KEY not present in environment");
        }

        return V1Client(apiKey, applicationKey, apiURL);
    }
}