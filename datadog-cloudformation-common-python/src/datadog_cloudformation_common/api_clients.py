from contextlib import contextmanager
import pkg_resources

from datadog_api_client import ApiClient, Configuration

DEFAULT_API_URL = "https://api.datadoghq.com"

# Defaults for the upstream datadog-api-client retry behavior. Caller-supplied
# datadog_config overrides any of these. See:
# https://github.com/DataDog/datadog-api-client-python/blob/2.50.0/src/datadog_api_client/configuration.py
DEFAULT_RETRY_KWARGS = {
    "enable_retry": True,
    "max_retries": 4,
    "retry_backoff_factor": 2,
    "request_timeout": (15, 60),
}


@contextmanager
def client(
    api_key: str,
    app_key: str,
    api_url: str,
    resource_name: str,
    resource_version: str,
    datadog_config: dict = {},
    unstable_operations: dict = {},
) -> ApiClient:
    config_kwargs = {
        "host": api_url or DEFAULT_API_URL,
        "api_key": {
            "apiKeyAuth": api_key,
            "appKeyAuth": app_key,
        },
        **DEFAULT_RETRY_KWARGS,
        **datadog_config,
    }
    configuration = Configuration(**config_kwargs)
    for key, value in unstable_operations.items():
        configuration.unstable_operations[key] = value

    with ApiClient(configuration) as api_client:
        try:
            plugin_ver = pkg_resources.get_distribution("cloudformation_cli_python_lib").version
        except ValueError:
            # Fallback if we're unable to retrieve the plugin version for any reason
            plugin_ver = "NA"
        api_client.user_agent = f"aws-cloudformation-datadog/{plugin_ver} (resource-name {resource_name}; resource-version {resource_version}) {api_client.user_agent}"
        yield api_client
