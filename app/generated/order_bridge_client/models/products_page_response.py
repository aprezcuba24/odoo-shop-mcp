from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.product_list_row import ProductListRow


T = TypeVar("T", bound="ProductsPageResponse")


@_attrs_define
class ProductsPageResponse:
    """
    Attributes:
        items (list[ProductListRow]):
        limit (int):
        offset (int):
        total (int):
    """

    items: list[ProductListRow]
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
        from ..models.product_list_row import ProductListRow

        d = dict(app_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = ProductListRow.from_dict(items_item_data)

            items.append(items_item)

        limit = d.pop("limit")

        offset = d.pop("offset")

        total = d.pop("total")

        products_page_response = cls(
            items=items,
            limit=limit,
            offset=offset,
            total=total,
        )

        return products_page_response
