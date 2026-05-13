"""Catalog tools — product list and detail (public)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from apk_mcp.server import OrderBridgeClientRef, get_apk_api, mcp
from apk_mcp.services.order_bridge.products import get_product_detail, list_products_page


@mcp.tool(
    name="list_products",
    description=(
        "List products from the Tienda Apk catalog via GET /api/order_bridge/products. "
        "Public endpoint (no Bearer). Supports pagination (limit default 80, max 200), "
        "optional category_id filter, and case-insensitive partial name search."
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


@mcp.tool(
    name="get_product",
    description=(
        "Get full detail for a single product via GET /api/order_bridge/products/{product_id}. "
        "Public endpoint (no Bearer). Returns name, price, category, barcode, images and unit of measure."
    ),
)
async def get_product(
    product_id: int,
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    return await get_product_detail(api.client, product_id=product_id)
