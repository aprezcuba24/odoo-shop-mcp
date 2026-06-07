from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.product_category_row import ProductCategoryRow


T = TypeVar("T", bound="CategoriesListResponse")


@_attrs_define
class CategoriesListResponse:
    """
    Attributes:
        items (list[ProductCategoryRow]):
        total (int):
    """

    items: list[ProductCategoryRow]
    total: int

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        total = self.total

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "items": items,
                "total": total,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.product_category_row import ProductCategoryRow

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = ProductCategoryRow.from_dict(items_item_data)

            items.append(items_item)

        total = d.pop("total")

        categories_list_response = cls(
            items=items,
            total=total,
        )

        return categories_list_response
