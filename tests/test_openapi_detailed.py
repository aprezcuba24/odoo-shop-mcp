"""Tests for openapi_detailed HTTP error mapping."""

from __future__ import annotations

import pytest

from app.utils.exceptions import InsufficientStockError, ValidationApiError
from app.utils.openapi_detailed import raise_apk_http, raise_insufficient_stock_if_body


def test_raise_insufficient_stock_if_body() -> None:
    body = {
        "error": "insufficient_stock",
        "message": "Stock insuficiente para uno o más productos",
        "products": [{"product_id": 8, "available_qty": 15.0}],
    }
    with pytest.raises(InsufficientStockError) as exc_info:
        raise_insufficient_stock_if_body(body, status_code=400)

    assert exc_info.value.body == body
    assert exc_info.value.status_code == 400


def test_raise_apk_http_maps_insufficient_stock() -> None:
    content = (
        b'{"error":"insufficient_stock","message":"Stock insuficiente",'
        b'"products":[{"product_id":8,"available_qty":15.0}]}'
    )
    with pytest.raises(InsufficientStockError) as exc_info:
        raise_apk_http(status_code=400, content=content, fallback_text="")

    assert exc_info.value.body is not None
    assert exc_info.value.body["error"] == "insufficient_stock"
    assert exc_info.value.body["products"][0]["product_id"] == 8


def test_raise_apk_http_other_400_stays_validation() -> None:
    content = b'{"error":"invalid_json","message":"JSON mal formado"}'
    with pytest.raises(ValidationApiError):
        raise_apk_http(status_code=400, content=content, fallback_text="")
