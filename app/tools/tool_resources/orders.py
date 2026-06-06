"""Tools de lectura de pedidos — equivalente a Resources apk://orders/... (ChatGPT)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from app.resources.orders import read_order, read_orders
from app.server import (
    AuthenticatedOrderBridgeRef,
    get_authenticated_order_bridge,
    mcp,
)
from app.tools.tool_resources._common import READ_ONLY


@mcp.tool(
    name="read_orders",
    description=(
        "Listado paginado de pedidos (GET /api/order_bridge/orders, Bearer). "
        "Cada ítem: order_number, status (español), importes; _agent con order_id (uso interno del agente). "
        "Equivalente al Resource apk://orders."
    ),
    annotations=READ_ONLY,
)
async def read_orders_tool(
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
    limit: int | None = None,
    offset: int | None = None,
    state: str | None = None,
) -> dict[str, Any]:
    return await read_orders(
        auth,
        limit=limit,
        offset=offset,
        state=state,
    )


@mcp.tool(
    name="read_order",
    description=(
        "Detalle de pedido por ID (GET /api/order_bridge/orders/{order_id}, Bearer): "
        "líneas, importes, dirección y status en español; "
        "_agent con order_id y product_id por línea (no mostrar al usuario final). "
        "Equivalente al Resource apk://orders/{order_id}."
    ),
    annotations=READ_ONLY,
)
async def read_order_tool(
    order_id: int,
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await read_order(auth, order_id=order_id)
