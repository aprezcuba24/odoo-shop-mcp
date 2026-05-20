"""User profile service — get, partial update (PATCH), full replace (PUT)."""

from __future__ import annotations

from typing import Any

from apk_mcp.generated.order_bridge_client import Client
from apk_mcp.generated.order_bridge_client.api.default import (
    order_bridge_profile_get,
    order_bridge_profile_patch,
    order_bridge_profile_put,
)
from apk_mcp.generated.order_bridge_client.models.address_full import AddressFull
from apk_mcp.generated.order_bridge_client.models.address_patch import AddressPatch
from apk_mcp.generated.order_bridge_client.models.profile_patch_body import (
    ProfilePatchBody,
)
from apk_mcp.generated.order_bridge_client.models.profile_put_body import ProfilePutBody
from apk_mcp.generated.order_bridge_client.models.profile_response import ProfileResponse
from apk_mcp.services.order_bridge.profile_presenters import present_profile
from apk_mcp.utils.openapi_detailed import bearer_authorization, client_helper, unset_str


async def get_profile(
    client: Client,
    *,
    bearer_token: str,
) -> dict[str, Any]:
    async with bearer_authorization(client, bearer_token):
        raw = await client_helper(
            order_bridge_profile_get,
            client,
            success_type=ProfileResponse,
            unexpected_shape_message="Unexpected response shape for profile get",
        )
    return present_profile(raw)


async def update_profile(
    client: Client,
    *,
    bearer_token: str,
    name: str | None = None,
    street: str | None = None,
    municipality_id: int | None = None,
    neighborhood_id: int | None = None,
    state: str | None = None,
) -> dict[str, Any]:
    address: AddressPatch | None = None
    if any(v is not None for v in (street, municipality_id, neighborhood_id, state)):
        address = AddressPatch(
            street=street,
            municipality_id=municipality_id,
            neighborhood_id=neighborhood_id,
            state=state,
        )
    body = ProfilePatchBody(name=unset_str(name), address=address)
    async with bearer_authorization(client, bearer_token):
        raw = await client_helper(
            order_bridge_profile_patch,
            client,
            success_type=ProfileResponse,
            unexpected_shape_message="Unexpected response shape for profile patch",
            body=body,
        )
    return present_profile(raw)


async def replace_profile(
    client: Client,
    *,
    bearer_token: str,
    name: str,
    street: str,
    municipality_id: int,
    neighborhood_id: int,
    state: str,
) -> dict[str, Any]:
    body = ProfilePutBody(
        name=name,
        address=AddressFull(
            street=street,
            municipality_id=municipality_id,
            neighborhood_id=neighborhood_id,
            state=state,
        ),
    )
    async with bearer_authorization(client, bearer_token):
        return await client_helper(
            order_bridge_profile_put,
            client,
            success_type=ProfileResponse,
            unexpected_shape_message="Unexpected response shape for profile put",
            body=body,
        )
