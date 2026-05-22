from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="OrderLineIn")


@_attrs_define
class OrderLineIn:
    """
    Attributes:
        product_id (int):
        qty (float):
    """

    product_id: int
    qty: float

    def to_dict(self) -> dict[str, Any]:
        product_id = self.product_id

        qty = self.qty

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "product_id": product_id,
                "qty": qty,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], app_dict: Mapping[str, Any]) -> T:
        d = dict(app_dict)
        product_id = d.pop("product_id")

        qty = d.pop("qty")

        order_line_in = cls(
            product_id=product_id,
            qty=qty,
        )

        return order_line_in
