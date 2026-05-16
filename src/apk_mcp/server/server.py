"""FastMCP server: Streamable HTTP + REST bridge lifespan."""

from __future__ import annotations

import httpx
from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan

from apk_mcp.config import get_settings
from apk_mcp.generated.order_bridge_client import Client
from apk_mcp.utils import create_tenant_credential_store
from .app_state import app_state


@lifespan
async def app_lifespan(server: FastMCP):
    settings = get_settings()
    tenant_store = create_tenant_credential_store()
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
        app_state.tenant_credential_store = tenant_store
        try:
            yield {"settings": settings, "tenant_credential_store": tenant_store}
        finally:
            app_state.api = None
            app_state.tenant_credential_store = None


tools = [
    "Adicionar producto al carrito de compras: add_to_cart",
]
resources = [
    "Categorías de producto: apk://catalog/categories",
    "Detalle de producto: apk://catalog/products/{product_id}",
    "Catálogo de productos: apk://catalog/products{?limit,offset,category_id,search}",
]
prompts = [
    "shop_assistant: flujo guiado — explorar catálogo (resources) y usar la tool add_to_cart",
]
instructions = (
    "Esto es la tienda de YY-Mercado que permite comprar productos a los clientes.\n"
    "TOOLS: Úsalas para ejecutar acciones.\n"
    f'{"\n".join(tools)}\n'
    "RESOURCES: Adjúntalas o léelas como contexto (catálogo público: categorías y productos).\n"
    f'{"\n".join(resources)}\n'
    "PROMPTS: Úsalas para orquestar flujos multi-paso.\n"
    f'{"\n".join(prompts)}\n'
)

mcp = FastMCP(
    name="apk-mcp",
    instructions=instructions,
    # instructions=(
    #     "Puente a la API REST order_bridge de Tienda Apk (/api/order_bridge/). "
    #     "Multi-tenant: cada cliente MCP debe enviar la cabecera HTTP configurada "
    #     "(por defecto X-Apk-Tenant-Id) para aislar dispositivo y Bearer; sin cabecera "
    #     "se usa el tenant por defecto (solo desarrollo). El token de dispositivo lo "
    #     "genera el servidor por tenant en memoria.\n\n"
    #     "TOOLS: úsalas para ejecutar acciones.\n"
    #     "  Catálogo (público): list_products, get_product\n"
    #     "  Dispositivo: register_device (público; device_key interno por tenant), get_device_status (Bearer)\n"
    #     "  Pedidos (Bearer): list_orders, get_order, create_order, cancel_order\n"
    #     "  Perfil (Bearer): get_profile, update_profile, replace_profile\n"
    #     "  Push (Bearer): register_push_token, update_push_topics\n\n"
    #     "RESOURCES: adjúntalas o léelas como contexto.\n"
    #     "  apk://catalog/categories — categorías de producto\n"
    #     "  apk://catalog/banners — banners promocionales\n"
    #     "  apk://catalog/products/{product_id} — detalle de un producto\n"
    #     "  apk://store/settings — teléfono y configuración general\n"
    #     "  apk://locations/municipalities — municipios y barrios (IDs para dirección)\n"
    #     "  apk://session/status — validación del dispositivo (Bearer)\n"
    #     "  apk://session/profile — perfil del contacto (Bearer)\n"
    #     "  apk://orders/{order_id} — detalle de un pedido (Bearer)\n\n"
    #     "PROMPTS: flujos guiados de varios pasos.\n"
    #     "  find_products(query, category?, limit?) — búsqueda con resolución de categoría\n"
    #     "  place_order(items_text) — carrito en lenguaje natural y manejo de stock\n"
    #     "  track_order(order_id) — estado del pedido y líneas\n"
    #     "  reorder_last() — repetir el último pedido con confirmación\n"
    #     "  update_my_address(street, state, municipality_name, neighborhood_name)\n"
    #     "  onboard_device(phone?) — registro y validación del dispositivo"
    # ),
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
