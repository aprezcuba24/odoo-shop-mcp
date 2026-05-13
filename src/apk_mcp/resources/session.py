"""Session resources — device status and contact profile (Bearer)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from apk_mcp.server import (
    AuthenticatedOrderBridgeRef,
    get_authenticated_order_bridge,
    mcp,
)
from apk_mcp.services.order_bridge.device import get_device_status
from apk_mcp.services.order_bridge.profile import get_profile


@mcp.resource(
    uri="apk://session/status",
    name="Sesión: estado del dispositivo",
    description=(
        "Estado de validación del dispositivo (Bearer). "
        "Devuelve partner_id, partner_name, phone y validated. "
        "validated:false indica que el dispositivo está pendiente de aprobación en Odoo."
    ),
    mime_type="application/json",
)
async def session_status_resource(
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await get_device_status(auth.client, bearer_token=auth.bearer_token)


@mcp.resource(
    uri="apk://session/profile",
    name="Sesión: perfil del contacto",
    description=(
        "Perfil completo del contacto del dispositivo (Bearer): "
        "id, nombre, email, teléfono y dirección de entrega."
    ),
    mime_type="application/json",
)
async def session_profile_resource(
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await get_profile(auth.client, bearer_token=auth.bearer_token)
