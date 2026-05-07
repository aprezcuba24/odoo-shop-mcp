from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PushTopicsOkResponse")


@_attrs_define
class PushTopicsOkResponse:
    """Respuestas 200 de ``POST /push/token`` y ``PATCH /push/topics``.

    Attributes:
        subscribed_topics (list[str]):
        status (Literal['ok'] | Unset):  Default: 'ok'.
    """

    subscribed_topics: list[str]
    status: Literal["ok"] | Unset = "ok"

    def to_dict(self) -> dict[str, Any]:
        subscribed_topics = self.subscribed_topics

        status = self.status

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "subscribed_topics": subscribed_topics,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        subscribed_topics = cast(list[str], d.pop("subscribed_topics"))

        status = cast(Literal["ok"] | Unset, d.pop("status", UNSET))
        if status != "ok" and not isinstance(status, Unset):
            raise ValueError(f"status must match const 'ok', got '{status}'")

        push_topics_ok_response = cls(
            subscribed_topics=subscribed_topics,
            status=status,
        )

        return push_topics_ok_response
