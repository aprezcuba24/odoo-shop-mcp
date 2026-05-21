"""FastMCP server package."""

from __future__ import annotations

from .app_state import (
    AuthenticatedOrderBridgeRef,
    OrderBridgeClientRef,
    get_apk_api,
    get_authenticated_order_bridge,
)
from apk_mcp.utils.exceptions import InvalidShopKeyError
from apk_mcp.utils.shop_key_codec import (
    SHOP_KEY_HEADER,
    ShopContext,
    resolve_shop_context,
    resolve_shop_key,
)
from .server import mcp, run

import apk_mcp.tools  # noqa: F401  # register tools
import apk_mcp.resources  # noqa: F401  # register resources
import apk_mcp.prompts  # noqa: F401  # register prompts

__all__ = [
    "AuthenticatedOrderBridgeRef",
    "InvalidShopKeyError",
    "OrderBridgeClientRef",
    "SHOP_KEY_HEADER",
    "ShopContext",
    "get_apk_api",
    "get_authenticated_order_bridge",
    "resolve_shop_context",
    "resolve_shop_key",
    "mcp",
    "run",
]
