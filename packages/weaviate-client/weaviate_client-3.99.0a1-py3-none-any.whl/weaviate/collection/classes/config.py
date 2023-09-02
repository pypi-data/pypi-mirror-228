from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from weaviate.util import _capitalize_first_letter


class DataType(str, Enum):
    TEXT = "text"
    TEXT_ARRAY = "text[]"
    INT = "int"
    INT_ARRAY = "int[]"
    BOOL = "boolean"
    BOOL_ARRAY = "boolean[]"
    NUMBER = "number"
    NUMBER_ARRAY = "number[]"
    DATE = "date"
    DATE_ARRAY = "date[]"
    UUID = "uuid"
    UUID_ARRAY = "uuid[]"
    GEO_COORDINATES = "geoCoordinates"
    BLOB = "blob"
    PHONE_NUMBER = "phoneNumber"


class VectorIndexType(str, Enum):
    HNSW = "hnsw"


class Tokenization(str, Enum):
    WORD = "word"
    WHITESPACE = "whitespace"
    LOWERCASE = "lowercase"
    FIELD = "field"


class Vectorizer(str, Enum):
    NONE = "none"
    TEXT2VEC_OPENAI = "text2vec-openai"
    TEXT2VEC_COHERE = "text2vec-cohere"
    TEXT2VEC_PALM = "text2vec-palm"
    TEXT2VEC_HUGGINGFACE = "text2vec-huggingface"
    TEXT2VEC_TRANSFORMERS = "text2vec-transformers"
    TEXT2VEC_CONTEXTIONARY = "text2vec-contextionary"
    IMG2VEC_NEURAL = "img2vec-neural"
    MULTI2VEC_CLIP = "multi2vec-clip"
    REF2VEC_CENTROID = "ref2vec_centroid"


class VectorDistance(str, Enum):
    COSINE = "cosine"
    DOT = "dot"
    L2_SQUARED = "l2-squared"
    HAMMING = "hamming"
    MANHATTAN = "manhattan"


class StopwordsPreset(str, Enum):
    NONE = "none"
    EN = "en"


class PQEncoderType(str, Enum):
    KMEANS = "kmeans"
    TILE = "tile"


class PQEncoderDistribution(str, Enum):
    LOG_NORMAL = "log-normal"
    NORMAL = "normal"


ModuleConfig = Dict[Vectorizer, Dict[str, Any]]


class ConfigCreateModel(BaseModel):
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)


class ConfigUpdateModel(BaseModel):
    def merge_with_existing(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        for cls_field in self.model_fields:
            val = getattr(self, cls_field)
            if val is None:
                continue
            if isinstance(val, Enum):
                schema[cls_field] = str(val.value)
            elif isinstance(val, (int, float, bool, str, list)):
                schema[cls_field] = val
            else:
                assert isinstance(val, ConfigUpdateModel)
                schema[cls_field] = val.merge_with_existing(schema[cls_field])
        return schema


class PQEncoderConfigCreate(ConfigCreateModel):
    type_: PQEncoderType = PQEncoderType.KMEANS
    distribution: PQEncoderDistribution = PQEncoderDistribution.LOG_NORMAL

    def merge_with_existing(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Must be done manually since Pydantic does not work well with type and type_.
        Errors shadowing type occur if we want to use type as a field name.
        """
        if self.type_ is not None:
            schema["type"] = str(self.type_.value)
        if self.distribution is not None:
            schema["distribution"] = str(self.distribution.value)
        return schema


class PQEncoderConfigUpdate(ConfigUpdateModel):
    type_: Optional[PQEncoderType] = None
    distribution: Optional[PQEncoderDistribution] = None

    def merge_with_existing(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Must be done manually since Pydantic does not work well with type and type_.
        Errors shadowing type occur if we want to use type as a field name.
        """
        if self.type_ is not None:
            schema["type"] = str(self.type_.value)
        if self.distribution is not None:
            schema["distribution"] = str(self.distribution.value)
        return schema


class PQConfigCreate(ConfigCreateModel):
    bitCompression: bool = Field(False, alias="bit_compression")
    centroids: int = 256
    enabled: bool = False
    segments: int = 0
    trainingLimit: int = Field(10000, alias="training_limit")
    encoder: PQEncoderConfigCreate = PQEncoderConfigCreate()


class PQConfigUpdate(ConfigUpdateModel):
    bitCompression: Optional[bool] = Field(None, alias="bit_compression")
    centroids: Optional[int] = None
    enabled: Optional[bool] = None
    segments: Optional[int] = None
    trainingLimit: Optional[int] = Field(None, alias="training_limit")
    encoder: Optional[PQEncoderConfigUpdate] = None


class VectorIndexConfigCreate(ConfigCreateModel):
    cleanupIntervalSeconds: int = Field(300, alias="cleanup_interval_seconds")
    distance: VectorDistance = VectorDistance.COSINE
    dynamicEfMin: int = Field(100, alias="dynamic_ef_min")
    dynamicEfMax: int = Field(500, alias="dynamic_ef_max")
    dynamicEfFactor: int = Field(8, alias="dynamic_ef_factor")
    efConstruction: int = Field(128, alias="ef_construction")
    ef: int = -1
    flatSearchCutoff: int = Field(40000, alias="flat_search_cutoff")
    maxConnections: int = Field(64, alias="max_connections")
    pq: PQConfigCreate = PQConfigCreate(bit_compression=False, training_limit=10000)
    skip: bool = False
    vectorCacheMaxObjects: int = Field(1000000000000, alias="vector_cache_max_objects")


class VectorIndexConfigUpdate(ConfigUpdateModel):
    dynamicEfFactor: Optional[int] = Field(None, alias="dynamic_ef_factor")
    dynamicEfMin: Optional[int] = Field(None, alias="dynamic_ef_min")
    dynamicEfMax: Optional[int] = Field(None, alias="dynamic_ef_max")
    ef: Optional[int] = None
    flatSearchCutoff: Optional[int] = Field(None, alias="flat_search_cutoff")
    skip: Optional[bool] = None
    vectorCacheMaxObjects: Optional[int] = Field(None, alias="vector_cache_max_objects")
    pq: Optional[PQConfigUpdate] = None


class ShardingConfigCreate(ConfigCreateModel):
    virtualPerPhysical: int = Field(128, alias="virtual_per_physical")
    desiredCount: int = Field(1, alias="desired_count")
    actualCount: int = Field(1, alias="actual_count")
    desiredVirtualCount: int = Field(128, alias="desired_virtual_count")
    actualVirtualCount: int = Field(128, alias="actual_virtual_count")
    key: str = "_id"
    strategy: str = "hash"
    function: str = "murmur3"


class ReplicationConfigCreate(ConfigCreateModel):
    factor: int = 1


class ReplicationConfigUpdate(ConfigUpdateModel):
    factor: Optional[int] = None


class BM25ConfigCreate(ConfigCreateModel):
    b: float = 0.75
    k1: float = 1.2


class BM25ConfigUpdate(ConfigUpdateModel):
    b: Optional[float] = None
    k1: Optional[float] = None


class StopwordsCreate(ConfigCreateModel):
    preset: StopwordsPreset = StopwordsPreset.EN
    additions: Optional[List[str]] = None
    removals: Optional[List[str]] = None


class StopwordsUpdate(ConfigUpdateModel):
    preset: Optional[StopwordsPreset] = None
    additions: Optional[List[str]] = None
    removals: Optional[List[str]] = None


class InvertedIndexConfigCreate(ConfigCreateModel):
    bm25: BM25ConfigCreate = BM25ConfigCreate()
    cleanupIntervalSeconds: int = Field(60, alias="cleanup_interval_seconds")
    indexTimestamps: bool = Field(False, alias="index_timestamps")
    indexPropertyLength: bool = Field(False, alias="index_property_length")
    indexNullState: bool = Field(False, alias="index_null_state")
    stopwords: StopwordsCreate = StopwordsCreate()


class InvertedIndexConfigUpdate(ConfigUpdateModel):
    bm25: Optional[BM25ConfigUpdate] = None
    cleanupIntervalSeconds: Optional[int] = Field(None, alias="cleanup_interval_seconds")
    indexTimestamps: Optional[bool] = Field(None, alias="index_timestamps")
    indexPropertyLength: Optional[bool] = Field(None, alias="index_property_length")
    indexNullState: Optional[bool] = Field(None, alias="index_null_state")
    stopwords: Optional[StopwordsUpdate] = None


class MultiTenancyConfig(ConfigCreateModel):
    enabled: bool = False


class CollectionConfigCreateBase(ConfigCreateModel):
    description: Optional[str] = None
    invertedIndexConfig: Optional[InvertedIndexConfigCreate] = Field(
        None, alias="inverted_index_config"
    )
    multiTenancyConfig: Optional[MultiTenancyConfig] = Field(None, alias="multi_tenancy_config")
    replicationConfig: Optional[ReplicationConfigCreate] = Field(None, alias="replication_config")
    shardingConfig: Optional[ShardingConfigCreate] = Field(None, alias="sharding_config")
    vectorIndexConfig: Optional[VectorIndexConfigCreate] = Field(None, alias="vector_index_config")
    vectorIndexType: VectorIndexType = Field(VectorIndexType.HNSW, alias="vector_index_type")
    vectorizer: Vectorizer = Vectorizer.NONE
    moduleConfig: Dict[str, Any] = Field(None, alias="module_config")

    def to_dict(self) -> Dict[str, Any]:
        ret_dict: Dict[str, Any] = {}

        for cls_field in self.model_fields:
            val = getattr(self, cls_field)
            if cls_field in ["name", "model", "properties"] or val is None:
                continue
            if isinstance(val, Enum):
                ret_dict[cls_field] = str(val.value)
            elif isinstance(val, (bool, float, str, int)):
                ret_dict[cls_field] = str(val)
            elif isinstance(val, dict):
                ret_dict[cls_field] = val
            else:
                assert isinstance(val, ConfigCreateModel)
                ret_dict[cls_field] = val.to_dict()

        return ret_dict


class CollectionConfigUpdate(ConfigUpdateModel):
    description: Optional[str] = None
    invertedIndexConfig: Optional[InvertedIndexConfigUpdate] = Field(
        None, alias="inverted_index_config"
    )
    replicationConfig: Optional[ReplicationConfigUpdate] = Field(None, alias="replication_config")
    vectorIndexConfig: Optional[VectorIndexConfigUpdate] = Field(None, alias="vector_index_config")


@dataclass
class _BM25Config:
    b: float
    k1: float


@dataclass
class _StopwordsConfig:
    preset: StopwordsPreset
    additions: Optional[List[str]]
    removals: Optional[List[str]]


@dataclass
class _InvertedIndexConfig:
    bm25: _BM25Config
    cleanup_interval_seconds: int
    stopwords: _StopwordsConfig


@dataclass
class _MultiTenancyConfig:
    enabled: bool


@dataclass
class _ReferenceDataType:
    target_collection: str


@dataclass
class _ReferenceDataTypeMultiTarget:
    target_collections: List[str]


@dataclass
class _Property:
    data_type: Union[DataType, _ReferenceDataType, _ReferenceDataTypeMultiTarget]
    description: Optional[str]
    index_filterable: bool
    index_searchable: bool
    name: str
    tokenization: Optional[Tokenization]

    def to_weaviate_dict(self) -> Dict[str, Any]:
        if isinstance(self.data_type, DataType):
            data_type = [self.data_type.value]
        elif isinstance(self.data_type, _ReferenceDataType):
            data_type = [self.data_type.target_collection]
        else:
            data_type = self.data_type.target_collections
        return {
            "dataType": data_type,
            "description": self.description,
            "indexFilterable": self.index_filterable,
            "indexVector": self.index_searchable,
            "name": self.name,
            "tokenizer": self.tokenization.value if self.tokenization else None,
        }


@dataclass
class _ReplicationFactor:
    factor: int


@dataclass
class _ShardingConfig:
    virtual_per_physical: int
    desired_count: int
    actual_count: int
    desired_virtual_count: int
    actual_virtual_count: int
    key: str
    strategy: str
    function: str


@dataclass
class _PQEncoderConfig:
    type_: PQEncoderType
    distribution: PQEncoderDistribution


@dataclass
class _PQConfig:
    enabled: bool
    bit_compression: bool
    segments: int
    centroids: int
    training_limit: int
    encoder: _PQEncoderConfig


@dataclass
class _VectorIndexConfig:
    cleanup_interval_seconds: int
    distance: VectorDistance
    dynamic_ef_min: int
    dynamic_ef_max: int
    dynamic_ef_factor: int
    ef: int
    ef_construction: int
    flat_search_cutoff: int
    max_connections: int
    pq: _PQConfig
    skip: bool
    vector_cache_max_objects: int


@dataclass
class _CollectionConfig:
    name: str
    description: Optional[str]
    inverted_index_config: _InvertedIndexConfig
    multi_tenancy_config: _MultiTenancyConfig
    properties: List[_Property]
    replication_factor: _ReplicationFactor
    sharding_config: _ShardingConfig
    vector_index_config: _VectorIndexConfig
    vector_index_type: VectorIndexType
    vectorizer: Vectorizer


# class PropertyConfig(ConfigCreateModel):
#     indexFilterable: Optional[bool] = Field(None, alias="index_filterable")
#     indexSearchable: Optional[bool] = Field(None, alias="index_searchable")
#     tokenization: Optional[Tokenization] = None
#     description: Optional[str] = None
#     moduleConfig: Optional[ModuleConfig] = Field(None, alias="module_config")


@dataclass
class PropertyConfig:
    index_filterable: Optional[bool] = None
    index_searchable: Optional[bool] = None
    tokenization: Optional[Tokenization] = None
    description: Optional[str] = None
    module_config: Optional[ModuleConfig] = None

    # tmp solution. replace with a pydantic BaseModel, see bugreport: https://github.com/pydantic/pydantic/issues/6948
    # bugreport was closed as not planned :( so dataclasses must stay
    def to_dict(self) -> Dict[str, Any]:
        return {
            "indexFilterable": self.index_filterable,
            "indexSearchable": self.index_searchable,
            "tokenization": self.tokenization,
            "description": self.description,
            "moduleConfig": self.module_config,
        }


class Property(ConfigCreateModel):
    name: str
    dataType: DataType = Field(..., alias="data_type")
    indexFilterable: Optional[bool] = Field(None, alias="index_filterable")
    indexSearchable: Optional[bool] = Field(None, alias="index_searchable")
    description: Optional[str] = None
    moduleConfig: Optional[ModuleConfig] = Field(None, alias="module_config")
    tokenization: Optional[Tokenization] = None

    def to_dict(self) -> Dict[str, Any]:
        ret_dict = super().to_dict()
        ret_dict["dataType"] = [ret_dict["dataType"]]
        return ret_dict


class ReferencePropertyBase(ConfigCreateModel):
    name: str


class ReferenceProperty(ReferencePropertyBase):
    target_collection: str

    def to_dict(self) -> Dict[str, Any]:
        ret_dict = super().to_dict()
        ret_dict["dataType"] = [_capitalize_first_letter(self.target_collection)]
        del ret_dict["target_collection"]
        return ret_dict


class ReferencePropertyMultiTarget(ReferencePropertyBase):
    target_collections: List[str]

    def to_dict(self) -> Dict[str, Any]:
        ret_dict = super().to_dict()
        ret_dict["dataType"] = [
            _capitalize_first_letter(target) for target in self.target_collections
        ]
        del ret_dict["target_collections"]
        return ret_dict


PropertyType = Union[Property, ReferenceProperty, ReferencePropertyMultiTarget]


class CollectionConfig(CollectionConfigCreateBase):
    """Use this class when specifying all the configuration options relevant to your collection when using
    the non-ORM collections API. This class is a superset of the `CollectionConfigCreateBase` class, and
    includes all the options available to the `CollectionConfigCreateBase` class.

    When using this non-ORM API, you must specify the name and properties of the collection explicitly here.

    Example:
        ```python
        from weaviate.weaviate_classes as wvc

        config = wvc.CollectionConfig(
            name = "MyCollection",
            properties = [
                wvc.Property(
                    name="myProperty",
                    data_type=wvc.DataType.STRING,
                    index_searchable=True,
                    index_filterable=True,
                    description="A string property"
                )
            ]
        )
        ```
    """

    name: str
    properties: Optional[List[Union[Property, ReferencePropertyBase]]] = None

    def model_post_init(self, __context: Any) -> None:
        self.name = _capitalize_first_letter(self.name)

    def to_dict(self) -> Dict[str, Any]:
        ret_dict = super().to_dict()

        ret_dict["class"] = self.name

        if self.properties is not None:
            ret_dict["properties"] = [prop.to_dict() for prop in self.properties]

        return ret_dict
