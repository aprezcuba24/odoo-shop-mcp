from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="NeighborhoodRow")


@_attrs_define
class NeighborhoodRow:
    """
    Attributes:
        id (int):
        name (str):
    """

    id: int
    name: str

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], app_dict: Mapping[str, Any]) -> T:
        d = dict(app_dict)
        id = d.pop("id")

        name = d.pop("name")

        neighborhood_row = cls(
            id=id,
            name=name,
        )

        return neighborhood_row
