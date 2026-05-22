"""Store settings service — general shop configuration."""

from __future__ import annotations

from typing import Any

from app.generated.order_bridge_client import Client
from app.generated.order_bridge_client.api.default import order_bridge_settings
from app.generated.order_bridge_client.models.general_settings_response import (
    GeneralSettingsResponse,
)
from app.utils.openapi_detailed import client_helper


async def get_settings(client: Client) -> dict[str, Any]:
    return await client_helper(
        order_bridge_settings,
        client,
        success_type=GeneralSettingsResponse,
        unexpected_shape_message="Unexpected response shape for store settings",
    )
