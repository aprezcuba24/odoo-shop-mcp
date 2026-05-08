"""FastMCP server: Streamable HTTP + REST bridge lifespan."""

from __future__ import annotations

import httpx
from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan

from apk_mcp.config import get_settings
from apk_mcp.generated.order_bridge_client import Client
from apk_mcp.utils import create_device_key_store
from .app_state import app_state


@lifespan
async def app_lifespan(server: FastMCP):
    settings = get_settings()
    store = create_device_key_store(settings)
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
        try:
            yield {"settings": settings, "store": store}
        finally:
            app_state.api = None
            backend = getattr(store, "repository", None)
            if backend is not None:
                await backend.aclose()


mcp = FastMCP(
    name="apk-mcp",
    instructions=(
        "Bridge to Tienda Apk order_bridge REST API under /api/order_bridge/. "
        "Use list_products for the public product catalog. "
        "Use list_orders for the authenticated orders list (requires stored device_key). "
        "Authenticated routes require a device_key (Bearer); store modes: context, sqlite, layered."
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
