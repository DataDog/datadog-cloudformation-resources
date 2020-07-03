// Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
// This product includes software developed at Datadog (https://www.datadoghq.com/).
// Copyright 2019-Present Datadog, Inc.
package com.datadog.cloudformation.common.clients;

import com.datadog.api.v1.client.ApiClient;
import com.datadog.api.v1.client.auth.ApiKeyAuth;

import com.datadog.cloudformation.common.exceptions.CredentialsMissingException;

public class ApiClients {
    public static ApiClient V1Client(String apiKey, String applicationKey, String apiURL, String resourceName, String resourceVersion) {
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

        // Configure User-Agent header
        String originalUA = client.getUserAgent();
        // NOTE: for now we hardcode the AWS SDK version as 2.0.0 until it's possible to get it dynamically from the SDK
        String userAgent = String.format(
            "aws-cloudformation-datadog/%s (resource-name %s; resource-version %s) %s",
            "2.0.0", resourceName, resourceVersion, originalUA
        );
        client.setUserAgent(userAgent);

        return client;
    }

    public static ApiClient V1ClientFromEnv(String resourceName, String resourceVersion) throws CredentialsMissingException {
        String apiKey = System.getenv("DATADOG_API_KEY");
        String applicationKey = System.getenv("DATADOG_APP_KEY");
        String apiURL = System.getenv("DATADOG_API_URL");

        if (apiKey == null) {
            throw new CredentialsMissingException("DATADOG_API_KEY not present in environment");
        }
        if (applicationKey == null) {
            throw new CredentialsMissingException("DATADOG_APP_KEY not present in environment");
        }

        return V1Client(apiKey, applicationKey, apiURL, resourceName, resourceVersion);
    }
}
