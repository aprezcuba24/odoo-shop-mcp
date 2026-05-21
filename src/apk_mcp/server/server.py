"""FastMCP server: Streamable HTTP + REST bridge lifespan."""

from __future__ import annotations

from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan

from apk_mcp.config import get_settings
from .app_state import ClientRegistry, app_state


@lifespan
async def app_lifespan(server: FastMCP):
    settings = get_settings()
    registry = ClientRegistry(timeout=settings.apk_api_timeout)
    app_state.registry = registry
    try:
        yield {"settings": settings}
    finally:
        await registry.close_all()
        app_state.registry = None


tools = [
    "Carrito en memoria (shop-key del cliente): add_to_cart, get_cart, clear_cart",
    "Confirmar pedido desde carrito: checkout_cart",
    "Último pedido del usuario: get_last_order",
    "Actualizar nombre y dirección del perfil: update_profile",
]
resources = [
    "Categorías de producto: apk://catalog/categories",
    "Detalle de producto: apk://catalog/products/{product_id}",
    "Catálogo de productos: apk://catalog/products{?limit,offset,category_id,search}",
    "Municipios y barrios para dirección: apk://locations/municipalities",
    "Perfil del usuario (nombre, teléfono, dirección): apk://session/profile",
    "Pedidos del usuario: apk://orders{?limit,offset,state}",
    "Detalle de pedido: apk://orders/{order_id}",
]
prompts = [
    "shop_assistant: flujo guiado — catálogo (resources), carrito y checkout_cart",
    "update_my_address: ver o actualizar nombre y dirección de entrega del perfil",
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
