"""Herramientas de pedidos — listado, detalle, creación y cancelación (todas Bearer)."""

from __future__ import annotations

import json
from typing import Any

from uncalled_for import Depends

from app.server import (
    AuthenticatedOrderBridgeRef,
    get_authenticated_order_bridge,
    mcp,
)
from app.utils.shop_key_codec import resolve_shop_context
from app.services.cart import cart_store, lines_payload
from app.services.order_bridge.orders import (
    cancel_order,
    create_order,
    get_last_order,
)
from app.services.order_bridge.order_presenters import present_insufficient_stock
from app.utils.exceptions import InsufficientStockError


@mcp.tool(
    name="get_last_order",
    description=(
        "Obtiene el detalle del pedido más reciente del contacto de este dispositivo "
        "(GET /api/order_bridge/orders?limit=1 y GET /api/order_bridge/orders/{order_id}, Bearer). "
        "Incluye líneas, importes y status en español; _agent con order_id y product_id por línea. "
        "Falla si el usuario no tiene pedidos."
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
    name="create_order",
    description=(
        "Crea un pedido de venta nuevo (POST /api/order_bridge/orders, Bearer). "
        "Pasa las líneas como cadena JSON: '[{\"product_id\": 1, \"qty\": 2.0}, ...]'. "
        "Devuelve order_number, status (español) y _agent.order_id. "
        "Si falta stock, ok=false, error=insufficient_stock, products (product_id, available_qty) "
        "y _agent.lines_submitted; no lanza excepción."
    ),
)
async def tool_create_order(
    lines_json: str,
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    lines = json.loads(lines_json)
    try:
        return await create_order(
            auth.client,
            bearer_token=auth.bearer_token,
            lines=lines,
        )
    except InsufficientStockError as exc:
        return present_insufficient_stock(exc.body or {}, lines_submitted=lines)


@mcp.tool(
    name="checkout_cart",
    description=(
        "Confirma el pedido con el carrito del dispositivo actual "
        "(POST /api/order_bridge/orders, Bearer). Lee las líneas del carrito asociado "
        "a la cabecera HTTP shop-key (add_to_cart / get_cart). Si el pedido se crea "
        "correctamente, vacía el carrito. Devuelve ok=true con order (order_number, status). "
        "Si el carrito está vacío, ok=false y error=empty_cart. "
        "Si falta stock, ok=false, error=insufficient_stock; products con product_id y available_qty; "
        "cantidad pedida en _agent.lines_submitted. Ajustar con add_to_cart y reintentar."
    ),
)
async def checkout_cart(
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    key = resolve_shop_context().cart_store_key()
    cart_lines = await cart_store.get_lines(key)
    lines_submitted = lines_payload(cart_lines)

    if not lines_submitted:
        return {
            "ok": False,
            "error": "empty_cart",
            "message": (
                "El carrito está vacío. Añade productos con add_to_cart antes de confirmar."
            ),
            "lines": [],
        }

    try:
        order = await create_order(
            auth.client,
            bearer_token=auth.bearer_token,
            lines=lines_submitted,
        )
    except InsufficientStockError as exc:
        body = exc.body or {}
        return present_insufficient_stock(body, lines_submitted=lines_submitted)

    await cart_store.clear(key)
    return {
        "ok": True,
        "order": order,
        "cart_cleared": True,
    }


@mcp.tool(
    name="cancel_order",
    description=(
        "Cancela un pedido en borrador (POST /api/order_bridge/orders/{order_id}/cancel, Bearer). "
        "Solo se pueden cancelar pedidos en borrador. Devuelve status Cancelado y _agent.order_id."
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
