from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.product_category_row import ProductCategoryRow


T = TypeVar("T", bound="ProductListRow")


@_attrs_define
class ProductListRow:
    """
    Attributes:
        id (int):
        list_price (float):
        name (str):
        barcode (None | str | Unset):
        category (None | ProductCategoryRow | Unset):
        default_code (None | str | Unset):
        image_thumbnail_url (None | str | Unset):
        image_url (None | str | Unset):
        uom_name (None | str | Unset):
    """

    id: int
    list_price: float
    name: str
    barcode: None | str | Unset = UNSET
    category: None | ProductCategoryRow | Unset = UNSET
    default_code: None | str | Unset = UNSET
    image_thumbnail_url: None | str | Unset = UNSET
    image_url: None | str | Unset = UNSET
    uom_name: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.product_category_row import ProductCategoryRow

        id = self.id

        list_price = self.list_price

        name = self.name

        barcode: None | str | Unset
        if isinstance(self.barcode, Unset):
            barcode = UNSET
        else:
            barcode = self.barcode

        category: dict[str, Any] | None | Unset
        if isinstance(self.category, Unset):
            category = UNSET
        elif isinstance(self.category, ProductCategoryRow):
            category = self.category.to_dict()
        else:
            category = self.category

        default_code: None | str | Unset
        if isinstance(self.default_code, Unset):
            default_code = UNSET
        else:
            default_code = self.default_code

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

        uom_name: None | str | Unset
        if isinstance(self.uom_name, Unset):
            uom_name = UNSET
        else:
            uom_name = self.uom_name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "list_price": list_price,
                "name": name,
            }
        )
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if category is not UNSET:
            field_dict["category"] = category
        if default_code is not UNSET:
            field_dict["default_code"] = default_code
        if image_thumbnail_url is not UNSET:
            field_dict["image_thumbnail_url"] = image_thumbnail_url
        if image_url is not UNSET:
            field_dict["image_url"] = image_url
        if uom_name is not UNSET:
            field_dict["uom_name"] = uom_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.product_category_row import ProductCategoryRow

        d = dict(src_dict)
        id = d.pop("id")

        list_price = d.pop("list_price")

        name = d.pop("name")

        def _parse_barcode(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        barcode = _parse_barcode(d.pop("barcode", UNSET))

        def _parse_category(data: object) -> None | ProductCategoryRow | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                category_type_0 = ProductCategoryRow.from_dict(data)

                return category_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProductCategoryRow | Unset, data)

        category = _parse_category(d.pop("category", UNSET))

        def _parse_default_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        default_code = _parse_default_code(d.pop("default_code", UNSET))

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

        def _parse_uom_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        uom_name = _parse_uom_name(d.pop("uom_name", UNSET))

        product_list_row = cls(
            id=id,
            list_price=list_price,
            name=name,
            barcode=barcode,
            category=category,
            default_code=default_code,
            image_thumbnail_url=image_thumbnail_url,
            image_url=image_url,
            uom_name=uom_name,
        )

        return product_list_row
