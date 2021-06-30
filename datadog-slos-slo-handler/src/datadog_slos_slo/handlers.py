import logging
from typing import Any, List, MutableMapping, Optional

from cloudformation_cli_python_lib import (
    Action,
    HandlerErrorCode,
    OperationStatus,
    ProgressEvent,
    Resource,
    SessionProxy,
)
from datadog_api_client.v1 import ApiException
from datadog_api_client.v1.api.service_level_objectives_api import ServiceLevelObjectivesApi
from datadog_api_client.v1.model.service_level_objective import ServiceLevelObjective as ApiSLO
from datadog_api_client.v1.model.service_level_objective_query import ServiceLevelObjectiveQuery as \
    ApiSLOQuery
from datadog_api_client.v1.model.slo_threshold import SLOThreshold as ApiSLOThreshold
from datadog_api_client.v1.model.slo_timeframe import SLOTimeframe as ApiSLOTimeframe
from datadog_api_client.v1.model.slo_type import SLOType as ApiSLOType
from datadog_cloudformation_common.api_clients import v1_client
from datadog_cloudformation_common.utils import http_to_handler_error_code

from .models import Creator, Threshold, Query, ResourceHandlerRequest, ResourceModel, TypeConfigurationModel
from .version import __version__

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "Datadog::SLOs::SLO"
TELEMETRY_TYPE_NAME = "slos-slo"

resource = Resource(TYPE_NAME, ResourceModel, TypeConfigurationModel)
test_entrypoint = resource.test_entrypoint


@resource.handler(Action.READ)
def read_handler(
        session: Optional[SessionProxy],
        request: ResourceHandlerRequest,
        callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    LOG.info("Starting %s Read Handler", TYPE_NAME)
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration

    with v1_client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = ServiceLevelObjectivesApi(api_client)
        slo_id = model.Id
        try:
            slo = api_instance.get_slo(slo_id)
        except ApiException as e:
            LOG.error("Exception when calling SLOApi->get_slo: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error getting monitor: {e}",
                errorCode=http_to_handler_error_code(e.status)
            )
    model.Created = slo.data.created_at
    model.Modified = slo.data.modified_at
    model.Description = slo.data.description
    model.Name = slo.data.name
    model.Tags = slo.data.tags
    model.Type = slo.data.type.value
    if slo.data.creator:
        model.Creator = Creator(Name=slo.data.creator.name,
                                Email=slo.data.creator.email,
                                Handle=slo.data.creator.handle)

    if slo.data.type.value == "monitor":
        if hasattr(slo.data, 'groups'):
            model.Groups = slo.data.groups
        model.MonitorIds = slo.data.monitor_ids
    elif slo.data.type.value == "metric":
        model.Query = Query(
            Denominator=slo.data.query.denominator,
            Numerator=slo.data.query.numerator
        )
    thresholds = []
    for th in slo.data.thresholds:
        thresholds.append(Threshold(
            Target=th.target if hasattr(th, "target") else None,
            TargetDisplay=th.target_display if hasattr(th, "target_display") else None,
            Timeframe=th.timeframe.value if hasattr(th, "timeframe") else None,
            Warning=th.warning if hasattr(th, "warning") else None,
            WarningDisplay=th.warning_display if hasattr(th,"warning_display") else None
        ))
    model.Thresholds = thresholds

    model.Id = slo.data.id

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model
    )


@resource.handler(Action.UPDATE)
def update_handler(
        session: Optional[SessionProxy],
        request: ResourceHandlerRequest,
        callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    LOG.info("Starting %s Update Handler", TYPE_NAME)
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration
    thresholds = build_slo_thresholds_from_model(model)

    slo = ApiSLO(name=model.Name, type=ApiSLOType(model.Type), thresholds=thresholds)
    if model.Description is not None:
        slo.description = model.Description
    if model.Groups is not None:
        slo.groups = model.Groups
    if model.MonitorIds is not None:
        slo.monitor_ids = model.MonitorIds
    if model.Query is not None:
        slo.query = ApiSLOQuery(numerator=model.Query.Numerator,
                                denominator=model.Query.Denominator)
    if model.Tags is not None:
        slo.tags = model.Tags

    with v1_client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = ServiceLevelObjectivesApi(api_client)
        try:
            api_instance.update_slo(model.Id, slo)
        except ApiException as e:
            LOG.error("Exception when calling SLOApi->update_slo: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error updating slo: {e}",
                errorCode=http_to_handler_error_code(e.status)
            )

    return read_handler(session, request, callback_context)


@resource.handler(Action.DELETE)
def delete_handler(
        session: Optional[SessionProxy],
        request: ResourceHandlerRequest,
        callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    LOG.info("Starting %s Delete Handler", TYPE_NAME)
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration

    with v1_client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = ServiceLevelObjectivesApi(api_client)
        try:
            api_instance.delete_slo(model.Id)
        except ApiException as e:
            LOG.error("Exception when calling SLOApi->delete_slo: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error deleting slo: {e}",
                errorCode=http_to_handler_error_code(e.status)
            )

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model
    )


@resource.handler(Action.CREATE)
def create_handler(
        session: Optional[SessionProxy],
        request: ResourceHandlerRequest,
        callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    LOG.info("Starting %s Create Handler", TYPE_NAME)
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration
    thresholds = build_slo_thresholds_from_model(model)

    slo = ApiSLO(name=model.Name, type=ApiSLOType(model.Type), thresholds=thresholds)
    if model.Description is not None:
        slo.description = model.Description
    if model.Groups is not None:
        slo.groups = model.Groups
    if model.MonitorIds is not None:
        slo.monitor_ids = model.MonitorIds
    if model.Query is not None:
        slo.query = ApiSLOQuery(numerator=model.Query.Numerator,
                                denominator=model.Query.Denominator)
    if model.Tags is not None:
        slo.tags = model.Tags

    with v1_client(
            type_configuration.DatadogCredentials.ApiKey,
            type_configuration.DatadogCredentials.ApplicationKey,
            type_configuration.DatadogCredentials.ApiURL,
            TELEMETRY_TYPE_NAME,
            __version__,
    ) as api_client:
        api_instance = ServiceLevelObjectivesApi(api_client)
        try:
            slo_resp = api_instance.create_slo(slo)
        except ApiException as e:
            LOG.error("Exception when calling SLOApi->create_slo: %s\n", e)
            return ProgressEvent(
                status=OperationStatus.FAILED,
                resourceModel=model,
                message=f"Error creating slo: {e}",
                errorCode=http_to_handler_error_code(e.status)
            )

    model.Id = slo_resp.data[0].id
    return read_handler(session, request, callback_context)


def build_slo_thresholds_from_model(model: ResourceModel) -> List[ApiSLOThreshold]:
    thresholds = []
    if model.Thresholds:
        for threshold in model.Thresholds:
            th = ApiSLOThreshold(target=threshold.Target,
                                 timeframe=ApiSLOTimeframe(threshold.Timeframe))

            if threshold.TargetDisplay is not None:
                th.target_display = threshold.TargetDisplay
            if threshold.Warning is not None:
                th.warning = threshold.Warning
            if threshold.WarningDisplay is not None:
                th.warning_display = threshold.WarningDisplay
            thresholds.append(th)

    return thresholds
