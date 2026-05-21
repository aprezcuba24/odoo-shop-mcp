"""Encode/decode shop-key header: Bearer base64(BASE_URL|user_token)."""

from __future__ import annotations

import base64
from dataclasses import dataclass

from fastmcp.server.dependencies import get_http_request

from apk_mcp.utils.exceptions import InvalidShopKeyError, MissingShopKeyError

SHOP_KEY_HEADER = "shop-key"
SHOP_KEY_BEARER_PREFIX = "Bearer "


@dataclass(frozen=True, slots=True)
class ShopContext:
    """Decoded shop-key: backend URL, Bearer token, and raw header value."""

    storage_key: str
    base_url: str
    bearer_token: str


def parse_credentials(credentials: str) -> tuple[str, str]:
    """Split ``BASE_URL|user_token`` (single pipe, both parts non-empty)."""
    if "|" not in credentials:
        raise InvalidShopKeyError(
            "Credentials must be BASE_URL|user_token (e.g. http://localhost:8069|abc-123)."
        )
    base_url, user_token = credentials.split("|", 1)
    base_url = base_url.strip()
    user_token = user_token.strip()
    if not base_url or not user_token:
        raise InvalidShopKeyError(
            "Credentials BASE_URL and user_token must be non-empty."
        )
    return base_url.rstrip("/"), user_token


def _payload_base64(base_url: str, user_token: str) -> str:
    payload = f"{base_url.rstrip('/')}|{user_token}"
    return base64.b64encode(payload.encode()).decode()


def encode_shop_key(base_url: str, user_token: str) -> str:
    """Build the shop-key header value: ``Bearer`` + base64(``BASE_URL|user_token``)."""
    return f"{SHOP_KEY_BEARER_PREFIX}{_payload_base64(base_url, user_token)}"


def encode_shop_key_from_credentials(credentials: str) -> str:
    """Encode ``BASE_URL|user_token`` into a full shop-key header value."""
    base_url, user_token = parse_credentials(credentials)
    return encode_shop_key(base_url, user_token)


def decode_shop_key(raw: str) -> ShopContext:
    """Decode ``Bearer base64(BASE_URL|user_token)`` into backend URL and API Bearer."""
    header = raw.strip()
    if not header.lower().startswith(SHOP_KEY_BEARER_PREFIX.lower()):
        raise InvalidShopKeyError(
            "shop-key must be 'Bearer ' followed by base64(BASE_URL|user_token)."
        )

    b64_part = header[len(SHOP_KEY_BEARER_PREFIX) :].strip()
    if not b64_part:
        raise InvalidShopKeyError("shop-key Bearer value must not be empty.")

    try:
        decoded = base64.b64decode(b64_part, validate=True).decode()
    except Exception as exc:
        raise InvalidShopKeyError(
            "shop-key must be Bearer + base64-encoded BASE_URL|user_token."
        ) from exc

    base_url, user_token = parse_credentials(decoded)
    bearer_token = (
        user_token
        if user_token.lower().startswith("bearer ")
        else f"Bearer {user_token}"
    )

    return ShopContext(
        storage_key=header,
        base_url=base_url,
        bearer_token=bearer_token,
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
    """Storage key for in-memory cart (full shop-key header value)."""
    return resolve_shop_context().storage_key
