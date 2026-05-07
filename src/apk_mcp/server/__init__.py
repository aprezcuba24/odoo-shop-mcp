"""FastMCP server package."""

from __future__ import annotations

from .app_state import OrderBridgeClientRef, get_apk_api
from .server import mcp, run

import apk_mcp.tools  # noqa: F401  # register tools

__all__ = ["OrderBridgeClientRef", "get_apk_api", "mcp", "run"]
