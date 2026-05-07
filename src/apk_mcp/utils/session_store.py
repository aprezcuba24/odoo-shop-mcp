"""device_key: session cache (FastMCP Context) + pluggable persistence (repository)."""

from __future__ import annotations

from typing import Literal, Protocol, runtime_checkable

from fastmcp.server.context import Context

from apk_mcp.config import Settings
from apk_mcp.persistence.base import DeviceKeyRepository
from apk_mcp.persistence.factory import create_device_key_repository

DEVICE_KEY_STATE = "device_key"


def resolve_persistence_key(ctx: Context) -> str:
    """Stable logical principal for storing ``device_key`` across MCP sessions.

    Order (first match wins):

    1. **OAuth** (p. ej. conector ChatGPT con login): mismo criterio que FastMCP
       ``get_task_scope`` — ``{client_id}|{sub}`` si el token trae ``sub``,
       si no ``{client_id}``. Prefijo ``oauth:`` para no colisionar con otros ids.
    2. **``Context.client_id``** — identificador que expone el runtime MCP (puede
       variar entre chats según el cliente).
    3. **Cabecera HTTP** ``X-Client-Id`` — útil detrás de un proxy que fije el usuario.
    4. **``default``** — un solo bucket compartido en toda la instancia (single-tenant).

    Con OAuth y ``sub`` estable por usuario, un **nuevo chat** suele reutilizar el
    mismo ``persistence_key`` y por tanto el ``device_key`` guardado en el repositorio.
    Sin OAuth, ``default`` también sobrevive a nuevos chats en un solo usuario.
    """
    try:
        from fastmcp.server.dependencies import get_access_token

        token = get_access_token()
        if token is not None:
            sub = (token.claims or {}).get("sub") if token.claims else None
            if sub:
                return f"oauth:{token.client_id}|{sub}"
            return f"oauth:{token.client_id}"
    except Exception:
        pass

    cid = ctx.client_id
    if cid:
        return str(cid)

    try:
        from fastmcp.server.dependencies import get_http_request

        req = get_http_request()
        if req is not None:
            raw = req.headers.get("x-client-id") or req.headers.get("X-Client-Id")
            if raw:
                return raw.strip()
    except RuntimeError:
        pass

    return "default"


# Backwards compatibility for callers importing the old name
def resolve_client_id(ctx: Context) -> str:
    """Deprecated alias for :func:`resolve_persistence_key`."""
    return resolve_persistence_key(ctx)


@runtime_checkable
class DeviceKeyStore(Protocol):
    async def get(self, ctx: Context) -> str | None: ...
    async def set(self, ctx: Context, device_key: str) -> None: ...
    async def clear(self, ctx: Context) -> None: ...


class ContextDeviceKeyStore:
    """Session-scoped cache via FastMCP ``Context``."""

    async def get(self, ctx: Context) -> str | None:
        val = await ctx.get_state(DEVICE_KEY_STATE)
        return val if isinstance(val, str) and val else None

    async def set(self, ctx: Context, device_key: str) -> None:
        await ctx.set_state(DEVICE_KEY_STATE, device_key)

    async def clear(self, ctx: Context) -> None:
        await ctx.set_state(DEVICE_KEY_STATE, None)


class RepositoryDeviceKeyStore:
    """Persist ``device_key`` via a :class:`~apk_mcp.persistence.DeviceKeyRepository`."""

    def __init__(self, repository: DeviceKeyRepository) -> None:
        self.repository = repository

    async def get(self, ctx: Context) -> str | None:
        key = resolve_persistence_key(ctx)
        return await self.repository.get(key)

    async def set(self, ctx: Context, device_key: str) -> None:
        key = resolve_persistence_key(ctx)
        await self.repository.set(key, device_key)

    async def clear(self, ctx: Context) -> None:
        key = resolve_persistence_key(ctx)
        await self.repository.delete(key)


class LayeredDeviceKeyStore:
    """Read-through Context cache + write-through to a repository."""

    def __init__(
        self,
        context_store: ContextDeviceKeyStore,
        repository_store: RepositoryDeviceKeyStore,
    ) -> None:
        self._ctx = context_store
        self._backing = repository_store

    @property
    def repository(self) -> DeviceKeyRepository:
        """Underlying persistence (for lifecycle ``aclose`` and custom backends)."""
        return self._backing.repository

    async def get(self, ctx: Context) -> str | None:
        cached = await self._ctx.get(ctx)
        if cached:
            return cached
        persisted = await self._backing.get(ctx)
        if persisted:
            await self._ctx.set(ctx, persisted)
        return persisted

    async def set(self, ctx: Context, device_key: str) -> None:
        await self._ctx.set(ctx, device_key)
        await self._backing.set(ctx, device_key)

    async def clear(self, ctx: Context) -> None:
        await self._ctx.clear(ctx)
        await self._backing.clear(ctx)


def create_device_key_store(settings: Settings) -> DeviceKeyStore:
    mode: Literal["context", "sqlite", "layered"] = settings.device_key_store_mode
    if mode == "context":
        return ContextDeviceKeyStore()
    repo = create_device_key_repository(settings)
    repo_store = RepositoryDeviceKeyStore(repo)
    if mode == "sqlite":
        return repo_store
    return LayeredDeviceKeyStore(ContextDeviceKeyStore(), repo_store)
