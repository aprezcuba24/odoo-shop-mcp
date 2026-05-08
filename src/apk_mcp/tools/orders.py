"""Order tools (authenticated listing)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from apk_mcp.server import (
    AuthenticatedOrderBridgeRef,
    get_authenticated_order_bridge,
    mcp,
)
from apk_mcp.services.order_bridge.orders import list_orders_page


@mcp.tool(
    name="list_orders",
    description=(
        "List orders for the device contact via GET /api/order_bridge/orders. "
        "Uses the in-process Bearer token (auto-created on first use for this server run). "
        "Supports pagination (limit, offset) and optional state filter."
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
