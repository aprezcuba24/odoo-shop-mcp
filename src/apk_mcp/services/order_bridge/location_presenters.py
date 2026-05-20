"""Presentación de nomencladores de ubicación para el agente MCP (vista pública + bloque _agent)."""

from __future__ import annotations

from typing import Any


def present_neighborhood_row(raw: dict[str, Any]) -> dict[str, Any]:
    return {"name": raw["name"]}


def present_municipality_row(raw: dict[str, Any]) -> dict[str, Any]:
    neighborhoods = raw.get("neighborhoods") or []
    return {
        "name": raw["name"],
        "neighborhoods": [present_neighborhood_row(nb) for nb in neighborhoods],
        "_agent": {
            "municipality_id": raw["id"],
            "neighborhoods": [
                {"neighborhood_id": nb["id"], "name": nb["name"]}
                for nb in neighborhoods
            ],
        },
    }


def present_municipalities_list(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "items": [present_municipality_row(item) for item in (raw.get("items") or [])],
        "total": raw["total"],
    }
