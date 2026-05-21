"""Cart service (in-memory or DynamoDB)."""

from apk_mcp.services.cart.base import CartLine, CartStore, CartStoreKey
from apk_mcp.services.cart.factory import create_cart_store
from apk_mcp.services.cart.helpers import lines_payload
from apk_mcp.services.cart.memory import InMemoryCartStore
from apk_mcp.services.cart.dynamodb import DynamoDBCartStore

cart_store = create_cart_store()

__all__ = [
    "CartLine",
    "CartStore",
    "CartStoreKey",
    "DynamoDBCartStore",
    "InMemoryCartStore",
    "cart_store",
    "create_cart_store",
    "lines_payload",
]
