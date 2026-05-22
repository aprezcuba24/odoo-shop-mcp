"""Cart service (in-memory or DynamoDB)."""

from app.services.cart.base import CartLine, CartStore, CartStoreKey
from app.services.cart.factory import create_cart_store
from app.services.cart.helpers import lines_payload
from app.services.cart.memory import InMemoryCartStore
from app.services.cart.dynamodb import DynamoDBCartStore

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
