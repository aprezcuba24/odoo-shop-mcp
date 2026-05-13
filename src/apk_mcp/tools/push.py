"""Push notification tools — FCM token registration and topic subscriptions (Bearer)."""

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
        "Register or update a Firebase Cloud Messaging token for push notifications via "
        "POST /api/order_bridge/push/token (Bearer). "
        "platform must be 'android' or 'ios'. "
        "Optionally subscribe to notification topics in the same call."
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
        "Change push notification topic subscriptions via "
        "PATCH /api/order_bridge/push/topics (Bearer). "
        "Requires a previously registered FCM token (use register_push_token first). "
        "Provide subscribe_topics to add and/or unsubscribe_topics to remove."
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
