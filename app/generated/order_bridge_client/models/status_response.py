from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="StatusResponse")


@_attrs_define
class StatusResponse:
    """
    Attributes:
        partner_id (int):
        partner_name (str):
        validated (bool):
        phone (None | str | Unset):
    """

    partner_id: int
    partner_name: str
    validated: bool
    phone: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        partner_id = self.partner_id

        partner_name = self.partner_name

        validated = self.validated

        phone: None | str | Unset
        if isinstance(self.phone, Unset):
            phone = UNSET
        else:
            phone = self.phone

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "partner_id": partner_id,
                "partner_name": partner_name,
                "validated": validated,
            }
        )
        if phone is not UNSET:
            field_dict["phone"] = phone

        return field_dict

    @classmethod
    def from_dict(cls: type[T], app_dict: Mapping[str, Any]) -> T:
        d = dict(app_dict)
        partner_id = d.pop("partner_id")

        partner_name = d.pop("partner_name")

        validated = d.pop("validated")

        def _parse_phone(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        phone = _parse_phone(d.pop("phone", UNSET))

        status_response = cls(
            partner_id=partner_id,
            partner_name=partner_name,
            validated=validated,
            phone=phone,
        )

        return status_response
