"""Unit tests for in-memory cart store."""

from __future__ import annotations

import asyncio
from unittest.mock import patch

import pytest

from apk_mcp.services.cart.base import CartStoreKey
from apk_mcp.services.cart.memory import InMemoryCartStore
from apk_mcp.utils.shop_key_codec import decode_shop_key, encode_shop_key


def _cart_key(base_url: str, token: str) -> CartStoreKey:
    return decode_shop_key(encode_shop_key(base_url, token)).cart_store_key()


_KEY_A = _cart_key("https://a.example.com", "token-a")
_KEY_B = _cart_key("https://b.example.com", "token-b")


def test_add_line_accumulates_qty() -> None:
    async def run() -> None:
        store = InMemoryCartStore()
        await store.add_line(_KEY_A, product_id=3, quantity=1.0)
        lines = await store.add_line(_KEY_A, product_id=3, quantity=2.0)

        assert len(lines) == 1
        assert lines[0].product_id == 3
        assert lines[0].qty == 3.0

    asyncio.run(run())


def test_get_cart_empty() -> None:
    async def run() -> None:
        store = InMemoryCartStore()
        missing = CartStoreKey(backend="missing.example.com", token="x")
        assert await store.get_lines(missing) == []

    asyncio.run(run())


def test_get_cart_with_lines() -> None:
    async def run() -> None:
        store = InMemoryCartStore()
        await store.add_line(_KEY_A, product_id=1, quantity=2.0)
        await store.add_line(_KEY_A, product_id=4, quantity=1.0)

        lines = await store.get_lines(_KEY_A)
        assert [(line.product_id, line.qty) for line in lines] == [(1, 2.0), (4, 1.0)]

    asyncio.run(run())


def test_clear_cart_idempotent() -> None:
    async def run() -> None:
        store = InMemoryCartStore()
        await store.add_line(_KEY_A, product_id=1, quantity=1.0)
        await store.clear(_KEY_A)
        assert await store.get_lines(_KEY_A) == []

        await store.clear(_KEY_A)
        assert await store.get_lines(_KEY_A) == []

    asyncio.run(run())


def test_separate_shop_keys() -> None:
    async def run() -> None:
        store = InMemoryCartStore()
        await store.add_line(_KEY_A, product_id=1, quantity=1.0)
        await store.add_line(_KEY_B, product_id=2, quantity=3.0)

        lines_a = await store.get_lines(_KEY_A)
        lines_b = await store.get_lines(_KEY_B)

        assert [(line.product_id, line.qty) for line in lines_a] == [(1, 1.0)]
        assert [(line.product_id, line.qty) for line in lines_b] == [(2, 3.0)]

    asyncio.run(run())


def test_same_domain_different_scheme_shares_cart() -> None:
    async def run() -> None:
        store = InMemoryCartStore()
        key_http = _cart_key("http://tienda.example.com", "tok")
        key_https = _cart_key("https://tienda.example.com", "tok")
        assert key_http.backend == key_https.backend == "tienda.example.com"

        await store.add_line(key_http, product_id=1, quantity=1.0)
        lines = await store.get_lines(key_https)
        assert [(line.product_id, line.qty) for line in lines] == [(1, 1.0)]

    asyncio.run(run())


def test_add_line_rejects_non_positive_quantity() -> None:
    async def run() -> None:
        store = InMemoryCartStore()
        with pytest.raises(ValueError, match="quantity"):
            await store.add_line(_KEY_A, product_id=1, quantity=0.0)

    asyncio.run(run())


def test_cart_tools_use_resolve_shop_context() -> None:
    from apk_mcp.tools import cart as cart_tools

    ctx = decode_shop_key(encode_shop_key("http://localhost:8069", "test-shop-key"))

    async def run() -> None:
        with patch(
            "apk_mcp.tools.cart.resolve_shop_context",
            return_value=ctx,
        ):
            added = await cart_tools.add_to_cart(product_id=5, quantity=2.0)
            assert "client_key" not in added
            assert added["_agent"]["lines"] == [{"product_id": 5, "qty": 2.0}]

            fetched = await cart_tools.get_cart()
            assert fetched["line_count"] == 1
            assert fetched["_agent"]["lines"] == [{"product_id": 5, "qty": 2.0}]

            cleared = await cart_tools.clear_cart()
            assert cleared["_agent"]["lines"] == []
            assert cleared["message"] == "Carrito vaciado."

            empty = await cart_tools.get_cart()
            assert empty["_agent"]["lines"] == []

    asyncio.run(run())
