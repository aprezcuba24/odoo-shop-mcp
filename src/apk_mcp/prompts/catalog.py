"""Prompts de catálogo — búsqueda guiada de productos con resolución de categoría."""

from __future__ import annotations

from fastmcp.prompts import Message

from apk_mcp.server import mcp


@mcp.prompt(
    name="find_products",
    description=(
        "Búsqueda guiada de productos: resuelve el nombre de categoría a su ID y llama a "
        "list_products con search y category_id. Entrega una lista con nombre, precio, "
        "unidad de medida e id lista para pedir."
    ),
)
def find_products(
    query: str,
    category: str | None = None,
    limit: int = 20,
) -> list[Message]:
    lines = [
        f'El usuario busca productos que coincidan con "{query}".',
    ]
    if category:
        lines += [
            f'Quiere filtrar por la categoría "{category}".',
            "1. Lee el recurso yy-shop://catalog/categories para obtener la lista completa de categorías.",
            f'2. Encuentra la categoría cuyo nombre coincide mejor (sin distinguir mayúsculas) con '
            f'"{category}" y anota su id.',
            "3. Llama a list_products con ese category_id, la consulta de búsqueda indicada abajo y el limit dado.",
        ]
    else:
        lines.append("1. Llama a list_products con la consulta de búsqueda y el limit indicados abajo.")

    lines += [
        f'   search="{query}", limit={limit}',
        "4. Presenta los resultados en una lista breve: nombre del producto, precio, unidad de medida (uom_name) e id.",
        "   Si no hay productos, dilo claramente y sugiere ampliar la búsqueda.",
    ]
    return [Message("\n".join(lines))]
