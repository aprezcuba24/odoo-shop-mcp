"""In-process singleton Bearer token for Tienda Apk API calls."""

from __future__ import annotations

import asyncio
import secrets
from typing import Protocol, runtime_checkable


@runtime_checkable
class BearerTokenStore(Protocol):
    async def ensure_token(self) -> str: ...


class InMemoryBearerTokenStore:
    """Single opaque token per process; generated on first ``ensure_token``."""

    __slots__ = ("_lock", "_token")

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._token: str | None = None

    async def ensure_token(self) -> str:
        async with self._lock:
            if self._token:
                return self._token
            self._token = secrets.token_urlsafe(32)
            return self._token


def create_bearer_token_store() -> InMemoryBearerTokenStore:
    return InMemoryBearerTokenStore()
