from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.sale_order_detail_response_delivery_status_type_0 import (
    SaleOrderDetailResponseDeliveryStatusType0,
)
from ..models.sale_order_detail_response_store_state import (
    SaleOrderDetailResponseStoreState,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.delivery_address_out import DeliveryAddressOut
    from ..models.sale_order_line_out import SaleOrderLineOut


T = TypeVar("T", bound="SaleOrderDetailResponse")


@_attrs_define
class SaleOrderDetailResponse:
    """
    Attributes:
        amount_total (float):
        device_validated (bool):
        id (int):
        lines (list[SaleOrderLineOut]):
        name (str):
        origin (str):
        state (str):
        store_state (SaleOrderDetailResponseStoreState):
        currency (None | str | Unset):
        date_order (None | str | Unset):
        delivery_address (DeliveryAddressOut | None | Unset):
        delivery_status (None | SaleOrderDetailResponseDeliveryStatusType0 | Unset):
        effective_date (None | str | Unset):
        order_ref (None | str | Unset):
    """

    amount_total: float
    device_validated: bool
    id: int
    lines: list[SaleOrderLineOut]
    name: str
    origin: str
    state: str
    store_state: SaleOrderDetailResponseStoreState
    currency: None | str | Unset = UNSET
    date_order: None | str | Unset = UNSET
    delivery_address: DeliveryAddressOut | None | Unset = UNSET
    delivery_status: None | SaleOrderDetailResponseDeliveryStatusType0 | Unset = UNSET
    effective_date: None | str | Unset = UNSET
    order_ref: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.delivery_address_out import DeliveryAddressOut

        amount_total = self.amount_total

        device_validated = self.device_validated

        id = self.id

        lines = []
        for lines_item_data in self.lines:
            lines_item = lines_item_data.to_dict()
            lines.append(lines_item)

        name = self.name

        origin = self.origin

        state = self.state

        store_state = self.store_state.value

        currency: None | str | Unset
        if isinstance(self.currency, Unset):
            currency = UNSET
        else:
            currency = self.currency

        date_order: None | str | Unset
        if isinstance(self.date_order, Unset):
            date_order = UNSET
        else:
            date_order = self.date_order

        delivery_address: dict[str, Any] | None | Unset
        if isinstance(self.delivery_address, Unset):
            delivery_address = UNSET
        elif isinstance(self.delivery_address, DeliveryAddressOut):
            delivery_address = self.delivery_address.to_dict()
        else:
            delivery_address = self.delivery_address

        delivery_status: None | str | Unset
        if isinstance(self.delivery_status, Unset):
            delivery_status = UNSET
        elif isinstance(
            self.delivery_status, SaleOrderDetailResponseDeliveryStatusType0
        ):
            delivery_status = self.delivery_status.value
        else:
            delivery_status = self.delivery_status

        effective_date: None | str | Unset
        if isinstance(self.effective_date, Unset):
            effective_date = UNSET
        else:
            effective_date = self.effective_date

        order_ref: None | str | Unset
        if isinstance(self.order_ref, Unset):
            order_ref = UNSET
        else:
            order_ref = self.order_ref

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "amount_total": amount_total,
                "device_validated": device_validated,
                "id": id,
                "lines": lines,
                "name": name,
                "origin": origin,
                "state": state,
                "store_state": store_state,
            }
        )
        if currency is not UNSET:
            field_dict["currency"] = currency
        if date_order is not UNSET:
            field_dict["date_order"] = date_order
        if delivery_address is not UNSET:
            field_dict["delivery_address"] = delivery_address
        if delivery_status is not UNSET:
            field_dict["delivery_status"] = delivery_status
        if effective_date is not UNSET:
            field_dict["effective_date"] = effective_date
        if order_ref is not UNSET:
            field_dict["order_ref"] = order_ref

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.delivery_address_out import DeliveryAddressOut
        from ..models.sale_order_line_out import SaleOrderLineOut

        d = dict(src_dict)
        amount_total = d.pop("amount_total")

        device_validated = d.pop("device_validated")

        id = d.pop("id")

        lines = []
        _lines = d.pop("lines")
        for lines_item_data in _lines:
            lines_item = SaleOrderLineOut.from_dict(lines_item_data)

            lines.append(lines_item)

        name = d.pop("name")

        origin = d.pop("origin")

        state = d.pop("state")

        store_state = SaleOrderDetailResponseStoreState(d.pop("store_state"))

        def _parse_currency(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        currency = _parse_currency(d.pop("currency", UNSET))

        def _parse_date_order(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        date_order = _parse_date_order(d.pop("date_order", UNSET))

        def _parse_delivery_address(data: object) -> DeliveryAddressOut | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                delivery_address_type_0 = DeliveryAddressOut.from_dict(data)

                return delivery_address_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeliveryAddressOut | None | Unset, data)

        delivery_address = _parse_delivery_address(d.pop("delivery_address", UNSET))

        def _parse_delivery_status(
            data: object,
        ) -> None | SaleOrderDetailResponseDeliveryStatusType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                delivery_status_type_0 = SaleOrderDetailResponseDeliveryStatusType0(
                    data
                )

                return delivery_status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SaleOrderDetailResponseDeliveryStatusType0 | Unset, data)

        delivery_status = _parse_delivery_status(d.pop("delivery_status", UNSET))

        def _parse_effective_date(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        effective_date = _parse_effective_date(d.pop("effective_date", UNSET))

        def _parse_order_ref(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        order_ref = _parse_order_ref(d.pop("order_ref", UNSET))

        sale_order_detail_response = cls(
            amount_total=amount_total,
            device_validated=device_validated,
            id=id,
            lines=lines,
            name=name,
            origin=origin,
            state=state,
            store_state=store_state,
            currency=currency,
            date_order=date_order,
            delivery_address=delivery_address,
            delivery_status=delivery_status,
            effective_date=effective_date,
            order_ref=order_ref,
        )

        return sale_order_detail_response
