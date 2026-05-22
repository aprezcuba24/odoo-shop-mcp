from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="MessageErrorResponse")


@_attrs_define
class MessageErrorResponse:
    """e.g. forbidden with a message.

    Attributes:
        error (str):
        message (str):
    """

    error: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        error = self.error

        message = self.message

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "error": error,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], app_dict: Mapping[str, Any]) -> T:
        d = dict(app_dict)
        error = d.pop("error")

        message = d.pop("message")

        message_error_response = cls(
            error=error,
            message=message,
        )

        return message_error_response
