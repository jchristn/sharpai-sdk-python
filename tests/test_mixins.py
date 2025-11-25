"""Tests for mixins.py to improve coverage."""

from unittest.mock import patch

import pytest
from pydantic import BaseModel

from sharpai_sdk.configuration import configure, get_client
from sharpai_sdk.mixins import (
    AllRetrievableAPIResource,
    CreateableAPIResource,
    CreateableMultipleAPIResource,
    DeletableAPIResource,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
    ExistsAPIResource,
    RetrievableAPIResource,
    SearchableAPIResource,
    UpdatableAPIResource,
)
from sharpai_sdk.models.enumeration_query import EnumerationQueryModel
from sharpai_sdk.models.enumeration_result import EnumerationResultModel


# Test model classes
class TestModel(BaseModel):
    """Test model for mixin tests."""

    id: str
    name: str = "test"
    value: int = 0


class TestResourceModel(BaseModel):
    """Test resource model."""

    guid: str
    data: dict = {}


@pytest.fixture
def mock_client():
    """Create a mock client."""
    with patch("httpx.Client"):
        configure("http://test-api.com")
        client = get_client()
        return client


# ExistsAPIResource tests
class TestExistsResource(ExistsAPIResource):
    """Test resource for ExistsAPIResource."""

    RESOURCE_NAME = "test-resource"


def test_exists_resource_success(mock_client):
    """Test exists method returns True when resource exists."""
    with patch.object(mock_client, "request", return_value=None):
        result = TestExistsResource.exists("test-guid")
        assert result is True
        mock_client.request.assert_called_once_with(
            "HEAD", "v1.0/test-resource/test-guid"
        )


def test_exists_resource_not_found(mock_client):
    """Test exists method returns False when resource doesn't exist."""
    with patch.object(mock_client, "request", side_effect=Exception("Not found")):
        result = TestExistsResource.exists("test-guid")
        assert result is False


# CreateableAPIResource tests
class TestCreateableResource(CreateableAPIResource):
    """Test resource for CreateableAPIResource."""

    RESOURCE_NAME = "test-resource"
    MODEL = TestModel
    CREATE_METHOD = "PUT"


class TestCreateableResourceNoModel(CreateableAPIResource):
    """Test resource without MODEL."""

    RESOURCE_NAME = "test-resource"
    MODEL = None


def test_create_resource_with_model(mock_client):
    """Test create method with MODEL."""
    response_data = {"id": "new-id", "name": "created", "value": 10}
    with patch.object(mock_client, "request", return_value=response_data):
        result = TestCreateableResource.create(id="new-id", name="created", value=10)
        assert isinstance(result, TestModel)
        assert result.id == "new-id"
        assert result.name == "created"
        assert result.value == 10


def test_create_resource_without_model(mock_client):
    """Test create method without MODEL."""
    response_data = {"id": "new-id", "name": "created"}
    with patch.object(mock_client, "request", return_value=response_data):
        result = TestCreateableResourceNoModel.create(id="new-id", name="created")
        assert result == response_data


def test_create_resource_with_headers(mock_client):
    """Test create method with custom headers."""
    response_data = {"id": "new-id", "name": "created", "value": 5}
    with patch.object(
        mock_client, "request", return_value=response_data
    ) as mock_request:
        _ = TestCreateableResource.create(
            id="new-id", headers={"Custom-Header": "value"}
        )
        call_kwargs = mock_request.call_args[1]
        assert "headers" in call_kwargs
        assert call_kwargs["headers"]["Custom-Header"] == "value"


def test_create_resource_with_data_param(mock_client):
    """Test create method with _data parameter."""
    response_data = {"id": "new-id", "name": "created", "value": 5}
    with patch.object(mock_client, "request", return_value=response_data):
        result = TestCreateableResource.create(
            _data={"id": "new-id", "name": "created"}
        )
        assert isinstance(result, TestModel)


def test_create_resource_post_method(mock_client):
    """Test create method with POST method."""

    class TestCreateableResourcePOST(CreateableAPIResource):
        RESOURCE_NAME = "test-resource"
        MODEL = TestModel
        CREATE_METHOD = "POST"

    response_data = {"id": "new-id", "name": "created", "value": 5}
    with patch.object(
        mock_client, "request", return_value=response_data
    ) as mock_request:
        TestCreateableResourcePOST.create(id="new-id")
        call_args = mock_request.call_args[0]
        assert call_args[0] == "POST"


# CreateableMultipleAPIResource tests
class TestCreateableMultipleResource(CreateableMultipleAPIResource):
    """Test resource for CreateableMultipleAPIResource."""

    RESOURCE_NAME = "test-resource"
    MODEL = TestModel


class TestCreateableMultipleResourceNoModel(CreateableMultipleAPIResource):
    """Test resource without MODEL."""

    RESOURCE_NAME = "test-resource"
    MODEL = None


def test_create_multiple_resource_with_model(mock_client):
    """Test create_multiple method with MODEL."""
    response_data = [
        {"id": "id1", "name": "test1", "value": 1},
        {"id": "id2", "name": "test2", "value": 2},
    ]
    with patch.object(mock_client, "request", return_value=response_data):
        result = TestCreateableMultipleResource.create_multiple(
            [{"id": "id1", "name": "test1"}, {"id": "id2", "name": "test2"}]
        )
        assert len(result) == 2
        assert all(isinstance(item, TestModel) for item in result)
        assert result[0].id == "id1"
        assert result[1].id == "id2"


def test_create_multiple_resource_without_model(mock_client):
    """Test create_multiple method without MODEL."""
    response_data = [{"id": "id1"}, {"id": "id2"}]
    with patch.object(mock_client, "request", return_value=response_data):
        result = TestCreateableMultipleResourceNoModel.create_multiple(
            [{"id": "id1"}, {"id": "id2"}]
        )
        assert result == response_data


def test_create_multiple_resource_empty_list(mock_client):
    """Test create_multiple method with empty list."""
    result = TestCreateableMultipleResource.create_multiple([])
    assert result == []


def test_create_multiple_resource_none_error(mock_client):
    """Test create_multiple method raises error when data is None."""
    with pytest.raises(TypeError, match="Nodes parameter cannot be None"):
        TestCreateableMultipleResource.create_multiple(None)


# RetrievableAPIResource tests
class TestRetrievableResource(RetrievableAPIResource):
    """Test resource for RetrievableAPIResource."""

    RESOURCE_NAME = "test-resource"
    MODEL = TestModel


class TestRetrievableResourceNoModel(RetrievableAPIResource):
    """Test resource without MODEL."""

    RESOURCE_NAME = "test-resource"
    MODEL = None


def test_retrieve_resource_with_model(mock_client):
    """Test retrieve method with MODEL."""
    response_data = {"id": "test-id", "name": "test", "value": 5}
    with patch.object(mock_client, "request", return_value=response_data):
        result = TestRetrievableResource.retrieve("test-guid")
        assert isinstance(result, TestModel)
        assert result.id == "test-id"


def test_retrieve_resource_without_model(mock_client):
    """Test retrieve method without MODEL."""
    response_data = {"id": "test-id", "name": "test"}
    with patch.object(mock_client, "request", return_value=response_data):
        result = TestRetrievableResourceNoModel.retrieve("test-guid")
        assert result == response_data


def test_retrieve_resource_with_include_data(mock_client):
    """Test retrieve method with include_data."""
    response_data = {"id": "test-id", "name": "test", "value": 5}
    with patch.object(
        mock_client, "request", return_value=response_data
    ) as mock_request:
        TestRetrievableResource.retrieve("test-guid", include_data=True)
        call_args = mock_request.call_args[0]
        assert "incldata" in call_args[1]


def test_retrieve_resource_with_include_subordinates(mock_client):
    """Test retrieve method with include_subordinates."""
    response_data = {"id": "test-id", "name": "test", "value": 5}
    with patch.object(
        mock_client, "request", return_value=response_data
    ) as mock_request:
        TestRetrievableResource.retrieve("test-guid", include_subordinates=True)
        call_args = mock_request.call_args[0]
        assert "inclsub" in call_args[1]


# UpdatableAPIResource tests
class TestUpdatableResource(UpdatableAPIResource):
    """Test resource for UpdatableAPIResource."""

    RESOURCE_NAME = "test-resource"
    MODEL = TestModel


class TestUpdatableResourceNoModel(UpdatableAPIResource):
    """Test resource without MODEL."""

    RESOURCE_NAME = "test-resource"
    MODEL = None


def test_update_resource_with_model(mock_client):
    """Test update method with MODEL."""
    response_data = {"id": "test-id", "name": "updated", "value": 10}
    with patch.object(mock_client, "request", return_value=response_data):
        result = TestUpdatableResource.update("test-guid", name="updated", value=10)
        assert isinstance(result, TestModel)
        assert result.name == "updated"
        assert result.value == 10


def test_update_resource_without_model(mock_client):
    """Test update method without MODEL."""
    response_data = {"id": "test-id", "name": "updated"}
    with patch.object(mock_client, "request", return_value=response_data):
        result = TestUpdatableResourceNoModel.update("test-guid", name="updated")
        assert result == response_data


# DeletableAPIResource tests
class TestDeletableResource(DeletableAPIResource):
    """Test resource for DeletableAPIResource."""

    RESOURCE_NAME = "test-resource"


def test_delete_resource(mock_client):
    """Test delete method."""
    with patch.object(mock_client, "request", return_value=None) as mock_request:
        TestDeletableResource.delete("test-guid")
        call_args = mock_request.call_args[0]
        assert call_args[0] == "DELETE"
        assert "test-guid" in call_args[1]


def test_delete_resource_with_kwargs(mock_client):
    """Test delete method with additional kwargs."""
    with patch.object(mock_client, "request", return_value=None) as mock_request:
        TestDeletableResource.delete("test-guid", force=True)
        call_args = mock_request.call_args[0]
        assert "force" in call_args[1] or "force" in str(call_args[1])


# AllRetrievableAPIResource tests
class TestAllRetrievableResource(AllRetrievableAPIResource):
    """Test resource for AllRetrievableAPIResource."""

    RESOURCE_NAME = "test-resource"
    MODEL = TestModel


class TestAllRetrievableResourceNoModel(AllRetrievableAPIResource):
    """Test resource without MODEL."""

    RESOURCE_NAME = "test-resource"
    MODEL = None


def test_retrieve_all_resource_with_model(mock_client):
    """Test retrieve_all method with MODEL."""
    response_data = [
        {"id": "id1", "name": "test1", "value": 1},
        {"id": "id2", "name": "test2", "value": 2},
    ]
    with patch.object(mock_client, "request", return_value=response_data):
        result = TestAllRetrievableResource.retrieve_all()
        assert len(result) == 2
        assert all(isinstance(item, TestModel) for item in result)


def test_retrieve_all_resource_without_model(mock_client):
    """Test retrieve_all method without MODEL."""
    response_data = [{"id": "id1"}, {"id": "id2"}]
    with patch.object(mock_client, "request", return_value=response_data):
        result = TestAllRetrievableResourceNoModel.retrieve_all()
        assert result == response_data


def test_retrieve_all_resource_with_include_data(mock_client):
    """Test retrieve_all method with include_data."""
    response_data = [{"id": "id1"}]
    with patch.object(
        mock_client, "request", return_value=response_data
    ) as mock_request:
        TestAllRetrievableResource.retrieve_all(include_data=True)
        call_args = mock_request.call_args[0]
        assert "incldata" in call_args[1]


def test_retrieve_all_resource_with_include_subordinates(mock_client):
    """Test retrieve_all method with include_subordinates."""
    response_data = [{"id": "id1"}]
    with patch.object(
        mock_client, "request", return_value=response_data
    ) as mock_request:
        TestAllRetrievableResource.retrieve_all(include_subordinates=True)
        call_args = mock_request.call_args[0]
        assert "inclsub" in call_args[1]


# SearchableAPIResource tests
class TestSearchableResource(SearchableAPIResource):
    """Test resource for SearchableAPIResource."""

    RESOURCE_NAME = "test-resource"
    SEARCH_MODELS = (EnumerationQueryModel, EnumerationResultModel)


def test_search_resource(mock_client):
    """Test search method."""
    response_data = {
        "Success": True,
        "Timestamp": {"Timestamp": "2024-01-01T00:00:00Z"},
        "MaxResults": 1000,
        "IterationsRequired": 0,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 0,
        "RecordsRemaining": 0,
        "Objects": [],
    }
    with patch.object(mock_client, "request", return_value=response_data):
        result = TestSearchableResource.search(query="test")
        assert isinstance(result, EnumerationResultModel)


def test_search_resource_with_include_data(mock_client):
    """Test search method with include_data."""
    response_data = {
        "Success": True,
        "Timestamp": {"Timestamp": "2024-01-01T00:00:00Z"},
        "MaxResults": 1000,
        "IterationsRequired": 0,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 0,
        "RecordsRemaining": 0,
        "Objects": [],
    }
    with patch.object(
        mock_client, "request", return_value=response_data
    ) as mock_request:
        TestSearchableResource.search(include_data=True)
        call_kwargs = mock_request.call_args[1]
        assert "data" in call_kwargs
        data_str = (
            call_kwargs["data"].decode()
            if isinstance(call_kwargs["data"], bytes)
            else call_kwargs["data"]
        )
        assert "IncludeData" in data_str or "include_data" in data_str.lower()


def test_search_resource_with_include_subordinates(mock_client):
    """Test search method with include_subordinates."""
    response_data = {
        "Success": True,
        "Timestamp": {"Timestamp": "2024-01-01T00:00:00Z"},
        "MaxResults": 1000,
        "IterationsRequired": 0,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 0,
        "RecordsRemaining": 0,
        "Objects": [],
    }
    with patch.object(
        mock_client, "request", return_value=response_data
    ) as mock_request:
        TestSearchableResource.search(include_subordinates=True)
        call_kwargs = mock_request.call_args[1]
        assert "data" in call_kwargs


# EnumerableAPIResource tests
class TestEnumerableResource(EnumerableAPIResource):
    """Test resource for EnumerableAPIResource."""

    RESOURCE_NAME = "test-resource"
    MODEL = TestModel


class TestEnumerableResourceNoModel(EnumerableAPIResource):
    """Test resource without MODEL."""

    RESOURCE_NAME = "test-resource"
    MODEL = None


def test_enumerate_resource_with_model(mock_client):
    """Test enumerate method with MODEL."""
    response_data = {
        "Success": True,
        "Timestamp": {"Timestamp": "2024-01-01T00:00:00Z"},
        "MaxResults": 1000,
        "IterationsRequired": 0,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 0,
        "RecordsRemaining": 0,
        "Objects": [],
    }
    with patch.object(mock_client, "request", return_value=response_data):
        result = TestEnumerableResource.enumerate()
        assert isinstance(result, EnumerationResultModel)


def test_enumerate_resource_without_model(mock_client):
    """Test enumerate method without MODEL."""
    response_data = {
        "Success": True,
        "Timestamp": {"Timestamp": "2024-01-01T00:00:00Z"},
        "MaxResults": 1000,
        "IterationsRequired": 0,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 0,
        "RecordsRemaining": 0,
        "Objects": [],
    }
    with patch.object(mock_client, "request", return_value=response_data):
        result = TestEnumerableResourceNoModel.enumerate()
        assert result == response_data


def test_enumerate_resource_with_include_data(mock_client):
    """Test enumerate method with include_data."""
    response_data = {
        "Success": True,
        "Timestamp": {"Timestamp": "2024-01-01T00:00:00Z"},
        "MaxResults": 1000,
        "IterationsRequired": 0,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 0,
        "RecordsRemaining": 0,
        "Objects": [],
    }
    with patch.object(
        mock_client, "request", return_value=response_data
    ) as mock_request:
        TestEnumerableResource.enumerate(include_data=True)
        call_args = mock_request.call_args[0]
        assert "incldata" in call_args[1]


def test_enumerate_resource_with_include_subordinates(mock_client):
    """Test enumerate method with include_subordinates."""
    response_data = {
        "Success": True,
        "Timestamp": {"Timestamp": "2024-01-01T00:00:00Z"},
        "MaxResults": 1000,
        "IterationsRequired": 0,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 0,
        "RecordsRemaining": 0,
        "Objects": [],
    }
    with patch.object(
        mock_client, "request", return_value=response_data
    ) as mock_request:
        TestEnumerableResource.enumerate(include_subordinates=True)
        call_args = mock_request.call_args[0]
        assert "inclsub" in call_args[1]


# EnumerableAPIResourceWithData tests
class TestEnumerableResourceWithData(EnumerableAPIResourceWithData):
    """Test resource for EnumerableAPIResourceWithData."""

    RESOURCE_NAME = "test-resource"
    MODEL = TestModel


class TestEnumerableResourceWithDataNoModel(EnumerableAPIResourceWithData):
    """Test resource without MODEL."""

    RESOURCE_NAME = "test-resource"
    MODEL = None


def test_enumerate_with_query_resource_with_model(mock_client):
    """Test enumerate_with_query method with MODEL."""
    response_data = {
        "Success": True,
        "Timestamp": {"Timestamp": "2024-01-01T00:00:00Z"},
        "MaxResults": 1000,
        "IterationsRequired": 0,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 0,
        "RecordsRemaining": 0,
        "Objects": [],
    }
    with patch.object(mock_client, "request", return_value=response_data):
        result = TestEnumerableResourceWithData.enumerate_with_query(max_results=10)
        assert isinstance(result, EnumerationResultModel)


def test_enumerate_with_query_resource_without_model(mock_client):
    """Test enumerate_with_query method without MODEL."""
    response_data = {
        "Success": True,
        "Timestamp": {"Timestamp": "2024-01-01T00:00:00Z"},
        "MaxResults": 1000,
        "IterationsRequired": 0,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 0,
        "RecordsRemaining": 0,
        "Objects": [],
    }
    with patch.object(mock_client, "request", return_value=response_data):
        result = TestEnumerableResourceWithDataNoModel.enumerate_with_query(
            max_results=10
        )
        assert result == response_data


def test_enumerate_with_query_resource_with_data_param(mock_client):
    """Test enumerate_with_query method with _data parameter."""
    response_data = {
        "Success": True,
        "Timestamp": {"Timestamp": "2024-01-01T00:00:00Z"},
        "MaxResults": 1000,
        "IterationsRequired": 0,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 0,
        "RecordsRemaining": 0,
        "Objects": [],
    }
    with patch.object(mock_client, "request", return_value=response_data):
        result = TestEnumerableResourceWithData.enumerate_with_query(
            _data={"max_results": 10}
        )
        assert isinstance(result, EnumerationResultModel)


def test_enumerate_with_query_resource_with_include_data(mock_client):
    """Test enumerate_with_query method with include_data."""
    response_data = {
        "Success": True,
        "Timestamp": {"Timestamp": "2024-01-01T00:00:00Z"},
        "MaxResults": 1000,
        "IterationsRequired": 0,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 0,
        "RecordsRemaining": 0,
        "Objects": [],
    }
    with patch.object(
        mock_client, "request", return_value=response_data
    ) as mock_request:
        TestEnumerableResourceWithData.enumerate_with_query(include_data=True)
        call_kwargs = mock_request.call_args[1]
        assert "json" in call_kwargs
        assert "IncludeData" in str(call_kwargs["json"])


def test_enumerate_with_query_resource_with_include_subordinates(mock_client):
    """Test enumerate_with_query method with include_subordinates."""
    response_data = {
        "Success": True,
        "Timestamp": {"Timestamp": "2024-01-01T00:00:00Z"},
        "MaxResults": 1000,
        "IterationsRequired": 0,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 0,
        "RecordsRemaining": 0,
        "Objects": [],
    }
    with patch.object(
        mock_client, "request", return_value=response_data
    ) as mock_request:
        TestEnumerableResourceWithData.enumerate_with_query(include_subordinates=True)
        call_kwargs = mock_request.call_args[1]
        assert "json" in call_kwargs
        assert "IncludeSubordinates" in str(call_kwargs["json"])
