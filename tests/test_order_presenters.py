"""Unit tests for order response presenters."""

from __future__ import annotations

from app.services.order_bridge.order_presenters import (
    present_insufficient_stock,
    present_order_cancelled,
    present_order_created,
    present_order_detail,
    present_order_summary,
    present_orders_page,
)

_RAW_SUMMARY = {
    "id": 101,
    "name": "S00101",
    "state": "draft",
    "store_state": "reviewing",
    "origin": "MCP",
    "device_validated": True,
    "amount_total": 450.0,
    "currency": "CUP",
    "order_ref": "REF-1",
    "delivery_status": "pending",
    "delivery_address": {
        "street": "Calle 5",
        "state": "Holguín",
        "municipality_id": 8,
        "municipality_name": "Holguín",
        "neighborhood_id": 42,
        "neighborhood_name": "Peralta",
    },
}

_RAW_LINE = {
    "name": "Leche entera 1L",
    "product_id": 12,
    "qty": 2.0,
    "price_unit": 120.0,
    "price_subtotal": 240.0,
    "qty_delivered": 0.0,
    "qty_reserved": 2.0,
}


def test_present_order_summary_strips_internal_fields() -> None:
    result = present_order_summary(_RAW_SUMMARY)

    assert result["order_number"] == "S00101"
    assert result["status"] == "En revisión"
    assert result["amount_total"] == 450.0
    assert "id" not in result
    assert "state" not in result
    assert "device_validated" not in result
    assert "origin" not in result
    assert "order_ref" not in result
    assert "delivery_status" not in result
    assert result["_agent"]["order_id"] == 101
    assert result["_agent"]["store_state"] == "reviewing"
    addr = result["delivery_address"]
    assert "municipality_id" not in addr
    assert "neighborhood_id" not in addr
    assert addr["street"] == "Calle 5"


def test_present_order_detail_lines_and_agent() -> None:
    raw = {**_RAW_SUMMARY, "lines": [_RAW_LINE]}
    result = present_order_detail(raw)

    assert len(result["lines"]) == 1
    line = result["lines"][0]
    assert line["name"] == "Leche entera 1L"
    assert "product_id" not in line
    assert "qty_delivered" not in line
    assert result["_agent"]["lines"] == [{"product_id": 12, "qty": 2.0}]


def test_present_order_created() -> None:
    raw = {
        "id": 102,
        "name": "S00102",
        "state": "draft",
        "store_state": "reviewing",
        "device_validated": True,
        "order_ref": None,
    }
    result = present_order_created(raw)

    assert result["order_number"] == "S00102"
    assert result["status"] == "En revisión"
    assert "state" not in result
    assert result["_agent"]["order_id"] == 102


def test_present_orders_page() -> None:
    raw = {"items": [_RAW_SUMMARY], "limit": 10, "offset": 0, "total": 1}
    result = present_orders_page(raw)

    assert result["total"] == 1
    assert len(result["items"]) == 1
    assert result["items"][0]["order_number"] == "S00101"


def test_present_order_cancelled() -> None:
    result = present_order_cancelled({"id": 99, "state": "cancel"})

    assert result["status"] == "Cancelado"
    assert result["_agent"]["order_id"] == 99


def test_present_insufficient_stock() -> None:
    body = {
        "error": "insufficient_stock",
        "message": "Solo hay 1 unidad.",
        "products": [{"product_id": 5, "available_qty": 1.0}],
    }
    lines = [{"product_id": 5, "qty": 2.0}]
    result = present_insufficient_stock(body, lines_submitted=lines)

    assert result["ok"] is False
    assert result["products"] == [{"available_qty": 1.0}]
    assert "product_id" not in result["products"][0]
    assert result["_agent"]["products"] == [{"product_id": 5, "available_qty": 1.0}]
    assert result["_agent"]["lines_submitted"] == lines
