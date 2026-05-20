"""Recursos de pedidos — listado paginado y detalle por ID (Bearer)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from apk_mcp.server import (
    AuthenticatedOrderBridgeRef,
    get_authenticated_order_bridge,
    mcp,
)
from apk_mcp.services.order_bridge.orders import get_order_detail, list_orders_page


@mcp.resource(
    uri="apk://orders{?limit,offset,state}",
    name="Pedidos del usuario",
    description=(
        "Listado paginado de pedidos de venta del contacto de este dispositivo "
        "(GET /api/order_bridge/orders, Bearer). Parámetros opcionales: limit, offset "
        "y filtro por state (p. ej. 'draft', 'sale', 'cancel')."
    ),
    mime_type="application/json",
)
async def orders_list_resource(
    limit: int | None = None,
    offset: int | None = None,
    state: str | None = None,
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await list_orders_page(
        auth.client,
        bearer_token=auth.bearer_token,
        limit=limit,
        offset=offset,
        state=state,
    )


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
