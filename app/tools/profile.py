"""Herramientas de perfil — actualización parcial de nombre y dirección (Bearer)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from app.server import (
    AuthenticatedOrderBridgeRef,
    get_authenticated_order_bridge,
    mcp,
)
from app.services.order_bridge.profile import update_profile


@mcp.tool(
    name="update_profile",
    description=(
        "Actualiza parcialmente el perfil del contacto (PATCH /api/order_bridge/profile, Bearer). "
        "Puedes cambiar name y/o campos de address (street, state, municipality_id, neighborhood_id). "
        "Para resolver municipality_id y neighborhood_id, llama antes a read_locations_municipalities. "
        "El teléfono no se modifica con esta tool. Devuelve el perfil actualizado."
    ),
)
async def update_profile_tool(
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
    name: str | None = None,
    street: str | None = None,
    state: str | None = None,
    municipality_id: int | None = None,
    neighborhood_id: int | None = None,
) -> dict[str, Any]:
    return await update_profile(
        auth.client,
        bearer_token=auth.bearer_token,
        name=name,
        street=street,
        state=state,
        municipality_id=municipality_id,
        neighborhood_id=neighborhood_id,
    )
