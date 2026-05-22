from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="PaginationMeta")


@_attrs_define
class PaginationMeta:
    """
    Attributes:
        limit (int):
        offset (int):
        total (int):
    """

    limit: int
    offset: int
    total: int

    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        offset = self.offset

        total = self.total

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "limit": limit,
                "offset": offset,
                "total": total,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], app_dict: Mapping[str, Any]) -> T:
        d = dict(app_dict)
        limit = d.pop("limit")

        offset = d.pop("offset")

        total = d.pop("total")

        pagination_meta = cls(
            limit=limit,
            offset=offset,
            total=total,
        )

        return pagination_meta
