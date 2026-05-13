"""Catalog resources — categories, banners, and individual product detail."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from apk_mcp.server import OrderBridgeClientRef, get_apk_api, mcp
from apk_mcp.services.order_bridge.banners import list_banners
from apk_mcp.services.order_bridge.categories import list_categories
from apk_mcp.services.order_bridge.products import get_product_detail


@mcp.resource(
    uri="apk://catalog/categories",
    name="Catálogo: categorías",
    description="Lista completa de categorías de producto del catálogo (pública).",
    mime_type="application/json",
)
async def categories_resource(
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    return await list_categories(api.client)


@mcp.resource(
    uri="apk://catalog/banners",
    name="Catálogo: banners",
    description="Banners publicitarios activos del catálogo (público).",
    mime_type="application/json",
)
async def banners_resource(
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    return await list_banners(api.client)


@mcp.resource(
    uri="apk://catalog/products/{product_id}",
    name="Catálogo: producto",
    description="Detalle completo de un producto por ID (público): nombre, precio, categoría, código, imágenes y unidad de medida.",
    mime_type="application/json",
)
async def product_resource(
    product_id: int,
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    return await get_product_detail(api.client, product_id=product_id)
