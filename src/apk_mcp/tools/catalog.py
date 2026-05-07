"""Catalog tools (public product listing)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from apk_mcp.server import OrderBridgeClientRef, get_apk_api, mcp
from apk_mcp.services.order_bridge.products import list_products_page


@mcp.tool(
    name="list_products",
    description=(
        "List products from the Tienda Apk catalog via GET /api/order_bridge/products. "
        "This endpoint is public (no device_key). Supports pagination (limit default 80, "
        "max 200), optional category_id, and case-insensitive partial name search."
    ),
)
async def list_products(
    api: OrderBridgeClientRef = Depends(get_apk_api),
    limit: int | None = None,
    offset: int | None = None,
    category_id: int | None = None,
    search: str | None = None,
) -> dict[str, Any]:
    return await list_products_page(
        api.client,
        limit=limit,
        offset=offset,
        category_id=category_id,
        search=search,
    )
