"""Per-tenant device credentials (opaque token = device_key = Bearer toward order_bridge)."""

from __future__ import annotations

import asyncio
import secrets
from typing import Protocol, runtime_checkable


@runtime_checkable
class TenantCredentialStore(Protocol):
    """In-memory map ``tenant_id -> opaque token`` (also used as ``device_key`` on register)."""

    async def ensure_device_token(self, tenant_id: str) -> str:
        """Return the stable token for this tenant, creating it on first use."""
        ...


class InMemoryTenantCredentialStore:
    """Thread-safe in-process map; lost on process restart."""

    __slots__ = ("_lock", "_by_tenant")

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._by_tenant: dict[str, str] = {}

    async def ensure_device_token(self, tenant_id: str) -> str:
        async with self._lock:
            existing = self._by_tenant.get(tenant_id)
            if existing:
                return existing
            token = secrets.token_urlsafe(32)
            self._by_tenant[tenant_id] = token
            return token


def create_tenant_credential_store() -> InMemoryTenantCredentialStore:
    return InMemoryTenantCredentialStore()
