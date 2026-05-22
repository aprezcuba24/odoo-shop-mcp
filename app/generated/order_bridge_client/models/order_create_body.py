from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.order_line_in import OrderLineIn


T = TypeVar("T", bound="OrderCreateBody")


@_attrs_define
class OrderCreateBody:
    """
    Attributes:
        lines (list[OrderLineIn]):
    """

    lines: list[OrderLineIn]

    def to_dict(self) -> dict[str, Any]:
        lines = []
        for lines_item_data in self.lines:
            lines_item = lines_item_data.to_dict()
            lines.append(lines_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "lines": lines,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], app_dict: Mapping[str, Any]) -> T:
        from ..models.order_line_in import OrderLineIn

        d = dict(app_dict)
        lines = []
        _lines = d.pop("lines")
        for lines_item_data in _lines:
            lines_item = OrderLineIn.from_dict(lines_item_data)

            lines.append(lines_item)

        order_create_body = cls(
            lines=lines,
        )

        return order_create_body
