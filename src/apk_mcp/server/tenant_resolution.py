"""Resolve MCP tenant id from the current HTTP request (Streamable HTTP)."""

from __future__ import annotations

from fastmcp.server.dependencies import get_http_request

from apk_mcp.config import get_settings
from apk_mcp.utils.exceptions import MissingTenantError


def resolve_tenant_id() -> str:
    """Read tenant id from the configured header, or the fallback when allowed."""
    settings = get_settings()
    try:
        request = get_http_request()
    except RuntimeError:
        if settings.apk_mcp_require_tenant_header:
            raise MissingTenantError(
                "No HTTP request context; cannot resolve tenant. "
                "Use Streamable HTTP with the tenant header, or disable APK_MCP_REQUIRE_TENANT_HEADER."
            ) from None
        return settings.apk_mcp_fallback_tenant_id

    header = settings.apk_mcp_tenant_header
    raw = request.headers.get(header)
    if raw is None:
        for hk, hv in request.headers.items():
            if hk.lower() == header.lower():
                raw = hv
                break

    if raw is not None and raw.strip():
        return raw.strip()

    if settings.apk_mcp_require_tenant_header:
        raise MissingTenantError(
            f"Missing required HTTP header {header!r} for tenant identification."
        )
    return settings.apk_mcp_fallback_tenant_id
