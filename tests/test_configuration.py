import pytest

from sharpai_sdk.configuration import configure, get_client


def test_configure():
    """Test SDK configuration."""
    configure(endpoint="http://localhost:8000", timeout=10, retries=3)
    client = get_client()
    assert client.base_url == "http://localhost:8000"
    assert client.timeout == 10
    assert client.retries == 3


def test_configure_custom_timeout():
    """Test SDK configuration with custom timeout."""
    configure(endpoint="http://localhost:8000", timeout=30, retries=5)
    client = get_client()
    assert client.timeout == 30
    assert client.retries == 5


def test_get_client_before_configure():
    """Test getting client before configuration raises error."""
    # Reset global client
    import sharpai_sdk.configuration as config_module

    config_module._client = None

    with pytest.raises(ValueError, match="SDK is not configured"):
        get_client()

    # Reconfigure for other tests
    configure(endpoint="http://localhost:8000")


def test_configure_multiple_times():
    """Test that configure can be called multiple times."""
    configure(endpoint="http://localhost:8000", timeout=10)
    client1 = get_client()

    configure(endpoint="http://localhost:9000", timeout=20)
    client2 = get_client()

    # After reconfiguration, get_client() should return the new client
    # with updated configuration
    assert client2.base_url == "http://localhost:9000"
    assert client2.timeout == 20
    # The new client should have different configuration than the old one
    assert client1.base_url != client2.base_url
