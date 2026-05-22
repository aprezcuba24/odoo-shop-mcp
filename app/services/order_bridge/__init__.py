"""Order Bridge REST integration."""

from app.services.order_bridge.banners import list_banners
from app.services.order_bridge.categories import list_categories
from app.services.order_bridge.device import get_device_status, register_device
from app.services.order_bridge.locations import list_municipalities
from app.services.order_bridge.orders import (
    cancel_order,
    create_order,
    get_last_order,
    get_order_detail,
    list_orders_page,
)
from app.services.order_bridge.products import get_product_detail, list_products_page
from app.services.order_bridge.profile import get_profile, replace_profile, update_profile
from app.services.order_bridge.push import register_push_token, update_push_topics
from app.services.order_bridge.store import get_settings

__all__ = [
    "cancel_order",
    "create_order",
    "get_device_status",
    "get_last_order",
    "get_order_detail",
    "get_product_detail",
    "get_profile",
    "get_settings",
    "list_banners",
    "list_categories",
    "list_municipalities",
    "list_orders_page",
    "list_products_page",
    "register_device",
    "register_push_token",
    "replace_profile",
    "update_profile",
    "update_push_topics",
]
