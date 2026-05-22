from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.profile_address_out import ProfileAddressOut


T = TypeVar("T", bound="ProfileResponse")


@_attrs_define
class ProfileResponse:
    """
    Attributes:
        id (int):
        name (str):
        phone (str):
        address (None | ProfileAddressOut | Unset):
        email (None | str | Unset):
    """

    id: int
    name: str
    phone: str
    address: None | ProfileAddressOut | Unset = UNSET
    email: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.profile_address_out import ProfileAddressOut

        id = self.id

        name = self.name

        phone = self.phone

        address: dict[str, Any] | None | Unset
        if isinstance(self.address, Unset):
            address = UNSET
        elif isinstance(self.address, ProfileAddressOut):
            address = self.address.to_dict()
        else:
            address = self.address

        email: None | str | Unset
        if isinstance(self.email, Unset):
            email = UNSET
        else:
            email = self.email

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "name": name,
                "phone": phone,
            }
        )
        if address is not UNSET:
            field_dict["address"] = address
        if email is not UNSET:
            field_dict["email"] = email

        return field_dict

    @classmethod
    def from_dict(cls: type[T], app_dict: Mapping[str, Any]) -> T:
        from ..models.profile_address_out import ProfileAddressOut

        d = dict(app_dict)
        id = d.pop("id")

        name = d.pop("name")

        phone = d.pop("phone")

        def _parse_address(data: object) -> None | ProfileAddressOut | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                address_type_0 = ProfileAddressOut.from_dict(data)

                return address_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProfileAddressOut | Unset, data)

        address = _parse_address(d.pop("address", UNSET))

        def _parse_email(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        email = _parse_email(d.pop("email", UNSET))

        profile_response = cls(
            id=id,
            name=name,
            phone=phone,
            address=address,
            email=email,
        )

        return profile_response
