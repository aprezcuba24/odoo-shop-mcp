from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.sale_order_summary import SaleOrderSummary


T = TypeVar("T", bound="OrdersPageResponse")


@_attrs_define
class OrdersPageResponse:
    """
    Attributes:
        items (list[SaleOrderSummary]):
        limit (int):
        offset (int):
        total (int):
    """

    items: list[SaleOrderSummary]
    limit: int
    offset: int
    total: int

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        limit = self.limit

        offset = self.offset

        total = self.total

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "items": items,
                "limit": limit,
                "offset": offset,
                "total": total,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], app_dict: Mapping[str, Any]) -> T:
        from ..models.sale_order_summary import SaleOrderSummary

        d = dict(app_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = SaleOrderSummary.from_dict(items_item_data)

            items.append(items_item)

        limit = d.pop("limit")

        offset = d.pop("offset")

        total = d.pop("total")

        orders_page_response = cls(
            items=items,
            limit=limit,
            offset=offset,
            total=total,
        )

        return orders_page_response
