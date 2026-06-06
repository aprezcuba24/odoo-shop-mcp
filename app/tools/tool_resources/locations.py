"""Tool de lectura de ubicaciones — equivalente a Resource apk://locations/... (ChatGPT)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from app.resources.locations import read_locations_municipalities
from app.server import OrderBridgeClientRef, get_apk_api, mcp
from app.tools.tool_resources._common import READ_ONLY


@mcp.tool(
    name="read_locations_municipalities",
    description=(
        "Municipios y barrios para crear o actualizar dirección "
        "(GET /api/order_bridge/municipalities, público). "
        "Cada ítem expone name y neighborhoods (solo nombres); "
        "_agent con municipality_id y neighborhood_id — uso interno del agente, no mostrar al usuario. "
        "Equivalente al Resource apk://locations/municipalities."
    ),
    annotations=READ_ONLY,
)
async def read_locations_municipalities_tool(
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    return await read_locations_municipalities(api)
