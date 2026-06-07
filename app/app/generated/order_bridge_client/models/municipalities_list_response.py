from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.municipality_with_neighborhoods_row import (
        MunicipalityWithNeighborhoodsRow,
    )


T = TypeVar("T", bound="MunicipalitiesListResponse")


@_attrs_define
class MunicipalitiesListResponse:
    """
    Attributes:
        items (list[MunicipalityWithNeighborhoodsRow]):
        total (int):
    """

    items: list[MunicipalityWithNeighborhoodsRow]
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
        from ..models.municipality_with_neighborhoods_row import (
            MunicipalityWithNeighborhoodsRow,
        )

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = MunicipalityWithNeighborhoodsRow.from_dict(items_item_data)

            items.append(items_item)

        total = d.pop("total")

        municipalities_list_response = cls(
            items=items,
            total=total,
        )

        return municipalities_list_response
