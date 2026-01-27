# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2.0 style license (see LICENSE).
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2020-Present Datadog, Inc.
import logging
from functools import wraps
from typing import Callable

from cloudformation_cli_python_lib import (
    HandlerErrorCode,
    ProgressEvent,
    OperationStatus,
)

LOG = logging.getLogger(__name__)


def http_to_handler_error_code(http_error_code: int) -> HandlerErrorCode:
    if http_error_code == 400:
        return HandlerErrorCode.InvalidRequest
    elif http_error_code == 402:
        return HandlerErrorCode.ServiceLimitExceeded
    elif http_error_code == 403:
        return HandlerErrorCode.AccessDenied
    elif http_error_code == 404:
        return HandlerErrorCode.NotFound
    elif http_error_code == 409:
        return HandlerErrorCode.ResourceConflict
    elif http_error_code == 422:
        return HandlerErrorCode.GeneralServiceException
    elif http_error_code == 429:
        return HandlerErrorCode.Throttling
    return HandlerErrorCode.ServiceInternalError


def errors_handler(f) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs) -> ProgressEvent:
        try:
            return f(*args, **kwargs)
        except Exception as e:
            try:
                model = args[1].desiredResourceState
            except Exception:
                model = None
            LOG.exception("Exception when calling %s: %s\n", f.__name__, e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Exception when calling {f.__name__}: {e}",
                errorCode=HandlerErrorCode.GeneralServiceException,
            )

    return decorated
