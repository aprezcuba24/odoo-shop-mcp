from apk_mcp.server import mcp


@mcp.tool(
    name="add_to_cart",
    description=(
        "Añade un producto al carrito de compras (POST /api/order_bridge/cart, Bearer)."
    ),
)
async def add_to_cart(
    product_id: int,
    quantity: float,
) -> dict[str, str]:
    print({
        "product_id": product_id,
        "quantity": quantity,
    })
    return {
        "message": "Producto añadido al carrito",
    }