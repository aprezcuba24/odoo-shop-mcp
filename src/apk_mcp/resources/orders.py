"""Order resources — single order detail by ID (Bearer, templated URI)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from apk_mcp.server import (
    AuthenticatedOrderBridgeRef,
    get_authenticated_order_bridge,
    mcp,
)
from apk_mcp.services.order_bridge.orders import get_order_detail


@mcp.resource(
    uri="apk://orders/{order_id}",
    name="Pedido",
    description=(
        "Detalle completo de un pedido de venta por ID (Bearer): "
        "líneas, importes, dirección de entrega, estado de entrega y store_state."
    ),
    mime_type="application/json",
)
async def order_resource(
    order_id: int,
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await get_order_detail(
        auth.client,
        bearer_token=auth.bearer_token,
        order_id=order_id,
    )
