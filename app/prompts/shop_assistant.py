"""Prompt de asistente de tienda: carrito y uso del catálogo (tools y resources MCP)."""

from __future__ import annotations

from fastmcp.prompts import Message

from app.server import mcp


@mcp.prompt(
    name="shop_assistant",
    description=(
        "Guía para explorar el catálogo (resources apk://catalog/... en primer lugar; "
        "si no hay resources/read, read_catalog_products, read_catalog_categories, read_catalog_product) "
        "y gestionar el carrito con add_to_cart, get_cart, clear_cart y checkout_cart "
        "(carrito por cabecera shop-key del host MCP)."
    ),
)
def shop_assistant() -> list[Message]:
    lines = [
        "Ayuda al usuario a buscar y seleccionar los productos que quiere añadir al carrito de compras.",
        "El carrito se asocia al dispositivo/tienda mediante la cabecera HTTP shop-key configurada en el cliente MCP; "
        "no hace falta pasar un identificador manual en las tools de carrito.",
        "El usuario puede buscar productos por nombre o categoría.",
        "Para listar o buscar productos, lee primero apk://catalog/products o apk://catalog/categories; "
        "si el cliente no soporta resources/read, usa read_catalog_products(search=...) o read_catalog_categories(). "
        "Para detalle de producto, lee apk://catalog/products/{product_id}; "
        "si no hay resources/read, usa read_catalog_product(product_id).",
        "El usuario puede hacer varias iteraciones hasta encontrar el producto que le interesa.",
        "Una vez seleccionado el producto, llama a add_to_cart con product_id y quantity.",
        "Para mostrar el carrito actual usa get_cart; para vaciarlo usa clear_cart.",
        "Cuando el usuario quiera confirmar la compra, llama a checkout_cart (crea el pedido en el backend con las líneas del carrito).",
        "Si checkout_cart o create_order devuelven error=insufficient_stock, consulta el catálogo "
        "(apk://catalog/products/{product_id} o read_catalog_product) para obtener el nombre de cada producto "
        "y explícale al usuario qué pidió, cuánto hay disponible (products) y qué cantidad pedía "
        "(_agent.lines_submitted); pide ajustar con add_to_cart y reintenta checkout_cart.",
        "Si el usuario dice que quiere hacer una compra, muéstrale productos o categorías del catálogo "
        "(resource apk://catalog/... o, si no puedes, read_catalog_products) para que pueda elegir.",
        "Toda interacción con la tienda empieza explorando productos o categorías; prioriza Resources apk:// y usa tools read_catalog_* solo como respaldo.",
    ]
    return [Message("\n".join(lines))]
