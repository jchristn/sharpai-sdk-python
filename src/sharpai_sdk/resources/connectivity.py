from ..configuration import get_client


class Connectivity:
    """
    Connectivity validation resource class.
    Provides methods for validating API connectivity.
    """

    @classmethod
    def validate(cls) -> bool:
        """
        Validate connectivity to the API.

        Returns:
            bool: True if the API is reachable, False otherwise.
        """
        client = get_client()
        try:
            client.request("HEAD", "")
            return True
        except Exception:
            return False
