# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2.0 style license (see LICENSE).
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2020-Present Datadog, Inc.
import pytest
from pytest_httpserver import HTTPServer


@pytest.fixture
def httpserver():
    server = HTTPServer(host="127.0.0.1", port=0)
    server.start()
    try:
        yield server
    finally:
        server.clear()
        if server.is_running():
            server.stop()
