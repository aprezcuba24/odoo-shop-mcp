from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.address_patch import AddressPatch


T = TypeVar("T", bound="ProfilePatchBody")


@_attrs_define
class ProfilePatchBody:
    """
    Attributes:
        address (AddressPatch | None | Unset):
        name (None | str | Unset):
    """

    address: AddressPatch | None | Unset = UNSET
    name: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.address_patch import AddressPatch

        address: dict[str, Any] | None | Unset
        if isinstance(self.address, Unset):
            address = UNSET
        elif isinstance(self.address, AddressPatch):
            address = self.address.to_dict()
        else:
            address = self.address

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if address is not UNSET:
            field_dict["address"] = address
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_patch import AddressPatch

        d = dict(src_dict)

        def _parse_address(data: object) -> AddressPatch | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                address_type_0 = AddressPatch.from_dict(data)

                return address_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AddressPatch | None | Unset, data)

        address = _parse_address(d.pop("address", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        profile_patch_body = cls(
            address=address,
            name=name,
        )

        return profile_patch_body
