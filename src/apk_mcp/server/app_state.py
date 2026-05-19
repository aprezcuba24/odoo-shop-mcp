"""Process-wide references set during FastMCP lifespan (HTTP client + API bridge)."""

from __future__ import annotations

from dataclasses import dataclass

from fastmcp.server.dependencies import get_http_request

from apk_mcp.generated.order_bridge_client import Client
from apk_mcp.utils.exceptions import MissingShopKeyError

SHOP_KEY_HEADER = "shop-key"


def resolve_shop_key() -> str:
    """Read shop-key header from the current HTTP request (passthrough value)."""
    try:
        request = get_http_request()
    except RuntimeError as exc:
        raise MissingShopKeyError(
            "No HTTP request context; cannot resolve shop-key. "
            "Use Streamable HTTP with the shop-key header."
        ) from exc

    raw = request.headers.get(SHOP_KEY_HEADER)
    if raw:
        return raw

    raise MissingShopKeyError(f"Missing required HTTP header {SHOP_KEY_HEADER!r}.")


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
    __slots__ = ("api",)

    def __init__(self) -> None:
        self.api: Client | None = None


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
    return AuthenticatedOrderBridgeRef(client=api, bearer_token=resolve_shop_key())
