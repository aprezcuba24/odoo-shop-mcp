"""Profile tools — get, partial update (PATCH), full replace (PUT). All Bearer."""

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
        "Get the contact profile for this device via GET /api/order_bridge/profile (Bearer). "
        "Returns id, name, email, phone and delivery address."
    ),
)
async def tool_get_profile(
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await get_profile(auth.client, bearer_token=auth.bearer_token)


@mcp.tool(
    name="update_profile",
    description=(
        "Partially update the contact profile via PATCH /api/order_bridge/profile (Bearer). "
        "All parameters are optional; provide only the fields to change. "
        "Address fields (street, municipality_id, neighborhood_id, state) are merged with "
        "the saved address — municipality and neighborhood must both be set after the merge."
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
        "Fully replace the contact profile via PUT /api/order_bridge/profile (Bearer). "
        "All fields required: name, street, municipality_id, neighborhood_id, state. "
        "Use list_municipalities / get the apk://locations/municipalities resource to resolve IDs."
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
