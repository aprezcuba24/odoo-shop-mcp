from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.order_created_response_delivery_status_type_0 import (
    OrderCreatedResponseDeliveryStatusType0,
)
from ..models.order_created_response_store_state import OrderCreatedResponseStoreState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.delivery_address_out import DeliveryAddressOut


T = TypeVar("T", bound="OrderCreatedResponse")


@_attrs_define
class OrderCreatedResponse:
    """
    Attributes:
        device_validated (bool):
        id (int):
        name (str):
        state (str):
        store_state (OrderCreatedResponseStoreState):
        delivery_address (DeliveryAddressOut | None | Unset):
        delivery_status (None | OrderCreatedResponseDeliveryStatusType0 | Unset):
        effective_date (None | str | Unset):
        order_ref (None | str | Unset):
    """

    device_validated: bool
    id: int
    name: str
    state: str
    store_state: OrderCreatedResponseStoreState
    delivery_address: DeliveryAddressOut | None | Unset = UNSET
    delivery_status: None | OrderCreatedResponseDeliveryStatusType0 | Unset = UNSET
    effective_date: None | str | Unset = UNSET
    order_ref: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.delivery_address_out import DeliveryAddressOut

        device_validated = self.device_validated

        id = self.id

        name = self.name

        state = self.state

        store_state = self.store_state.value

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
        elif isinstance(self.delivery_status, OrderCreatedResponseDeliveryStatusType0):
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
                "device_validated": device_validated,
                "id": id,
                "name": name,
                "state": state,
                "store_state": store_state,
            }
        )
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

        d = dict(src_dict)
        device_validated = d.pop("device_validated")

        id = d.pop("id")

        name = d.pop("name")

        state = d.pop("state")

        store_state = OrderCreatedResponseStoreState(d.pop("store_state"))

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
        ) -> None | OrderCreatedResponseDeliveryStatusType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                delivery_status_type_0 = OrderCreatedResponseDeliveryStatusType0(data)

                return delivery_status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | OrderCreatedResponseDeliveryStatusType0 | Unset, data)

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

        order_created_response = cls(
            device_validated=device_validated,
            id=id,
            name=name,
            state=state,
            store_state=store_state,
            delivery_address=delivery_address,
            delivery_status=delivery_status,
            effective_date=effective_date,
            order_ref=order_ref,
        )

        return order_created_response
