"""Recursos de ubicación — municipios con barrios (nomencladores públicos)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from apk_mcp.server import OrderBridgeClientRef, get_apk_api, mcp
from apk_mcp.services.order_bridge.locations import list_municipalities


@mcp.resource(
    uri="yy-shop://locations/municipalities",
    name="Nomencladores: municipios y barrios",
    description=(
        "Lista completa de municipios con sus barrios (nomencladores de Tienda Apk). "
        "Usar para resolver nombres de municipio/barrio a IDs antes de actualizar una dirección. "
        "Endpoint público."
    ),
    mime_type="application/json",
)
async def municipalities_resource(
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    return await list_municipalities(api.client)
