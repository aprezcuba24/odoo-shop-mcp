"""Catalog prompts — guided product search with category resolution."""

from __future__ import annotations

from fastmcp.prompts import Message

from apk_mcp.server import mcp


@mcp.prompt(
    name="find_products",
    description=(
        "Guided product search: resolves a category name to its ID, then calls "
        "list_products with search + category_id. Returns a formatted list with "
        "name, price, unit of measure and id ready for ordering."
    ),
)
def find_products(
    query: str,
    category: str | None = None,
    limit: int = 20,
) -> list[Message]:
    lines = [
        f'The user is looking for products matching "{query}".',
    ]
    if category:
        lines += [
            f'They want to filter by category "{category}".',
            "1. Read the resource apk://catalog/categories to get the full category list.",
            f'2. Find the category whose name (case-insensitive) best matches "{category}" and note its id.',
            "3. Call list_products with that category_id, the search query below, and the given limit.",
        ]
    else:
        lines.append("1. Call list_products with the search query and limit below.")

    lines += [
        f'   search="{query}", limit={limit}',
        "4. Present the results as a concise list: product name, price, unit of measure (uom_name) and id.",
        "   If no products are found, say so clearly and suggest broadening the search.",
    ]
    return [Message("\n".join(lines))]
