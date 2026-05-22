"""In-memory shopping cart (development)."""

from __future__ import annotations

import asyncio

from app.services.cart.base import CartLine, CartStoreKey, normalize_lines


def _storage_key(key: CartStoreKey) -> str:
    return f"{key.backend}\0{key.token}"


class InMemoryCartStore:
    """Per-process cart storage keyed by backend domain + token."""

    __slots__ = ("_carts", "_lock")

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._carts: dict[str, dict[int, float]] = {}

    async def add_line(
        self,
        key: CartStoreKey,
        *,
        product_id: int,
        quantity: float,
    ) -> list[CartLine]:
        if quantity <= 0:
            raise ValueError("quantity must be greater than 0.")

        storage_key = _storage_key(key)
        async with self._lock:
            cart = self._carts.setdefault(storage_key, {})
            cart[product_id] = cart.get(product_id, 0.0) + quantity
            return normalize_lines(cart)

    async def get_lines(self, key: CartStoreKey) -> list[CartLine]:
        storage_key = _storage_key(key)
        async with self._lock:
            cart = self._carts.get(storage_key)
            if not cart:
                return []
            return normalize_lines(cart)

    async def clear(self, key: CartStoreKey) -> None:
        storage_key = _storage_key(key)
        async with self._lock:
            self._carts.pop(storage_key, None)
