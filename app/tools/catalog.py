"""Herramientas de catálogo — consulta de productos y categorías (públicas)."""

from __future__ import annotations

from typing import Any

from mcp.types import ToolAnnotations
from uncalled_for import Depends

from app.server import OrderBridgeClientRef, get_apk_api, mcp
from app.services.order_bridge.catalog_presenters import (
    present_fetch_product,
    present_search_results,
)
from app.services.order_bridge.categories import list_categories
from app.services.order_bridge.products import get_product_detail, list_products_page

_READ_ONLY = ToolAnnotations(readOnlyHint=True, openWorldHint=False)


@mcp.tool(
    name="search",
    description=(
        "Busca productos en el catálogo YY-Mercado (GET /api/order_bridge/products, público). "
        "Usar para consultas del usuario sobre productos, precios o disponibilidad. "
        "Devuelve results con id, title y url (apk://catalog/products/{id}). "
        "Preferir esta tool en ChatGPT; luego fetch(id) para el detalle."
    ),
    annotations=_READ_ONLY,
)
async def search(
    query: str,
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    page = await list_products_page(api.client, search=query or None)
    return present_search_results(page)


@mcp.tool(
    name="fetch",
    description=(
        "Obtiene el detalle de un producto del catálogo por id devuelto por search "
        "(GET /api/order_bridge/products/{product_id}, público). "
        "El id es el string numérico del producto."
    ),
    annotations=_READ_ONLY,
)
async def fetch(
    id: str,
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    product_id = int(id)
    detail = await get_product_detail(api.client, product_id=product_id)
    return present_fetch_product(detail, product_id=product_id)


@mcp.tool(
    name="list_products",
    description=(
        "Lista productos del catálogo (GET /api/order_bridge/products, público). "
        "Admite búsqueda por nombre (search), filtro por categoría (category_id) y paginación "
        "(limit, offset). Cada ítem incluye id, name, list_price, category y uom_name."
    ),
    annotations=_READ_ONLY,
)
async def list_products(
    api: OrderBridgeClientRef = Depends(get_apk_api),
    search: str | None = None,
    category_id: int | None = None,
    limit: int | None = None,
    offset: int | None = None,
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
        "Obtiene el detalle de un producto por ID (GET /api/order_bridge/products/{product_id}, "
        "público): nombre, precio, categoría, código, imágenes y unidad de medida."
    ),
    annotations=_READ_ONLY,
)
async def get_product(
    product_id: int,
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    return await get_product_detail(api.client, product_id=product_id)


@mcp.tool(
    name="list_categories",
    description=(
        "Lista categorías de producto del catálogo (GET /api/order_bridge/categories, público). "
        "Cada ítem incluye id, name y parent_id opcional."
    ),
    annotations=_READ_ONLY,
)
async def list_categories_tool(
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    return await list_categories(api.client)
