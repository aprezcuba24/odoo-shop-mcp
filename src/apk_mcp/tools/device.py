"""Device tools — register and status (mixed auth)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from apk_mcp.server import (
    AuthenticatedOrderBridgeRef,
    OrderBridgeClientRef,
    get_apk_api,
    get_authenticated_order_bridge,
    mcp,
)
from apk_mcp.services.order_bridge.device import get_device_status, register_device


@mcp.tool(
    name="register_device",
    description=(
        "Register or retrieve a device contact via POST /api/order_bridge/register. "
        "Public endpoint (no Bearer). Provide a stable device_key (e.g. UUID). "
        "Returns partner_id, created flag, and validation status. "
        "A validated:false result means the device still needs approval in the Odoo backend."
    ),
)
async def tool_register_device(
    device_key: str,
    api: OrderBridgeClientRef = Depends(get_apk_api),
    phone: str | None = None,
    device_info: str | None = None,
) -> dict[str, Any]:
    return await register_device(
        api.client,
        device_key=device_key,
        phone=phone,
        device_info=device_info,
    )


@mcp.tool(
    name="get_device_status",
    description=(
        "Get validation status for this device's contact via GET /api/order_bridge/status (Bearer). "
        "Returns partner_id, partner_name, phone and validated flag."
    ),
)
async def tool_get_device_status(
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await get_device_status(auth.client, bearer_token=auth.bearer_token)
