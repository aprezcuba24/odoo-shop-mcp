"""FastMCP server: Streamable HTTP + REST bridge lifespan."""

from __future__ import annotations

import httpx
from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan

from apk_mcp.config import get_settings
from apk_mcp.generated.order_bridge_client import Client
from apk_mcp.utils import create_bearer_token_store
from .app_state import app_state


@lifespan
async def app_lifespan(server: FastMCP):
    settings = get_settings()
    bearer_token_store = create_bearer_token_store()
    base = settings.apk_api_base_url.rstrip("/")
    async with httpx.AsyncClient(
        base_url=base,
        timeout=settings.apk_api_timeout,
    ) as http:
        ob_client = Client(
            base_url=base,
            raise_on_unexpected_status=False,
            timeout=settings.apk_api_timeout,
        )
        ob_client.set_async_httpx_client(http)
        app_state.api = ob_client
        app_state.bearer_token_store = bearer_token_store
        try:
            yield {"settings": settings, "bearer_token_store": bearer_token_store}
        finally:
            app_state.api = None
            app_state.bearer_token_store = None


mcp = FastMCP(
    name="apk-mcp",
    instructions=(
        "Bridge to Tienda Apk order_bridge REST API (/api/order_bridge/). "
        "A single Bearer token is auto-generated per server process and reused for all authenticated calls.\n\n"
        "TOOLS — call these to act:\n"
        "  Catalog (public): list_products, get_product\n"
        "  Device (public): register_device, get_device_status\n"
        "  Orders (Bearer): list_orders, get_order, create_order, cancel_order\n"
        "  Profile (Bearer): get_profile, update_profile, replace_profile\n"
        "  Push (Bearer): register_push_token, update_push_topics\n\n"
        "RESOURCES — attach or read for context:\n"
        "  apk://catalog/categories   — product categories list\n"
        "  apk://catalog/banners      — promotional banners\n"
        "  apk://catalog/products/{product_id} — single product detail\n"
        "  apk://store/settings       — shop phone and general config\n"
        "  apk://locations/municipalities — municipalities + neighborhoods (for address IDs)\n"
        "  apk://session/status       — device validation status (Bearer)\n"
        "  apk://session/profile      — contact profile (Bearer)\n"
        "  apk://orders/{order_id}    — single order detail (Bearer)\n\n"
        "PROMPTS — use these for multi-step workflows:\n"
        "  find_products(query, category?, limit?) — search with category resolution\n"
        "  place_order(items_text) — natural-language cart → create_order with stock handling\n"
        "  track_order(order_id) — formatted order status and lines\n"
        "  reorder_last() — repeat most recent order with confirmation\n"
        "  update_my_address(street, state, municipality_name, neighborhood_name)\n"
        "  onboard_device(device_key, phone?) — register + validate device"
    ),
    lifespan=app_lifespan,
)


def run() -> None:
    settings = get_settings()
    mcp.run(
        transport="streamable-http",
        host=settings.mcp_host,
        port=settings.mcp_port,
        path=settings.mcp_path,
    )
