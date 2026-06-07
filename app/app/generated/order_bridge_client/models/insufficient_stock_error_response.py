from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.insufficient_stock_product_item import InsufficientStockProductItem


T = TypeVar("T", bound="InsufficientStockErrorResponse")


@_attrs_define
class InsufficientStockErrorResponse:
    """Stock insuficiente al validar líneas del POST crear pedido.

    Attributes:
        message (str): Mensaje resumido
        products (list[InsufficientStockProductItem]): Productos almacenables con cantidad libre inferior a la
            solicitada
        error (str | Unset): Código fijo 'insufficient_stock' Default: 'insufficient_stock'.
    """

    message: str
    products: list[InsufficientStockProductItem]
    error: str | Unset = "insufficient_stock"

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        products = []
        for products_item_data in self.products:
            products_item = products_item_data.to_dict()
            products.append(products_item)

        error = self.error

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "message": message,
                "products": products,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.insufficient_stock_product_item import (
            InsufficientStockProductItem,
        )

        d = dict(src_dict)
        message = d.pop("message")

        products = []
        _products = d.pop("products")
        for products_item_data in _products:
            products_item = InsufficientStockProductItem.from_dict(products_item_data)

            products.append(products_item)

        error = d.pop("error", UNSET)

        insufficient_stock_error_response = cls(
            message=message,
            products=products,
            error=error,
        )

        return insufficient_stock_error_response
