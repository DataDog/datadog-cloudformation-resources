package com.datadog.monitors.downtime;

import com.datadog.api.v1.client.ApiClient;
import com.datadog.cloudformation.common.clients.ApiClients;
import java.util.Properties;

public class ClientFactory {
    String apiKey;
    String appKey;
    String apiURL;

    public ClientFactory(String apiKey, String appKey, String apiURL) {
        this.apiKey = apiKey;
        this.appKey = appKey;
        this.apiURL = apiURL;
    }

    public ApiClient createV1Client() {
        String version = "N/A";
        try {
            final Properties properties = new Properties();
            properties.load(this.getClass().getClassLoader().getResourceAsStream("com/datadog/monitors/downtime/project.properties"));
            version = properties.getProperty("version");
        } catch (java.io.IOException e) {}
        return ApiClients.V1Client(apiKey, appKey, apiURL, "monitors-downtime", version);
    }
}
