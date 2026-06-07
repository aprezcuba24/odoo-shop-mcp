from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="InsufficientStockProductItem")


@_attrs_define
class InsufficientStockProductItem:
    """
    Attributes:
        available_qty (float): Cantidad disponible en el almacén del catálogo
        product_id (int): Variante de producto (`product.product`)
    """

    available_qty: float
    product_id: int

    def to_dict(self) -> dict[str, Any]:
        available_qty = self.available_qty

        product_id = self.product_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "available_qty": available_qty,
                "product_id": product_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        available_qty = d.pop("available_qty")

        product_id = d.pop("product_id")

        insufficient_stock_product_item = cls(
            available_qty=available_qty,
            product_id=product_id,
        )

        return insufficient_stock_product_item
