"""Recurso de perfil del contacto — nombre, teléfono y dirección (Bearer)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from app.server import (
    AuthenticatedOrderBridgeRef,
    get_authenticated_order_bridge,
    mcp,
)
from app.services.order_bridge.profile import get_profile


@mcp.resource(
    uri="apk://session/profile",
    name="Perfil del usuario",
    description=(
        "Perfil del contacto del dispositivo (GET /api/order_bridge/profile, Bearer): "
        "nombre, teléfono y dirección configurada (nombres de municipio/barrio, sin IDs). "
        "_agent con contact_id y municipality_id/neighborhood_id — uso interno del agente."
    ),
    mime_type="application/json",
)
async def profile_resource(
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await get_profile(auth.client, bearer_token=auth.bearer_token)
