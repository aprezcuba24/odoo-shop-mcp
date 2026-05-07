from enum import Enum


class SaleOrderDetailResponseStoreState(str, Enum):
    CANCELED = "canceled"
    DELIVERED = "delivered"
    NEGOTIATING = "negotiating"
    READY_FOR_DELIVERY = "ready_for_delivery"
    REVIEWING = "reviewing"

    def __str__(self) -> str:
        return str(self.value)
