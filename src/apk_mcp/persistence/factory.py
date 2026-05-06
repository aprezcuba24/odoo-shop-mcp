"""Construct a :class:`~apk_mcp.persistence.base.DeviceKeyRepository` from settings."""

from __future__ import annotations

from apk_mcp.config import DeviceKeyPersistenceBackend, Settings
from apk_mcp.persistence.base import DeviceKeyRepository
from apk_mcp.persistence.memory_backend import InMemoryDeviceKeyRepository
from apk_mcp.persistence.sqlite_backend import SqliteDeviceKeyRepository


def create_device_key_repository(settings: Settings) -> DeviceKeyRepository:
    backend: DeviceKeyPersistenceBackend = settings.device_key_persistence_backend
    if backend == "memory":
        return InMemoryDeviceKeyRepository()
    return SqliteDeviceKeyRepository(settings.device_key_db_path)
