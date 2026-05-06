"""In-process repository (tests, local dev without SQLite)."""

from __future__ import annotations


class InMemoryDeviceKeyRepository:
    def __init__(self) -> None:
        self._rows: dict[str, str] = {}

    async def get(self, persistence_key: str) -> str | None:
        v = self._rows.get(persistence_key)
        return v if v else None

    async def set(self, persistence_key: str, device_key: str) -> None:
        self._rows[persistence_key] = device_key

    async def delete(self, persistence_key: str) -> None:
        self._rows.pop(persistence_key, None)

    async def aclose(self) -> None:
        return None
