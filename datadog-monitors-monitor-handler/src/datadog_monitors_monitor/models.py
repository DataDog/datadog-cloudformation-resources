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
    Creator: Optional["_Creator"]
    Id: Optional[int]
    Message: Optional[str]
    Name: Optional[str]
    Tags: Optional[Sequence[str]]
    Options: Optional["_MonitorOptions"]
    Query: Optional[str]
    Type: Optional[str]
    Multi: Optional[bool]
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
            Id=json_data.get("Id"),
            Message=json_data.get("Message"),
            Name=json_data.get("Name"),
            Tags=json_data.get("Tags"),
            Options=MonitorOptions._deserialize(json_data.get("Options")),
            Query=json_data.get("Query"),
            Type=json_data.get("Type"),
            Multi=json_data.get("Multi"),
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
class MonitorOptions(BaseModel):
    EnableLogsSample: Optional[bool]
    EscalationMessage: Optional[str]
    EvaluationDelay: Optional[int]
    IncludeTags: Optional[bool]
    Locked: Optional[bool]
    MinLocationFailed: Optional[int]
    NewHostDelay: Optional[int]
    NoDataTimeframe: Optional[int]
    NotifyAudit: Optional[bool]
    NotifyNoData: Optional[bool]
    RenotifyInterval: Optional[int]
    RequireFullWindow: Optional[bool]
    SyntheticsCheckID: Optional[int]
    Thresholds: Optional["_MonitorThresholds"]
    ThresholdWindows: Optional["_MonitorThresholdWindows"]
    TimeoutH: Optional[int]

    @classmethod
    def _deserialize(
        cls: Type["_MonitorOptions"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_MonitorOptions"]:
        if not json_data:
            return None
        return cls(
            EnableLogsSample=json_data.get("EnableLogsSample"),
            EscalationMessage=json_data.get("EscalationMessage"),
            EvaluationDelay=json_data.get("EvaluationDelay"),
            IncludeTags=json_data.get("IncludeTags"),
            Locked=json_data.get("Locked"),
            MinLocationFailed=json_data.get("MinLocationFailed"),
            NewHostDelay=json_data.get("NewHostDelay"),
            NoDataTimeframe=json_data.get("NoDataTimeframe"),
            NotifyAudit=json_data.get("NotifyAudit"),
            NotifyNoData=json_data.get("NotifyNoData"),
            RenotifyInterval=json_data.get("RenotifyInterval"),
            RequireFullWindow=json_data.get("RequireFullWindow"),
            SyntheticsCheckID=json_data.get("SyntheticsCheckID"),
            Thresholds=MonitorThresholds._deserialize(json_data.get("Thresholds")),
            ThresholdWindows=MonitorThresholdWindows._deserialize(json_data.get("ThresholdWindows")),
            TimeoutH=json_data.get("TimeoutH"),
        )


# work around possible type aliasing issues when variable has same name as a model
_MonitorOptions = MonitorOptions


@dataclass
class MonitorThresholds(BaseModel):
    Critical: Optional[float]
    CriticalRecovery: Optional[float]
    OK: Optional[float]
    Warning: Optional[float]
    WarningRecovery: Optional[float]

    @classmethod
    def _deserialize(
        cls: Type["_MonitorThresholds"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_MonitorThresholds"]:
        if not json_data:
            return None
        return cls(
            Critical=json_data.get("Critical"),
            CriticalRecovery=json_data.get("CriticalRecovery"),
            OK=json_data.get("OK"),
            Warning=json_data.get("Warning"),
            WarningRecovery=json_data.get("WarningRecovery"),
        )


# work around possible type aliasing issues when variable has same name as a model
_MonitorThresholds = MonitorThresholds


@dataclass
class MonitorThresholdWindows(BaseModel):
    TriggerWindow: Optional[str]
    RecoveryWindow: Optional[str]

    @classmethod
    def _deserialize(
        cls: Type["_MonitorThresholdWindows"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_MonitorThresholdWindows"]:
        if not json_data:
            return None
        return cls(
            TriggerWindow=json_data.get("TriggerWindow"),
            RecoveryWindow=json_data.get("RecoveryWindow"),
        )


# work around possible type aliasing issues when variable has same name as a model
_MonitorThresholdWindows = MonitorThresholdWindows


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


