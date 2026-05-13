"""FastMCP server: Streamable HTTP + REST bridge lifespan."""

from __future__ import annotations

import httpx
from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan

from apk_mcp.config import get_settings
from apk_mcp.generated.order_bridge_client import Client
from apk_mcp.utils import create_bearer_token_store
from .app_state import app_state


@lifespan
async def app_lifespan(server: FastMCP):
    settings = get_settings()
    bearer_token_store = create_bearer_token_store()
    base = settings.apk_api_base_url.rstrip("/")
    async with httpx.AsyncClient(
        base_url=base,
        timeout=settings.apk_api_timeout,
    ) as http:
        ob_client = Client(
            base_url=base,
            raise_on_unexpected_status=False,
            timeout=settings.apk_api_timeout,
        )
        ob_client.set_async_httpx_client(http)
        app_state.api = ob_client
        app_state.bearer_token_store = bearer_token_store
        try:
            yield {"settings": settings, "bearer_token_store": bearer_token_store}
        finally:
            app_state.api = None
            app_state.bearer_token_store = None


mcp = FastMCP(
    name="apk-mcp",
    instructions=(
        "Puente a la API REST order_bridge de Tienda Apk (/api/order_bridge/). "
        "Se genera un único token Bearer por proceso del servidor y se reutiliza en todas las "
        "llamadas autenticadas.\n\n"
        "TOOLS: úsalas para ejecutar acciones.\n"
        "  Catálogo (público): list_products, get_product\n"
        "  Dispositivo: register_device (público), get_device_status (Bearer)\n"
        "  Pedidos (Bearer): list_orders, get_order, create_order, cancel_order\n"
        "  Perfil (Bearer): get_profile, update_profile, replace_profile\n"
        "  Push (Bearer): register_push_token, update_push_topics\n\n"
        "RESOURCES: adjúntalas o léelas como contexto.\n"
        "  apk://catalog/categories — categorías de producto\n"
        "  apk://catalog/banners — banners promocionales\n"
        "  apk://catalog/products/{product_id} — detalle de un producto\n"
        "  apk://store/settings — teléfono y configuración general\n"
        "  apk://locations/municipalities — municipios y barrios (IDs para dirección)\n"
        "  apk://session/status — validación del dispositivo (Bearer)\n"
        "  apk://session/profile — perfil del contacto (Bearer)\n"
        "  apk://orders/{order_id} — detalle de un pedido (Bearer)\n\n"
        "PROMPTS: flujos guiados de varios pasos.\n"
        "  find_products(query, category?, limit?) — búsqueda con resolución de categoría\n"
        "  place_order(items_text) — carrito en lenguaje natural y manejo de stock\n"
        "  track_order(order_id) — estado del pedido y líneas\n"
        "  reorder_last() — repetir el último pedido con confirmación\n"
        "  update_my_address(street, state, municipality_name, neighborhood_name)\n"
        "  onboard_device(device_key, phone?) — registro y validación del dispositivo"
    ),
    lifespan=app_lifespan,
)


def run() -> None:
    settings = get_settings()
    mcp.run(
        transport="streamable-http",
        host=settings.mcp_host,
        port=settings.mcp_port,
        path=settings.mcp_path,
    )
