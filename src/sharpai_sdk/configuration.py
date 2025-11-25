from .base import BaseClient

# Global client instance
_client = None


def configure(
    endpoint: str,
    timeout: int = 10,
    retries: int = 3,
):
    """
    Configure the SDK with endpoint.
    Note: SharpAI SDK does not require access tokens/keys, tenant GUID, or graph GUID.

    Args:
        endpoint (str): The base URL of the SharpAI API (e.g., "http://localhost:8000").
        timeout (int): Request timeout in seconds. Default is 10.
        retries (int): Number of retry attempts for failed requests. Default is 3.
    """
    global _client
    _client = BaseClient(
        base_url=endpoint,
        timeout=timeout,
        retries=retries,
    )


# Utility function to get the shared client
def get_client():
    """Get the shared client instance."""
    if _client is None:
        raise ValueError("SDK is not configured. Call 'configure' first.")
    return _client
