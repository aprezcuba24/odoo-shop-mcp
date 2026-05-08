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
        "Bridge to Tienda Apk order_bridge REST API under /api/order_bridge/. "
        "Use list_products for the public product catalog. "
        "Use list_orders for the authenticated orders list (Bearer token auto-created in memory for this server process). "
        "Authenticated routes use that same in-process Bearer token."
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
