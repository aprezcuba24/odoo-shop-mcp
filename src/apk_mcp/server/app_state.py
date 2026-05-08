"""Process-wide references set during FastMCP lifespan (HTTP client + API bridge)."""

from __future__ import annotations

from dataclasses import dataclass

from apk_mcp.generated.order_bridge_client import Client
from apk_mcp.utils.bearer_token_store import BearerTokenStore


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
    """Same lifespan ``Client`` plus Bearer token (see ``bearer_authorization``)."""

    client: Client
    bearer_token: str


class AppState:
    __slots__ = ("api", "bearer_token_store")

    def __init__(self) -> None:
        self.api: Client | None = None
        self.bearer_token_store: BearerTokenStore | None = None


app_state = AppState()


def get_apk_api() -> OrderBridgeClientRef:
    api = app_state.api
    if api is None:
        raise RuntimeError("API client not initialized; server lifespan did not start.")
    return OrderBridgeClientRef(api)


async def get_authenticated_order_bridge() -> AuthenticatedOrderBridgeRef:
    api = app_state.api
    if api is None:
        raise RuntimeError("API client not initialized; server lifespan did not start.")
    token_store = app_state.bearer_token_store
    if token_store is None:
        raise RuntimeError("Bearer token store not initialized; server lifespan did not start.")
    bearer_token = await token_store.ensure_token()
    return AuthenticatedOrderBridgeRef(client=api, bearer_token=bearer_token)
