"""Banners service — promotional banners for the store catalog."""

from __future__ import annotations

from typing import Any

from app.generated.order_bridge_client import Client
from app.generated.order_bridge_client.api.default import order_bridge_banners
from app.generated.order_bridge_client.models.banners_list_response import (
    BannersListResponse,
)
from app.utils.openapi_detailed import client_helper


async def list_banners(client: Client) -> dict[str, Any]:
    return await client_helper(
        order_bridge_banners,
        client,
        success_type=BannersListResponse,
        unexpected_shape_message="Unexpected response shape for banners list",
    )
