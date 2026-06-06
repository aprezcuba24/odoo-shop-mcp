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


@mcp.resource(
    uri="apk://orders",
    name="Pedidos del usuario (listado)",
    description=(
        "Listado de pedidos del contacto sin filtros (Bearer). "
        "Para paginación o filtro por estado usar el template con parámetros."
    ),
    mime_type="application/json",
)
async def orders_resource(
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await list_orders_page(
        auth.client,
        bearer_token=auth.bearer_token,
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
        "Detalle de pedido por ID (Bearer): líneas, importes, dirección y status en español; "
        "_agent con order_id y product_id por línea (no mostrar al usuario final)."
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
