"""Tool de lectura de perfil — equivalente a Resource apk://session/profile (ChatGPT)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from app.resources.profile import read_session_profile
from app.server import (
    AuthenticatedOrderBridgeRef,
    get_authenticated_order_bridge,
    mcp,
)
from app.tools.tool_resources._common import READ_ONLY


@mcp.tool(
    name="read_session_profile",
    description=(
        "Perfil del contacto del dispositivo (GET /api/order_bridge/profile, Bearer): "
        "nombre, teléfono y dirección configurada (nombres de municipio/barrio, sin IDs). "
        "_agent con contact_id y municipality_id/neighborhood_id — uso interno del agente. "
        "Equivalente al Resource apk://session/profile."
    ),
    annotations=READ_ONLY,
)
async def read_session_profile_tool(
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await read_session_profile(auth)
