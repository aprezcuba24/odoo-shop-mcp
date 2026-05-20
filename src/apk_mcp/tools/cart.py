"""Herramientas de carrito en memoria (clave = cabecera shop-key vía resolve_shop_key)."""

from __future__ import annotations

from typing import Any

from apk_mcp.server import mcp
from apk_mcp.server.app_state import resolve_shop_key
from apk_mcp.services.cart import CartLine, cart_store


def _lines_payload(lines: list[CartLine]) -> list[dict[str, float | int]]:
    return [{"product_id": line.product_id, "qty": line.qty} for line in lines]


def _cart_response(
    client_key: str,
    lines: list[CartLine],
    *,
    message: str | None = None,
) -> dict[str, Any]:
    line_count, total_qty = (
        (0, 0.0) if not lines else (len(lines), sum(line.qty for line in lines))
    )
    payload: dict[str, Any] = {
        "client_key": client_key,
        "lines": _lines_payload(lines),
        "line_count": line_count,
        "total_qty": total_qty,
    }
    if message is not None:
        payload["message"] = message
    return payload


@mcp.tool(
    name="add_to_cart",
    description=(
        "Añade o actualiza un producto en el carrito en memoria del servidor MCP. "
        "El carrito se identifica con la cabecera HTTP shop-key del cliente (Bearer del dispositivo). "
        "Parámetros: product_id y quantity (> 0). Si el producto ya está en el carrito, suma la cantidad. "
        "Devuelve el carrito completo actualizado."
    ),
)
async def add_to_cart(
    product_id: int,
    quantity: float,
) -> dict[str, Any]:
    client_key = resolve_shop_key()
    lines = await cart_store.add_line(
        client_key,
        product_id=product_id,
        quantity=quantity,
    )
    return _cart_response(
        client_key,
        lines,
        message="Producto añadido al carrito.",
    )


@mcp.tool(
    name="get_cart",
    description=(
        "Obtiene el carrito en memoria del dispositivo actual (cabecera HTTP shop-key). "
        "Devuelve client_key (valor de shop-key), líneas (product_id, qty), line_count y total_qty."
    ),
)
async def get_cart() -> dict[str, Any]:
    client_key = resolve_shop_key()
    lines = await cart_store.get_lines(client_key)
    return _cart_response(client_key, lines)


@mcp.tool(
    name="clear_cart",
    description=(
        "Vacía el carrito en memoria del dispositivo actual (cabecera HTTP shop-key). "
        "Idempotente si el carrito ya estaba vacío."
    ),
)
async def clear_cart() -> dict[str, Any]:
    client_key = resolve_shop_key()
    await cart_store.clear(client_key)
    return _cart_response(
        client_key,
        [],
        message="Carrito vaciado.",
    )
