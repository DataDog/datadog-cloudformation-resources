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
    Creator: Optional["_Creator"]
    Description: Optional[str]
    Groups: Optional[Sequence[str]]
    Id: Optional[str]
    MonitorIds: Optional[Sequence[int]]
    Name: Optional[str]
    Query: Optional["_Query"]
    Tags: Optional[Sequence[str]]
    Thresholds: Optional[Sequence["_Threshold"]]
    Type: Optional[str]
    Created: Optional[str]
    Deleted: Optional[str]
    Modified: Optional[str]

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
            Creator=Creator._deserialize(json_data.get("Creator")),
            Description=json_data.get("Description"),
            Groups=json_data.get("Groups"),
            Id=json_data.get("Id"),
            MonitorIds=json_data.get("MonitorIds"),
            Name=json_data.get("Name"),
            Query=Query._deserialize(json_data.get("Query")),
            Tags=json_data.get("Tags"),
            Thresholds=deserialize_list(json_data.get("Thresholds"), Threshold),
            Type=json_data.get("Type"),
            Created=json_data.get("Created"),
            Deleted=json_data.get("Deleted"),
            Modified=json_data.get("Modified"),
        )


# work around possible type aliasing issues when variable has same name as a model
_ResourceModel = ResourceModel


@dataclass
class Creator(BaseModel):
    Name: Optional[str]
    Handle: Optional[str]
    Email: Optional[str]

    @classmethod
    def _deserialize(
        cls: Type["_Creator"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_Creator"]:
        if not json_data:
            return None
        return cls(
            Name=json_data.get("Name"),
            Handle=json_data.get("Handle"),
            Email=json_data.get("Email"),
        )


# work around possible type aliasing issues when variable has same name as a model
_Creator = Creator


@dataclass
class Query(BaseModel):
    Numerator: Optional[str]
    Denominator: Optional[str]

    @classmethod
    def _deserialize(
        cls: Type["_Query"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_Query"]:
        if not json_data:
            return None
        return cls(
            Numerator=json_data.get("Numerator"),
            Denominator=json_data.get("Denominator"),
        )


# work around possible type aliasing issues when variable has same name as a model
_Query = Query


@dataclass
class Threshold(BaseModel):
    Target: Optional[float]
    TargetDisplay: Optional[str]
    Timeframe: Optional[str]
    Warning: Optional[float]
    WarningDisplay: Optional[str]

    @classmethod
    def _deserialize(
        cls: Type["_Threshold"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_Threshold"]:
        if not json_data:
            return None
        return cls(
            Target=json_data.get("Target"),
            TargetDisplay=json_data.get("TargetDisplay"),
            Timeframe=json_data.get("Timeframe"),
            Warning=json_data.get("Warning"),
            WarningDisplay=json_data.get("WarningDisplay"),
        )


# work around possible type aliasing issues when variable has same name as a model
_Threshold = Threshold


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


