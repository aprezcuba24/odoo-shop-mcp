"""Prompts de pedidos — realizar pedido, seguimiento y repetir último."""

from __future__ import annotations

from fastmcp.prompts import Message

from apk_mcp.server import mcp


@mcp.prompt(
    name="place_order",
    description=(
        "Colocar un pedido de extremo a extremo: interpreta la lista de artículos en lenguaje natural, "
        "resuelve IDs de producto, valida stock y llama a create_order. Ante errores de stock insuficiente, "
        "propone ajustar cantidades o quitar líneas."
    ),
)
def place_order(items_text: str) -> list[Message]:
    return [
        Message(
            f"El usuario quiere realizar un pedido con los siguientes artículos:\n\n{items_text}\n\n"
            "Sigue estos pasos:\n"
            "1. Interpreta la lista y extrae nombres de producto y cantidades.\n"
            "2. Por cada nombre, llama a list_products con search=<nombre>, limit=5 para encontrar "
            "la mejor coincidencia. Si hay ambigüedad, confírmalo con el usuario.\n"
            "3. Construye un array JSON de líneas: [{\"product_id\": <id>, \"qty\": <cantidad>}, ...].\n"
            "4. Llama a create_order con ese JSON.\n"
            "5. Si create_order devuelve InsufficientStockError:\n"
            "   - Muestra qué productos no tienen stock suficiente y cuánto hay disponible.\n"
            "   - Ofrece ajustar las cantidades al disponible o eliminar esas líneas.\n"
            "   - Vuelve a llamar a create_order con las líneas ajustadas tras confirmar el usuario.\n"
            "6. Si el dispositivo no está validado (device_validated:false en la respuesta), "
            "advierte al usuario de que el pedido puede quedar pendiente de aprobación en la tienda.\n"
            "7. Si todo va bien, muestra al usuario el name, id, state y store_state del pedido."
        )
    ]


@mcp.prompt(
    name="track_order",
    description=(
        "Obtiene y presenta un pedido de venta: estado, store_state, estado de entrega, "
        "líneas con cantidades entregadas frente a pedidas e importe total."
    ),
)
def track_order(order_id: int) -> list[Message]:
    return [
        Message(
            f"El usuario quiere hacer seguimiento del pedido #{order_id}.\n\n"
            "1. Lee el recurso yy-shop://orders/{order_id} (o llama a get_order si el recurso "
            f"no está disponible) con order_id={order_id}.\n"
            "2. Presenta la siguiente información de forma clara y amable:\n"
            "   - Nombre y referencia del pedido (name, order_ref)\n"
            "   - Fecha del pedido (date_order)\n"
            "   - Estado actual y store_state\n"
            "   - Estado de entrega (delivery_status)\n"
            "   - Dirección de entrega\n"
            "   - Líneas: nombre del producto, cantidad pedida, entregada, precio unitario, subtotal\n"
            "   - Importe total con moneda\n"
            "3. Traduce los valores de store_state para el usuario:\n"
            "   reviewing→'En revisión', negotiating→'En negociación', "
            "ready_for_delivery→'Listo para entrega', delivered→'Entregado', "
            "canceled→'Cancelado'.\n"
            "4. Traduce delivery_status: pending→'Pendiente', started→'Iniciada', "
            "partial→'Entrega parcial', full→'Entrega completa'."
        )
    ]


@mcp.prompt(
    name="reorder_last",
    description=(
        "Repite el pedido más reciente: obtiene el último pedido, muestra sus líneas al usuario "
        "para confirmación y llama a create_order con las mismas líneas."
    ),
)
def reorder_last() -> list[Message]:
    return [
        Message(
            "El usuario quiere repetir su último pedido.\n\n"
            "1. Llama a list_orders con limit=1, offset=0 para obtener el resumen del pedido más reciente.\n"
            "   Si no hay pedidos, infórmalo al usuario y detente.\n"
            "2. Llama a get_order con el id de ese pedido para ver el detalle de las líneas.\n"
            "3. Muestra al usuario las líneas (nombre, cantidad, precio unitario) y el total, "
            "y pide confirmación antes de crear el nuevo pedido.\n"
            "4. Tras confirmar, construye el JSON de líneas a partir de las líneas del pedido "
            "(product_id y qty de cada línea) y llama a create_order.\n"
            "5. Ante InsufficientStockError, actúa como en el prompt place_order: "
            "muestra productos afectados y stock disponible y pregunta cómo continuar.\n"
            "6. Si todo va bien, muestra el name, id y store_state del nuevo pedido."
        )
    ]
