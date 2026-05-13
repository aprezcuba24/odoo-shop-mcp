"""Store resources — general shop settings (public)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from apk_mcp.server import OrderBridgeClientRef, get_apk_api, mcp
from apk_mcp.services.order_bridge.store import get_settings


@mcp.resource(
    uri="apk://store/settings",
    name="Tienda: configuración",
    description="Datos generales de la tienda (teléfono, etc.). Endpoint público.",
    mime_type="application/json",
)
async def settings_resource(
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    return await get_settings(api.client)
