"""Herramientas de dispositivo — registro y estado (autenticación mixta)."""

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
        "Registra u obtiene el contacto de un dispositivo (POST /api/order_bridge/register). "
        "Endpoint público (sin Bearer). Usa un device_key estable (p. ej. UUID). "
        "Devuelve partner_id, indicador created y estado de validación. "
        "Si validated es false, el dispositivo sigue pendiente de aprobación en Odoo."
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
        "Obtiene el estado de validación del contacto de este dispositivo "
        "(GET /api/order_bridge/status, Bearer). Devuelve partner_id, partner_name, phone y validated."
    ),
)
async def tool_get_device_status(
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await get_device_status(auth.client, bearer_token=auth.bearer_token)
