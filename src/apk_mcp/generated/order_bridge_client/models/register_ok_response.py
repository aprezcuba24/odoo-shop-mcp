from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="RegisterOkResponse")


@_attrs_define
class RegisterOkResponse:
    """
    Attributes:
        created (bool):
        partner_id (int):
        status (str): Siempre 'ok' si tiene éxito
        validated (bool):
    """

    created: bool
    partner_id: int
    status: str
    validated: bool

    def to_dict(self) -> dict[str, Any]:
        created = self.created

        partner_id = self.partner_id

        status = self.status

        validated = self.validated

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "created": created,
                "partner_id": partner_id,
                "status": status,
                "validated": validated,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created = d.pop("created")

        partner_id = d.pop("partner_id")

        status = d.pop("status")

        validated = d.pop("validated")

        register_ok_response = cls(
            created=created,
            partner_id=partner_id,
            status=status,
            validated=validated,
        )

        return register_ok_response
