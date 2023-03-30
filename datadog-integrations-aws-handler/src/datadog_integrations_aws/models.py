# DO NOT modify this file by hand, changes will be overwritten
from dataclasses import dataclass

from cloudformation_cli_python_lib.interface import (
    BaseModel,
    BaseResourceHandlerRequest,
)
from cloudformation_cli_python_lib.recast import recast_object
from cloudformation_cli_python_lib.utils import deserialize_list

import sys
from inspect import getmembers, isclass
from typing import (
    AbstractSet,
    Any,
    Generic,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Type,
    TypeVar,
)

T = TypeVar("T")


def set_or_none(value: Optional[Sequence[T]]) -> Optional[AbstractSet[T]]:
    if value:
        return set(value)
    return None


@dataclass
class ResourceHandlerRequest(BaseResourceHandlerRequest):
    # pylint: disable=invalid-name
    desiredResourceState: Optional["ResourceModel"]
    previousResourceState: Optional["ResourceModel"]
    typeConfiguration: Optional["TypeConfigurationModel"]


@dataclass
class ResourceModel(BaseModel):
    AccountID: Optional[str]
    RoleName: Optional[str]
    AccessKeyID: Optional[str]
    FilterTags: Optional[Sequence[str]]
    HostTags: Optional[Sequence[str]]
    AccountSpecificNamespaceRules: Optional[MutableMapping[str, bool]]
    IntegrationID: Optional[str]
    ExternalIDSecretName: Optional[str]
    MetricsCollection: Optional[bool]
    CSPMResourceCollection: Optional[bool]
    ResourceCollection: Optional[bool]
    ExcludedRegions: Optional[Sequence[str]]

    @classmethod
    def _deserialize(
        cls: Type["_ResourceModel"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_ResourceModel"]:
        if not json_data:
            return None
        dataclasses = {n: o for n, o in getmembers(sys.modules[__name__]) if isclass(o)}
        recast_object(cls, json_data, dataclasses)
        return cls(
            AccountID=json_data.get("AccountID"),
            RoleName=json_data.get("RoleName"),
            AccessKeyID=json_data.get("AccessKeyID"),
            FilterTags=json_data.get("FilterTags"),
            HostTags=json_data.get("HostTags"),
            AccountSpecificNamespaceRules=json_data.get("AccountSpecificNamespaceRules"),
            IntegrationID=json_data.get("IntegrationID"),
            ExternalIDSecretName=json_data.get("ExternalIDSecretName"),
            MetricsCollection=json_data.get("MetricsCollection"),
            CSPMResourceCollection=json_data.get("CSPMResourceCollection"),
            ResourceCollection=json_data.get("ResourceCollection"),
            ExcludedRegions=json_data.get("ExcludedRegions"),
        )


# work around possible type aliasing issues when variable has same name as a model
_ResourceModel = ResourceModel


@dataclass
class TypeConfigurationModel(BaseModel):
    DatadogCredentials: Optional["_DatadogCredentials"]

    @classmethod
    def _deserialize(
        cls: Type["_TypeConfigurationModel"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_TypeConfigurationModel"]:
        if not json_data:
            return None
        return cls(
            DatadogCredentials=DatadogCredentials._deserialize(json_data.get("DatadogCredentials")),
        )


# work around possible type aliasing issues when variable has same name as a model
_TypeConfigurationModel = TypeConfigurationModel


@dataclass
class DatadogCredentials(BaseModel):
    ApiKey: Optional[str]
    ApplicationKey: Optional[str]
    ApiURL: Optional[str]

    @classmethod
    def _deserialize(
        cls: Type["_DatadogCredentials"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_DatadogCredentials"]:
        if not json_data:
            return None
        return cls(
            ApiKey=json_data.get("ApiKey"),
            ApplicationKey=json_data.get("ApplicationKey"),
            ApiURL=json_data.get("ApiURL"),
        )


# work around possible type aliasing issues when variable has same name as a model
_DatadogCredentials = DatadogCredentials
