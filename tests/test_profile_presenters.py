"""Unit tests for profile response presenters."""

from __future__ import annotations

from apk_mcp.services.order_bridge.profile_presenters import present_profile

_RAW_PROFILE = {
    "id": 101,
    "name": "María López",
    "phone": "+5355512345",
    "address": {
        "street": "Calle 5 #12",
        "state": "Boyeros",
        "municipality_id": 8,
        "municipality_name": "Boyeros",
        "neighborhood_id": 42,
        "neighborhood_name": "Alta Habana",
    },
}


def test_present_profile_strips_address_ids_from_public_view() -> None:
    result = present_profile(_RAW_PROFILE)

    assert result["name"] == "María López"
    assert result["phone"] == "+5355512345"
    addr = result["address"]
    assert addr is not None
    assert addr["street"] == "Calle 5 #12"
    assert addr["state"] == "Holguín"
    assert addr["municipality_name"] == "Holguín"
    assert addr["neighborhood_name"] == "Peralta"
    assert "municipality_id" not in addr
    assert "neighborhood_id" not in addr


def test_present_profile_agent_block() -> None:
    result = present_profile(_RAW_PROFILE)

    assert result["_agent"]["contact_id"] == 101
    assert result["_agent"]["address"] == {
        "municipality_id": 8,
        "neighborhood_id": 42,
    }


def test_present_profile_without_address() -> None:
    raw = {
        "id": 102,
        "name": "Juan",
        "phone": "+5355599999",
        "address": None,
    }

    result = present_profile(raw)

    assert result["address"] is None
    assert result["_agent"] == {"contact_id": 102}
