"""Herramientas de perfil — lectura, actualización parcial (PATCH) y reemplazo total (PUT). Todas Bearer."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from apk_mcp.server import (
    AuthenticatedOrderBridgeRef,
    get_authenticated_order_bridge,
    mcp,
)
from apk_mcp.services.order_bridge.profile import (
    get_profile,
    replace_profile,
    update_profile,
)


@mcp.tool(
    name="get_profile",
    description=(
        "Obtiene el perfil del contacto de este dispositivo (GET /api/order_bridge/profile, Bearer). "
        "Devuelve id, nombre, email, teléfono y dirección de entrega."
    ),
)
async def tool_get_profile(
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await get_profile(auth.client, bearer_token=auth.bearer_token)


@mcp.tool(
    name="update_profile",
    description=(
        "Actualiza parcialmente el perfil del contacto (PATCH /api/order_bridge/profile, Bearer). "
        "Todos los parámetros son opcionales; envía solo los campos a cambiar. "
        "Los campos de dirección (street, municipality_id, neighborhood_id, state) se fusionan con "
        "la dirección guardada: tras el merge deben quedar municipio y barrio definidos."
    ),
)
async def tool_update_profile(
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
    name: str | None = None,
    street: str | None = None,
    municipality_id: int | None = None,
    neighborhood_id: int | None = None,
    state: str | None = None,
) -> dict[str, Any]:
    return await update_profile(
        auth.client,
        bearer_token=auth.bearer_token,
        name=name,
        street=street,
        municipality_id=municipality_id,
        neighborhood_id=neighborhood_id,
        state=state,
    )


@mcp.tool(
    name="replace_profile",
    description=(
        "Reemplaza por completo el perfil del contacto (PUT /api/order_bridge/profile, Bearer). "
        "Campos obligatorios: name, street, municipality_id, neighborhood_id, state. "
        "Usa el recurso yy-shop://locations/municipalities para resolver IDs de municipio y barrio."
    ),
)
async def tool_replace_profile(
    name: str,
    street: str,
    municipality_id: int,
    neighborhood_id: int,
    state: str,
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await replace_profile(
        auth.client,
        bearer_token=auth.bearer_token,
        name=name,
        street=street,
        municipality_id=municipality_id,
        neighborhood_id=neighborhood_id,
        state=state,
    )
