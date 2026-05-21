"""Encode/decode shop-key header: Bearer base64(BASE_URL|user_token)."""

from __future__ import annotations

import base64
import re
from dataclasses import dataclass
from urllib.parse import urlparse

from fastmcp.server.dependencies import get_http_request

from apk_mcp.services.cart.base import CartStoreKey
from apk_mcp.utils.exceptions import InvalidShopKeyError, MissingShopKeyError

SHOP_KEY_HEADER = "shop-key"
SHOP_KEY_BEARER_PREFIX = "Bearer "

_INVALID_SHOP_KEY_MSG = (
    "Invalid shop-key: expected Bearer base64(BASE_URL|user_token)."
)
_SHOP_KEY_HEADER_RE = re.compile(r"^Bearer\s+(\S+)\s*$", re.IGNORECASE)
_CREDENTIALS_PAYLOAD_RE = re.compile(r"^(.+)\|(.+)$")


@dataclass(frozen=True, slots=True)
class ShopContext:
    """Decoded shop-key: backend URL, Bearer token, and raw header value."""

    storage_key: str
    base_url: str
    bearer_token: str
    user_token: str

    def cart_store_key(self) -> CartStoreKey:
        return CartStoreKey(
            backend=backend_domain(self.base_url),
            token=self.user_token,
        )


def backend_domain(base_url: str) -> str:
    """Extract host (netloc) from base_url without scheme (e.g. https://)."""
    url = base_url if "://" in base_url else f"//{base_url}"
    netloc = urlparse(url).netloc
    return netloc or base_url.strip("/")


def _payload_base64(base_url: str, user_token: str) -> str:
    payload = f"{base_url.rstrip('/')}|{user_token}"
    return base64.b64encode(payload.encode()).decode()


def encode_shop_key(base_url: str, user_token: str) -> str:
    """Build the shop-key header value: ``Bearer`` + base64(``BASE_URL|user_token``)."""
    return f"{SHOP_KEY_BEARER_PREFIX}{_payload_base64(base_url, user_token)}"


def encode_shop_key_from_credentials(credentials: str) -> str:
    """Encode ``BASE_URL|user_token`` into a full shop-key header value."""
    base_url, _, user_token = credentials.partition("|")
    return encode_shop_key(base_url.rstrip("/"), user_token.strip())


def decode_shop_key(raw: str) -> ShopContext:
    """Validate Bearer base64(BASE_URL|user_token) and return decoded context."""
    header = raw.strip()
    header_match = _SHOP_KEY_HEADER_RE.match(header)
    if not header_match:
        raise InvalidShopKeyError(_INVALID_SHOP_KEY_MSG)

    try:
        decoded = base64.b64decode(
            header_match.group(1), validate=True
        ).decode()
    except Exception as exc:
        raise InvalidShopKeyError(_INVALID_SHOP_KEY_MSG) from exc

    payload_match = _CREDENTIALS_PAYLOAD_RE.match(decoded)
    if not payload_match:
        raise InvalidShopKeyError(_INVALID_SHOP_KEY_MSG)

    base_url = payload_match.group(1).rstrip("/")
    user_token = payload_match.group(2).strip()
    bearer_token = (
        user_token
        if user_token.lower().startswith("bearer ")
        else f"Bearer {user_token}"
    )

    return ShopContext(
        storage_key=header,
        base_url=base_url,
        bearer_token=bearer_token,
        user_token=user_token,
    )


def _read_shop_key_header() -> str:
    try:
        request = get_http_request()
    except RuntimeError as exc:
        raise MissingShopKeyError(
            "No HTTP request context; cannot resolve shop-key. "
            "Use Streamable HTTP with the shop-key header."
        ) from exc

    raw = request.headers.get(SHOP_KEY_HEADER)
    if raw:
        return raw

    raise MissingShopKeyError(f"Missing required HTTP header {SHOP_KEY_HEADER!r}.")


def resolve_shop_context() -> ShopContext:
    """Decode shop-key header from the current HTTP request."""
    return decode_shop_key(_read_shop_key_header())


def resolve_shop_key() -> str:
    """Full shop-key header value (legacy; cart uses cart_store_key())."""
    return resolve_shop_context().storage_key
