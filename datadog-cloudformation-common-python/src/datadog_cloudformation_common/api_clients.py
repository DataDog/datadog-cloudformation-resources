from contextlib import contextmanager

from datadog_api_client.v1 import ApiClient, Configuration


@contextmanager
def v1_client(api_key: str, app_key: str, api_url: str, resource_name: str, resource_version: str) -> ApiClient:
    configuration = Configuration(
        host=api_url,
        api_key={
            "apiKeyAuth": api_key,
            "appKeyAuth": app_key,
        }
    )

    with ApiClient(configuration) as api_client:
        api_client.user_agent = f"datadog-cloudformation-{resource_name}/{resource_version} {api_client.user_agent}"
        yield api_client
