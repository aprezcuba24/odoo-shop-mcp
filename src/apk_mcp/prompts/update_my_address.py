"""Prompt para ver y actualizar perfil: nombre y dirección de entrega."""

from __future__ import annotations

from fastmcp.prompts import Message

from apk_mcp.server import mcp


def _intent_summary(
    *,
    name: str | None,
    street: str | None,
    state: str | None,
    municipality_name: str | None,
    neighborhood_name: str | None,
) -> str | None:
    parts: list[str] = []
    if name:
        parts.append(f"nombre={name!r}")
    if street:
        parts.append(f"calle={street!r}")
    if state:
        parts.append(f"provincia={state!r}")
    if municipality_name:
        parts.append(f"municipio={municipality_name!r}")
    if neighborhood_name:
        parts.append(f"barrio={neighborhood_name!r}")
    if not parts:
        return None
    return "El usuario quiere actualizar su perfil: " + ", ".join(parts) + "."


@mcp.prompt(
    name="update_my_address",
    description=(
        "Guía para ver o actualizar nombre y dirección de entrega del perfil "
        "(resources apk://session/profile y apk://locations/municipalities, tool update_profile)."
    ),
)
def update_my_address(
    street: str | None = None,
    state: str | None = None,
    municipality_name: str | None = None,
    neighborhood_name: str | None = None,
    name: str | None = None,
) -> list[Message]:
    lines: list[str] = []
    summary = _intent_summary(
        name=name,
        street=street,
        state=state,
        municipality_name=municipality_name,
        neighborhood_name=neighborhood_name,
    )
    if summary:
        lines.append(summary)
    lines.extend(
        [
            "La dirección guardada en el perfil es la que usa la tienda al crear "
            "pedidos de entrega (checkout_cart y create_order); conviene tenerla correcta "
            "antes de confirmar una compra.",
            "Lee el resource apk://session/profile y muestra al usuario su nombre, "
            "teléfono y dirección actual (solo campos legibles; no muestres el bloque _agent).",
            "El teléfono del perfil no se puede cambiar con update_profile; si el usuario "
            "pide modificarlo, explícale que no está disponible en esta tienda.",
            "Para cambiar el nombre, llama update_profile con el parámetro name.",
            "Para cambiar la dirección (calle, provincia, municipio, barrio):",
            "  1. Lee apk://locations/municipalities.",
            "  2. Resuelve los nombres de municipio y barrio a municipality_id y "
            "neighborhood_id usando el bloque _agent de cada ítem (no muestres esos IDs al usuario).",
            "  3. Llama update_profile con street, state, municipality_id y neighborhood_id "
            "(solo los campos que cambien respecto al perfil actual).",
            "La respuesta de update_profile ya incluye el perfil actualizado; confirma el "
            "cambio al usuario en lenguaje natural.",
            "Si el municipio o barrio indicado no aparece en el nomenclador, pide al usuario "
            "que aclare o elija de la lista que devuelve el resource de ubicaciones.",
        ]
    )
    return [Message("\n".join(lines))]
