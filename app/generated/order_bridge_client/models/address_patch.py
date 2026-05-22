from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddressPatch")


@_attrs_define
class AddressPatch:
    """
    Attributes:
        municipality_id (int | None | Unset): Tras el merge con la dirección guardada, municipio y barrio deben quedar
            definidos.
        neighborhood_id (int | None | Unset): Tras el merge con la dirección guardada, municipio y barrio deben quedar
            definidos.
        state (None | str | Unset):
        street (None | str | Unset):
    """

    municipality_id: int | None | Unset = UNSET
    neighborhood_id: int | None | Unset = UNSET
    state: None | str | Unset = UNSET
    street: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        municipality_id: int | None | Unset
        if isinstance(self.municipality_id, Unset):
            municipality_id = UNSET
        else:
            municipality_id = self.municipality_id

        neighborhood_id: int | None | Unset
        if isinstance(self.neighborhood_id, Unset):
            neighborhood_id = UNSET
        else:
            neighborhood_id = self.neighborhood_id

        state: None | str | Unset
        if isinstance(self.state, Unset):
            state = UNSET
        else:
            state = self.state

        street: None | str | Unset
        if isinstance(self.street, Unset):
            street = UNSET
        else:
            street = self.street

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if municipality_id is not UNSET:
            field_dict["municipality_id"] = municipality_id
        if neighborhood_id is not UNSET:
            field_dict["neighborhood_id"] = neighborhood_id
        if state is not UNSET:
            field_dict["state"] = state
        if street is not UNSET:
            field_dict["street"] = street

        return field_dict

    @classmethod
    def from_dict(cls: type[T], app_dict: Mapping[str, Any]) -> T:
        d = dict(app_dict)

        def _parse_municipality_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        municipality_id = _parse_municipality_id(d.pop("municipality_id", UNSET))

        def _parse_neighborhood_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        neighborhood_id = _parse_neighborhood_id(d.pop("neighborhood_id", UNSET))

        def _parse_state(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        state = _parse_state(d.pop("state", UNSET))

        def _parse_street(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        street = _parse_street(d.pop("street", UNSET))

        address_patch = cls(
            municipality_id=municipality_id,
            neighborhood_id=neighborhood_id,
            state=state,
            street=street,
        )

        return address_patch
