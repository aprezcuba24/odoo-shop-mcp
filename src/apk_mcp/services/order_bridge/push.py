"""Push notification service — register FCM token and update topic subscriptions."""

from __future__ import annotations

from typing import Any

from apk_mcp.generated.order_bridge_client import Client
from apk_mcp.generated.order_bridge_client.api.default import (
    order_bridge_push_token,
    order_bridge_push_topics,
)
from apk_mcp.generated.order_bridge_client.models.push_token_body import PushTokenBody
from apk_mcp.generated.order_bridge_client.models.push_token_body_platform import (
    PushTokenBodyPlatform,
)
from apk_mcp.generated.order_bridge_client.models.push_topics_ok_response import (
    PushTopicsOkResponse,
)
from apk_mcp.generated.order_bridge_client.models.push_topics_patch_body import (
    PushTopicsPatchBody,
)
from apk_mcp.generated.order_bridge_client.types import UNSET
from apk_mcp.utils.openapi_detailed import bearer_authorization, client_helper


async def register_push_token(
    client: Client,
    *,
    bearer_token: str,
    fcm_token: str,
    platform: str,
    subscribe_topics: list[str] | None = None,
) -> dict[str, Any]:
    body = PushTokenBody(
        fcm_token=fcm_token,
        platform=PushTokenBodyPlatform(platform),
        subscribe_topics=subscribe_topics if subscribe_topics is not None else UNSET,
    )
    async with bearer_authorization(client, bearer_token):
        return await client_helper(
            order_bridge_push_token,
            client,
            success_type=PushTopicsOkResponse,
            unexpected_shape_message="Unexpected response shape for push token register",
            body=body,
        )


async def update_push_topics(
    client: Client,
    *,
    bearer_token: str,
    subscribe_topics: list[str] | None = None,
    unsubscribe_topics: list[str] | None = None,
) -> dict[str, Any]:
    body = PushTopicsPatchBody(
        subscribe_topics=subscribe_topics if subscribe_topics is not None else UNSET,
        unsubscribe_topics=unsubscribe_topics if unsubscribe_topics is not None else UNSET,
    )
    async with bearer_authorization(client, bearer_token):
        return await client_helper(
            order_bridge_push_topics,
            client,
            success_type=PushTopicsOkResponse,
            unexpected_shape_message="Unexpected response shape for push topics update",
            body=body,
        )
