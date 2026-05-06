"""Catalog tools (public product listing)."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import FastMCP
from pydantic import Field

from apk_mcp.app_state import app_state
from apk_mcp.models.catalog import ProductsPageResponse

_registered_servers: set[int] = set()


def register_catalog_tools(mcp: FastMCP) -> None:
    sid = id(mcp)
    if sid in _registered_servers:
        return
    @mcp.tool(
        name="list_products",
        description=(
            "List products from the Tienda Apk catalog via GET /api/order_bridge/products. "
            "This endpoint is public (no device_key). Supports pagination (limit default 80, "
            "max 200), optional category_id, and case-insensitive partial name search."
        ),
    )
    async def list_products(
        limit: Annotated[
            int | None,
            Field(
                default=None,
                ge=1,
                le=200,
                description="Page size (API default 80, max 200).",
            ),
        ] = None,
        offset: Annotated[
            int | None,
            Field(
                default=None,
                ge=0,
                description="Offset for pagination (API default 0).",
            ),
        ] = None,
        category_id: Annotated[
            int | None,
            Field(
                default=None,
                gt=0,
                description="Filter by product.category id.",
            ),
        ] = None,
        search: Annotated[
            str | None,
            Field(
                default=None,
                description="Partial product name search (case-insensitive).",
            ),
        ] = None,
    ) -> dict[str, Any]:
        api = app_state.api
        if api is None:
            raise RuntimeError("API client not initialized; server lifespan did not start.")

        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if category_id is not None:
            params["category_id"] = category_id
        if search is not None:
            params["search"] = search

        raw = await api.get_json("/api/order_bridge/products", params=params or None)
        page = ProductsPageResponse.model_validate(raw)
        return page.model_dump(mode="json")

    _registered_servers.add(sid)
