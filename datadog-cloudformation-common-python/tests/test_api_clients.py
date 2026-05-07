# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2.0 style license (see LICENSE).
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2020-Present Datadog, Inc.
from datadog_api_client.rest import RESTClientObject
from urllib3.util.retry import Retry

from datadog_cloudformation_common.api_clients import DEFAULT_RETRY_KWARGS, client


def _make_client(**kwargs):
    return client(
        api_key="k",
        app_key="a",
        api_url="https://api.datadoghq.com",
        resource_name="test",
        resource_version="0",
        **kwargs,
    )


def test_default_retry_settings_applied():
    with _make_client() as api_client:
        cfg = api_client.configuration
        assert cfg.enable_retry is True
        assert cfg.max_retries == 4
        assert cfg.retry_backoff_factor == 2
        assert cfg.request_timeout == (15, 60)


def test_default_kwargs_constants_match():
    assert DEFAULT_RETRY_KWARGS == {
        "enable_retry": True,
        "max_retries": 4,
        "retry_backoff_factor": 2,
        "request_timeout": (15, 60),
    }


def test_default_api_url_used_when_none():
    with client("k", "a", None, "test", "0") as api_client:
        assert api_client.configuration.host == "https://api.datadoghq.com"


def test_caller_can_override_enable_retry_via_datadog_config():
    with _make_client(datadog_config={"enable_retry": False}) as api_client:
        assert api_client.configuration.enable_retry is False


def test_caller_can_override_max_retries():
    with _make_client(datadog_config={"max_retries": 7}) as api_client:
        assert api_client.configuration.max_retries == 7


def test_caller_can_override_request_timeout():
    with _make_client(datadog_config={"request_timeout": (5, 15)}) as api_client:
        assert api_client.configuration.request_timeout == (5, 15)


def test_default_retry_propagates_to_pool_manager():
    """End-to-end wiring: Configuration -> RESTClientObject -> urllib3 Retry."""
    with _make_client() as api_client:
        rest = RESTClientObject(api_client.configuration)
        retries = rest.pool_manager.connection_pool_kw["retries"]
        assert isinstance(retries, Retry)
        assert retries.total == 4
        assert retries.backoff_factor == 2


def test_custom_retry_policy_overrides_built_in():
    custom = Retry(total=1, backoff_factor=0)
    with _make_client(datadog_config={"retry_policy": custom}) as api_client:
        rest = RESTClientObject(api_client.configuration)
        assert rest.pool_manager.connection_pool_kw["retries"] is custom


def test_unstable_operations_still_applied():
    # _UnstableOperations expects the bare op name (no v1/v2 prefix); the setter
    # resolves it against the configured op list internally.
    with _make_client(unstable_operations={"create_incident": True}) as api_client:
        assert api_client.configuration.unstable_operations["create_incident"] is True


def test_user_agent_includes_resource_metadata():
    with _make_client() as api_client:
        ua = api_client.user_agent
        assert "aws-cloudformation-datadog/" in ua
        assert "resource-name test" in ua
        assert "resource-version 0" in ua
