"""Shared OpenAPI-aligned models (pagination, errors)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PaginationMeta(BaseModel):
    model_config = ConfigDict(extra="forbid")

    limit: int
    offset: int
    total: int


class ValidationDetailItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    loc: list[str]
    msg: str
    type: str


class ValidationErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    error: str
    message: str
    details: list[ValidationDetailItem] | None = None


class UnauthorizedErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    error: str
    message: str


class SimpleErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    error: str


class MessageErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    error: str
    message: str


class ConfigurationErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    error: str
    message: str


class InsufficientStockProductItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    product_id: int
    available_qty: float


class InsufficientStockErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    error: str = Field(default="insufficient_stock")
    message: str
    products: list[InsufficientStockProductItem]
