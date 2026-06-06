"""Recursos de ubicación — municipios y barrios para direcciones."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from app.server import OrderBridgeClientRef, get_apk_api, mcp
from app.services.order_bridge.locations import list_municipalities


async def read_locations_municipalities(api: OrderBridgeClientRef) -> dict[str, Any]:
    return await list_municipalities(api.client)


@mcp.resource(
    uri="apk://locations/municipalities",
    name="Ubicaciones: municipios y barrios",
    description=(
        "Municipios y barrios para crear o actualizar dirección "
        "(GET /api/order_bridge/municipalities, público). "
        "Cada ítem expone name y neighborhoods (solo nombres); "
        "_agent con municipality_id y neighborhood_id — uso interno del agente, no mostrar al usuario."
    ),
    mime_type="application/json",
)
async def municipalities_resource(
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    return await read_locations_municipalities(api)
