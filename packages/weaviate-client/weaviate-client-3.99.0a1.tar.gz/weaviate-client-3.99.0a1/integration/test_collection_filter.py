import datetime
from typing import List

import pytest as pytest

import weaviate
from weaviate import Config
from weaviate.collection.classes.config import (
    CollectionConfig,
    Property,
    DataType,
    ReferenceProperty,
    ReferencePropertyMultiTarget,
    Vectorizer,
    InvertedIndexConfigCreate,
)
from weaviate.collection.classes.data import (
    ReferenceTo,
    ReferenceToMultiTarget,
)
from weaviate.collection.classes.filters import (
    Filter,
    _Filters,
    _FilterValue,
)
from weaviate.collection.classes.grpc import MetadataQuery


@pytest.fixture(scope="module")
def client():
    client = weaviate.Client(
        "http://localhost:8080", additional_config=Config(grpc_port_experimental=50051)
    )
    client.schema.delete_all()
    yield client
    client.schema.delete_all()


@pytest.mark.parametrize(
    "weaviate_filter,results",
    [
        (Filter(path="name").equal("Banana"), [0]),
        (Filter(path="name").not_equal("Banana"), [1, 2]),
        (Filter(path="name").like("*nana"), [0]),
    ],
)
def test_filters_text(client: weaviate.Client, weaviate_filter: _FilterValue, results: List[int]):
    client.collection.delete("TestFilterText")
    collection = client.collection.create(
        CollectionConfig(
            name="TestFilterText",
            vectorizer=Vectorizer.NONE,
            properties=[Property(name="name", data_type=DataType.TEXT)],
        )
    )

    uuids = [
        collection.data.insert({"name": "Banana"}),
        collection.data.insert({"name": "Apple"}),
        collection.data.insert({"name": "Mountain"}),
    ]

    objects = collection.query.get_flat(filters=weaviate_filter)
    assert len(objects) == len(results)

    uuids = [uuids[result] for result in results]
    assert all(obj.metadata.uuid in uuids for obj in objects)


@pytest.mark.parametrize(
    "weaviate_filter,results",
    [
        (Filter(path="num").greater_than(1) & Filter(path="num").less_than(3), [1]),
        (
            (Filter(path="num").less_than_equal(1)) | Filter(path="num").greater_than_equal(3),
            [0, 2],
        ),
        (
            Filter(path="num").less_than_equal(1) | Filter(path="num").greater_than_equal(3),
            [0, 2],
        ),
        (
            (Filter(path="num").less_than_equal(1) & Filter(path="num").greater_than_equal(1))
            | Filter(path="num").greater_than_equal(3)
            | Filter(path="num").is_none(True),
            [0, 2, 3],
        ),
    ],
)
def test_filters_nested(
    client: weaviate.Client,
    weaviate_filter: _Filters,
    results: List[int],
):
    client.collection.delete("TestFilterNested")
    collection = client.collection.create(
        CollectionConfig(
            name="TestFilterNested",
            vectorizer=Vectorizer.NONE,
            properties=[Property(name="num", data_type=DataType.NUMBER)],
            inverted_index_config=InvertedIndexConfigCreate(index_null_state=True),
        )
    )

    uuids = [
        collection.data.insert({"num": 1.0}),
        collection.data.insert({"num": 2.0}),
        collection.data.insert({"num": 3.0}),
        collection.data.insert({"num": None}),
    ]

    objects = collection.query.get_flat(
        filters=weaviate_filter, return_metadata=MetadataQuery(uuid=True)
    )
    assert len(objects) == len(results)

    uuids = [uuids[result] for result in results]
    assert all(obj.metadata.uuid in uuids for obj in objects)


def test_length_filter(client: weaviate.Client):
    client.collection.delete("TestFilterNested")
    collection = client.collection.create(
        CollectionConfig(
            name="TestFilterNested",
            vectorizer=Vectorizer.NONE,
            properties=[Property(name="field", data_type=DataType.TEXT)],
            inverted_index_config=InvertedIndexConfigCreate(index_property_length=True),
        )
    )
    uuids = [
        collection.data.insert({"field": "one"}),
        collection.data.insert({"field": "two"}),
        collection.data.insert({"field": "three"}),
        collection.data.insert({"field": "four"}),
    ]
    objects = collection.query.get_flat(filters=Filter(path="field", length=True).equal(3))

    results = [0, 1]
    assert len(objects) == len(results)
    uuids = [uuids[result] for result in results]
    assert all(obj.metadata.uuid in uuids for obj in objects)


@pytest.mark.parametrize(
    "weaviate_filter,results",
    [
        (Filter(path="number").is_none(True), [3]),
        (Filter(path="number").is_none(False), [0, 1, 2]),
    ],
)
def test_filters_comparison(
    client: weaviate.Client, weaviate_filter: _FilterValue, results: List[int]
):
    client.collection.delete("TestFilterNumber")
    collection = client.collection.create(
        CollectionConfig(
            name="TestFilterNumber",
            vectorizer=Vectorizer.NONE,
            properties=[Property(name="number", data_type=DataType.INT)],
            inverted_index_config=InvertedIndexConfigCreate(index_null_state=True),
        )
    )

    uuids = [
        collection.data.insert({"number": 1}),
        collection.data.insert({"number": 2}),
        collection.data.insert({"number": 3}),
        collection.data.insert({"number": None}),
    ]

    objects = collection.query.get_flat(filters=weaviate_filter)
    assert len(objects) == len(results)

    uuids = [uuids[result] for result in results]
    assert all(obj.metadata.uuid in uuids for obj in objects)


@pytest.mark.parametrize(
    "weaviate_filter,results",
    [
        (Filter(path="nums").contains_any([1, 4]), [0, 3]),
        (Filter(path="nums").contains_any([10]), []),
        (Filter(path="num").contains_any([1]), [0, 1]),
        (Filter(path="text").contains_any(["test"]), [0, 1]),
        (Filter(path="text").contains_any(["real", "deal"]), [1, 2, 3]),
        (Filter(path="texts").contains_any(["test"]), [0, 1]),
        (Filter(path="texts").contains_any(["real", "deal"]), [1, 2, 3]),
        (Filter(path="float").contains_any([2.0]), []),
        (Filter(path="float").contains_any([2]), []),
        (Filter(path="float").contains_any([8]), [3]),
        (Filter(path="float").contains_any([8.0]), [3]),
        (Filter(path="floats").contains_any([2.0]), [0, 1]),
        (Filter(path="floats").contains_any([0.4, 0.7]), [0, 1, 3]),
        (Filter(path="floats").contains_any([2]), [0, 1]),
        (Filter(path="bools").contains_any([True, False]), [0, 1, 3]),
        (Filter(path="bools").contains_any([False]), [0, 1]),
        (Filter(path="bool").contains_any([True]), [0, 1, 3]),
        (Filter(path="nums").contains_all([1, 4]), [0]),
        (Filter(path="text").contains_all(["real", "test"]), [1]),
        (Filter(path="texts").contains_all(["real", "test"]), [1]),
        (Filter(path="floats").contains_all([0.7, 2]), [1]),
        (Filter(path="bools").contains_all([True, False]), [0]),
        (Filter(path="bool").contains_all([True, False]), []),
        (Filter(path="bool").contains_all([True]), [0, 1, 3]),
    ],
)
def test_filters_contains(
    client: weaviate.Client, weaviate_filter: _FilterValue, results: List[int]
):
    client.collection.delete("TestFilterContains")
    collection = client.collection.create(
        CollectionConfig(
            name="TestFilterContains",
            vectorizer=Vectorizer.NONE,
            properties=[
                Property(name="text", data_type=DataType.TEXT),
                Property(name="texts", data_type=DataType.TEXT_ARRAY),
                Property(name="num", data_type=DataType.INT),
                Property(name="nums", data_type=DataType.INT_ARRAY),
                Property(name="float", data_type=DataType.NUMBER),
                Property(name="floats", data_type=DataType.NUMBER_ARRAY),
                Property(name="bool", data_type=DataType.BOOL),
                Property(name="bools", data_type=DataType.BOOL_ARRAY),
            ],
        )
    )

    uuids = [
        collection.data.insert(
            {
                "text": "this is a test",
                "texts": "this is a test".split(" "),
                "num": 1,
                "nums": [1, 2, 4],
                "float": 0.5,
                "floats": [0.4, 0.9, 2],
                "bool": True,
                "bools": [True, False],
            }
        ),
        collection.data.insert(
            {
                "text": "this is not a real test",
                "texts": "this is not a real test".split(" "),
                "num": 1,
                "nums": [5, 6, 9],
                "float": 0.3,
                "floats": [0.1, 0.7, 2],
                "bool": True,
                "bools": [False, False],
            }
        ),
        collection.data.insert(
            {
                "text": "real deal",
                "texts": "real deal".split(" "),
                "num": 3,
                "nums": [],
                "floats": [],
                "bool": False,
                "bools": [],
            }
        ),
        collection.data.insert(
            {
                "text": "not real deal",
                "texts": "not real deal".split(" "),
                "num": 4,
                "nums": [4],
                "float": 8,
                "floats": [0.7],
                "bool": True,
                "bools": [True],
            }
        ),
    ]

    objects = collection.query.get_flat(
        filters=weaviate_filter, return_metadata=MetadataQuery(uuid=True)
    )
    assert len(objects) == len(results)

    uuids = [uuids[result] for result in results]
    assert all(obj.metadata.uuid in uuids for obj in objects)


@pytest.mark.parametrize("test_number,results", [(0, [0, 1])])
def test_filters_contains_dates(client: weaviate.Client, test_number: int, results: List[int]):
    pytest.skip("Date arrays not yet supported")
    client.collection.delete("TestFilterContainsDates")
    collection = client.collection.create(
        CollectionConfig(
            name="TestFilterContainsDates",
            vectorizer=Vectorizer.NONE,
            properties=[Property(name="dates", data_type=DataType.DATE_ARRAY)],
        )
    )
    now = datetime.datetime.now(datetime.timezone.utc)
    later = now + datetime.timedelta(hours=1)
    much_later = now + datetime.timedelta(days=1)

    uuids = [
        collection.data.insert({"dates": [now, later, much_later]}),
        collection.data.insert({"dates": [now, now, much_later]}),
        collection.data.insert({"dates": []}),
        collection.data.insert({"dates": [much_later]}),
    ]

    if test_number == 1:
        contains = [now, later]
    else:
        contains = [now]

    weav_filter = Filter(path="dates").contains_any(contains)

    objects = collection.query.get_flat(
        filters=weav_filter, return_metadata=MetadataQuery(uuid=True)
    )
    assert len(objects) == len(results)

    uuids = [uuids[result] for result in results]
    assert all(obj.metadata.uuid in uuids for obj in objects)


@pytest.mark.parametrize(
    "weaviate_filter,results",
    [
        (Filter(path=["ref", "TestFilterRef2", "int"]).greater_than(3), [1]),
        (Filter(path=["ref", "TestFilterRef2", "text"], length=True).less_than(6), [0]),
    ],
)
def test_ref_filters(client: weaviate.Client, weaviate_filter: _FilterValue, results: List[int]):
    client.collection.delete("TestFilterRef")
    client.collection.delete("TestFilterRef2")
    to_collection = client.collection.create(
        CollectionConfig(
            name="TestFilterRef2",
            vectorizer=Vectorizer.NONE,
            properties=[
                Property(name="int", data_type=DataType.INT),
                Property(name="text", data_type=DataType.TEXT),
            ],
            inverted_index_config=InvertedIndexConfigCreate(index_property_length=True),
        )
    )
    uuids_to = [
        to_collection.data.insert(properties={"int": 0, "text": "first"}),
        to_collection.data.insert(properties={"int": 15, "text": "second"}),
    ]
    from_collection = client.collection.create(
        CollectionConfig(
            name="TestFilterRef",
            properties=[
                ReferenceProperty(name="ref", target_collection="TestFilterRef2"),
                Property(name="name", data_type=DataType.TEXT),
            ],
            vectorizer=Vectorizer.NONE,
        )
    )

    uuids_from = [
        from_collection.data.insert({"ref": ReferenceTo(uuids_to[0]), "name": "first"}),
        from_collection.data.insert({"ref": ReferenceTo(uuids_to[1]), "name": "second"}),
    ]

    objects = from_collection.query.get_flat(
        filters=weaviate_filter, return_metadata=MetadataQuery(uuid=True)
    )
    assert len(objects) == len(results)

    uuids = [uuids_from[result] for result in results]
    assert all(obj.metadata.uuid in uuids for obj in objects)


def test_ref_filters_multi_target(client: weaviate.Client):
    target = "TestFilterRefMulti2"
    source = "TestFilterRefMulti"
    client.collection.delete(source)
    client.collection.delete(target)
    to_collection = client.collection.create(
        CollectionConfig(
            name=target,
            vectorizer=Vectorizer.NONE,
            properties=[Property(name="int", data_type=DataType.INT)],
        )
    )
    uuid_to = to_collection.data.insert(properties={"int": 0})
    uuid_to2 = to_collection.data.insert(properties={"int": 5})
    from_collection = client.collection.create(
        CollectionConfig(
            name=source,
            properties=[
                ReferencePropertyMultiTarget(
                    name="ref", target_collections=[target, "TestFilterRefMulti"]
                ),
                Property(name="name", data_type=DataType.TEXT),
            ],
            vectorizer=Vectorizer.NONE,
        )
    )

    uuid_from_to_target1 = from_collection.data.insert(
        {"ref": ReferenceToMultiTarget(uuids=uuid_to, target_collection=target), "name": "first"}
    )
    uuid_from_to_target2 = from_collection.data.insert(
        {"ref": ReferenceToMultiTarget(uuids=uuid_to2, target_collection=target), "name": "second"}
    )
    from_collection.data.insert(
        {
            "ref": ReferenceToMultiTarget(uuids=uuid_from_to_target1, target_collection=source),
            "name": "third",
        }
    )
    from_collection.data.insert(
        {
            "ref": ReferenceToMultiTarget(uuids=uuid_from_to_target2, target_collection=source),
            "name": "fourth",
        }
    )

    objects = from_collection.query.get_flat(
        filters=Filter(path=["ref", target, "int"]).greater_than(3)
    )
    assert len(objects) == 1
    assert objects[0].properties["name"] == "second"

    objects = from_collection.query.get_flat(
        filters=Filter(path=["ref", source, "name"]).equal("first")
    )
    assert len(objects) == 1
    assert objects[0].properties["name"] == "third"
