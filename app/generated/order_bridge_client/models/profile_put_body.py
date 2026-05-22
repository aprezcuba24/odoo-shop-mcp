from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.address_full import AddressFull


T = TypeVar("T", bound="ProfilePutBody")


@_attrs_define
class ProfilePutBody:
    """
    Attributes:
        address (AddressFull):
        name (str):
    """

    address: AddressFull
    name: str

    def to_dict(self) -> dict[str, Any]:
        address = self.address.to_dict()

        name = self.name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "address": address,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], app_dict: Mapping[str, Any]) -> T:
        from ..models.address_full import AddressFull

        d = dict(app_dict)
        address = AddressFull.from_dict(d.pop("address"))

        name = d.pop("name")

        profile_put_body = cls(
            address=address,
            name=name,
        )

        return profile_put_body
