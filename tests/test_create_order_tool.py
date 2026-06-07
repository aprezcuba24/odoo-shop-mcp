"""Unit tests for create_order tool insufficient stock handling."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, patch

from app.utils.exceptions import InsufficientStockError


def _auth_stub(*, bearer_token: str = "Bearer test-key") -> object:
    return type("Auth", (), {"client": object(), "bearer_token": bearer_token})()


def test_create_order_insufficient_stock_returns_structured_response() -> None:
    from app.tools import orders as orders_tools

    async def run() -> None:
        with patch(
            "app.tools.orders.create_order",
            new_callable=AsyncMock,
            side_effect=InsufficientStockError(
                "Stock insuficiente para uno o más productos",
                status_code=400,
                body={
                    "error": "insufficient_stock",
                    "message": "Stock insuficiente para uno o más productos",
                    "products": [{"product_id": 8, "available_qty": 15.0}],
                },
            ),
        ):
            result = await orders_tools.tool_create_order(
                lines_json='[{"product_id": 8, "qty": 20.0}]',
                auth=_auth_stub(),
            )

        assert result["ok"] is False
        assert result["error"] == "insufficient_stock"
        assert result["products"] == [{"product_id": 8, "available_qty": 15.0}]
        assert result["_agent"]["lines_submitted"] == [{"product_id": 8, "qty": 20.0}]

    asyncio.run(run())
