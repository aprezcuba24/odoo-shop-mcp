"""Product catalog via generated openapi-python-client."""

from __future__ import annotations

from typing import Any

from apk_mcp.generated.order_bridge_client import Client
from apk_mcp.generated.order_bridge_client.api.default import order_bridge_products
from apk_mcp.generated.order_bridge_client.models.products_page_response import (
    ProductsPageResponse,
)
from apk_mcp.utils.openapi_detailed import client_helper, unset_int, unset_str


async def list_products_page(
    client: Client,
    *,
    limit: int | None = None,
    offset: int | None = None,
    category_id: int | None = None,
    search: str | None = None,
) -> dict[str, Any]:
    return await client_helper(
        order_bridge_products,
        client,
        success_type=ProductsPageResponse,
        unexpected_shape_message="Unexpected response shape for products list",
        limit=unset_int(limit),
        offset=unset_int(offset),
        category_id=unset_int(category_id),
        search=unset_str(search),
    )
