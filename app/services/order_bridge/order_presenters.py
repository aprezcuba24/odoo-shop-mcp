"""Presentación de respuestas de pedidos para el agente MCP (vista pública + bloque _agent)."""

from __future__ import annotations

from typing import Any

_STORE_STATE_LABELS: dict[str, str] = {
    "reviewing": "En revisión",
    "negotiating": "En negociación",
    "ready_for_delivery": "Listo para entrega",
    "delivered": "Entregado",
    "canceled": "Cancelado",
}

_ADDRESS_ID_KEYS = frozenset({"municipality_id", "neighborhood_id"})


def _status_label(store_state: str | None) -> str | None:
    if store_state is None:
        return None
    return _STORE_STATE_LABELS.get(store_state, store_state)


def _present_address(raw: dict[str, Any] | None) -> dict[str, Any] | None:
    if raw is None:
        return None
    return {k: v for k, v in raw.items() if k not in _ADDRESS_ID_KEYS}


def _present_line(raw: dict[str, Any]) -> dict[str, Any]:
    public: dict[str, Any] = {
        "name": raw["name"],
        "qty": raw["qty"],
        "price_unit": raw["price_unit"],
        "price_subtotal": raw["price_subtotal"],
    }
    if raw.get("image_url") is not None:
        public["image_url"] = raw["image_url"]
    if raw.get("image_thumbnail_url") is not None:
        public["image_thumbnail_url"] = raw["image_thumbnail_url"]
    return public


def _agent_line_refs(raw_lines: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"product_id": ln["product_id"], "qty": ln["qty"]} for ln in raw_lines]


def _public_order_fields(raw: dict[str, Any]) -> dict[str, Any]:
    store_state = raw.get("store_state")
    public: dict[str, Any] = {
        "order_number": raw["name"],
        "status": _status_label(store_state),
    }
    if "amount_total" in raw:
        public["amount_total"] = raw["amount_total"]
    if raw.get("currency") is not None:
        public["currency"] = raw["currency"]
    if raw.get("date_order") is not None:
        public["date_order"] = raw["date_order"]
    if raw.get("effective_date") is not None:
        public["effective_date"] = raw["effective_date"]
    if raw.get("delivery_address") is not None:
        public["delivery_address"] = _present_address(raw["delivery_address"])
    return public


def _agent_order_refs(raw: dict[str, Any], *, lines: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    agent: dict[str, Any] = {
        "order_id": raw["id"],
        "store_state": raw.get("store_state"),
    }
    if lines is not None:
        agent["lines"] = _agent_line_refs(lines)
    return agent


def present_order_summary(raw: dict[str, Any]) -> dict[str, Any]:
    public = _public_order_fields(raw)
    public["_agent"] = _agent_order_refs(raw)
    return public


def present_order_detail(raw: dict[str, Any]) -> dict[str, Any]:
    raw_lines = raw.get("lines") or []
    public = _public_order_fields(raw)
    public["lines"] = [_present_line(ln) for ln in raw_lines]
    public["_agent"] = _agent_order_refs(raw, lines=raw_lines)
    return public


def present_order_created(raw: dict[str, Any]) -> dict[str, Any]:
    store_state = raw.get("store_state")
    public: dict[str, Any] = {
        "order_number": raw["name"],
        "status": _status_label(store_state),
    }
    if raw.get("effective_date") is not None:
        public["effective_date"] = raw["effective_date"]
    if raw.get("delivery_address") is not None:
        public["delivery_address"] = _present_address(raw["delivery_address"])
    public["_agent"] = _agent_order_refs(raw)
    return public


def present_orders_page(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "items": [present_order_summary(item) for item in (raw.get("items") or [])],
        "limit": raw["limit"],
        "offset": raw["offset"],
        "total": raw["total"],
    }


def present_order_cancelled(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "order_number": None,
        "status": "Cancelado",
        "_agent": {
            "order_id": raw["id"],
            "store_state": "canceled",
            "odoo_state": raw.get("state"),
        },
    }


def present_insufficient_stock(
    body: dict[str, Any],
    *,
    lines_submitted: list[dict[str, Any]],
) -> dict[str, Any]:
    raw_products = body.get("products") or []
    return {
        "ok": False,
        "error": "insufficient_stock",
        "message": body.get("message") or "Stock insuficiente para uno o más productos.",
        "products": [
            {
                "product_id": p.get("product_id"),
                "available_qty": p.get("available_qty"),
            }
            for p in raw_products
        ],
        "_agent": {
            "lines_submitted": lines_submitted,
        },
    }
