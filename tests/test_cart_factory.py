"""Unit tests for cart store factory."""

from unittest.mock import MagicMock, patch

from apk_mcp.config import Settings
from apk_mcp.services.cart.factory import create_cart_store
from apk_mcp.services.cart.dynamodb import DynamoDBCartStore
from apk_mcp.services.cart.memory import InMemoryCartStore


def test_create_cart_store_memory_default() -> None:
    store = create_cart_store(Settings())
    assert isinstance(store, InMemoryCartStore)


def test_create_cart_store_dynamodb() -> None:
    mock_store = MagicMock(spec=DynamoDBCartStore)
    with patch(
        "apk_mcp.services.cart.factory.DynamoDBCartStore",
        return_value=mock_store,
    ) as mock_cls:
        store = create_cart_store(
            Settings(cart_store_backend="dynamodb", dynamodb_cart_table="my-cart")
        )
    mock_cls.assert_called_once_with(table_name="my-cart")
    assert store is mock_store
