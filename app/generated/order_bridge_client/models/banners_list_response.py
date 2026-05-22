from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.banner_row import BannerRow


T = TypeVar("T", bound="BannersListResponse")


@_attrs_define
class BannersListResponse:
    """
    Attributes:
        items (list[BannerRow]):
        total (int):
    """

    items: list[BannerRow]
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
    def from_dict(cls: type[T], app_dict: Mapping[str, Any]) -> T:
        from ..models.banner_row import BannerRow

        d = dict(app_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = BannerRow.from_dict(items_item_data)

            items.append(items_item)

        total = d.pop("total")

        banners_list_response = cls(
            items=items,
            total=total,
        )

        return banners_list_response
