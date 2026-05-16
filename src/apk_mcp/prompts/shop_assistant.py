"""Prompt de asistente de tienda: carrito y uso del catálogo (recursos MCP)."""

from __future__ import annotations

from fastmcp.prompts import Message

from apk_mcp.server import mcp


@mcp.prompt(
    name="shop_assistant",
    description=(
        "Guía para ayudar al usuario a explorar el catálogo (vía resources apk://catalog/...) "
        "y añadir al carrito con la tool add_to_cart cuando tenga product_id y cantidad."
    ),
)
def shop_assistant() -> list[Message]:
    lines = [
        "Ayuda al usuario a buscar y seleccionar los productos que quiere añadir al carrito de compras.",
        "El usuario puede buscar productos por nombre o categoría.",
        "Para listar categorías o productos, lee los resources MCP del catálogo (apk://catalog/...).",
        "El usuario puede hacer varias iteraciones hasta encontrar el producto que le interesa.",
        "Una vez seleccionado el producto, llama a la tool add_to_cart con el id del producto y la cantidad.",
        "Si el usuario dice que quiere hacer una compra, muéstrale productos o categorías leyendo los resources del catálogo para que pueda elegir.",
        "Toda interacción con la tienda empieza explorando productos o categorías vía resources.",
    ]
    return [Message("\n".join(lines))]
