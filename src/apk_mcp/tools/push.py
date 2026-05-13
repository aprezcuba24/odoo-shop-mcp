"""Herramientas de notificaciones push — registro de token FCM y suscripciones a temas (Bearer)."""

from __future__ import annotations

from typing import Any

from uncalled_for import Depends

from apk_mcp.server import (
    AuthenticatedOrderBridgeRef,
    get_authenticated_order_bridge,
    mcp,
)
from apk_mcp.services.order_bridge.push import register_push_token, update_push_topics


@mcp.tool(
    name="register_push_token",
    description=(
        "Registra o actualiza el token de Firebase Cloud Messaging para notificaciones push "
        "(POST /api/order_bridge/push/token, Bearer). "
        "platform debe ser 'android' o 'ios'. "
        "Opcionalmente suscribe a temas de notificación en la misma llamada."
    ),
)
async def tool_register_push_token(
    fcm_token: str,
    platform: str,
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
    subscribe_topics: list[str] | None = None,
) -> dict[str, Any]:
    return await register_push_token(
        auth.client,
        bearer_token=auth.bearer_token,
        fcm_token=fcm_token,
        platform=platform,
        subscribe_topics=subscribe_topics,
    )


@mcp.tool(
    name="update_push_topics",
    description=(
        "Modifica las suscripciones a temas de notificaciones push "
        "(PATCH /api/order_bridge/push/topics, Bearer). "
        "Requiere un token FCM registrado previamente (usa register_push_token antes). "
        "Pasa subscribe_topics para añadir y/o unsubscribe_topics para quitar."
    ),
)
async def tool_update_push_topics(
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
    subscribe_topics: list[str] | None = None,
    unsubscribe_topics: list[str] | None = None,
) -> dict[str, Any]:
    return await update_push_topics(
        auth.client,
        bearer_token=auth.bearer_token,
        subscribe_topics=subscribe_topics,
        unsubscribe_topics=unsubscribe_topics,
    )
