"""Extended tests for exceptions.py to improve coverage."""

from sharpai_sdk.enums.api_error_enum import ApiError_Enum
from sharpai_sdk.exceptions import (
    AuthenticationError,
    AuthorizationError,
    BadRequestError,
    ConflictError,
    DeserializationError,
    InactiveError,
    InUseError,
    InvalidRangeError,
    NotEmptyError,
    ResourceNotFoundError,
    ServerError,
    SdkException,
    get_exception_for_error_code,
)


def test_get_exception_for_invalid_error_code():
    """Test get_exception_for_error_code with invalid error code type."""
    result = get_exception_for_error_code("invalid_error")
    assert isinstance(result, SdkException)
    assert "Invalid error code type" in str(result)


def test_get_exception_for_authentication_failed():
    """Test get_exception_for_error_code with authentication_failed."""
    result = get_exception_for_error_code(ApiError_Enum.authentication_failed)
    assert isinstance(result, AuthenticationError)


def test_get_exception_for_authorization_failed():
    """Test get_exception_for_error_code with authorization_failed."""
    result = get_exception_for_error_code(ApiError_Enum.authorization_failed)
    assert isinstance(result, AuthorizationError)


def test_get_exception_for_bad_request():
    """Test get_exception_for_error_code with bad_request."""
    result = get_exception_for_error_code(ApiError_Enum.bad_request)
    assert isinstance(result, BadRequestError)


def test_get_exception_for_not_found():
    """Test get_exception_for_error_code with not_found."""
    result = get_exception_for_error_code(ApiError_Enum.not_found)
    assert isinstance(result, ResourceNotFoundError)


def test_get_exception_for_internal_error():
    """Test get_exception_for_error_code with internal_error."""
    result = get_exception_for_error_code(ApiError_Enum.internal_error)
    assert isinstance(result, ServerError)


def test_get_exception_for_too_large():
    """Test get_exception_for_error_code with too_large."""
    result = get_exception_for_error_code(ApiError_Enum.too_large)
    assert isinstance(result, BadRequestError)


def test_get_exception_for_conflict():
    """Test get_exception_for_error_code with conflict."""
    result = get_exception_for_error_code(ApiError_Enum.conflict)
    assert isinstance(result, ConflictError)


def test_get_exception_for_inactive():
    """Test get_exception_for_error_code with inactive."""
    result = get_exception_for_error_code(ApiError_Enum.inactive)
    assert isinstance(result, InactiveError)


def test_get_exception_for_invalid_range():
    """Test get_exception_for_error_code with invalid_range."""
    result = get_exception_for_error_code(ApiError_Enum.invalid_range)
    assert isinstance(result, InvalidRangeError)


def test_get_exception_for_in_use():
    """Test get_exception_for_error_code with in_use."""
    result = get_exception_for_error_code(ApiError_Enum.in_use)
    assert isinstance(result, InUseError)


def test_get_exception_for_not_empty():
    """Test get_exception_for_error_code with not_empty."""
    result = get_exception_for_error_code(ApiError_Enum.not_empty)
    assert isinstance(result, NotEmptyError)


def test_get_exception_for_deserialization_error():
    """Test get_exception_for_error_code with deserialization_error."""
    result = get_exception_for_error_code(ApiError_Enum.deserialization_error)
    assert isinstance(result, DeserializationError)
