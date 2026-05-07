# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2.0 style license (see LICENSE).
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2020-Present Datadog, Inc.
import time
from unittest.mock import patch

import pytest
from datadog_api_client.exceptions import ServiceException
from datadog_api_client.v1.api.authentication_api import AuthenticationApi
from pytest_httpserver import HTTPServer
from urllib3.connectionpool import HTTPConnectionPool
from urllib3.exceptions import ProtocolError, SSLError
from urllib3.util.retry import Retry

from datadog_cloudformation_common.api_clients import client

# Zero-backoff retry policy used by the HTTP-status tests so they don't sleep.
# Mirrors enable_retry=True semantics (same status codes, same allowed methods)
# but skips exponential backoff between attempts. The upstream
# retry_backoff_factor minimum is 2 which would otherwise force ~6s of sleeps
# for 3 attempts.
FAST_RETRY = Retry(
    total=4,
    status_forcelist=frozenset({408, 429, 500, 501, 502, 503, 504}),
    allowed_methods=frozenset({"GET", "PUT", "DELETE", "POST", "PATCH"}),
    backoff_factor=0,
    respect_retry_after_header=True,
)


def _client(httpserver: HTTPServer, **datadog_overrides):
    overrides = {"retry_policy": FAST_RETRY}
    overrides.update(datadog_overrides)
    return client(
        api_key="k",
        app_key="a",
        api_url=httpserver.url_for("").rstrip("/"),
        resource_name="test",
        resource_version="0",
        datadog_config=overrides,
    )


def test_retries_on_503_then_succeeds(httpserver: HTTPServer):
    httpserver.expect_ordered_request("/api/v1/validate").respond_with_data("oops", status=503)
    httpserver.expect_ordered_request("/api/v1/validate").respond_with_data("oops", status=503)
    httpserver.expect_ordered_request("/api/v1/validate").respond_with_json(
        {"valid": True}, status=200
    )

    with _client(httpserver) as api_client:
        AuthenticationApi(api_client).validate()

    assert len(httpserver.log) == 3


def test_retries_on_429_honors_x_ratelimit_reset(httpserver: HTTPServer):
    """Datadog's ClientRetry reads X-Ratelimit-Reset (seconds) instead of Retry-After."""
    httpserver.expect_ordered_request("/api/v1/validate").respond_with_data(
        "rate limited", status=429, headers={"X-Ratelimit-Reset": "1"}
    )
    httpserver.expect_ordered_request("/api/v1/validate").respond_with_json(
        {"valid": True}, status=200
    )

    # Use the production retry path so ClientRetry.get_retry_after is exercised.
    start = time.monotonic()
    with _client(
        httpserver,
        retry_policy=None,
        enable_retry=True,
        max_retries=4,
        retry_backoff_factor=2,
    ) as api_client:
        AuthenticationApi(api_client).validate()
    elapsed = time.monotonic() - start

    assert len(httpserver.log) == 2
    assert elapsed >= 0.9  # waited ~1s per X-Ratelimit-Reset


def test_no_retry_when_disabled(httpserver: HTTPServer):
    httpserver.expect_request("/api/v1/validate").respond_with_data("oops", status=503)

    with pytest.raises(ServiceException):
        with _client(httpserver, retry_policy=None, enable_retry=False) as api_client:
            AuthenticationApi(api_client).validate()

    assert len(httpserver.log) == 1


def test_exhausts_retries_then_raises(httpserver: HTTPServer):
    # 5 attempts (1 initial + 4 retries) all 503 -> request raises
    for _ in range(5):
        httpserver.expect_ordered_request("/api/v1/validate").respond_with_data(
            "oops", status=503
        )

    with pytest.raises(Exception):
        with _client(httpserver) as api_client:
            AuthenticationApi(api_client).validate()

    assert len(httpserver.log) == 5


def test_retries_on_ssl_handshake_error(httpserver: HTTPServer):
    """SSLError raised at the connection layer is retried, then the call recovers."""
    httpserver.expect_request("/api/v1/validate").respond_with_json({"valid": True})

    original = HTTPConnectionPool._make_request
    calls = {"n": 0}

    def flaky(self, *args, **kwargs):
        calls["n"] += 1
        if calls["n"] <= 2:
            raise SSLError("simulated handshake error")
        return original(self, *args, **kwargs)

    with patch.object(HTTPConnectionPool, "_make_request", flaky):
        with _client(httpserver) as api_client:
            AuthenticationApi(api_client).validate()

    assert calls["n"] == 3  # 2 transient SSLErrors + 1 success
    assert len(httpserver.log) == 1  # only the successful attempt reached the server


def test_retries_on_connection_reset(httpserver: HTTPServer):
    """Mid-flight connection reset (urllib3 ProtocolError) is retried."""
    httpserver.expect_request("/api/v1/validate").respond_with_json({"valid": True})

    original = HTTPConnectionPool._make_request
    calls = {"n": 0}

    def flaky(self, *args, **kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            raise ProtocolError("Connection broken: ConnectionResetError")
        return original(self, *args, **kwargs)

    with patch.object(HTTPConnectionPool, "_make_request", flaky):
        with _client(httpserver) as api_client:
            AuthenticationApi(api_client).validate()

    assert calls["n"] == 2


def test_persistent_ssl_error_eventually_raises(httpserver: HTTPServer):
    """When SSLError persists, all retries are exhausted and the wrapped error propagates."""
    calls = {"n": 0}

    def always_fail(self, *args, **kwargs):
        calls["n"] += 1
        raise SSLError("persistent handshake error")

    with patch.object(HTTPConnectionPool, "_make_request", always_fail):
        with pytest.raises(Exception):
            with _client(httpserver) as api_client:
                AuthenticationApi(api_client).validate()

    # 1 initial + 4 retries = 5 total attempts (max_retries=4 in our FAST_RETRY)
    assert calls["n"] == 5
