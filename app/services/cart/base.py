"""Cart store protocol and shared types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class CartStoreKey:
    """Cart partition: backend domain (netloc) + device user token."""

    backend: str
    token: str


@dataclass(frozen=True, slots=True)
class CartLine:
    product_id: int
    qty: float


def normalize_lines(lines: dict[int, float]) -> list[CartLine]:
    return [
        CartLine(product_id=product_id, qty=qty)
        for product_id, qty in sorted(lines.items())
    ]


@runtime_checkable
class CartStore(Protocol):
    async def add_line(
        self,
        key: CartStoreKey,
        *,
        product_id: int,
        quantity: float,
    ) -> list[CartLine]: ...

    async def get_lines(self, key: CartStoreKey) -> list[CartLine]: ...

    async def clear(self, key: CartStoreKey) -> None: ...
