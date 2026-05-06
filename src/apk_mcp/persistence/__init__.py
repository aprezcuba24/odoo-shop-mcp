"""Pluggable persistence for ``device_key`` (SQLite today; swap repository implementation later)."""

from apk_mcp.config import DeviceKeyPersistenceBackend
from apk_mcp.persistence.base import DeviceKeyRepository
from apk_mcp.persistence.factory import create_device_key_repository
from apk_mcp.persistence.memory_backend import InMemoryDeviceKeyRepository
from apk_mcp.persistence.sqlite_backend import SqliteDeviceKeyRepository

__all__ = [
    "DeviceKeyPersistenceBackend",
    "DeviceKeyRepository",
    "InMemoryDeviceKeyRepository",
    "SqliteDeviceKeyRepository",
    "create_device_key_repository",
]
