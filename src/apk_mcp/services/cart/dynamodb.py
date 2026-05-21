"""DynamoDB-backed cart store (production / Lambda)."""

from __future__ import annotations

import asyncio
from decimal import Decimal
from typing import Any

from apk_mcp.services.cart.base import CartLine, CartStoreKey, normalize_lines


def _lines_to_dynamo(lines: dict[int, float]) -> dict[str, Decimal]:
    return {str(product_id): Decimal(str(qty)) for product_id, qty in lines.items()}


def _dynamo_number(value: Any) -> float:
    if isinstance(value, dict):
        if "N" in value:
            return float(value["N"])
        if "S" in value:
            return float(value["S"])
    if isinstance(value, Decimal):
        return float(value)
    return float(value)


def _lines_from_dynamo(raw: dict[str, Any] | None) -> dict[int, float]:
    if not raw:
        return {}
    result: dict[int, float] = {}
    for product_id, qty in raw.items():
        result[int(product_id)] = _dynamo_number(qty)
    return result


def _item_key(key: CartStoreKey) -> dict[str, str]:
    return {"backend": key.backend, "token": key.token}


class DynamoDBCartStore:
    """Cart persistence in DynamoDB (PK=backend domain, SK=token)."""

    __slots__ = ("_client", "_table_name")

    def __init__(self, table_name: str, *, client: Any | None = None) -> None:
        if client is None:
            import boto3

            client = boto3.client("dynamodb")
        self._client = client
        self._table_name = table_name

    async def add_line(
        self,
        key: CartStoreKey,
        *,
        product_id: int,
        quantity: float,
    ) -> list[CartLine]:
        if quantity <= 0:
            raise ValueError("quantity must be greater than 0.")

        lines = await self._get_raw_lines(key)
        lines[product_id] = lines.get(product_id, 0.0) + quantity
        await asyncio.to_thread(self._put_lines, key, lines)
        return normalize_lines(lines)

    async def get_lines(self, key: CartStoreKey) -> list[CartLine]:
        lines = await self._get_raw_lines(key)
        return normalize_lines(lines)

    async def clear(self, key: CartStoreKey) -> None:
        await asyncio.to_thread(
            self._client.delete_item,
            TableName=self._table_name,
            Key=_item_key(key),
        )

    async def _get_raw_lines(self, key: CartStoreKey) -> dict[int, float]:
        response = await asyncio.to_thread(
            self._client.get_item,
            TableName=self._table_name,
            Key=_item_key(key),
        )
        item = response.get("Item")
        if not item:
            return {}
        raw_lines = item.get("lines", {}).get("M")
        return _lines_from_dynamo(raw_lines)

    def _put_lines(self, key: CartStoreKey, lines: dict[int, float]) -> None:
        self._client.put_item(
            TableName=self._table_name,
            Item={
                "backend": {"S": key.backend},
                "token": {"S": key.token},
                "lines": {"M": _lines_to_dynamo(lines)},
            },
        )
