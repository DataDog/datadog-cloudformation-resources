from contextlib import contextmanager
import pkg_resources

from datadog_api_client.v1 import ApiClient, Configuration


@contextmanager
def v1_client(api_key: str, app_key: str, api_url: str, resource_name: str, resource_version: str) -> ApiClient:
    configuration = Configuration(
        host=api_url or "https://api.datadoghq.com",
        api_key={
            "apiKeyAuth": api_key,
            "appKeyAuth": app_key,
        }
    )

    with ApiClient(configuration) as api_client:
        try:
            plugin_ver = pkg_resources.get_distribution('cloudformation_cli_python_lib').version
        except ValueError:
            # Fallback if we're unable to retrieve the plugin version for any reason
            plugin_ver = "NA"
        api_client.user_agent = f"aws-cloudformation-datadog/{plugin_ver} (resource-name {resource_name}; resource-version {resource_version}) {api_client.user_agent}"
        yield api_client
