"""Shared helpers: HTTP client, session/device key store, typed API errors."""

from .exceptions import (
    ApkApiError,
    ApkMcpError,
    MessageApiError,
    MissingDeviceKeyError,
    NotFoundError,
    UnauthorizedError,
    ValidationApiError,
)
from .http_client import ApkApiClient
from .openapi_detailed import client_helper, message_from_error_body, raise_apk_http
from .session_store import (
    DEVICE_KEY_STATE,
    ContextDeviceKeyStore,
    DeviceKeyStore,
    LayeredDeviceKeyStore,
    RepositoryDeviceKeyStore,
    create_device_key_store,
    resolve_client_id,
    resolve_persistence_key,
)

__all__ = [
    "ApkApiClient",
    "ApkApiError",
    "client_helper",
    "ApkMcpError",
    "ContextDeviceKeyStore",
    "DEVICE_KEY_STATE",
    "DeviceKeyStore",
    "LayeredDeviceKeyStore",
    "MessageApiError",
    "MissingDeviceKeyError",
    "NotFoundError",
    "RepositoryDeviceKeyStore",
    "UnauthorizedError",
    "ValidationApiError",
    "create_device_key_store",
    "message_from_error_body",
    "resolve_client_id",
    "resolve_persistence_key",
    "raise_apk_http",
]
