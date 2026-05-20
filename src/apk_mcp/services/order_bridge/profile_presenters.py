"""Presentación de perfil de contacto para el agente MCP (vista pública + bloque _agent)."""

from __future__ import annotations

from typing import Any

_ADDRESS_PUBLIC_KEYS = frozenset(
    {"street", "state", "municipality_name", "neighborhood_name"}
)
_ADDRESS_ID_KEYS = frozenset({"municipality_id", "neighborhood_id"})


def _present_address(raw: dict[str, Any] | None) -> dict[str, Any] | None:
    if raw is None:
        return None
    return {k: raw[k] for k in _ADDRESS_PUBLIC_KEYS if k in raw}


def present_profile(raw: dict[str, Any]) -> dict[str, Any]:
    public: dict[str, Any] = {
        "name": raw["name"],
        "phone": raw["phone"],
        "address": _present_address(raw.get("address")),
    }
    agent: dict[str, Any] = {"contact_id": raw["id"]}
    address = raw.get("address")
    if isinstance(address, dict):
        addr_agent: dict[str, Any] = {}
        for key in _ADDRESS_ID_KEYS:
            if key in address:
                addr_agent[key] = address[key]
        if addr_agent:
            agent["address"] = addr_agent
    public["_agent"] = agent
    return public
