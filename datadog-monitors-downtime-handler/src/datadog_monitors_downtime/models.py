# DO NOT modify this file by hand, changes will be overwritten
import sys
from dataclasses import dataclass
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

from cloudformation_cli_python_lib.interface import (
    BaseModel,
    BaseResourceHandlerRequest,
)
from cloudformation_cli_python_lib.recast import recast_object
from cloudformation_cli_python_lib.utils import deserialize_list

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
    Active: Optional[bool]
    Canceled: Optional[int]
    CreatorId: Optional[int]
    Disabled: Optional[bool]
    DowntimeType: Optional[int]
    End: Optional[int]
    Id: Optional[int]
    Message: Optional[str]
    MonitorId: Optional[int]
    MonitorTags: Optional[Sequence[str]]
    ParentId: Optional[int]
    Scope: Optional[Sequence[str]]
    Start: Optional[int]
    Timezone: Optional[str]
    UpdaterId: Optional[int]

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
            Active=json_data.get("Active"),
            Canceled=json_data.get("Canceled"),
            CreatorId=json_data.get("CreatorId"),
            Disabled=json_data.get("Disabled"),
            DowntimeType=json_data.get("DowntimeType"),
            End=json_data.get("End"),
            Id=json_data.get("Id"),
            Message=json_data.get("Message"),
            MonitorId=json_data.get("MonitorId"),
            MonitorTags=json_data.get("MonitorTags"),
            ParentId=json_data.get("ParentId"),
            Scope=json_data.get("Scope"),
            Start=json_data.get("Start"),
            Timezone=json_data.get("Timezone"),
            UpdaterId=json_data.get("UpdaterId"),
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


