from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.push_token_body_platform import PushTokenBodyPlatform
from ..types import UNSET, Unset

T = TypeVar("T", bound="PushTokenBody")


@_attrs_define
class PushTokenBody:
    """
    Attributes:
        fcm_token (str):
        platform (PushTokenBodyPlatform):
        subscribe_topics (list[str] | Unset):
    """

    fcm_token: str
    platform: PushTokenBodyPlatform
    subscribe_topics: list[str] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        fcm_token = self.fcm_token

        platform = self.platform.value

        subscribe_topics: list[str] | Unset = UNSET
        if not isinstance(self.subscribe_topics, Unset):
            subscribe_topics = self.subscribe_topics

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "fcm_token": fcm_token,
                "platform": platform,
            }
        )
        if subscribe_topics is not UNSET:
            field_dict["subscribe_topics"] = subscribe_topics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        fcm_token = d.pop("fcm_token")

        platform = PushTokenBodyPlatform(d.pop("platform"))

        subscribe_topics = cast(list[str], d.pop("subscribe_topics", UNSET))

        push_token_body = cls(
            fcm_token=fcm_token,
            platform=platform,
            subscribe_topics=subscribe_topics,
        )

        return push_token_body
