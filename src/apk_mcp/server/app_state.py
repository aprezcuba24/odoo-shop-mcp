"""Process-wide references set during FastMCP lifespan (HTTP client + API bridge)."""

from __future__ import annotations

from apk_mcp.utils import ApkApiClient


class AppState:
    __slots__ = ("api",)

    def __init__(self) -> None:
        self.api: ApkApiClient | None = None


app_state = AppState()


def get_apk_api() -> ApkApiClient:
    api = app_state.api
    if api is None:
        raise RuntimeError("API client not initialized; server lifespan did not start.")
    return api
