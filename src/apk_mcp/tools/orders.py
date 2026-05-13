"""Order tools — list, detail, create, cancel (all Bearer)."""

from __future__ import annotations

import json
from typing import Any

from uncalled_for import Depends

from apk_mcp.server import (
    AuthenticatedOrderBridgeRef,
    get_authenticated_order_bridge,
    mcp,
)
from apk_mcp.services.order_bridge.orders import (
    cancel_order,
    create_order,
    get_order_detail,
    list_orders_page,
)


@mcp.tool(
    name="list_orders",
    description=(
        "List sale orders for this device's contact via GET /api/order_bridge/orders (Bearer). "
        "Supports pagination (limit, offset) and optional state filter "
        "(e.g. 'draft', 'sale', 'cancel')."
    ),
)
async def list_orders(
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
    limit: int | None = None,
    offset: int | None = None,
    state: str | None = None,
) -> dict[str, Any]:
    return await list_orders_page(
        auth.client,
        bearer_token=auth.bearer_token,
        limit=limit,
        offset=offset,
        state=state,
    )


@mcp.tool(
    name="get_order",
    description=(
        "Get full detail of a sale order (lines, amounts, delivery status) via "
        "GET /api/order_bridge/orders/{order_id} (Bearer)."
    ),
)
async def get_order(
    order_id: int,
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await get_order_detail(
        auth.client,
        bearer_token=auth.bearer_token,
        order_id=order_id,
    )


@mcp.tool(
    name="create_order",
    description=(
        "Create a new sale order via POST /api/order_bridge/orders (Bearer). "
        "Pass lines as a JSON array string: '[{\"product_id\": 1, \"qty\": 2.0}, ...]'. "
        "Returns the created order with id, name, state and store_state. "
        "Raises an error with product details when any line exceeds available stock."
    ),
)
async def tool_create_order(
    lines_json: str,
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    lines = json.loads(lines_json)
    return await create_order(
        auth.client,
        bearer_token=auth.bearer_token,
        lines=lines,
    )


@mcp.tool(
    name="cancel_order",
    description=(
        "Cancel a draft sale order via POST /api/order_bridge/orders/{order_id}/cancel (Bearer). "
        "Only orders in 'draft' state can be cancelled. Returns updated id and state."
    ),
)
async def tool_cancel_order(
    order_id: int,
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await cancel_order(
        auth.client,
        bearer_token=auth.bearer_token,
        order_id=order_id,
    )
