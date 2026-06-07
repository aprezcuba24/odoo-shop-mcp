from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PushTopicsPatchBody")


@_attrs_define
class PushTopicsPatchBody:
    """
    Attributes:
        subscribe_topics (list[str] | Unset):
        unsubscribe_topics (list[str] | Unset):
    """

    subscribe_topics: list[str] | Unset = UNSET
    unsubscribe_topics: list[str] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        subscribe_topics: list[str] | Unset = UNSET
        if not isinstance(self.subscribe_topics, Unset):
            subscribe_topics = self.subscribe_topics

        unsubscribe_topics: list[str] | Unset = UNSET
        if not isinstance(self.unsubscribe_topics, Unset):
            unsubscribe_topics = self.unsubscribe_topics

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if subscribe_topics is not UNSET:
            field_dict["subscribe_topics"] = subscribe_topics
        if unsubscribe_topics is not UNSET:
            field_dict["unsubscribe_topics"] = unsubscribe_topics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        subscribe_topics = cast(list[str], d.pop("subscribe_topics", UNSET))

        unsubscribe_topics = cast(list[str], d.pop("unsubscribe_topics", UNSET))

        push_topics_patch_body = cls(
            subscribe_topics=subscribe_topics,
            unsubscribe_topics=unsubscribe_topics,
        )

        return push_topics_patch_body
