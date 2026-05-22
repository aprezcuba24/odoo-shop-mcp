from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SaleOrderLineOut")


@_attrs_define
class SaleOrderLineOut:
    """
    Attributes:
        name (str):
        price_subtotal (float):
        price_unit (float):
        product_id (int):
        qty (float):
        qty_delivered (float):
        qty_reserved (float):
        image_thumbnail_url (None | str | Unset):
        image_url (None | str | Unset):
    """

    name: str
    price_subtotal: float
    price_unit: float
    product_id: int
    qty: float
    qty_delivered: float
    qty_reserved: float
    image_thumbnail_url: None | str | Unset = UNSET
    image_url: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        price_subtotal = self.price_subtotal

        price_unit = self.price_unit

        product_id = self.product_id

        qty = self.qty

        qty_delivered = self.qty_delivered

        qty_reserved = self.qty_reserved

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

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "price_subtotal": price_subtotal,
                "price_unit": price_unit,
                "product_id": product_id,
                "qty": qty,
                "qty_delivered": qty_delivered,
                "qty_reserved": qty_reserved,
            }
        )
        if image_thumbnail_url is not UNSET:
            field_dict["image_thumbnail_url"] = image_thumbnail_url
        if image_url is not UNSET:
            field_dict["image_url"] = image_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], app_dict: Mapping[str, Any]) -> T:
        d = dict(app_dict)
        name = d.pop("name")

        price_subtotal = d.pop("price_subtotal")

        price_unit = d.pop("price_unit")

        product_id = d.pop("product_id")

        qty = d.pop("qty")

        qty_delivered = d.pop("qty_delivered")

        qty_reserved = d.pop("qty_reserved")

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

        sale_order_line_out = cls(
            name=name,
            price_subtotal=price_subtotal,
            price_unit=price_unit,
            product_id=product_id,
            qty=qty,
            qty_delivered=qty_delivered,
            qty_reserved=qty_reserved,
            image_thumbnail_url=image_thumbnail_url,
            image_url=image_url,
        )

        return sale_order_line_out
