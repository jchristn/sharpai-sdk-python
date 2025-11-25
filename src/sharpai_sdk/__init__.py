# ruff: noqa

import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "sharpai-sdk-python"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from .base import BaseClient
from .configuration import configure, get_client
from .enums.enumeration_order_enum import EnumerationOrder_Enum
from .enums.operator_enum import Opertator_Enum
from .exceptions import (
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
    TimeoutError,
)
from .models.expression import ExprModel
from .resources import Connectivity, Ollama, OpenAI

__all__ = [
    "__version__",
    "BaseClient",
    "configure",
    "get_client",
    "EnumerationOrder_Enum",
    "Opertator_Enum",
    "ExprModel",
    "Ollama",
    "OpenAI",
    "Connectivity",
    "SdkException",
    "AuthenticationError",
    "AuthorizationError",
    "BadRequestError",
    "ConflictError",
    "DeserializationError",
    "InactiveError",
    "InUseError",
    "InvalidRangeError",
    "NotEmptyError",
    "ResourceNotFoundError",
    "ServerError",
    "TimeoutError",
]
