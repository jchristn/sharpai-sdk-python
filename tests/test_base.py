from unittest.mock import Mock, patch

import httpx
import pytest

from sharpai_sdk.base import BaseClient
from sharpai_sdk.exceptions import SdkException


@pytest.fixture
def base_url():
    return "http://test-api.com"


@pytest.fixture
def base_client(base_url):
    """Create a base client for testing."""
    with patch("httpx.Client"):
        return BaseClient(base_url=base_url, timeout=10, retries=3)


@pytest.fixture
def mock_httpx_client(monkeypatch):
    """Create a mock httpx client that properly handles requests."""

    def mock_request(*args, **kwargs):
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.content = b'{"data": "test"}'
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status.return_value = None
        return mock_response

    mock_client = Mock(spec=httpx.Client)
    mock_client.request = mock_request
    mock_client.close.return_value = None

    def mock_client_constructor(*args, **kwargs):
        return mock_client

    monkeypatch.setattr(httpx, "Client", mock_client_constructor)
    return mock_client


def test_client_initialization(base_url):
    """Test client initialization with different parameters."""
    with patch("httpx.Client"):
        # Test default values
        client = BaseClient(base_url=base_url)
        assert client.base_url == base_url
        assert client.timeout == 10
        assert client.retries == 3
        # Test custom values
        custom_client = BaseClient(base_url=base_url, timeout=20, retries=5)
        assert custom_client.base_url == base_url
        assert custom_client.timeout == 20
        assert custom_client.retries == 5


def test_successful_request(base_client, monkeypatch):
    """Test successful request with JSON response."""
    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.content = b'{"data": "test"}'
    mock_response.json.return_value = {"data": "test"}
    mock_response.raise_for_status.return_value = None

    with patch.object(base_client.client, "request", return_value=mock_response):
        response = base_client.request("GET", "/test")
        assert response == {"data": "test"}


def test_empty_response(base_client, monkeypatch):
    """Test successful request with empty response."""
    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.content = b""
    mock_response.raise_for_status.return_value = None

    with patch.object(base_client.client, "request", return_value=mock_response):
        response = base_client.request("GET", "/test")
        assert response is None


def test_request_with_headers(base_client, monkeypatch):
    """Test request with headers."""
    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.content = b'{"data": "test"}'
    mock_response.json.return_value = {"data": "test"}
    mock_response.raise_for_status.return_value = None

    mock_request = Mock(return_value=mock_response)
    with patch.object(base_client.client, "request", mock_request):
        headers = {"Custom-Header": "value"}
        base_client.request("GET", "/test", headers=headers)

        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args[1]
        assert "Content-Type" in call_kwargs["headers"]
        assert call_kwargs["headers"]["Custom-Header"] == "value"


def test_client_close(base_client):
    """Test client close method."""
    mock_close = Mock()
    base_client.client.close = mock_close
    base_client.close()
    mock_close.assert_called_once()


def test_request_with_retry_success(base_client, monkeypatch):
    """Test request that succeeds after retries."""
    success_response = Mock(spec=httpx.Response)
    success_response.status_code = 200
    success_response.content = b'{"data": "success"}'
    success_response.json.return_value = {"data": "success"}
    success_response.raise_for_status.return_value = None

    mock_request = Mock(
        side_effect=[httpx.RequestError("First attempt failed"), success_response]
    )

    with patch.object(base_client.client, "request", mock_request):
        response = base_client.request("GET", "/test")
        assert response == {"data": "success"}
        assert mock_request.call_count == 2


def test_request_max_retries_exhausted(base_client, monkeypatch):
    """Test request fails after max retries with RequestError."""
    with patch.object(
        base_client.client,
        "request",
        side_effect=httpx.RequestError("Connection failed"),
    ):
        with pytest.raises(SdkException) as exc_info:
            base_client.request("GET", "/test")
        assert f"Request failed after {base_client.retries} attempts" in str(
            exc_info.value
        )


def test_request_with_json_payload(base_client, monkeypatch):
    """Test request with JSON payload."""
    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.content = b'{"data": "test"}'
    mock_response.json.return_value = {"data": "test"}
    mock_response.raise_for_status.return_value = None
    mock_request = Mock(return_value=mock_response)
    with patch.object(base_client.client, "request", mock_request):
        payload = {"key": "value", "nested": {"data": [1, 2, 3]}}
        base_client.request("POST", "/test", json=payload)
        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args[1]
        assert call_kwargs["json"] == payload
