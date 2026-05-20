"""Unit tests for location response presenters."""

from __future__ import annotations

from apk_mcp.services.order_bridge.location_presenters import (
    present_municipalities_list,
    present_municipality_row,
)

_RAW_MUNICIPALITY = {
    "id": 8,
    "name": "Holguín",
    "neighborhoods": [
        {"id": 42, "name": "Peralta"},
        {"id": 43, "name": "Centro"},
    ],
}

_RAW_LIST = {
    "items": [_RAW_MUNICIPALITY],
    "total": 1,
}


def test_present_municipality_row_strips_public_ids() -> None:
    result = present_municipality_row(_RAW_MUNICIPALITY)

    assert result["name"] == "Holguín"
    assert "id" not in result
    assert len(result["neighborhoods"]) == 2
    assert result["neighborhoods"][0] == {"name": "Peralta"}
    assert "id" not in result["neighborhoods"][0]
    assert result["_agent"]["municipality_id"] == 8
    assert result["_agent"]["neighborhoods"] == [
        {"neighborhood_id": 42, "name": "Peralta"},
        {"neighborhood_id": 43, "name": "Centro"},
    ]


def test_present_municipalities_list() -> None:
    result = present_municipalities_list(_RAW_LIST)

    assert result["total"] == 1
    assert len(result["items"]) == 1
    item = result["items"][0]
    assert item["name"] == "Holguín"
    assert "id" not in item
    assert item["_agent"]["municipality_id"] == 8
