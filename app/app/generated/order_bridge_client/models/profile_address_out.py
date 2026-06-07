from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProfileAddressOut")


@_attrs_define
class ProfileAddressOut:
    """
    Attributes:
        state (str):
        street (str):
        municipality_id (int | None | Unset):
        municipality_name (None | str | Unset):
        neighborhood_id (int | None | Unset):
        neighborhood_name (None | str | Unset):
    """

    state: str
    street: str
    municipality_id: int | None | Unset = UNSET
    municipality_name: None | str | Unset = UNSET
    neighborhood_id: int | None | Unset = UNSET
    neighborhood_name: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        state = self.state

        street = self.street

        municipality_id: int | None | Unset
        if isinstance(self.municipality_id, Unset):
            municipality_id = UNSET
        else:
            municipality_id = self.municipality_id

        municipality_name: None | str | Unset
        if isinstance(self.municipality_name, Unset):
            municipality_name = UNSET
        else:
            municipality_name = self.municipality_name

        neighborhood_id: int | None | Unset
        if isinstance(self.neighborhood_id, Unset):
            neighborhood_id = UNSET
        else:
            neighborhood_id = self.neighborhood_id

        neighborhood_name: None | str | Unset
        if isinstance(self.neighborhood_name, Unset):
            neighborhood_name = UNSET
        else:
            neighborhood_name = self.neighborhood_name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "state": state,
                "street": street,
            }
        )
        if municipality_id is not UNSET:
            field_dict["municipality_id"] = municipality_id
        if municipality_name is not UNSET:
            field_dict["municipality_name"] = municipality_name
        if neighborhood_id is not UNSET:
            field_dict["neighborhood_id"] = neighborhood_id
        if neighborhood_name is not UNSET:
            field_dict["neighborhood_name"] = neighborhood_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        state = d.pop("state")

        street = d.pop("street")

        def _parse_municipality_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        municipality_id = _parse_municipality_id(d.pop("municipality_id", UNSET))

        def _parse_municipality_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        municipality_name = _parse_municipality_name(d.pop("municipality_name", UNSET))

        def _parse_neighborhood_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        neighborhood_id = _parse_neighborhood_id(d.pop("neighborhood_id", UNSET))

        def _parse_neighborhood_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        neighborhood_name = _parse_neighborhood_name(d.pop("neighborhood_name", UNSET))

        profile_address_out = cls(
            state=state,
            street=street,
            municipality_id=municipality_id,
            municipality_name=municipality_name,
            neighborhood_id=neighborhood_id,
            neighborhood_name=neighborhood_name,
        )

        return profile_address_out
