"""Presenters for ChatGPT-compatible search/fetch tool responses."""

from __future__ import annotations

import json
from typing import Any


def product_uri(product_id: int) -> str:
    return f"apk://catalog/products/{product_id}"


def present_search_results(page: dict[str, Any]) -> dict[str, Any]:
    """OpenAI connector search shape: { results: [{ id, title, url }] }."""
    results = []
    for item in page.get("items", []):
        product_id = item["id"]
        results.append(
            {
                "id": str(product_id),
                "title": item["name"],
                "url": product_uri(product_id),
            }
        )
    return {"results": results}


def present_fetch_product(detail: dict[str, Any], *, product_id: int) -> dict[str, Any]:
    """OpenAI connector fetch shape: { id, title, text, url, metadata? }."""
    return {
        "id": str(product_id),
        "title": detail.get("name", ""),
        "text": json.dumps(detail, ensure_ascii=False),
        "url": product_uri(product_id),
        "metadata": {"type": "product"},
    }
