"""FastMCP server package."""

from __future__ import annotations

from .app_state import (
    AuthenticatedOrderBridgeRef,
    OrderBridgeClientRef,
    get_apk_api,
    get_authenticated_order_bridge,
)
from app.utils.exceptions import InvalidShopKeyError
from app.utils.shop_key_codec import (
    SHOP_KEY_HEADER,
    ShopContext,
    resolve_shop_context,
    resolve_shop_key,
)
from .server import mcp, run

import app.tools  # noqa: F401  # register tools
import app.resources  # noqa: F401  # register resources
import app.prompts  # noqa: F401  # register prompts

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
