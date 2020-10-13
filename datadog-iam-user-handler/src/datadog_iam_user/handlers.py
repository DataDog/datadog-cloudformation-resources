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
from datadog_api_client.v1 import Configuration, ApiClient, ApiException
from datadog_api_client.v1.api import users_api
from datadog_api_client.v1.model.access_role import AccessRole
from datadog_api_client.v1.model.user import User

from .models import ResourceHandlerRequest, ResourceModel

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

    configuration = setup_api_configuration(request)

    with ApiClient(configuration) as api_client:
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
            return ProgressEvent.failed(HandlerErrorCode.InternalFailure, f"Exception when creating user {e}")

    progress.status = OperationStatus.SUCCESS
    return progress


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
    # TODO: put code here
    return progress


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
    # TODO: put code here
    return progress


@resource.handler(Action.READ)
def read_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState

    configuration = setup_api_configuration(request)

    with ApiClient(configuration) as api_client:
        api_instance = users_api.UsersApi(api_client)
        user_handle = model.Handle
        try:
            api_response = api_instance.get_user(user_handle)
        except ApiException as e:
            LOG.error("Exception when calling UsersApi->get_user: %s\n" % e)
            return ProgressEvent(status=OperationStatus.FAILED, resourceModel=model)

    model.AccessRole = api_response.user.access_role
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


def setup_api_configuration(request: ResourceHandlerRequest) -> Configuration:
    model = request.desiredResourceState
    configuration = Configuration(
        host="https://api.datadoghq.com"
    )
    configuration.api_key['apiKeyAuth'] = model.DatadogCredentials.ApiKey
    configuration.api_key['appKeyAuth'] = model.DatadogCredentials.ApplicationKey
    return configuration
