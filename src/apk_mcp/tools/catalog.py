"""Catalog tools (public product listing)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from apk_mcp.http_client import ApkApiClient
from apk_mcp.models.catalog import ListProductsParams, ProductsPageResponse
from apk_mcp.server import get_apk_api, mcp


@mcp.tool(
    name="list_products",
    description=(
        "List products from the Tienda Apk catalog via GET /api/order_bridge/products. "
        "This endpoint is public (no device_key). Supports pagination (limit default 80, "
        "max 200), optional category_id, and case-insensitive partial name search."
    ),
)
async def list_products(
    api: ApkApiClient = Depends(get_apk_api),
    params: ListProductsParams | None = None,
) -> dict[str, Any]:
    p = params or ListProductsParams()
    query = p.model_dump(mode="json", exclude_none=True)
    raw = await api.get_json("/api/order_bridge/products", params=query or None)
    page = ProductsPageResponse.model_validate(raw)
    return page.model_dump(mode="json")
