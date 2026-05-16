"""Prompts de perfil — actualización de dirección resolviendo IDs de municipio y barrio."""

from __future__ import annotations

from fastmcp.prompts import Message

from apk_mcp.server import mcp


@mcp.prompt(
    name="update_my_address",
    description=(
        "Actualiza la dirección de entrega: resuelve nombres de municipio y barrio a IDs con el "
        "nomenclador de ubicaciones, llama a update_profile (PATCH) y confirma el cambio con get_profile."
    ),
)
def update_my_address(
    street: str,
    state: str,
    municipality_name: str,
    neighborhood_name: str,
) -> list[Message]:
    return [
        Message(
            "El usuario quiere actualizar su dirección de entrega con estos datos:\n"
            f"  Calle: {street}\n"
            f"  Provincia / estado: {state}\n"
            f"  Municipio: {municipality_name}\n"
            f"  Barrio: {neighborhood_name}\n\n"
            "Sigue estos pasos:\n"
            "1. Lee el recurso yy-shop://locations/municipalities para obtener la lista completa de "
            "municipios y sus barrios.\n"
            f'2. Encuentra el municipio cuyo nombre coincide mejor (sin distinguir mayúsculas) con '
            f'"{municipality_name}". Anota su id como municipality_id.\n'
            f'3. Dentro de ese municipio, encuentra el barrio cuyo nombre coincide mejor con '
            f'"{neighborhood_name}". Anota su id como neighborhood_id.\n'
            "4. Si no encuentras alguno, muestra opciones al usuario y pide que elija.\n"
            "5. Llama a update_profile con:\n"
            f'   street="{street}", state="{state}", '
            "municipality_id=<id>, neighborhood_id=<id>.\n"
            "6. Llama a get_profile para verificar la dirección guardada y confirma el cambio al usuario "
            "con un resumen claro."
        )
    ]
