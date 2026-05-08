"""Process-wide references set during FastMCP lifespan (HTTP client + API bridge)."""

from __future__ import annotations

from dataclasses import dataclass

from fastmcp.server.context import Context

from apk_mcp.generated.order_bridge_client import Client
from apk_mcp.utils.exceptions import MissingDeviceKeyError


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
    """Same lifespan ``Client`` plus ``device_key`` for Bearer (see ``bearer_authorization``)."""

    client: Client
    bearer_token: str


class AppState:
    __slots__ = ("api",)

    def __init__(self) -> None:
        self.api: Client | None = None


app_state = AppState()


def get_apk_api() -> OrderBridgeClientRef:
    api = app_state.api
    if api is None:
        raise RuntimeError("API client not initialized; server lifespan did not start.")
    return OrderBridgeClientRef(api)


async def get_authenticated_order_bridge(ctx: Context) -> AuthenticatedOrderBridgeRef:
    api = app_state.api
    if api is None:
        raise RuntimeError("API client not initialized; server lifespan did not start.")
    store = ctx.lifespan_context.get("store")
    if store is None:
        raise RuntimeError("Device key store not initialized; server lifespan did not start.")
    device_key = await store.get(ctx)
    if not device_key:
        raise MissingDeviceKeyError(
            "No device_key in session or store. Call register_device (or set device key) first."
        )
    return AuthenticatedOrderBridgeRef(client=api, bearer_token=device_key)
