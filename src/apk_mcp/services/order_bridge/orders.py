"""Orders listing via generated openapi-python-client."""

from __future__ import annotations

from typing import Any

from apk_mcp.generated.order_bridge_client import Client
from apk_mcp.generated.order_bridge_client.api.default import order_bridge_orders_list
from apk_mcp.generated.order_bridge_client.models.orders_page_response import (
    OrdersPageResponse,
)
from apk_mcp.utils.openapi_detailed import (
    bearer_authorization,
    client_helper,
    unset_int,
    unset_str,
)


async def list_orders_page(
    client: Client,
    *,
    bearer_token: str,
    limit: int | None = None,
    offset: int | None = None,
    state: str | None = None,
) -> dict[str, Any]:
    async with bearer_authorization(client, bearer_token):
        return await client_helper(
            order_bridge_orders_list,
            client,
            success_type=OrdersPageResponse,
            unexpected_shape_message="Unexpected response shape for orders list",
            limit=unset_int(limit),
            offset=unset_int(offset),
            state=unset_str(state),
        )
