"""Process-wide references set during FastMCP lifespan (HTTP client + API bridge)."""

from __future__ import annotations

from dataclasses import dataclass

from fastmcp.server.dependencies import get_http_request

from apk_mcp.generated.order_bridge_client import Client
from apk_mcp.utils.tenant_credentials import TenantCredentialStore

from .tenant_resolution import resolve_tenant_id


SHOP_KEY_HEADER = "shop-key"

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
    __slots__ = ("api", "tenant_credential_store")

    def __init__(self) -> None:
        self.api: Client | None = None
        self.tenant_credential_store: TenantCredentialStore | None = None


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
    store = app_state.tenant_credential_store
    if store is None:
        raise RuntimeError("Tenant credential store not initialized; server lifespan did not start.")
    # tenant_id = resolve_tenant_id()
    request = get_http_request()
    bearer_token = request.headers.get(SHOP_KEY_HEADER)
    return AuthenticatedOrderBridgeRef(client=api, bearer_token=bearer_token)


async def get_device_token_for_current_tenant() -> str:
    """Opaque device key / Bearer secret for ``POST /register`` (same value as authenticated calls)."""
    store = app_state.tenant_credential_store
    if store is None:
        raise RuntimeError("Tenant credential store not initialized; server lifespan did not start.")
    tenant_id = resolve_tenant_id()
    return await store.ensure_device_token(tenant_id)
