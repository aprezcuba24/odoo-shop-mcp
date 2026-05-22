"""Herramientas de carrito del servidor (clave = dominio + token del shop-key)."""

from __future__ import annotations

from typing import Any

from app.server import mcp
from app.utils.shop_key_codec import resolve_shop_context
from app.services.cart import CartLine, cart_store, lines_payload


def _cart_response(
    lines: list[CartLine],
    *,
    message: str | None = None,
) -> dict[str, Any]:
    line_count, total_qty = (
        (0, 0.0) if not lines else (len(lines), sum(line.qty for line in lines))
    )
    payload: dict[str, Any] = {
        "line_count": line_count,
        "total_qty": total_qty,
        "_agent": {"lines": lines_payload(lines)},
    }
    if message is not None:
        payload["message"] = message
    return payload


@mcp.tool(
    name="add_to_cart",
    description=(
        "Añade o actualiza un producto en el carrito del servidor MCP. "
        "El carrito se identifica con la cabecera HTTP shop-key (dominio del backend + token). "
        "Parámetros: product_id y quantity (> 0). Si el producto ya está en el carrito, suma la cantidad. "
        "Devuelve line_count, total_qty y _agent.lines (product_id, qty) para uso interno del agente."
    ),
)
async def add_to_cart(
    product_id: int,
    quantity: float,
) -> dict[str, Any]:
    key = resolve_shop_context().cart_store_key()
    lines = await cart_store.add_line(
        key,
        product_id=product_id,
        quantity=quantity,
    )
    return _cart_response(lines, message="Producto añadido al carrito.")


@mcp.tool(
    name="get_cart",
    description=(
        "Obtiene el carrito del dispositivo actual (cabecera HTTP shop-key). "
        "Devuelve line_count, total_qty y _agent.lines (product_id, qty)."
    ),
)
async def get_cart() -> dict[str, Any]:
    key = resolve_shop_context().cart_store_key()
    lines = await cart_store.get_lines(key)
    return _cart_response(lines)


@mcp.tool(
    name="clear_cart",
    description=(
        "Vacía el carrito del dispositivo actual (cabecera HTTP shop-key). "
        "Idempotente si el carrito ya estaba vacío."
    ),
)
async def clear_cart() -> dict[str, Any]:
    key = resolve_shop_context().cart_store_key()
    await cart_store.clear(key)
    return _cart_response([], message="Carrito vaciado.")
