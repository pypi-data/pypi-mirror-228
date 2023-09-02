"""Generated implementation of scheduler."""

# WARNING DO NOT EDIT
# This code was generated from scheduler.mcn

from __future__ import annotations

import abc  # noqa: F401
import dataclasses  # noqa: F401
import datetime  # noqa: F401
import enum  # noqa: F401
import isodate  # noqa: F401
import json  # noqa: F401
import jsonschema  # noqa: F401
import logging  # noqa: F401
import typing  # noqa: F401
import uuid  # noqa: F401
try:
    from anaml_client.utils.serialisation import JsonObject  # noqa: F401
except ImportError:
    pass

from ..cluster import ClusterId, ClusterPropertySetId
from ..date_range import DateRange
from ..destination_reference import DestinationReference
from ..entity_population import EntityPopulationId
from ..event_store import EventStoreId
from ..feature_set import FeatureSetId
from ..feature_store import FeatureStoreId, VersionTarget
from ..feature_store_run import FeatureStoreRunId
from ..source_reference import SourceReference
from ..table import TableId
from ..table_caching import TableCachingJobId
from ..table_monitoring import TableMonitoringJobId
from ..view_materialisation import (
    ViewMaterialisationJobId, ViewMaterialisationJobVersionId,
    ViewMaterialisationRunId
)


@dataclasses.dataclass(frozen=True)
class SchedulerRunRequest(abc.ABC):
    """A request for the scheduler to immediately kick off a job.

     Only one job id should be set in each call to the
     endpoint.

     If the job is an event store batch run, then also include
     a subject and source."""
    
    ADT_TYPE: typing.ClassVar[str] = ""
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    @classmethod
    def json_schema(cls) -> SchedulerRunRequest:
        """JSON schema for variant SchedulerRunRequest.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        adt_types = [klass.ADT_TYPE for klass in cls.__subclasses__()]
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": adt_types
                }
            },
            "required": [
                "adt_type",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> SchedulerRunRequest:
        """Validate and parse JSON data into an instance of SchedulerRunRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of SchedulerRunRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            adt_type = data.get("adt_type", None)
            for klass in cls.__subclasses__():
                if klass.ADT_TYPE == adt_type:
                    return klass.from_json(data)
            raise ValueError("Unknown adt_type: '{ty}'".format(ty=adt_type))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing SchedulerRunRequest", exc_info=ex)
            raise
    
    @abc.abstractmethod
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class RunFeatureStore(SchedulerRunRequest):
    """Run a feature store
    
    Args:
        id (FeatureStoreId): A data field.
        dateRange (typing.Optional[DateRange]): A data field.
        mergeRunId (typing.Optional[FeatureStoreRunId]): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "runfeaturestore"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: FeatureStoreId
    dateRange: typing.Optional[DateRange]
    mergeRunId: typing.Optional[FeatureStoreRunId]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for RunFeatureStore data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": [cls.ADT_TYPE]
                },
                "id": FeatureStoreId.json_schema(),
                "dateRange": {
                    "oneOf": [
                        {"type": "null"},
                        DateRange.json_schema(),
                    ]
                },
                "mergeRunId": {
                    "oneOf": [
                        {"type": "null"},
                        FeatureStoreRunId.json_schema(),
                    ]
                }
            },
            "required": [
                "adt_type",
                "id",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> RunFeatureStore:
        """Validate and parse JSON data into an instance of RunFeatureStore.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of RunFeatureStore.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return RunFeatureStore(
                id=FeatureStoreId.from_json(data["id"]),
                dateRange=(
                    lambda v: DateRange.from_json(v) if v is not None else None
                )(
                    data.get("dateRange", None)
                ),
                mergeRunId=(
                    lambda v: FeatureStoreRunId.from_json(v) if v is not None else None
                )(
                    data.get("mergeRunId", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing RunFeatureStore",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "adt_type": self.ADT_TYPE,
            "id": self.id.to_json(),
            "dateRange": (lambda v: v.to_json() if v is not None else v)(self.dateRange),
            "mergeRunId": (lambda v: v.to_json() if v is not None else v)(self.mergeRunId)
        }


@dataclasses.dataclass(frozen=True)
class RunTableMonitoring(SchedulerRunRequest):
    """Run a table monitoring job
    
    Args:
        id (TableMonitoringJobId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "runtablemonitoring"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: TableMonitoringJobId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for RunTableMonitoring data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": [cls.ADT_TYPE]
                },
                "id": TableMonitoringJobId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> RunTableMonitoring:
        """Validate and parse JSON data into an instance of RunTableMonitoring.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of RunTableMonitoring.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return RunTableMonitoring(
                id=TableMonitoringJobId.from_json(data["id"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing RunTableMonitoring",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "adt_type": self.ADT_TYPE,
            "id": self.id.to_json()
        }


@dataclasses.dataclass(frozen=True)
class RunTableCaching(SchedulerRunRequest):
    """Run a feature set
    
    Args:
        id (TableCachingJobId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "runtablecaching"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: TableCachingJobId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for RunTableCaching data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": [cls.ADT_TYPE]
                },
                "id": TableCachingJobId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> RunTableCaching:
        """Validate and parse JSON data into an instance of RunTableCaching.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of RunTableCaching.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return RunTableCaching(
                id=TableCachingJobId.from_json(data["id"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing RunTableCaching",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "adt_type": self.ADT_TYPE,
            "id": self.id.to_json()
        }


@dataclasses.dataclass(frozen=True)
class RunViewMaterialisation(SchedulerRunRequest):
    """Run a view materialisation set
    
    Args:
        id (ViewMaterialisationJobId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "runviewmaterialisation"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: ViewMaterialisationJobId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for RunViewMaterialisation data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": [cls.ADT_TYPE]
                },
                "id": ViewMaterialisationJobId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> RunViewMaterialisation:
        """Validate and parse JSON data into an instance of RunViewMaterialisation.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of RunViewMaterialisation.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return RunViewMaterialisation(
                id=ViewMaterialisationJobId.from_json(data["id"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing RunViewMaterialisation",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "adt_type": self.ADT_TYPE,
            "id": self.id.to_json()
        }


@dataclasses.dataclass(frozen=True)
class RunViewTable(SchedulerRunRequest):
    """Run a view table
    
    Args:
        additionalClusterProperties (typing.Dict[str, str]): A data field.
        cluster (ClusterId): A data field.
        clusterPropertySets (typing.List[ClusterPropertySetId]): A data field.
        destinations (typing.List[DestinationReference]): A data field.
        table (TableId): A data field.
        versionTarget (typing.Optional[VersionTarget]): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "runviewtable"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    additionalClusterProperties: typing.Dict[str, str]
    cluster: ClusterId
    clusterPropertySets: typing.List[ClusterPropertySetId]
    destinations: typing.List[DestinationReference]
    table: TableId
    versionTarget: typing.Optional[VersionTarget]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for RunViewTable data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": [cls.ADT_TYPE]
                },
                "additionalClusterProperties": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "string"
                    }
                },
                "cluster": ClusterId.json_schema(),
                "clusterPropertySets": {
                    "type": "array",
                    "item": ClusterPropertySetId.json_schema()
                },
                "destinations": {
                    "type": "array",
                    "item": DestinationReference.json_schema()
                },
                "table": TableId.json_schema(),
                "versionTarget": {
                    "oneOf": [
                        {"type": "null"},
                        VersionTarget.json_schema(),
                    ]
                }
            },
            "required": [
                "adt_type",
                "additionalClusterProperties",
                "cluster",
                "clusterPropertySets",
                "destinations",
                "table",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> RunViewTable:
        """Validate and parse JSON data into an instance of RunViewTable.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of RunViewTable.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return RunViewTable(
                additionalClusterProperties={
                    str(k): str(v) for k, v in data["additionalClusterProperties"].items()
                },
                cluster=ClusterId.from_json(data["cluster"]),
                clusterPropertySets=[ClusterPropertySetId.from_json(v) for v in data["clusterPropertySets"]],
                destinations=[DestinationReference.from_json(v) for v in data["destinations"]],
                table=TableId.from_json(data["table"]),
                versionTarget=(
                    lambda v: VersionTarget.from_json(v) if v is not None else None
                )(
                    data.get("versionTarget", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing RunViewTable",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "adt_type": self.ADT_TYPE,
            "additionalClusterProperties": {str(k): str(v) for k, v in self.additionalClusterProperties.items()},
            "cluster": self.cluster.to_json(),
            "clusterPropertySets": [v.to_json() for v in self.clusterPropertySets],
            "destinations": [v.to_json() for v in self.destinations],
            "table": self.table.to_json(),
            "versionTarget": (lambda v: v.to_json() if v is not None else v)(self.versionTarget)
        }


@dataclasses.dataclass(frozen=True)
class RunEventStoreJob(SchedulerRunRequest):
    """Run an event store job
    
    Args:
        id (EventStoreId): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "runeventstorejob"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: EventStoreId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for RunEventStoreJob data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": [cls.ADT_TYPE]
                },
                "id": EventStoreId.json_schema()
            },
            "required": [
                "adt_type",
                "id",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> RunEventStoreJob:
        """Validate and parse JSON data into an instance of RunEventStoreJob.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of RunEventStoreJob.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return RunEventStoreJob(
                id=EventStoreId.from_json(data["id"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing RunEventStoreJob",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "adt_type": self.ADT_TYPE,
            "id": self.id.to_json()
        }


@dataclasses.dataclass(frozen=True)
class RunEventStoreBatchIngest(SchedulerRunRequest):
    """Run an event store batch ingest
    
    Args:
        id (EventStoreId): A data field.
        subject (str): A data field.
        source (SourceReference): A data field.
        clusterPropertySets (typing.Optional[typing.List[ClusterPropertySetId]]): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "runeventstorebatchingest"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: EventStoreId
    subject: str
    source: SourceReference
    clusterPropertySets: typing.Optional[typing.List[ClusterPropertySetId]]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for RunEventStoreBatchIngest data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": [cls.ADT_TYPE]
                },
                "id": EventStoreId.json_schema(),
                "subject": {
                    "type": "string"
                },
                "source": SourceReference.json_schema(),
                "clusterPropertySets": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "array", "item": ClusterPropertySetId.json_schema()},
                    ]
                }
            },
            "required": [
                "adt_type",
                "id",
                "subject",
                "source",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> RunEventStoreBatchIngest:
        """Validate and parse JSON data into an instance of RunEventStoreBatchIngest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of RunEventStoreBatchIngest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return RunEventStoreBatchIngest(
                id=EventStoreId.from_json(data["id"]),
                subject=str(data["subject"]),
                source=SourceReference.from_json(data["source"]),
                clusterPropertySets=(
                    lambda v: [ClusterPropertySetId.from_json(v) for v in v] if v is not None else None
                )(
                    data.get("clusterPropertySets", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing RunEventStoreBatchIngest",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "adt_type": self.ADT_TYPE,
            "id": self.id.to_json(),
            "subject": str(self.subject),
            "source": self.source.to_json(),
            "clusterPropertySets": (lambda v: [v.to_json() for v in v] if v is not None else v)(self.clusterPropertySets)
        }


@dataclasses.dataclass(frozen=True)
class RunFeatureSet(SchedulerRunRequest):
    """Run an feature set
    
    Args:
        id (FeatureSetId): A data field.
        additionalSparkProperties (typing.Optional[typing.Dict[str, str]]): A data field.
        cluster (ClusterId): A data field.
        clusterPropertySet (typing.Optional[ClusterPropertySetId]): A data field.
        dateRange (DateRange): A data field.
        destinations (typing.List[DestinationReference]): A data field.
        entityPopulation (typing.Optional[EntityPopulationId]): A data field.
        versionTarget (VersionTarget): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "runfeatureset"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    id: FeatureSetId
    additionalSparkProperties: typing.Optional[typing.Dict[str, str]]
    cluster: ClusterId
    clusterPropertySet: typing.Optional[ClusterPropertySetId]
    dateRange: DateRange
    destinations: typing.List[DestinationReference]
    entityPopulation: typing.Optional[EntityPopulationId]
    versionTarget: VersionTarget
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for RunFeatureSet data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": [cls.ADT_TYPE]
                },
                "id": FeatureSetId.json_schema(),
                "additionalSparkProperties": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "object", "additionalProperties": {"type": "string"}},
                    ]
                },
                "cluster": ClusterId.json_schema(),
                "clusterPropertySet": {
                    "oneOf": [
                        {"type": "null"},
                        ClusterPropertySetId.json_schema(),
                    ]
                },
                "dateRange": DateRange.json_schema(),
                "destinations": {
                    "type": "array",
                    "item": DestinationReference.json_schema()
                },
                "entityPopulation": {
                    "oneOf": [
                        {"type": "null"},
                        EntityPopulationId.json_schema(),
                    ]
                },
                "versionTarget": VersionTarget.json_schema()
            },
            "required": [
                "adt_type",
                "id",
                "cluster",
                "dateRange",
                "destinations",
                "versionTarget",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> RunFeatureSet:
        """Validate and parse JSON data into an instance of RunFeatureSet.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of RunFeatureSet.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return RunFeatureSet(
                id=FeatureSetId.from_json(data["id"]),
                additionalSparkProperties=(
                    lambda v: {str(k): str(v) for k, v in v.items()} if v is not None else None
                )(
                    data.get("additionalSparkProperties", None)
                ),
                cluster=ClusterId.from_json(data["cluster"]),
                clusterPropertySet=(
                    lambda v: ClusterPropertySetId.from_json(v) if v is not None else None
                )(
                    data.get("clusterPropertySet", None)
                ),
                dateRange=DateRange.from_json(data["dateRange"]),
                destinations=[DestinationReference.from_json(v) for v in data["destinations"]],
                entityPopulation=(
                    lambda v: EntityPopulationId.from_json(v) if v is not None else None
                )(
                    data.get("entityPopulation", None)
                ),
                versionTarget=VersionTarget.from_json(data["versionTarget"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing RunFeatureSet",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "adt_type": self.ADT_TYPE,
            "id": self.id.to_json(),
            "additionalSparkProperties": (lambda v: {str(k): str(v) for k, v in v.items()} if v is not None else v)(self.additionalSparkProperties),
            "cluster": self.cluster.to_json(),
            "clusterPropertySet": (lambda v: v.to_json() if v is not None else v)(self.clusterPropertySet),
            "dateRange": self.dateRange.to_json(),
            "destinations": [v.to_json() for v in self.destinations],
            "entityPopulation": (lambda v: v.to_json() if v is not None else v)(self.entityPopulation),
            "versionTarget": self.versionTarget.to_json()
        }


@dataclasses.dataclass(frozen=True)
class RunViewTableResponse:
    """Args:
        jobId (ViewMaterialisationJobId): A data field.
        jobVersion (ViewMaterialisationJobVersionId): A data field.
        runId (ViewMaterialisationRunId): A data field."""
    
    jobId: ViewMaterialisationJobId
    jobVersion: ViewMaterialisationJobVersionId
    runId: ViewMaterialisationRunId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for RunViewTableResponse data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "jobId": ViewMaterialisationJobId.json_schema(),
                "jobVersion": ViewMaterialisationJobVersionId.json_schema(),
                "runId": ViewMaterialisationRunId.json_schema()
            },
            "required": [
                "jobId",
                "jobVersion",
                "runId",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> RunViewTableResponse:
        """Validate and parse JSON data into an instance of RunViewTableResponse.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of RunViewTableResponse.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return RunViewTableResponse(
                jobId=ViewMaterialisationJobId.from_json(data["jobId"]),
                jobVersion=ViewMaterialisationJobVersionId.from_json(data["jobVersion"]),
                runId=ViewMaterialisationRunId.from_json(data["runId"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing RunViewTableResponse",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "jobId": self.jobId.to_json(),
            "jobVersion": self.jobVersion.to_json(),
            "runId": self.runId.to_json()
        }
