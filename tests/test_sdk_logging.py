"""Tests for sdk_logging.py to improve coverage."""

import logging
import tempfile
from pathlib import Path


from sharpai_sdk.sdk_logging import (
    add_file_logging,
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


def test_add_file_logging():
    """Test add_file_logging function."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
        log_file_path = f.name

    try:
        handler = add_file_logging(log_file_path, "DEBUG")
        assert handler is not None
        assert isinstance(handler, logging.FileHandler)
        assert handler.level == logging.DEBUG
    finally:
        # Clean up
        Path(log_file_path).unlink(missing_ok=True)


def test_add_file_logging_with_none_level():
    """Test add_file_logging with None level."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
        log_file_path = f.name

    try:
        handler = add_file_logging(log_file_path, None)
        assert handler is not None
    finally:
        Path(log_file_path).unlink(missing_ok=True)


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
