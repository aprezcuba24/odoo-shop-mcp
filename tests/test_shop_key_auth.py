"""Unit tests for shop-key resolution and authenticated bridge."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.server.app_state import get_authenticated_order_bridge
from app.utils.shop_key_codec import (
    SHOP_CONTEXT_STATE_KEY,
    SHOP_KEY_BEARER_PREFIX,
    backend_domain,
    encode_shop_key,
    resolve_shop_context,
    resolve_shop_key,
    shop_context_from_encoded,
)
from app.server import app_state as app_state_module

_BASE = "http://localhost:8069"
_USER_TOKEN = "99031c76-d288-41ea-866b-ef656f58e497"
_BEARER = f"Bearer {_USER_TOKEN}"
_ENCODED = encode_shop_key(_BASE, _USER_TOKEN)
_B64_ONLY = _ENCODED.removeprefix(SHOP_KEY_BEARER_PREFIX)
_CTX = shop_context_from_encoded(_ENCODED)


def _http_scope(*, query_string: bytes = b"", headers: list[tuple[bytes, bytes]] | None = None):
    return {
        "type": "http",
        "asgi": {"spec_version": "2.1", "version": "3.0"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": "/mcp",
        "raw_path": b"/mcp",
        "query_string": query_string,
        "headers": headers or [],
        "client": None,
        "server": ("127.0.0.1", 8000),
    }


def _with_middleware_state(request, *, ctx=_CTX):
    setattr(request.state, SHOP_CONTEXT_STATE_KEY, ctx)
    return request


def _request_with_shop_key(encoded: str):
    from starlette.requests import Request

    ctx = shop_context_from_encoded(encoded)
    return _with_middleware_state(
        Request(_http_scope(headers=[(b"shop-key", encoded.encode())])),
        ctx=ctx,
    )


def _request_with_query_key(b64: str):
    from starlette.requests import Request

    ctx = shop_context_from_encoded(b64)
    return _with_middleware_state(
        Request(_http_scope(query_string=f"key={b64}".encode())),
        ctx=ctx,
    )


def test_resolve_shop_context_from_query_key() -> None:
    req = _request_with_query_key(_B64_ONLY)
    with patch("app.utils.shop_key_codec.get_http_request", return_value=req):
        ctx = resolve_shop_context()

    assert ctx.storage_key == _B64_ONLY
    assert ctx.base_url == _BASE
    assert ctx.bearer_token == _BEARER
    assert ctx.user_token == _USER_TOKEN
    assert ctx.cart_store_key().backend == "localhost:8069"
    assert ctx.cart_store_key().token == _USER_TOKEN


def test_resolve_shop_context_from_header() -> None:
    req = _request_with_shop_key(_ENCODED)
    with patch("app.utils.shop_key_codec.get_http_request", return_value=req):
        ctx = resolve_shop_context()

    assert ctx.storage_key == _B64_ONLY
    assert ctx.base_url == _BASE
    assert ctx.bearer_token == _BEARER
    assert ctx.user_token == _USER_TOKEN
    assert ctx.cart_store_key().backend == "localhost:8069"
    assert ctx.cart_store_key().token == _USER_TOKEN


def test_backend_domain_strips_scheme() -> None:
    assert backend_domain("https://tienda.example.com") == "tienda.example.com"
    assert backend_domain("http://localhost:8069") == "localhost:8069"


def test_backend_domain_http_and_https_same_host() -> None:
    assert backend_domain("http://tienda.example.com") == backend_domain(
        "https://tienda.example.com"
    )


def test_resolve_shop_key_returns_raw_base64() -> None:
    req = _request_with_shop_key(_ENCODED)
    with patch("app.utils.shop_key_codec.get_http_request", return_value=req):
        assert resolve_shop_key() == _B64_ONLY


def test_resolve_shop_key_without_middleware_state_raises() -> None:
    from starlette.requests import Request

    req = Request(_http_scope(headers=[(b"shop-key", _ENCODED.encode())]))
    with patch("app.utils.shop_key_codec.get_http_request", return_value=req):
        with pytest.raises(RuntimeError, match="ShopKeyMiddleware"):
            resolve_shop_key()


def test_resolve_shop_key_no_http_context_raises() -> None:
    with patch(
        "app.utils.shop_key_codec.get_http_request",
        side_effect=RuntimeError("No active HTTP request found."),
    ):
        with pytest.raises(RuntimeError, match="No active HTTP request"):
            resolve_shop_key()


def test_get_authenticated_order_bridge_uses_decoded_token_and_registry() -> None:
    async def run() -> None:
        mock_client = MagicMock()
        registry = MagicMock()
        registry.get_client = AsyncMock(return_value=mock_client)
        app_state_module.app_state.registry = registry
        try:
            req = _request_with_shop_key(_ENCODED)
            with patch("app.utils.shop_key_codec.get_http_request", return_value=req):
                ref = await get_authenticated_order_bridge()

            registry.get_client.assert_awaited_once_with(_BASE)
            assert ref.client is mock_client
            assert ref.bearer_token == _BEARER
        finally:
            app_state_module.app_state.registry = None

    asyncio.run(run())


def test_get_authenticated_order_bridge_no_http_context_raises() -> None:
    async def run() -> None:
        app_state_module.app_state.registry = MagicMock()
        try:
            with patch(
                "app.utils.shop_key_codec.get_http_request",
                side_effect=RuntimeError("No active HTTP request found."),
            ):
                with pytest.raises(RuntimeError, match="No active HTTP request"):
                    await get_authenticated_order_bridge()
        finally:
            app_state_module.app_state.registry = None

    asyncio.run(run())
