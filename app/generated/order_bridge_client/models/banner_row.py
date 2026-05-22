from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="BannerRow")


@_attrs_define
class BannerRow:
    """`GET /api/order_bridge/banners` — un banner publicitario del catálogo.

    Attributes:
        id (int):
        title (str):
        active (bool | Unset):  Default: True.
        bg_color (None | str | Unset):
        href (None | str | Unset):
        image_thumbnail_url (None | str | Unset):
        image_url (None | str | Unset):
        subtitle (None | str | Unset):
        text_color (None | str | Unset):
    """

    id: int
    title: str
    active: bool | Unset = True
    bg_color: None | str | Unset = UNSET
    href: None | str | Unset = UNSET
    image_thumbnail_url: None | str | Unset = UNSET
    image_url: None | str | Unset = UNSET
    subtitle: None | str | Unset = UNSET
    text_color: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        title = self.title

        active = self.active

        bg_color: None | str | Unset
        if isinstance(self.bg_color, Unset):
            bg_color = UNSET
        else:
            bg_color = self.bg_color

        href: None | str | Unset
        if isinstance(self.href, Unset):
            href = UNSET
        else:
            href = self.href

        image_thumbnail_url: None | str | Unset
        if isinstance(self.image_thumbnail_url, Unset):
            image_thumbnail_url = UNSET
        else:
            image_thumbnail_url = self.image_thumbnail_url

        image_url: None | str | Unset
        if isinstance(self.image_url, Unset):
            image_url = UNSET
        else:
            image_url = self.image_url

        subtitle: None | str | Unset
        if isinstance(self.subtitle, Unset):
            subtitle = UNSET
        else:
            subtitle = self.subtitle

        text_color: None | str | Unset
        if isinstance(self.text_color, Unset):
            text_color = UNSET
        else:
            text_color = self.text_color

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "title": title,
            }
        )
        if active is not UNSET:
            field_dict["active"] = active
        if bg_color is not UNSET:
            field_dict["bg_color"] = bg_color
        if href is not UNSET:
            field_dict["href"] = href
        if image_thumbnail_url is not UNSET:
            field_dict["image_thumbnail_url"] = image_thumbnail_url
        if image_url is not UNSET:
            field_dict["image_url"] = image_url
        if subtitle is not UNSET:
            field_dict["subtitle"] = subtitle
        if text_color is not UNSET:
            field_dict["text_color"] = text_color

        return field_dict

    @classmethod
    def from_dict(cls: type[T], app_dict: Mapping[str, Any]) -> T:
        d = dict(app_dict)
        id = d.pop("id")

        title = d.pop("title")

        active = d.pop("active", UNSET)

        def _parse_bg_color(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        bg_color = _parse_bg_color(d.pop("bg_color", UNSET))

        def _parse_href(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        href = _parse_href(d.pop("href", UNSET))

        def _parse_image_thumbnail_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        image_thumbnail_url = _parse_image_thumbnail_url(
            d.pop("image_thumbnail_url", UNSET)
        )

        def _parse_image_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        image_url = _parse_image_url(d.pop("image_url", UNSET))

        def _parse_subtitle(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        subtitle = _parse_subtitle(d.pop("subtitle", UNSET))

        def _parse_text_color(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        text_color = _parse_text_color(d.pop("text_color", UNSET))

        banner_row = cls(
            id=id,
            title=title,
            active=active,
            bg_color=bg_color,
            href=href,
            image_thumbnail_url=image_thumbnail_url,
            image_url=image_url,
            subtitle=subtitle,
            text_color=text_color,
        )

        return banner_row
