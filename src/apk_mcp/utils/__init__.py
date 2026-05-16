"""Shared helpers: HTTP client, in-memory bearer token, typed API errors."""

from .bearer_token_store import (
    BearerTokenStore,
    InMemoryBearerTokenStore,
    create_bearer_token_store,
)
from .exceptions import (
    ApkApiError,
    ApkMcpError,
    InsufficientStockError,
    MessageApiError,
    MissingTenantError,
    NotFoundError,
    UnauthorizedError,
    ValidationApiError,
)
from .http_client import ApkApiClient
from .openapi_detailed import client_helper, message_from_error_body, raise_apk_http
from .tenant_credentials import (
    InMemoryTenantCredentialStore,
    TenantCredentialStore,
    create_tenant_credential_store,
)

__all__ = [
    "ApkApiClient",
    "ApkApiError",
    "ApkMcpError",
    "BearerTokenStore",
    "InMemoryBearerTokenStore",
    "InMemoryTenantCredentialStore",
    "InsufficientStockError",
    "MessageApiError",
    "MissingTenantError",
    "NotFoundError",
    "TenantCredentialStore",
    "UnauthorizedError",
    "ValidationApiError",
    "client_helper",
    "create_bearer_token_store",
    "create_tenant_credential_store",
    "message_from_error_body",
    "raise_apk_http",
]
