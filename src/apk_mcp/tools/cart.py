from uncalled_for import Depends
from apk_mcp.server import AuthenticatedOrderBridgeRef, get_authenticated_order_bridge, mcp


@mcp.tool(
    name="add_to_cart",
    description=(
        "Añade un producto al carrito de compras (POST /api/order_bridge/cart, Bearer)."
    ),
)
async def add_to_cart(
    product_id: int,
    quantity: float,
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, str]:
    print({
        "product_id": product_id,
        "quantity": quantity,
        "bearer_token": auth.bearer_token,
    })
    return {
        "message": f"Producto añadido al carrito {auth.bearer_token} eee",
    }