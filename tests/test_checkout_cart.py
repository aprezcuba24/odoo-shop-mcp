"""Unit tests for checkout_cart tool."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, patch

from apk_mcp.services.cart.memory import InMemoryCartStore
from apk_mcp.utils.exceptions import InsufficientStockError
from apk_mcp.utils.shop_key_codec import decode_shop_key, encode_shop_key

_CTX = decode_shop_key(encode_shop_key("http://localhost:8069", "test-key"))
_CART_KEY = _CTX.cart_store_key()


def _auth_stub(*, bearer_token: str = "Bearer test-key") -> object:
    return type("Auth", (), {"client": object(), "bearer_token": bearer_token})()


def test_checkout_cart_empty() -> None:
    from apk_mcp.tools import orders as orders_tools

    async def run() -> None:
        with (
            patch(
                "apk_mcp.tools.orders.resolve_shop_context",
                return_value=_CTX,
            ),
            patch(
                "apk_mcp.tools.orders.create_order",
                new_callable=AsyncMock,
            ) as mock_create,
        ):
            result = await orders_tools.checkout_cart(auth=_auth_stub())

        assert result["ok"] is False
        assert result["error"] == "empty_cart"
        mock_create.assert_not_called()

    asyncio.run(run())


def test_checkout_cart_success_clears_cart() -> None:
    from apk_mcp.tools import orders as orders_tools

    async def run() -> None:
        store = InMemoryCartStore()
        with (
            patch(
                "apk_mcp.tools.orders.resolve_shop_context",
                return_value=_CTX,
            ),
            patch("apk_mcp.tools.orders.cart_store", store),
            patch(
                "apk_mcp.tools.orders.create_order",
                new_callable=AsyncMock,
                return_value={
                    "order_number": "S00101",
                    "status": "En revisión",
                    "_agent": {"order_id": 101, "store_state": "reviewing"},
                },
            ) as mock_create,
        ):
            await store.add_line(_CART_KEY, product_id=5, quantity=2.0)

            result = await orders_tools.checkout_cart(auth=_auth_stub())

        assert result["ok"] is True
        assert result["order"]["order_number"] == "S00101"
        assert result["order"]["_agent"]["order_id"] == 101
        assert result["cart_cleared"] is True
        assert "lines_submitted" not in result
        mock_create.assert_awaited_once()
        assert await store.get_lines(_CART_KEY) == []

    asyncio.run(run())


def test_checkout_cart_insufficient_stock_keeps_cart() -> None:
    from apk_mcp.tools import orders as orders_tools

    async def run() -> None:
        store = InMemoryCartStore()
        with (
            patch(
                "apk_mcp.tools.orders.resolve_shop_context",
                return_value=_CTX,
            ),
            patch("apk_mcp.tools.orders.cart_store", store),
            patch(
                "apk_mcp.tools.orders.create_order",
                new_callable=AsyncMock,
                side_effect=InsufficientStockError(
                    "Solo hay 1 unidad disponible.",
                    status_code=400,
                    body={
                        "error": "insufficient_stock",
                        "message": "Solo hay 1 unidad disponible.",
                        "products": [{"product_id": 5, "available_qty": 1.0}],
                    },
                ),
            ),
        ):
            await store.add_line(_CART_KEY, product_id=5, quantity=2.0)

            result = await orders_tools.checkout_cart(auth=_auth_stub())

        assert result["ok"] is False
        assert result["error"] == "insufficient_stock"
        assert result["products"] == [{"available_qty": 1.0}]
        assert result["_agent"]["products"] == [{"product_id": 5, "available_qty": 1.0}]
        assert result["_agent"]["lines_submitted"] == [{"product_id": 5, "qty": 2.0}]
        lines = await store.get_lines(_CART_KEY)
        assert len(lines) == 1
        assert lines[0].qty == 2.0

    asyncio.run(run())
