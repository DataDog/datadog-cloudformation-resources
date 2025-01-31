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
    AWSPartition: Optional[str]
    AuthConfig: Optional["_AuthConfig"]
    AWSRegions: Optional["_AWSRegions"]
    MetricsConfig: Optional["_MetricsConfig"]
    AccountTags: Optional[Sequence[str]]
    ResourcesConfig: Optional["_ResourcesConfig"]
    LogsConfig: Optional["_LogsConfig"]
    TracesConfig: Optional["_TracesConfig"]
    IntegrationID: Optional[str]
    ExternalIDSecretName: Optional[str]

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
            AWSPartition=json_data.get("AWSPartition"),
            AuthConfig=AuthConfig._deserialize(json_data.get("AuthConfig")),
            AWSRegions=AWSRegions._deserialize(json_data.get("AWSRegions")),
            MetricsConfig=MetricsConfig._deserialize(json_data.get("MetricsConfig")),
            AccountTags=json_data.get("AccountTags"),
            ResourcesConfig=ResourcesConfig._deserialize(json_data.get("ResourcesConfig")),
            LogsConfig=LogsConfig._deserialize(json_data.get("LogsConfig")),
            TracesConfig=TracesConfig._deserialize(json_data.get("TracesConfig")),
            IntegrationID=json_data.get("IntegrationID"),
            ExternalIDSecretName=json_data.get("ExternalIDSecretName"),
        )


# work around possible type aliasing issues when variable has same name as a model
_ResourceModel = ResourceModel


@dataclass
class AuthConfig(BaseModel):
    RoleName: Optional[str]

    @classmethod
    def _deserialize(
        cls: Type["_AuthConfig"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_AuthConfig"]:
        if not json_data:
            return None
        return cls(
            RoleName=json_data.get("RoleName"),
        )


# work around possible type aliasing issues when variable has same name as a model
_AuthConfig = AuthConfig


@dataclass
class AWSRegions(BaseModel):
    IncludeOnly: Optional[Sequence[str]]
    IncludeAll: Optional[bool]

    @classmethod
    def _deserialize(
        cls: Type["_AWSRegions"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_AWSRegions"]:
        if not json_data:
            return None
        return cls(
            IncludeOnly=json_data.get("IncludeOnly"),
            IncludeAll=json_data.get("IncludeAll"),
        )


# work around possible type aliasing issues when variable has same name as a model
_AWSRegions = AWSRegions


@dataclass
class MetricsConfig(BaseModel):
    Enabled: Optional[bool]
    AutomuteEnabled: Optional[bool]
    CollectCloudwatchAlarms: Optional[bool]
    CollectCustomMetrics: Optional[bool]
    TagFilters: Optional[Sequence["_TagFilters"]]
    NamespaceFilters: Optional["_NamespaceFilters"]

    @classmethod
    def _deserialize(
        cls: Type["_MetricsConfig"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_MetricsConfig"]:
        if not json_data:
            return None
        return cls(
            Enabled=json_data.get("Enabled"),
            AutomuteEnabled=json_data.get("AutomuteEnabled"),
            CollectCloudwatchAlarms=json_data.get("CollectCloudwatchAlarms"),
            CollectCustomMetrics=json_data.get("CollectCustomMetrics"),
            TagFilters=deserialize_list(json_data.get("TagFilters"), TagFilters),
            NamespaceFilters=NamespaceFilters._deserialize(json_data.get("NamespaceFilters")),
        )


# work around possible type aliasing issues when variable has same name as a model
_MetricsConfig = MetricsConfig


@dataclass
class TagFilters(BaseModel):
    Namespace: Optional[str]
    Tags: Optional[Sequence[str]]

    @classmethod
    def _deserialize(
        cls: Type["_TagFilters"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_TagFilters"]:
        if not json_data:
            return None
        return cls(
            Namespace=json_data.get("Namespace"),
            Tags=json_data.get("Tags"),
        )


# work around possible type aliasing issues when variable has same name as a model
_TagFilters = TagFilters


@dataclass
class NamespaceFilters(BaseModel):
    IncludeOnly: Optional[Sequence[str]]
    ExcludeOnly: Optional[Sequence[str]]

    @classmethod
    def _deserialize(
        cls: Type["_NamespaceFilters"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_NamespaceFilters"]:
        if not json_data:
            return None
        return cls(
            IncludeOnly=json_data.get("IncludeOnly"),
            ExcludeOnly=json_data.get("ExcludeOnly"),
        )


# work around possible type aliasing issues when variable has same name as a model
_NamespaceFilters = NamespaceFilters


@dataclass
class ResourcesConfig(BaseModel):
    CSPMResourceCollection: Optional[bool]
    ExtendedResourceCollection: Optional[bool]

    @classmethod
    def _deserialize(
        cls: Type["_ResourcesConfig"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_ResourcesConfig"]:
        if not json_data:
            return None
        return cls(
            CSPMResourceCollection=json_data.get("CSPMResourceCollection"),
            ExtendedResourceCollection=json_data.get("ExtendedResourceCollection"),
        )


# work around possible type aliasing issues when variable has same name as a model
_ResourcesConfig = ResourcesConfig


@dataclass
class LogsConfig(BaseModel):
    LambdaForwarder: Optional["_LambdaForwarder"]

    @classmethod
    def _deserialize(
        cls: Type["_LogsConfig"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_LogsConfig"]:
        if not json_data:
            return None
        return cls(
            LambdaForwarder=LambdaForwarder._deserialize(json_data.get("LambdaForwarder")),
        )


# work around possible type aliasing issues when variable has same name as a model
_LogsConfig = LogsConfig


@dataclass
class LambdaForwarder(BaseModel):
    Lambdas: Optional[Sequence[str]]
    Sources: Optional[Sequence[str]]

    @classmethod
    def _deserialize(
        cls: Type["_LambdaForwarder"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_LambdaForwarder"]:
        if not json_data:
            return None
        return cls(
            Lambdas=json_data.get("Lambdas"),
            Sources=json_data.get("Sources"),
        )


# work around possible type aliasing issues when variable has same name as a model
_LambdaForwarder = LambdaForwarder


@dataclass
class TracesConfig(BaseModel):
    XRayServices: Optional["_XRayServices"]

    @classmethod
    def _deserialize(
        cls: Type["_TracesConfig"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_TracesConfig"]:
        if not json_data:
            return None
        return cls(
            XRayServices=XRayServices._deserialize(json_data.get("XRayServices")),
        )


# work around possible type aliasing issues when variable has same name as a model
_TracesConfig = TracesConfig


@dataclass
class XRayServices(BaseModel):
    IncludeOnly: Optional[Sequence[str]]
    IncludeAll: Optional[bool]

    @classmethod
    def _deserialize(
        cls: Type["_XRayServices"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_XRayServices"]:
        if not json_data:
            return None
        return cls(
            IncludeOnly=json_data.get("IncludeOnly"),
            IncludeAll=json_data.get("IncludeAll"),
        )


# work around possible type aliasing issues when variable has same name as a model
_XRayServices = XRayServices


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


