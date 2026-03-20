# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2.0 style license (see LICENSE).
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2020-Present Datadog, Inc.
import logging
from functools import wraps
from typing import Callable
import urllib3.exceptions

from cloudformation_cli_python_lib import (
    HandlerErrorCode,
    ProgressEvent,
    OperationStatus,
)

LOG = logging.getLogger(__name__)
MAX_CFN_NETWORK_RETRIES = 2
NETWORK_RETRY_DELAY_SECONDS = 30


def _model_and_callback_from_args(args):
    try:
        model = args[1].desiredResourceState
    except Exception:
        model = None
    try:
        callback_context = dict(args[2] or {})
    except Exception:
        callback_context = {}
    return model, callback_context


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
        except urllib3.exceptions.MaxRetryError as e:
            model, callback_context = _model_and_callback_from_args(args)
            retry_count = callback_context.get("_network_retry_count", 0)
            if retry_count < MAX_CFN_NETWORK_RETRIES:
                callback_context["_network_retry_count"] = retry_count + 1
                LOG.warning(
                    "Transient network error in %s (CFN retry %d/%d): %s\n",
                    f.__name__, retry_count + 1, MAX_CFN_NETWORK_RETRIES, e,
                )
                return ProgressEvent(
                    status=OperationStatus.IN_PROGRESS,
                    resourceModel=model,
                    callbackContext=callback_context,
                    callbackDelaySeconds=NETWORK_RETRY_DELAY_SECONDS,
                )
            LOG.exception(
                "Transient network error when calling %s (all retries exhausted): %s\n",
                f.__name__, e,
            )
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Transient network error when calling {f.__name__}: {e}",
                errorCode=HandlerErrorCode.NetworkFailure,
            )
        except Exception as e:
            model, _ = _model_and_callback_from_args(args)
            LOG.exception("Exception when calling %s: %s\n", f.__name__, e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Exception when calling {f.__name__}: {e}",
                errorCode=HandlerErrorCode.GeneralServiceException,
            )

    return decorated
