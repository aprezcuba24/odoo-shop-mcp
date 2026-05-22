"""Device registration and status service."""

from __future__ import annotations

from typing import Any

from app.generated.order_bridge_client import Client
from app.generated.order_bridge_client.api.default import (
    order_bridge_register,
    order_bridge_status,
)
from app.generated.order_bridge_client.models.register_body import RegisterBody
from app.generated.order_bridge_client.models.register_ok_response import (
    RegisterOkResponse,
)
from app.generated.order_bridge_client.models.status_response import StatusResponse
from app.generated.order_bridge_client.types import UNSET
from app.utils.openapi_detailed import bearer_authorization, client_helper, unset_str


async def register_device(
    client: Client,
    *,
    device_key: str,
    phone: str | None = None,
    device_info: str | None = None,
) -> dict[str, Any]:
    body = RegisterBody(
        device_key=device_key,
        phone=unset_str(phone),
        device_info=unset_str(device_info),
    )
    return await client_helper(
        order_bridge_register,
        client,
        success_type=RegisterOkResponse,
        unexpected_shape_message="Unexpected response shape for register device",
        body=body,
    )


async def get_device_status(
    client: Client,
    *,
    bearer_token: str,
) -> dict[str, Any]:
    async with bearer_authorization(client, bearer_token):
        return await client_helper(
            order_bridge_status,
            client,
            success_type=StatusResponse,
            unexpected_shape_message="Unexpected response shape for device status",
        )
