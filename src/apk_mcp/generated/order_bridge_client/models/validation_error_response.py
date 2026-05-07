from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.validation_detail_item import ValidationDetailItem


T = TypeVar("T", bound="ValidationErrorResponse")


@_attrs_define
class ValidationErrorResponse:
    """Pydantic validation errors include ``details``; some handlers return only ``message``.

    Attributes:
        error (str): Normalmente 'validation'
        message (str):
        details (list[ValidationDetailItem] | None | Unset):
    """

    error: str
    message: str
    details: list[ValidationDetailItem] | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        error = self.error

        message = self.message

        details: list[dict[str, Any]] | None | Unset
        if isinstance(self.details, Unset):
            details = UNSET
        elif isinstance(self.details, list):
            details = []
            for details_type_0_item_data in self.details:
                details_type_0_item = details_type_0_item_data.to_dict()
                details.append(details_type_0_item)

        else:
            details = self.details

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "error": error,
                "message": message,
            }
        )
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.validation_detail_item import ValidationDetailItem

        d = dict(src_dict)
        error = d.pop("error")

        message = d.pop("message")

        def _parse_details(data: object) -> list[ValidationDetailItem] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                details_type_0 = []
                _details_type_0 = data
                for details_type_0_item_data in _details_type_0:
                    details_type_0_item = ValidationDetailItem.from_dict(
                        details_type_0_item_data
                    )

                    details_type_0.append(details_type_0_item)

                return details_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ValidationDetailItem] | None | Unset, data)

        details = _parse_details(d.pop("details", UNSET))

        validation_error_response = cls(
            error=error,
            message=message,
            details=details,
        )

        return validation_error_response
