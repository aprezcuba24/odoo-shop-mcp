from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="AddressFull")


@_attrs_define
class AddressFull:
    """
    Attributes:
        municipality_id (int):
        neighborhood_id (int):
        state (str):
        street (str):
    """

    municipality_id: int
    neighborhood_id: int
    state: str
    street: str

    def to_dict(self) -> dict[str, Any]:
        municipality_id = self.municipality_id

        neighborhood_id = self.neighborhood_id

        state = self.state

        street = self.street

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "municipality_id": municipality_id,
                "neighborhood_id": neighborhood_id,
                "state": state,
                "street": street,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        municipality_id = d.pop("municipality_id")

        neighborhood_id = d.pop("neighborhood_id")

        state = d.pop("state")

        street = d.pop("street")

        address_full = cls(
            municipality_id=municipality_id,
            neighborhood_id=neighborhood_id,
            state=state,
            street=street,
        )

        return address_full
