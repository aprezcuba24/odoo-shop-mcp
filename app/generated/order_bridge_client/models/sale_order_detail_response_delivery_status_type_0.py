from enum import Enum


class SaleOrderDetailResponseDeliveryStatusType0(str, Enum):
    FULL = "full"
    PARTIAL = "partial"
    PENDING = "pending"
    STARTED = "started"

    def __str__(self) -> str:
        return str(self.value)
