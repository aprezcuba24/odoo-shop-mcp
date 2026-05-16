"""FastMCP server package."""

from __future__ import annotations

from .app_state import (
    AuthenticatedOrderBridgeRef,
    OrderBridgeClientRef,
    get_apk_api,
    get_authenticated_order_bridge,
    get_device_token_for_current_tenant,
)
from .server import mcp, run

import apk_mcp.tools  # noqa: F401  # register tools
import apk_mcp.resources  # noqa: F401  # register resources
import apk_mcp.prompts  # noqa: F401  # register prompts

__all__ = [
    "AuthenticatedOrderBridgeRef",
    "OrderBridgeClientRef",
    "get_apk_api",
    "get_authenticated_order_bridge",
    "get_device_token_for_current_tenant",
    "mcp",
    "run",
]
