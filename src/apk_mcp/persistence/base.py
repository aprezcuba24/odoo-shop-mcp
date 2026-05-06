"""Abstract persistence for Tienda Apk ``device_key`` per logical principal."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class DeviceKeyRepository(Protocol):
    """Async key-value store: ``persistence_key`` → API ``device_key`` string.

    Implementations may use SQLite, Postgres, Redis, etc. Callers compute
    ``persistence_key`` via :func:`apk_mcp.session_store.resolve_persistence_key`.
    """

    async def get(self, persistence_key: str) -> str | None:
        """Return stored device_key or ``None``."""
        ...

    async def set(self, persistence_key: str, device_key: str) -> None:
        """Upsert device_key for this principal."""
        ...

    async def delete(self, persistence_key: str) -> None:
        """Remove stored key for this principal."""
        ...

    async def aclose(self) -> None:
        """Release connections (optional; default no-op in concrete classes)."""
        ...
