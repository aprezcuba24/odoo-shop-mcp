"""Helpers for cart line serialization."""

from __future__ import annotations

from app.services.cart.base import CartLine


def lines_payload(lines: list[CartLine]) -> list[dict[str, float | int]]:
    return [{"product_id": line.product_id, "qty": line.qty} for line in lines]
