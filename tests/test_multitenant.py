"""Unit tests for multi-tenant credential store and tenant resolution."""

from __future__ import annotations

import asyncio
from unittest.mock import patch

import pytest

from apk_mcp.utils.tenant_credentials import InMemoryTenantCredentialStore
from apk_mcp.utils.exceptions import MissingTenantError
from apk_mcp.server.tenant_resolution import resolve_tenant_id


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
