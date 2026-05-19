"""Unit tests for shop-key header resolution and authenticated bridge."""

from __future__ import annotations

import asyncio
from unittest.mock import MagicMock, patch

import pytest

from apk_mcp.server.app_state import get_authenticated_order_bridge, resolve_shop_key
from apk_mcp.server import app_state as app_state_module
from apk_mcp.utils.exceptions import MissingShopKeyError


def test_resolve_shop_key_from_header() -> None:
    from starlette.requests import Request

    scope = {
        "type": "http",
        "asgi": {"spec_version": "2.1", "version": "3.0"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": "/mcp",
        "raw_path": b"/mcp",
        "query_string": b"",
        "headers": [(b"shop-key", b"Bearer 99031c76-d288-41ea-866b-ef656f58e497")],
        "client": None,
        "server": ("127.0.0.1", 8000),
    }
    req = Request(scope)
    with patch("apk_mcp.server.app_state.get_http_request", return_value=req):
        assert resolve_shop_key() == "Bearer 99031c76-d288-41ea-866b-ef656f58e497"


def test_resolve_shop_key_missing_raises() -> None:
    from starlette.requests import Request

    scope = {
        "type": "http",
        "asgi": {"spec_version": "2.1", "version": "3.0"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": "/mcp",
        "raw_path": b"/mcp",
        "query_string": b"",
        "headers": [],
        "client": None,
        "server": ("127.0.0.1", 8000),
    }
    req = Request(scope)
    with patch("apk_mcp.server.app_state.get_http_request", return_value=req):
        with pytest.raises(MissingShopKeyError):
            resolve_shop_key()


def test_resolve_shop_key_no_http_context_raises() -> None:
    with patch(
        "apk_mcp.server.app_state.get_http_request",
        side_effect=RuntimeError("No active HTTP request found."),
    ):
        with pytest.raises(MissingShopKeyError):
            resolve_shop_key()


def test_get_authenticated_order_bridge_uses_shop_key_header() -> None:
    from starlette.requests import Request

    async def run() -> None:
        mock_client = MagicMock()
        app_state_module.app_state.api = mock_client
        try:
            scope = {
                "type": "http",
                "asgi": {"spec_version": "2.1", "version": "3.0"},
                "http_version": "1.1",
                "method": "POST",
                "scheme": "http",
                "path": "/mcp",
                "raw_path": b"/mcp",
                "query_string": b"",
                "headers": [(b"shop-key", b"Bearer client-supplied-token")],
                "client": None,
                "server": ("127.0.0.1", 8000),
            }
            req = Request(scope)
            with patch("apk_mcp.server.app_state.get_http_request", return_value=req):
                ref = await get_authenticated_order_bridge()
            assert ref.client is mock_client
            assert ref.bearer_token == "Bearer client-supplied-token"
        finally:
            app_state_module.app_state.api = None

    asyncio.run(run())


def test_get_authenticated_order_bridge_no_http_context_raises() -> None:
    async def run() -> None:
        mock_client = MagicMock()
        app_state_module.app_state.api = mock_client
        try:
            with patch(
                "apk_mcp.server.app_state.get_http_request",
                side_effect=RuntimeError("No active HTTP request found."),
            ):
                with pytest.raises(MissingShopKeyError):
                    await get_authenticated_order_bridge()
        finally:
            app_state_module.app_state.api = None

    asyncio.run(run())
