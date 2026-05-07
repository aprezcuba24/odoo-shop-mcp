from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="SimpleErrorResponse")


@_attrs_define
class SimpleErrorResponse:
    """e.g. invalid_json, not_found.

    Attributes:
        error (str):
    """

    error: str

    def to_dict(self) -> dict[str, Any]:
        error = self.error

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error = d.pop("error")

        simple_error_response = cls(
            error=error,
        )

        return simple_error_response
