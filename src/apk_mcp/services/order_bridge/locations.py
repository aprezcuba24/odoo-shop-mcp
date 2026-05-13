"""Location nomenclators service — municipalities with neighborhoods."""

from __future__ import annotations

from typing import Any

from apk_mcp.generated.order_bridge_client import Client
from apk_mcp.generated.order_bridge_client.api.default import order_bridge_municipalities
from apk_mcp.generated.order_bridge_client.models.municipalities_list_response import (
    MunicipalitiesListResponse,
)
from apk_mcp.utils.openapi_detailed import client_helper


async def list_municipalities(client: Client) -> dict[str, Any]:
    return await client_helper(
        order_bridge_municipalities,
        client,
        success_type=MunicipalitiesListResponse,
        unexpected_shape_message="Unexpected response shape for municipalities",
    )
