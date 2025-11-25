"""Extended tests for base.py to improve coverage."""

from unittest.mock import Mock, patch

import httpx
import pytest

from sharpai_sdk.base import BaseClient
from sharpai_sdk.enums.api_error_enum import ApiError_Enum
from sharpai_sdk.exceptions import SdkException


@pytest.fixture
def base_url():
    return "http://test-api.com"


@pytest.fixture
def base_client(base_url):
    """Create a base client for testing."""
    with patch("httpx.Client"):
        return BaseClient(base_url=base_url, timeout=10, retries=3)


def test_handle_response_json_decode_error(base_client, monkeypatch):
    """Test handling response with JSON decode error."""
    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.content = b"Not valid JSON"
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = ValueError("Invalid JSON")

    result = base_client._handle_response(mock_response)
    assert result == b"Not valid JSON"


def test_handle_error_response_json(base_client, monkeypatch):
    """Test handling error response with JSON content."""
    error_response_data = {
        "Error": ApiError_Enum.bad_request,
        "Description": "Bad request error",
    }
    mock_response = Mock(spec=httpx.Response)
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = error_response_data

    mock_error = Mock(spec=httpx.HTTPStatusError)
    mock_error.response = mock_response

    with pytest.raises(SdkException):
        base_client._handle_error_response(mock_error)


def test_handle_error_response_non_json(base_client, monkeypatch):
    """Test handling error response with non-JSON content."""
    mock_response = Mock(spec=httpx.Response)
    mock_response.headers = {"Content-Type": "text/plain"}
    mock_response.content = b"Plain text error"

    mock_error = Mock(spec=httpx.HTTPStatusError)
    mock_error.response = mock_response

    with pytest.raises(SdkException, match="Server responded with non-JSON content"):
        base_client._handle_error_response(mock_error)


def test_request_with_http_status_error_json(base_client, monkeypatch):
    """Test request handling HTTPStatusError with JSON error response."""
    error_response_data = {
        "Error": ApiError_Enum.not_found,
        "Description": "Resource not found",
    }
    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 404
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = error_response_data

    mock_error = httpx.HTTPStatusError(
        "404 Not Found", request=Mock(spec=httpx.Request), response=mock_response
    )

    with patch.object(base_client.client, "request", side_effect=mock_error):
        with pytest.raises(SdkException):
            base_client.request("GET", "/test")


def test_request_with_http_status_error_value_error(base_client, monkeypatch):
    """Test request handling HTTPStatusError that raises ValueError."""
    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 500
    mock_response.headers = {"Content-Type": "application/json"}
    # Make json() raise ValueError to trigger the ValueError handler
    mock_response.json.side_effect = ValueError("Invalid JSON")

    mock_error = httpx.HTTPStatusError(
        "500 Internal Server Error",
        request=Mock(spec=httpx.Request),
        response=mock_response,
    )

    with patch.object(base_client.client, "request", side_effect=mock_error):
        with pytest.raises(SdkException, match="Unexpected error"):
            base_client.request("GET", "/test")


def test_request_with_http_status_error_no_content_type(base_client, monkeypatch):
    """Test request handling HTTPStatusError without Content-Type header."""
    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 500
    mock_response.headers = {}  # No Content-Type header
    mock_response.content = b"Error message"

    mock_error = httpx.HTTPStatusError(
        "500 Internal Server Error",
        request=Mock(spec=httpx.Request),
        response=mock_response,
    )

    with patch.object(base_client.client, "request", side_effect=mock_error):
        with pytest.raises(
            SdkException, match="Server responded with non-JSON content"
        ):
            base_client.request("GET", "/test")
