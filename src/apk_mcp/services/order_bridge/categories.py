"""Product categories service."""

from __future__ import annotations

from typing import Any

from apk_mcp.generated.order_bridge_client import Client
from apk_mcp.generated.order_bridge_client.api.default import order_bridge_categories
from apk_mcp.generated.order_bridge_client.models.categories_list_response import (
    CategoriesListResponse,
)
from apk_mcp.utils.openapi_detailed import client_helper


async def list_categories(client: Client) -> dict[str, Any]:
    return await client_helper(
        order_bridge_categories,
        client,
        success_type=CategoriesListResponse,
        unexpected_shape_message="Unexpected response shape for categories list",
    )
