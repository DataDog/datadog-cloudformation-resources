import logging
from typing import Any, MutableMapping, Optional

from cloudformation_cli_python_lib import (
    Action,
    HandlerErrorCode,
    OperationStatus,
    ProgressEvent,
    Resource,
    SessionProxy,
)
from datadog_api_client.v1 import ApiException
from datadog_api_client.v1.api import users_api
from datadog_api_client.v1.model.access_role import AccessRole
from datadog_api_client.v1.model.user import User
from datadog_cloudformation_common.api_clients import v1_client

from .models import ResourceHandlerRequest, ResourceModel
from .version import __version__

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "Datadog::IAM::User"

resource = Resource(TYPE_NAME, ResourceModel)
test_entrypoint = resource.test_entrypoint


@resource.handler(Action.CREATE)
def create_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )

    LOG.info("Starting the User Resource Create Handler")

    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL or "https://api.datadoghq.com",
            TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = users_api.UsersApi(api_client)
        body = User(
            access_role=AccessRole(model.AccessRole),
            email=model.Email,
            handle=model.Handle,
            name=model.Name,
        )
        try:
            api_instance.create_user(body)
        except ApiException as e:
            LOG.error("Exception when calling UsersApi->create_user: %s\n" % e)
            return ProgressEvent(status=OperationStatus.FAILED, resourceModel=model, message=e.body)

    return read_handler(session, request, callback_context)


@resource.handler(Action.UPDATE)
def update_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )

    LOG.info("Starting the User Resource Update Handler")

    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL or "https://api.datadoghq.com",
            TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = users_api.UsersApi(api_client)
        body = User(
            access_role=AccessRole(model.AccessRole),
            email=model.Email,
            disabled=model.Disabled or False,
            name=model.Name,
        )
        try:
            api_instance.update_user(model.Handle, body)
        except ApiException as e:
            LOG.error("Exception when calling UsersApi->update_user: %s\n" % e)
            return ProgressEvent(status=OperationStatus.FAILED, resourceModel=model, message=e.body)

    return read_handler(session, request, callback_context)


@resource.handler(Action.DELETE)
def delete_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )

    LOG.info("Starting the User Resource Delete Handler")

    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL or "https://api.datadoghq.com",
            TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = users_api.UsersApi(api_client)
        user_handle = model.Handle
        try:
            api_instance.disable_user(user_handle)
        except ApiException as e:
            LOG.error("Exception when calling UsersApi->disable_user: %s\n" % e)
            return ProgressEvent(status=OperationStatus.FAILED, resourceModel=model, message=e.body)

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=None,
    )


@resource.handler(Action.READ)
def read_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    LOG.info("Starting the User Resource Delete Handler")

    with v1_client(
            model.DatadogCredentials.ApiKey,
            model.DatadogCredentials.ApplicationKey,
            model.DatadogCredentials.ApiURL or "https://api.datadoghq.com",
            TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = users_api.UsersApi(api_client)
        user_handle = model.Handle
        try:
            api_response = api_instance.get_user(user_handle)
        except ApiException as e:
            LOG.error("Exception when calling UsersApi->get_user: %s\n" % e)
            return ProgressEvent(status=OperationStatus.FAILED, resourceModel=model, message=e.body)

    model.AccessRole = api_response.user.access_role.value
    model.Name = api_response.user.name
    model.Disabled = api_response.user.disabled
    model.Verified = api_response.user.verified
    model.Email = api_response.user.email
    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )


@resource.handler(Action.LIST)
def list_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    # TODO: put code here
    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModels=[],
    )
