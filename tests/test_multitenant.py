"""Unit tests for multi-tenant credential store and tenant resolution."""

from __future__ import annotations

import asyncio
from unittest.mock import MagicMock, patch

import pytest

from apk_mcp.utils.tenant_credentials import InMemoryTenantCredentialStore
from apk_mcp.utils.exceptions import MissingTenantError
from apk_mcp.server.tenant_resolution import resolve_tenant_id
from apk_mcp.server.app_state import (
    _bearer_secret_from_authorization_header,
    get_authenticated_order_bridge,
)
from apk_mcp.server import app_state as app_state_module


def test_tenant_store_distinct_tokens() -> None:
    async def run() -> None:
        store = InMemoryTenantCredentialStore()
        a = await store.ensure_device_token("alice")
        b = await store.ensure_device_token("bob")
        a2 = await store.ensure_device_token("alice")
        assert a != b
        assert a == a2

    asyncio.run(run())


def test_tenant_store_concurrent_same_tenant() -> None:
    async def run() -> None:
        store = InMemoryTenantCredentialStore()

        async def get() -> str:
            return await store.ensure_device_token("same")

        results = await asyncio.gather(*[get() for _ in range(20)])
        assert len(set(results)) == 1

    asyncio.run(run())


def test_resolve_tenant_from_header() -> None:
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
        "headers": [(b"x-apk-tenant-id", b"user-99")],
        "client": None,
        "server": ("127.0.0.1", 8000),
    }
    req = Request(scope)
    with patch("apk_mcp.server.tenant_resolution.get_http_request", return_value=req):
        assert resolve_tenant_id() == "user-99"


def test_resolve_tenant_fallback_when_allowed() -> None:
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
    with patch("apk_mcp.server.tenant_resolution.get_http_request", return_value=req):
        with patch("apk_mcp.server.tenant_resolution.get_settings") as gs:
            s = gs.return_value
            s.apk_mcp_require_tenant_header = False
            s.apk_mcp_fallback_tenant_id = "default"
            s.apk_mcp_tenant_header = "X-Apk-Tenant-Id"
            assert resolve_tenant_id() == "default"


def test_resolve_tenant_required_missing_raises() -> None:
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
    with patch("apk_mcp.server.tenant_resolution.get_http_request", return_value=req):
        with patch("apk_mcp.server.tenant_resolution.get_settings") as gs:
            s = gs.return_value
            s.apk_mcp_require_tenant_header = True
            s.apk_mcp_tenant_header = "X-Apk-Tenant-Id"
            with pytest.raises(MissingTenantError):
                resolve_tenant_id()


@pytest.mark.parametrize(
    ("header_value", "expected"),
    [
        (None, None),
        ("", None),
        ("   ", None),
        ("Bearer abc.def", "abc.def"),
        ("bearer low", "low"),
        ("opaque-only", "opaque-only"),
        ("Bearer", None),
        ("Bearer  ", None),
    ],
)
def test_bearer_secret_from_authorization_header(header_value: str | None, expected: str | None) -> None:
    assert _bearer_secret_from_authorization_header(header_value) == expected


def test_get_authenticated_order_bridge_uses_authorization_header() -> None:
    from starlette.requests import Request

    async def run() -> None:
        mock_client = MagicMock()
        store = InMemoryTenantCredentialStore()
        app_state_module.app_state.api = mock_client
        app_state_module.app_state.tenant_credential_store = store
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
                "headers": [(b"authorization", b"Bearer client-supplied-token")],
                "client": None,
                "server": ("127.0.0.1", 8000),
            }
            req = Request(scope)
            with patch("apk_mcp.server.app_state.get_http_request", return_value=req):
                with patch("apk_mcp.server.app_state.resolve_tenant_id", return_value="t1"):
                    ref = await get_authenticated_order_bridge()
            assert ref.client is mock_client
            assert ref.bearer_token == "client-supplied-token"
        finally:
            app_state_module.app_state.api = None
            app_state_module.app_state.tenant_credential_store = None

    asyncio.run(run())


def test_get_authenticated_order_bridge_falls_back_without_http_request() -> None:
    async def run() -> None:
        mock_client = MagicMock()
        store = InMemoryTenantCredentialStore()
        app_state_module.app_state.api = mock_client
        app_state_module.app_state.tenant_credential_store = store
        try:
            with patch(
                "apk_mcp.server.app_state.get_http_request",
                side_effect=RuntimeError("No active HTTP request found."),
            ):
                with patch("apk_mcp.server.app_state.resolve_tenant_id", return_value="t1"):
                    ref = await get_authenticated_order_bridge()
            assert ref.client is mock_client
            device = await store.ensure_device_token("t1")
            assert ref.bearer_token == device
        finally:
            app_state_module.app_state.api = None
            app_state_module.app_state.tenant_credential_store = None

    asyncio.run(run())
