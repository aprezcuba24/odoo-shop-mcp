"""Process-wide references set during FastMCP lifespan (HTTP client + API bridge)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apk_mcp.http_client import ApkApiClient


class AppState:
    __slots__ = ("api",)

    def __init__(self) -> None:
        self.api: ApkApiClient | None = None


app_state = AppState()
