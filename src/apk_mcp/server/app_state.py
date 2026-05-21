"""Process-wide references set during FastMCP lifespan (HTTP client + API bridge)."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass

import httpx

from apk_mcp.generated.order_bridge_client import Client
from apk_mcp.utils.shop_key_codec import resolve_shop_context


@dataclass(frozen=True, slots=True)
class OrderBridgeClientRef:
    """Holds the generated OpenAPI ``Client`` without ``__aenter__``.

    FastMCP dependency resolution treats types with ``__aenter__`` as async context
    managers; the generated ``Client`` would call ``httpx.AsyncClient.__aenter__``
    again on an already-open client from the server lifespan, raising
    ``RuntimeError: Cannot open a client instance more than once``.
    """

    client: Client


@dataclass(frozen=True, slots=True)
class AuthenticatedOrderBridgeRef:
    """Per-request ``Client`` for the decoded backend plus Bearer token."""

    client: Client
    bearer_token: str


class ClientRegistry:
    """Lazy pool of order_bridge clients keyed by backend base URL."""

    __slots__ = ("_clients", "_lock", "_timeout")

    def __init__(self, *, timeout: float) -> None:
        self._timeout = timeout
        self._lock = asyncio.Lock()
        self._clients: dict[str, tuple[Client, httpx.AsyncClient]] = {}

    async def get_client(self, base_url: str) -> Client:
        key = base_url.rstrip("/")
        async with self._lock:
            entry = self._clients.get(key)
            if entry is not None:
                return entry[0]

            http = httpx.AsyncClient(base_url=key, timeout=self._timeout)
            ob_client = Client(
                base_url=key,
                raise_on_unexpected_status=False,
                timeout=self._timeout,
            )
            ob_client.set_async_httpx_client(http)
            self._clients[key] = (ob_client, http)
            return ob_client

    async def close_all(self) -> None:
        async with self._lock:
            entries = list(self._clients.values())
            self._clients.clear()

        for _ob_client, http in entries:
            await http.aclose()


class AppState:
    __slots__ = ("registry",)

    def __init__(self) -> None:
        self.registry: ClientRegistry | None = None


app_state = AppState()


async def get_apk_api() -> OrderBridgeClientRef:
    registry = app_state.registry
    if registry is None:
        raise RuntimeError("API client not initialized; server lifespan did not start.")
    ctx = resolve_shop_context()
    client = await registry.get_client(ctx.base_url)
    return OrderBridgeClientRef(client)


async def get_authenticated_order_bridge() -> AuthenticatedOrderBridgeRef:
    registry = app_state.registry
    if registry is None:
        raise RuntimeError("API client not initialized; server lifespan did not start.")
    ctx = resolve_shop_context()
    client = await registry.get_client(ctx.base_url)
    return AuthenticatedOrderBridgeRef(client=client, bearer_token=ctx.bearer_token)
