"""Extended tests for models to improve coverage."""

from datetime import datetime, timezone


from sharpai_sdk.enums.enumeration_order_enum import EnumerationOrder_Enum
from sharpai_sdk.models.enumeration_query import EnumerationQueryModel
from sharpai_sdk.models.enumeration_result import EnumerationResultModel
from sharpai_sdk.models.expression import ExprModel
from sharpai_sdk.models.timestamp import TimestampModel


def test_timestamp_model():
    """Test TimestampModel."""
    # Test default creation
    timestamp = TimestampModel()
    assert isinstance(timestamp.timestamp, datetime)
    assert timestamp.timestamp.tzinfo == timezone.utc

    # Test with explicit timestamp
    custom_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    timestamp = TimestampModel(timestamp=custom_time)
    assert timestamp.timestamp == custom_time

    # Test with alias
    timestamp = TimestampModel(Timestamp=custom_time)
    assert timestamp.timestamp == custom_time


def test_enumeration_query_model():
    """Test EnumerationQueryModel."""
    # Test default creation
    query = EnumerationQueryModel()
    assert query.ordering == EnumerationOrder_Enum.CreatedDescending
    assert query.include_data is False
    assert query.include_subordinates is False
    assert query.max_results == 5
    assert query.continuation_token is None
    assert query.labels == []
    assert query.tags == {}
    assert isinstance(query.expr, ExprModel)

    # Test with custom values
    query = EnumerationQueryModel(
        ordering=EnumerationOrder_Enum.NameAscending,
        include_data=True,
        include_subordinates=True,
        max_results=10,
        continuation_token="token123",
        labels=["label1", "label2"],
        tags={"key": "value"},
    )
    assert query.ordering == EnumerationOrder_Enum.NameAscending
    assert query.include_data is True
    assert query.include_subordinates is True
    assert query.max_results == 10
    assert query.continuation_token == "token123"
    assert query.labels == ["label1", "label2"]
    assert query.tags == {"key": "value"}

    # Test with aliases
    query = EnumerationQueryModel(
        Ordering=EnumerationOrder_Enum.CreatedAscending,
        IncludeData=True,
        MaxResults=20,
    )
    assert query.ordering == EnumerationOrder_Enum.CreatedAscending
    assert query.include_data is True
    assert query.max_results == 20


def test_enumeration_result_model():
    """Test EnumerationResultModel."""
    # Test default creation
    result = EnumerationResultModel()
    assert result.success is True
    assert isinstance(result.timestamp, TimestampModel)
    assert result.max_results == 1000
    assert result.iterations_required == 0
    assert result.continuation_token is None
    assert result.end_of_results is True
    assert result.total_records == 0
    assert result.records_remaining == 0
    assert result.objects == []

    # Test with custom values
    custom_timestamp = TimestampModel()
    result = EnumerationResultModel(
        success=False,
        timestamp=custom_timestamp,
        max_results=100,
        iterations_required=5,
        continuation_token="token123",
        end_of_results=False,
        total_records=50,
        records_remaining=25,
        objects=[{"id": 1}, {"id": 2}],
    )
    assert result.success is False
    assert result.timestamp == custom_timestamp
    assert result.max_results == 100
    assert result.iterations_required == 5
    assert result.continuation_token == "token123"
    assert result.end_of_results is False
    assert result.total_records == 50
    assert result.records_remaining == 25
    assert result.objects == [{"id": 1}, {"id": 2}]

    # Test with aliases
    result = EnumerationResultModel(
        Success=False,
        MaxResults=200,
        TotalRecords=100,
    )
    assert result.success is False
    assert result.max_results == 200
    assert result.total_records == 100

    # Test validate_objects with None
    result = EnumerationResultModel(objects=None)
    assert result.objects == []

    # Test validate_objects with empty list
    result = EnumerationResultModel(objects=[])
    assert result.objects == []

    # Test with typed objects
    class TestObject:
        def __init__(self, value):
            self.value = value

    result = EnumerationResultModel[TestObject](objects=[TestObject(1), TestObject(2)])
    assert len(result.objects) == 2
    assert result.objects[0].value == 1
    assert result.objects[1].value == 2
