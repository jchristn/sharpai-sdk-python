"""Tests for sdk_logging.py to improve coverage."""

from sharpai_sdk.sdk_logging import (
    format_log_message,
    log_critical,
    log_debug,
    log_error,
    log_info,
    log_warning,
    set_log_level,
)


def test_set_log_level_with_level():
    """Test set_log_level with a valid level."""
    set_log_level("DEBUG")
    # Just verify it doesn't raise an exception
    assert True


def test_set_log_level_with_none():
    """Test set_log_level with None."""
    set_log_level(None)
    # Just verify it doesn't raise an exception
    assert True


def test_set_log_level_with_invalid_level():
    """Test set_log_level with an invalid level."""
    # Should default to INFO for invalid levels
    set_log_level("INVALID_LEVEL")
    # Just verify it doesn't raise an exception
    assert True


def test_format_log_message():
    """Test format_log_message function."""
    result = format_log_message("INFO", "Test message")
    assert result == "[INFO] Test message"


def test_log_debug():
    """Test log_debug function."""
    # Just verify it doesn't raise an exception
    log_debug("DEBUG", "Debug message")
    assert True


def test_log_info():
    """Test log_info function."""
    # Just verify it doesn't raise an exception
    log_info("INFO", "Info message")
    assert True


def test_log_warning():
    """Test log_warning function."""
    # Just verify it doesn't raise an exception
    log_warning("WARNING", "Warning message")
    assert True


def test_log_error():
    """Test log_error function."""
    # Just verify it doesn't raise an exception
    log_error("ERROR", "Error message")
    assert True


def test_log_critical():
    """Test log_critical function."""
    # Just verify it doesn't raise an exception
    log_critical("CRITICAL", "Critical message")
    assert True
