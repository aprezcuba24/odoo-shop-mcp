"""Async HTTP client for Tienda Apk ``/api/order_bridge`` REST API."""

from __future__ import annotations

from typing import Any

import httpx
from fastmcp.server.context import Context

from .exceptions import (
    ApkApiError,
    MissingDeviceKeyError,
    NotFoundError,
    UnauthorizedError,
    ValidationApiError,
)
from .session_store import DeviceKeyStore


class ApkApiClient:
    def __init__(
        self,
        client: httpx.AsyncClient,
        store: DeviceKeyStore,
    ) -> None:
        self._client = client
        self._store = store

    def _json_or_raise(self, response: httpx.Response) -> Any:
        if response.is_success:
            return response.json()
        return _raise_for_status(response)

    async def request_json(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: Any = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        r = await self._client.request(
            method,
            path,
            params=params,
            json=json_body,
            headers=headers,
        )
        return self._json_or_raise(r)

    async def get_json(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self.request_json("GET", path, params=params, headers=headers)

    async def post_json(
        self,
        path: str,
        *,
        json_body: Any = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self.request_json(
            "POST", path, params=params, json_body=json_body, headers=headers
        )

    async def put_json(
        self,
        path: str,
        *,
        json_body: Any = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self.request_json(
            "PUT", path, params=params, json_body=json_body, headers=headers
        )

    async def patch_json(
        self,
        path: str,
        *,
        json_body: Any = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self.request_json(
            "PATCH", path, params=params, json_body=json_body, headers=headers
        )

    async def request_authenticated_json(
        self,
        ctx: Context,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: Any = None,
        extra_headers: dict[str, str] | None = None,
    ) -> Any:
        token = await self._store.get(ctx)
        if not token:
            raise MissingDeviceKeyError(
                "No device_key in session or store. Call register_device (or set device key) first."
            )
        headers = dict(extra_headers or {})
        headers["Authorization"] = f"Bearer {token}"
        return await self.request_json(
            method, path, params=params, json_body=json_body, headers=headers
        )


def _raise_for_status(response: httpx.Response) -> Any:
    body: dict[str, Any] | None = None
    try:
        raw = response.json()
        if isinstance(raw, dict):
            body = raw
    except Exception:
        body = None

    msg = _message_from_body(body, response.text)
    code = response.status_code

    if code == 401:
        raise UnauthorizedError(msg or "Unauthorized", status_code=code, body=body)
    if code == 404:
        raise NotFoundError(msg or "Not found", status_code=code, body=body)
    if code == 400:
        err = (body or {}).get("error") if body else None
        if err == "validation" or (body and "details" in body):
            raise ValidationApiError(msg or "Validation error", status_code=code, body=body)
        raise ValidationApiError(msg or "Bad request", status_code=code, body=body)

    raise ApkApiError(msg or f"HTTP {code}", status_code=code, body=body)


def _message_from_body(body: dict[str, Any] | None, fallback: str) -> str:
    if not body:
        return fallback.strip()
    m = body.get("message")
    if isinstance(m, str) and m:
        return m
    e = body.get("error")
    if isinstance(e, str) and e:
        return e
    return fallback.strip()
