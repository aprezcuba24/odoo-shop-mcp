"""FastMCP server: Streamable HTTP + REST bridge lifespan."""

from __future__ import annotations

import httpx
from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan

from apk_mcp.config import get_settings
from apk_mcp.generated.order_bridge_client import Client
from .app_state import app_state


@lifespan
async def app_lifespan(server: FastMCP):
    settings = get_settings()
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
        try:
            yield {"settings": settings}
        finally:
            app_state.api = None


tools = [
    "Carrito en memoria (shop-key del cliente): add_to_cart, get_cart, clear_cart",
    "Confirmar pedido desde carrito: checkout_cart",
    "Último pedido del usuario: get_last_order",
]
resources = [
    "Categorías de producto: apk://catalog/categories",
    "Detalle de producto: apk://catalog/products/{product_id}",
    "Catálogo de productos: apk://catalog/products{?limit,offset,category_id,search}",
    "Municipios y barrios para dirección: apk://locations/municipalities",
    "Pedidos del usuario: apk://orders{?limit,offset,state}",
    "Detalle de pedido: apk://orders/{order_id}",
]
prompts = [
    "shop_assistant: flujo guiado — catálogo (resources), carrito y checkout_cart",
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
