"""Herramientas de pedidos — listado, detalle, creación y cancelación (todas Bearer)."""

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
    get_last_order,
    get_order_detail,
    list_orders_page,
)


@mcp.tool(
    name="list_orders",
    description=(
        "Lista pedidos de venta del contacto de este dispositivo (GET /api/order_bridge/orders, Bearer). "
        "Admite paginación (limit, offset) y filtro opcional por estado "
        "(p. ej. 'draft', 'sale', 'cancel')."
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
    name="get_last_order",
    description=(
        "Obtiene el detalle del pedido más reciente del contacto de este dispositivo "
        "(GET /api/order_bridge/orders?limit=1 y GET /api/order_bridge/orders/{order_id}, Bearer). "
        "Incluye líneas, importes y estado. Falla si el usuario no tiene pedidos."
    ),
)
async def get_last_order_tool(
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await get_last_order(
        auth.client,
        bearer_token=auth.bearer_token,
    )


@mcp.tool(
    name="get_order",
    description=(
        "Obtiene el detalle completo de un pedido de venta (líneas, importes, estado de entrega) "
        "vía GET /api/order_bridge/orders/{order_id} (Bearer)."
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
        "Crea un pedido de venta nuevo (POST /api/order_bridge/orders, Bearer). "
        "Pasa las líneas como cadena JSON: '[{\"product_id\": 1, \"qty\": 2.0}, ...]'. "
        "Devuelve el pedido creado con id, name, state y store_state. "
        "Si alguna línea supera el stock disponible, devuelve error con detalle de productos."
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
        "Cancela un pedido en borrador (POST /api/order_bridge/orders/{order_id}/cancel, Bearer). "
        "Solo se pueden cancelar pedidos en estado 'draft'. Devuelve id y state actualizados."
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
