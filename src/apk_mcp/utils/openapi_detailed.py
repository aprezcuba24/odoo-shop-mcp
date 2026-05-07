"""Helpers for openapi-python-client ``asyncio_detailed`` modules."""

from __future__ import annotations

import json
from collections.abc import Sequence
from http import HTTPStatus
from typing import Any

from apk_mcp.generated.order_bridge_client import Client
from apk_mcp.generated.order_bridge_client.models.message_error_response import (
    MessageErrorResponse,
)
from apk_mcp.generated.order_bridge_client.models.validation_error_response import (
    ValidationErrorResponse,
)
from apk_mcp.generated.order_bridge_client.types import UNSET, Response, Unset

from apk_mcp.utils.exceptions import (
    ApkApiError,
    MessageApiError,
    NotFoundError,
    UnauthorizedError,
    ValidationApiError,
)

DEFAULT_BAD_REQUEST_SPEC: tuple[tuple[type[Any], type[ApkApiError]], ...] = (
    (ValidationErrorResponse, ValidationApiError),
    (MessageErrorResponse, MessageApiError),
)


def message_from_error_body(body: dict[str, Any] | None, fallback: str) -> str:
    if not body:
        return fallback.strip()
    m = body.get("message")
    if isinstance(m, str) and m:
        return m
    e = body.get("error")
    if isinstance(e, str) and e:
        return e
    return fallback.strip()


def body_from_content(content: bytes) -> dict[str, Any] | None:
    try:
        raw = json.loads(content.decode())
        return raw if isinstance(raw, dict) else None
    except Exception:
        return None


def raise_apk_http(*, status_code: int, content: bytes, fallback_text: str) -> None:
    body = body_from_content(content)
    msg = message_from_error_body(body, fallback_text)
    if status_code == 401:
        raise UnauthorizedError(msg or "Unauthorized", status_code=status_code, body=body)
    if status_code == 404:
        raise NotFoundError(msg or "Not found", status_code=status_code, body=body)
    if status_code == 400:
        err = (body or {}).get("error") if body else None
        if err == "validation" or (body and "details" in body):
            raise ValidationApiError(msg or "Validation error", status_code=status_code, body=body)
        raise ValidationApiError(msg or "Bad request", status_code=status_code, body=body)
    raise ApkApiError(msg or f"HTTP {status_code}", status_code=status_code, body=body)


async def client_helper(
    endpoint: Any,
    client: Client,
    *,
    success_type: type[Any],
    unexpected_shape_message: str = "Unexpected API response shape",
    bad_request_spec: Sequence[tuple[type[Any], type[ApkApiError]]] = DEFAULT_BAD_REQUEST_SPEC,
    **kwargs: Any,
) -> dict[str, Any]:
    """Call ``endpoint.asyncio_detailed``, map HTTP status to app errors, return ``to_dict()`` on success.

    ``endpoint`` is a generated API module (e.g. ``order_bridge_products``) exposing ``asyncio_detailed``.
    ``bad_request_spec`` pairs attrs response types for HTTP 400 with ``ApkApiError`` subclasses to raise.
    Defaults to validation + message error bodies; pass ``()`` to skip and use generic HTTP 400 handling.
    """
    detailed = getattr(endpoint, "asyncio_detailed", None)
    if detailed is None:
        raise TypeError("endpoint must expose asyncio_detailed")

    resp: Response[Any] = await detailed(client=client, **kwargs)
    parsed = resp.parsed
    code = resp.status_code.value

    if resp.status_code == HTTPStatus.OK:
        if not isinstance(parsed, success_type):
            raise ApkApiError(
                unexpected_shape_message,
                status_code=code,
                body=None,
            )
        return parsed.to_dict()

    if resp.status_code == HTTPStatus.BAD_REQUEST:
        for model_type, exc_type in bad_request_spec:
            if isinstance(parsed, model_type):
                d = parsed.to_dict()
                raise exc_type(
                    message_from_error_body(d, ""),
                    status_code=code,
                    body=d,
                )
        raise_apk_http(
            status_code=code,
            content=resp.content,
            fallback_text=resp.content.decode(errors="replace"),
        )

    raise_apk_http(
        status_code=code,
        content=resp.content,
        fallback_text=resp.content.decode(errors="replace"),
    )

def unset_int(value: int | None) -> int | Unset:
    return UNSET if value is None else value


def unset_str(value: str | None) -> str | Unset:
    return UNSET if value is None else value
