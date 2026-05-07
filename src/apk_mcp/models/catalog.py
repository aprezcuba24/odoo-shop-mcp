"""Catalog schemas (products list)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from apk_mcp.models.common import PaginationParams


class ListProductsParams(PaginationParams):
    """Query parameters for GET /api/order_bridge/products."""

    category_id: int | None = Field(
        default=None,
        gt=0,
        description="Filter by product.category id.",
    )
    search: str | None = Field(
        default=None,
        description="Partial product name search (case-insensitive).",
    )


class ProductCategoryRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    name: str
    parent_id: int | None = None


class ProductListRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    name: str
    list_price: float
    barcode: str | None = None
    category: ProductCategoryRow | None = None
    default_code: str | None = None
    image_thumbnail_url: str | None = None
    image_url: str | None = None
    uom_name: str | None = None


class ProductsPageResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[ProductListRow]
    limit: int
    offset: int
    total: int
