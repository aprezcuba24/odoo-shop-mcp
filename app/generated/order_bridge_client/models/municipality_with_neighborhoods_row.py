from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.neighborhood_row import NeighborhoodRow


T = TypeVar("T", bound="MunicipalityWithNeighborhoodsRow")


@_attrs_define
class MunicipalityWithNeighborhoodsRow:
    """
    Attributes:
        id (int):
        name (str):
        neighborhoods (list[NeighborhoodRow]):
    """

    id: int
    name: str
    neighborhoods: list[NeighborhoodRow]

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        neighborhoods = []
        for neighborhoods_item_data in self.neighborhoods:
            neighborhoods_item = neighborhoods_item_data.to_dict()
            neighborhoods.append(neighborhoods_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "name": name,
                "neighborhoods": neighborhoods,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], app_dict: Mapping[str, Any]) -> T:
        from ..models.neighborhood_row import NeighborhoodRow

        d = dict(app_dict)
        id = d.pop("id")

        name = d.pop("name")

        neighborhoods = []
        _neighborhoods = d.pop("neighborhoods")
        for neighborhoods_item_data in _neighborhoods:
            neighborhoods_item = NeighborhoodRow.from_dict(neighborhoods_item_data)

            neighborhoods.append(neighborhoods_item)

        municipality_with_neighborhoods_row = cls(
            id=id,
            name=name,
            neighborhoods=neighborhoods,
        )

        return municipality_with_neighborhoods_row
