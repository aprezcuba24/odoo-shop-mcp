"""Shared helpers: HTTP client, in-memory bearer token, typed API errors."""

from .bearer_token_store import (
    BearerTokenStore,
    InMemoryBearerTokenStore,
    create_bearer_token_store,
)
from .exceptions import (
    AmbiguousShopKeyError,
    ApkApiError,
    ApkMcpError,
    InsufficientStockError,
    MessageApiError,
    MissingShopKeyError,
    NotFoundError,
    UnauthorizedError,
    ValidationApiError,
)
from .http_client import ApkApiClient
from .openapi_detailed import client_helper, message_from_error_body, raise_apk_http

__all__ = [
    "AmbiguousShopKeyError",
    "ApkApiClient",
    "ApkApiError",
    "ApkMcpError",
    "BearerTokenStore",
    "InMemoryBearerTokenStore",
    "InsufficientStockError",
    "MessageApiError",
    "MissingShopKeyError",
    "NotFoundError",
    "UnauthorizedError",
    "ValidationApiError",
    "client_helper",
    "create_bearer_token_store",
    "message_from_error_body",
    "raise_apk_http",
]
