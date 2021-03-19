# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2.0 style license (see LICENSE).
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2020-Present Datadog, Inc.
from cloudformation_cli_python_lib import HandlerErrorCode


def http_to_handler_error_code(http_error_code: int) -> HandlerErrorCode:
    if http_error_code == 400:
        return HandlerErrorCode.InvalidRequest
    elif http_error_code == 403:
        return HandlerErrorCode.AccessDenied
    elif http_error_code == 404:
        return HandlerErrorCode.NotFound
    elif http_error_code == 409:
        return HandlerErrorCode.ResourceConflict
    elif http_error_code == 422:
        return HandlerErrorCode.ServiceLimitExceeded
    return HandlerErrorCode.ServiceInternalError
