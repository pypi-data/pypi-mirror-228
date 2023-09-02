import uuid as uuid_package
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, Mapping, Optional
from typing_extensions import TypeAlias, TypeVar

Properties = TypeVar("Properties", bound=Mapping[str, Any], default=Dict[str, Any])

P = TypeVar("P")


@dataclass
class _MetadataReturn:
    uuid: Optional[uuid_package.UUID] = None
    vector: Optional[List[float]] = None
    creation_time_unix: Optional[int] = None
    last_update_time_unix: Optional[int] = None
    distance: Optional[float] = None
    certainty: Optional[float] = None
    score: Optional[float] = None
    explain_score: Optional[str] = None
    is_consistent: Optional[bool] = None


@dataclass
class _Object(Generic[P]):
    properties: P
    metadata: _MetadataReturn


Reference: TypeAlias = List[_Object[Properties]]


def _metadata_from_dict(metadata: Dict[str, Any]) -> _MetadataReturn:
    return _MetadataReturn(
        uuid=uuid_package.UUID(metadata["id"]) if "id" in metadata else None,
        vector=metadata.get("vector"),
        creation_time_unix=metadata.get("creationTimeUnix"),
        last_update_time_unix=metadata.get("lastUpdateTimeUnix"),
        distance=metadata.get("distance"),
        certainty=metadata.get("certainty"),
        explain_score=metadata.get("explainScore"),
        score=metadata.get("score"),
        is_consistent=metadata.get("isConsistent"),
    )
