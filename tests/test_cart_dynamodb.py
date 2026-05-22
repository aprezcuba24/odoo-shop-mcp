"""Unit tests for DynamoDB cart store (mocked boto3 client)."""

from __future__ import annotations

import asyncio
from decimal import Decimal
from unittest.mock import MagicMock

from app.services.cart.base import CartStoreKey
from app.services.cart.dynamodb import DynamoDBCartStore

_KEY = CartStoreKey(backend="tienda.example.com", token="device-token-1")
_TABLE = "test-cart-table"


def _empty_get_response() -> dict:
    return {}


def _item_with_lines(lines: dict[int, float]) -> dict:
    return {
        "Item": {
            "backend": {"S": _KEY.backend},
            "token": {"S": _KEY.token},
            "lines": {
                "M": {str(pid): {"N": str(qty)} for pid, qty in lines.items()}
            },
        }
    }


def test_add_line_creates_item() -> None:
    async def run() -> None:
        client = MagicMock()
        client.get_item.return_value = _empty_get_response()
        store = DynamoDBCartStore(_TABLE, client=client)

        lines = await store.add_line(_KEY, product_id=3, quantity=2.0)

        assert len(lines) == 1
        assert lines[0].product_id == 3
        assert lines[0].qty == 2.0
        client.get_item.assert_called_once()
        client.put_item.assert_called_once()
        put_args = client.put_item.call_args.kwargs
        assert put_args["TableName"] == _TABLE
        assert put_args["Item"]["backend"]["S"] == _KEY.backend
        assert put_args["Item"]["lines"]["M"]["3"] == Decimal("2.0")

    asyncio.run(run())


def test_add_line_merges_existing() -> None:
    async def run() -> None:
        client = MagicMock()
        client.get_item.return_value = _item_with_lines({3: 1.0})
        store = DynamoDBCartStore(_TABLE, client=client)

        lines = await store.add_line(_KEY, product_id=3, quantity=2.0)

        assert len(lines) == 1
        assert lines[0].qty == 3.0
        put_lines = client.put_item.call_args.kwargs["Item"]["lines"]["M"]
        assert put_lines["3"] == Decimal("3.0")

    asyncio.run(run())


def test_get_lines_empty() -> None:
    async def run() -> None:
        client = MagicMock()
        client.get_item.return_value = _empty_get_response()
        store = DynamoDBCartStore(_TABLE, client=client)

        assert await store.get_lines(_KEY) == []

    asyncio.run(run())


def test_get_lines_returns_normalized() -> None:
    async def run() -> None:
        client = MagicMock()
        client.get_item.return_value = _item_with_lines({4: 1.0, 1: 2.0})
        store = DynamoDBCartStore(_TABLE, client=client)

        lines = await store.get_lines(_KEY)
        assert [(line.product_id, line.qty) for line in lines] == [(1, 2.0), (4, 1.0)]

    asyncio.run(run())


def test_clear_deletes_item() -> None:
    async def run() -> None:
        client = MagicMock()
        store = DynamoDBCartStore(_TABLE, client=client)

        await store.clear(_KEY)

        client.delete_item.assert_called_once_with(
            TableName=_TABLE,
            Key={"backend": _KEY.backend, "token": _KEY.token},
        )

    asyncio.run(run())
