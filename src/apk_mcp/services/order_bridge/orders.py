"""Orders service — list, detail, create, cancel."""

from __future__ import annotations

from typing import Any

from apk_mcp.generated.order_bridge_client import Client
from apk_mcp.generated.order_bridge_client.api.default import (
    order_bridge_order_cancel,
    order_bridge_order_detail,
    order_bridge_orders_create,
    order_bridge_orders_list,
)
from apk_mcp.generated.order_bridge_client.models.insufficient_stock_error_response import (
    InsufficientStockErrorResponse,
)
from apk_mcp.generated.order_bridge_client.models.order_cancel_response import (
    OrderCancelResponse,
)
from apk_mcp.generated.order_bridge_client.models.order_create_body import (
    OrderCreateBody,
)
from apk_mcp.generated.order_bridge_client.models.order_created_response import (
    OrderCreatedResponse,
)
from apk_mcp.generated.order_bridge_client.models.order_line_in import OrderLineIn
from apk_mcp.generated.order_bridge_client.models.orders_page_response import (
    OrdersPageResponse,
)
from apk_mcp.generated.order_bridge_client.models.sale_order_detail_response import (
    SaleOrderDetailResponse,
)
from apk_mcp.utils.exceptions import InsufficientStockError, NotFoundError
from apk_mcp.utils.openapi_detailed import (
    bearer_authorization,
    client_helper,
    unset_int,
    unset_str,
)

_CREATE_BAD_REQUEST_SPEC = (
    (
        InsufficientStockErrorResponse,
        InsufficientStockError,
    ),
)


async def list_orders_page(
    client: Client,
    *,
    bearer_token: str,
    limit: int | None = None,
    offset: int | None = None,
    state: str | None = None,
) -> dict[str, Any]:
    async with bearer_authorization(client, bearer_token):
        return await client_helper(
            order_bridge_orders_list,
            client,
            success_type=OrdersPageResponse,
            unexpected_shape_message="Unexpected response shape for orders list",
            limit=unset_int(limit),
            offset=unset_int(offset),
            state=unset_str(state),
        )


async def get_last_order(
    client: Client,
    *,
    bearer_token: str,
) -> dict[str, Any]:
    page = await list_orders_page(
        client,
        bearer_token=bearer_token,
        limit=1,
        offset=0,
    )
    items = page.get("items") or []
    if not items:
        raise NotFoundError(
            "No hay pedidos para este dispositivo",
            status_code=404,
            body=None,
        )
    order_id = items[0]["id"]
    return await get_order_detail(
        client,
        bearer_token=bearer_token,
        order_id=order_id,
    )


async def get_order_detail(
    client: Client,
    *,
    bearer_token: str,
    order_id: int,
) -> dict[str, Any]:
    async with bearer_authorization(client, bearer_token):
        return await client_helper(
            order_bridge_order_detail,
            client,
            success_type=SaleOrderDetailResponse,
            unexpected_shape_message="Unexpected response shape for order detail",
            order_id=order_id,
        )


async def create_order(
    client: Client,
    *,
    bearer_token: str,
    lines: list[dict[str, Any]],
) -> dict[str, Any]:
    body = OrderCreateBody(
        lines=[OrderLineIn(product_id=ln["product_id"], qty=ln["qty"]) for ln in lines]
    )
    async with bearer_authorization(client, bearer_token):
        return await client_helper(
            order_bridge_orders_create,
            client,
            success_type=OrderCreatedResponse,
            unexpected_shape_message="Unexpected response shape for create order",
            bad_request_spec=_CREATE_BAD_REQUEST_SPEC,
            body=body,
        )


async def cancel_order(
    client: Client,
    *,
    bearer_token: str,
    order_id: int,
) -> dict[str, Any]:
    async with bearer_authorization(client, bearer_token):
        return await client_helper(
            order_bridge_order_cancel,
            client,
            success_type=OrderCancelResponse,
            unexpected_shape_message="Unexpected response shape for order cancel",
            order_id=order_id,
        )
