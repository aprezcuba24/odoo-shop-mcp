from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="GeneralSettingsResponse")


@_attrs_define
class GeneralSettingsResponse:
    """`GET /api/order_bridge/settings` — datos generales de la tienda (catálogo).

    Attributes:
        shop_phone (None | str | Unset):
    """

    shop_phone: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        shop_phone: None | str | Unset
        if isinstance(self.shop_phone, Unset):
            shop_phone = UNSET
        else:
            shop_phone = self.shop_phone

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if shop_phone is not UNSET:
            field_dict["shop_phone"] = shop_phone

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_shop_phone(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        shop_phone = _parse_shop_phone(d.pop("shop_phone", UNSET))

        general_settings_response = cls(
            shop_phone=shop_phone,
        )

        return general_settings_response
