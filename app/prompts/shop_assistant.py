"""Prompt de asistente de tienda: carrito y uso del catálogo (tools y resources MCP)."""

from __future__ import annotations

from fastmcp.prompts import Message

from app.server import mcp


@mcp.prompt(
    name="shop_assistant",
    description=(
        "Guía para explorar el catálogo (search, list_products, list_categories, get_product "
        "o resources apk://catalog/...) y gestionar el carrito con add_to_cart, get_cart, "
        "clear_cart y checkout_cart (carrito por cabecera shop-key del host MCP)."
    ),
)
def shop_assistant() -> list[Message]:
    lines = [
        "Ayuda al usuario a buscar y seleccionar los productos que quiere añadir al carrito de compras.",
        "El carrito se asocia al dispositivo/tienda mediante la cabecera HTTP shop-key configurada en el cliente MCP; "
        "no hace falta pasar un identificador manual en las tools de carrito.",
        "El usuario puede buscar productos por nombre o categoría.",
        "Para listar o buscar productos usa search(query), list_products() o list_categories(); "
        "para detalle usa fetch(id) o get_product(product_id). "
        "En clientes con resources/read también puedes leer apk://catalog/...",
        "El usuario puede hacer varias iteraciones hasta encontrar el producto que le interesa.",
        "Una vez seleccionado el producto, llama a add_to_cart con product_id y quantity.",
        "Para mostrar el carrito actual usa get_cart; para vaciarlo usa clear_cart.",
        "Cuando el usuario quiera confirmar la compra, llama a checkout_cart (crea el pedido en el backend con las líneas del carrito).",
        "Si checkout_cart devuelve error=insufficient_stock, muestra products (available_qty por product_id), "
        "pide al usuario ajustar cantidades con add_to_cart y vuelve a intentar checkout_cart.",
        "Si el usuario dice que quiere hacer una compra, muéstrale productos o categorías con search o list_products "
        "para que pueda elegir.",
        "Toda interacción con la tienda empieza explorando productos o categorías vía tools de catálogo.",
    ]
    return [Message("\n".join(lines))]
