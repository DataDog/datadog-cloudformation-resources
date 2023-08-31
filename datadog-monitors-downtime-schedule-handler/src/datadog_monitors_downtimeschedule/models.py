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
    Id: Optional[str]
    DisplayTimezone: Optional[str]
    Message: Optional[str]
    MuteFirstRecoveryNotification: Optional[bool]
    Scope: Optional[str]
    NotifyEndStates: Optional[Sequence[str]]
    NotifyEndTypes: Optional[Sequence[str]]
    MonitorIdentifier: Optional["_MonitorIdentifier"]
    Schedule: Optional["_Schedule"]

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
            Id=json_data.get("Id"),
            DisplayTimezone=json_data.get("DisplayTimezone"),
            Message=json_data.get("Message"),
            MuteFirstRecoveryNotification=json_data.get("MuteFirstRecoveryNotification"),
            Scope=json_data.get("Scope"),
            NotifyEndStates=json_data.get("NotifyEndStates"),
            NotifyEndTypes=json_data.get("NotifyEndTypes"),
            MonitorIdentifier=MonitorIdentifier._deserialize(json_data.get("MonitorIdentifier")),
            Schedule=Schedule._deserialize(json_data.get("Schedule")),
        )


# work around possible type aliasing issues when variable has same name as a model
_ResourceModel = ResourceModel


@dataclass
class MonitorIdentifier(BaseModel):
    MonitorId: Optional[int]
    MonitorTags: Optional[Sequence[str]]

    @classmethod
    def _deserialize(
        cls: Type["_MonitorIdentifier"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_MonitorIdentifier"]:
        if not json_data:
            return None
        return cls(
            MonitorId=json_data.get("MonitorId"),
            MonitorTags=json_data.get("MonitorTags"),
        )


# work around possible type aliasing issues when variable has same name as a model
_MonitorIdentifier = MonitorIdentifier


@dataclass
class Schedule(BaseModel):
    Timezone: Optional[str]
    Recurrences: Optional[Sequence["_Recurrences"]]
    Start: Optional[str]
    End: Optional[str]

    @classmethod
    def _deserialize(
        cls: Type["_Schedule"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_Schedule"]:
        if not json_data:
            return None
        return cls(
            Timezone=json_data.get("Timezone"),
            Recurrences=deserialize_list(json_data.get("Recurrences"), Recurrences),
            Start=json_data.get("Start"),
            End=json_data.get("End"),
        )


# work around possible type aliasing issues when variable has same name as a model
_Schedule = Schedule


@dataclass
class Recurrences(BaseModel):
    Duration: Optional[str]
    Rrule: Optional[str]
    Start: Optional[str]

    @classmethod
    def _deserialize(
        cls: Type["_Recurrences"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_Recurrences"]:
        if not json_data:
            return None
        return cls(
            Duration=json_data.get("Duration"),
            Rrule=json_data.get("Rrule"),
            Start=json_data.get("Start"),
        )


# work around possible type aliasing issues when variable has same name as a model
_Recurrences = Recurrences


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


