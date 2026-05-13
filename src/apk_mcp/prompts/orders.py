"""Order prompts — place, track and reorder workflows."""

from __future__ import annotations

from fastmcp.prompts import Message

from apk_mcp.server import mcp


@mcp.prompt(
    name="place_order",
    description=(
        "End-to-end order placement: parse natural-language item list, resolve product IDs, "
        "validate stock, and call create_order. Handles insufficient_stock errors gracefully "
        "by proposing quantity adjustments or line removal."
    ),
)
def place_order(items_text: str) -> list[Message]:
    return [
        Message(
            f"The user wants to place an order with the following items:\n\n{items_text}\n\n"
            "Follow these steps:\n"
            "1. Parse the item list to extract product names and quantities.\n"
            "2. For each product name, call list_products with search=<name>, limit=5 to find "
            "the best match. Confirm the product with the user if there is ambiguity.\n"
            "3. Build a lines JSON array: [{\"product_id\": <id>, \"qty\": <qty>}, ...].\n"
            "4. Call create_order with that JSON.\n"
            "5. If create_order returns an InsufficientStockError:\n"
            "   - Show the user which products have insufficient stock and how much is available.\n"
            "   - Offer to adjust quantities to the available amount or remove those lines.\n"
            "   - Re-call create_order with the adjusted lines after the user confirms.\n"
            "6. If the device is not validated (device_validated:false in the response), "
            "warn the user that the order may be pending approval in the store backend.\n"
            "7. On success, present the order name, id, state and store_state to the user."
        )
    ]


@mcp.prompt(
    name="track_order",
    description=(
        "Fetch and format a sale order for the user: state, store_state, delivery status, "
        "line items with quantities delivered vs ordered, and total amount."
    ),
)
def track_order(order_id: int) -> list[Message]:
    return [
        Message(
            f"The user wants to track order #{order_id}.\n\n"
            "1. Read the resource apk://orders/{order_id} (or call get_order if the resource "
            f"is not available) for order_id={order_id}.\n"
            "2. Present the following information in a clear, friendly format:\n"
            "   - Order name and reference (name, order_ref)\n"
            "   - Order date (date_order)\n"
            "   - Current state and store_state\n"
            "   - Delivery status (delivery_status)\n"
            "   - Delivery address\n"
            "   - Line items: product name, qty ordered, qty delivered, unit price, subtotal\n"
            "   - Total amount with currency\n"
            "3. Translate store_state values for the user:\n"
            "   reviewing→'En revisión', negotiating→'En negociación', "
            "ready_for_delivery→'Listo para entrega', delivered→'Entregado', "
            "canceled→'Cancelado'.\n"
            "4. Translate delivery_status: pending→'Pendiente', started→'Iniciada', "
            "partial→'Entrega parcial', full→'Entrega completa'."
        )
    ]


@mcp.prompt(
    name="reorder_last",
    description=(
        "Repeat the most recent order: fetch the last order, show its lines to the user "
        "for confirmation, then call create_order with the same lines."
    ),
)
def reorder_last() -> list[Message]:
    return [
        Message(
            "The user wants to repeat their last order.\n\n"
            "1. Call list_orders with limit=1, offset=0 to get the most recent order summary.\n"
            "   If there are no orders, tell the user and stop.\n"
            "2. Call get_order with that order's id to get the full line details.\n"
            "3. Show the user the order lines (product name, qty, unit price) and the total, "
            "and ask them to confirm before placing the new order.\n"
            "4. Once confirmed, build the lines JSON from the order lines "
            "(use product_id and qty from each line) and call create_order.\n"
            "5. Handle InsufficientStockError as described in the place_order prompt: "
            "show affected products with available stock and ask the user how to proceed.\n"
            "6. On success, present the new order's name, id and store_state."
        )
    ]
