"""Recursos de pedidos — listado paginado y detalle por ID (Bearer)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from app.server import (
    AuthenticatedOrderBridgeRef,
    get_authenticated_order_bridge,
    mcp,
)
from app.services.order_bridge.orders import get_order_detail, list_orders_page


async def read_orders(
    auth: AuthenticatedOrderBridgeRef,
    *,
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


async def read_order(
    auth: AuthenticatedOrderBridgeRef,
    *,
    order_id: int,
) -> dict[str, Any]:
    return await get_order_detail(
        auth.client,
        bearer_token=auth.bearer_token,
        order_id=order_id,
    )


@mcp.resource(
    uri="apk://orders{?limit,offset,state}",
    name="Pedidos del usuario",
    description=(
        "Listado paginado de pedidos (GET /api/order_bridge/orders, Bearer). "
        "Cada ítem: order_number, status (español), importes; _agent con order_id (uso interno del agente)."
    ),
    mime_type="application/json",
)
async def orders_list_resource(
    limit: int | None = None,
    offset: int | None = None,
    state: str | None = None,
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await read_orders(
        auth,
        limit=limit,
        offset=offset,
        state=state,
    )


@mcp.resource(
    uri="apk://orders/{order_id}",
    name="Pedido",
    description=(
        "Detalle de pedido por ID (Bearer): líneas, importes, dirección y status en español; "
        "_agent con order_id y product_id por línea (no mostrar al usuario final)."
    ),
    mime_type="application/json",
)
async def order_resource(
    order_id: int,
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await read_order(auth, order_id=order_id)
