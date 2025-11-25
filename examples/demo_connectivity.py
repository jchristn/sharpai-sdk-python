"""
Demo script for validating connectivity to the SharpAI API.
"""

from sharpai_sdk import configure, Connectivity

# Configure the SDK
configure(
    endpoint="http://localhost:8000",
    timeout=30,
    retries=3,
)


def validate_connectivity():
    """Validate connectivity to the SharpAI API."""
    print("Validating connectivity to SharpAI API...")
    is_connected = Connectivity.validate()

    if is_connected:
        print("✓ Successfully connected to SharpAI API")
    else:
        print("✗ Failed to connect to SharpAI API")


validate_connectivity()
