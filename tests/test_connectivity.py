from unittest.mock import Mock, patch

import pytest

from sharpai_sdk.configuration import configure
from sharpai_sdk.resources.connectivity import Connectivity


@pytest.fixture
def mock_client():
    """Create a mock client for testing."""
    configure(endpoint="http://localhost:8000")
    client = Mock()
    with patch("sharpai_sdk.resources.connectivity.get_client", return_value=client):
        yield client


def test_validate_success(mock_client):
    """Test successful connectivity validation."""
    mock_client.request.return_value = None

    result = Connectivity.validate()
    assert result is True
    mock_client.request.assert_called_once_with("HEAD", "")


def test_validate_failure(mock_client):
    """Test failed connectivity validation."""
    mock_client.request.side_effect = Exception("Connection failed")

    result = Connectivity.validate()
    assert result is False
    mock_client.request.assert_called_once_with("HEAD", "")
