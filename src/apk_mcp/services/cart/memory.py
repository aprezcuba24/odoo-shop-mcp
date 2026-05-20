"""In-memory shopping cart keyed by shop-key (resolve_shop_key)."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CartLine:
    product_id: int
    qty: float


def _normalize_lines(lines: dict[int, float]) -> list[CartLine]:
    return [
        CartLine(product_id=product_id, qty=qty)
        for product_id, qty in sorted(lines.items())
    ]


class InMemoryCartStore:
    """Per-process cart storage: storage_key -> {product_id: qty}."""

    __slots__ = ("_carts", "_lock")

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._carts: dict[str, dict[int, float]] = {}

    async def add_line(
        self,
        storage_key: str,
        *,
        product_id: int,
        quantity: float,
    ) -> list[CartLine]:
        if quantity <= 0:
            raise ValueError("quantity must be greater than 0.")

        async with self._lock:
            cart = self._carts.setdefault(storage_key, {})
            cart[product_id] = cart.get(product_id, 0.0) + quantity
            return _normalize_lines(cart)

    async def get_lines(self, storage_key: str) -> list[CartLine]:
        async with self._lock:
            cart = self._carts.get(storage_key)
            if not cart:
                return []
            return _normalize_lines(cart)

    async def clear(self, storage_key: str) -> None:
        async with self._lock:
            self._carts.pop(storage_key, None)


cart_store = InMemoryCartStore()
