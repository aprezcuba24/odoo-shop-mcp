"""Tools de lectura de catálogo — equivalente a Resources apk://catalog/... (ChatGPT)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from app.resources.catalog import (
    read_catalog_categories,
    read_catalog_product,
    read_catalog_products,
)
from app.server import OrderBridgeClientRef, get_apk_api, mcp
from app.tools.tool_resources._common import READ_ONLY


@mcp.tool(
    name="read_catalog_categories",
    description=(
        "Lista completa de categorías de producto del catálogo "
        "(GET /api/order_bridge/categories, público). "
        "Equivalente al Resource apk://catalog/categories."
    ),
    annotations=READ_ONLY,
)
async def read_catalog_categories_tool(
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    return await read_catalog_categories(api)


@mcp.tool(
    name="read_catalog_products",
    description=(
        "Lista productos del catálogo (GET /api/order_bridge/products, público). "
        "Admite búsqueda por nombre (search), filtro por categoría (category_id) y paginación "
        "(limit, offset). Equivalente al Resource apk://catalog/products."
    ),
    annotations=READ_ONLY,
)
async def read_catalog_products_tool(
    api: OrderBridgeClientRef = Depends(get_apk_api),
    limit: int | None = None,
    offset: int | None = None,
    category_id: int | None = None,
    search: str | None = None,
) -> dict[str, Any]:
    return await read_catalog_products(
        api,
        limit=limit,
        offset=offset,
        category_id=category_id,
        search=search,
    )


@mcp.tool(
    name="read_catalog_product",
    description=(
        "Detalle completo de un producto por ID (GET /api/order_bridge/products/{product_id}, "
        "público): nombre, precio, categoría, código, imágenes y unidad de medida. "
        "Equivalente al Resource apk://catalog/products/{product_id}."
    ),
    annotations=READ_ONLY,
)
async def read_catalog_product_tool(
    product_id: int,
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    return await read_catalog_product(api, product_id=product_id)
