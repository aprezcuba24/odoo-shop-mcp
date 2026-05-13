"""Herramientas de catálogo — listado y detalle de productos (público)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from apk_mcp.server import OrderBridgeClientRef, get_apk_api, mcp
from apk_mcp.services.order_bridge.products import get_product_detail, list_products_page


@mcp.tool(
    name="list_products",
    description=(
        "Lista productos del catálogo Tienda Apk (GET /api/order_bridge/products). "
        "Endpoint público (sin Bearer). Paginación (limit por defecto 80, máx. 200), "
        "filtro opcional category_id y búsqueda parcial por nombre sin distinguir mayúsculas."
    ),
)
async def list_products(
    api: OrderBridgeClientRef = Depends(get_apk_api),
    limit: int | None = None,
    offset: int | None = None,
    category_id: int | None = None,
    search: str | None = None,
) -> dict[str, Any]:
    return await list_products_page(
        api.client,
        limit=limit,
        offset=offset,
        category_id=category_id,
        search=search,
    )


@mcp.tool(
    name="get_product",
    description=(
        "Obtiene el detalle completo de un producto (GET /api/order_bridge/products/{product_id}). "
        "Endpoint público (sin Bearer). Devuelve nombre, precio, categoría, código de barras, "
        "imágenes y unidad de medida."
    ),
)
async def get_product(
    product_id: int,
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    return await get_product_detail(api.client, product_id=product_id)
