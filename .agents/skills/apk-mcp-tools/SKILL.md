---
name: apk-mcp-tools
description: >-
  Defines how to add FastMCP tools, resources and prompts to ApkMCP: module
  layout, @mcp.tool / @mcp.resource / @mcp.prompt wiring,
  Depends(get_apk_api | get_authenticated_order_bridge), and thin services that
  call the generated order_bridge Client via client_helper. Use when adding or
  changing MCP surface under app/app/tools, app/app/resources or
  app/app/prompts, wiring Tienda Apk order_bridge endpoints, or mirroring
  existing patterns.
---

# ApkMCP: adding tools, resources and prompts

## Architecture (keep this separation)

1. **`app/app/tools/`** — MCP tools de acción: `@mcp.tool`, descriptions shown to the model, typed parameters. No raw HTTP.
2. **`app/app/tools/tool_resources/`** — MCP tools de solo lectura que espejan Resources (`read_*`) para clientes sin `resources/read` (p. ej. ChatGPT). Importan handlers de `app/app/resources/`.
3. **`app/app/resources/`** — MCP resources: `@mcp.resource`, static or templated URIs. **Fuente de verdad** para lecturas: define handlers `read_*` y el `@mcp.resource` delega en ellos.
4. **`app/app/prompts/`** — MCP prompts: `@mcp.prompt`, multi-step workflow templates that return `list[Message]`.
5. **`app/app/services/order_bridge/`** — One module per domain; calls the **generated** `openapi-python-client` and uses **`client_helper`** / **`bearer_authorization`** from `app.utils.openapi_detailed`.
6. **`app/app/server/app_state.py`** — Lifespan singleton: generated `Client`. Exposes **`get_apk_api`** (public), **`get_authenticated_order_bridge`** (Bearer from request), and **`resolve_shop_key()`** when a public tool needs the same token as `POST /register` (`register_device`).

## Autenticación (`shop-key`, Streamable HTTP)

Cada petición HTTP al MCP debe incluir la cabecera **`shop-key`**: `Bearer` + base64(`BASE_URL|user_token`). [`resolve_shop_context`](app/app/utils/shop_key_codec.py) decodifica URL y token; para el carrito usar **`ctx.cart_store_key()`** → `CartStoreKey(backend=dominio netloc, token=user_token)` vía [`cart_store`](app/app/services/cart/__init__.py) (`memory` en dev, DynamoDB en Lambda). Dev: `pnpm shop-key -- http://localhost:8069|<user_token>`.

Tools and resources stay thin; services own endpoint selection, `UNSET` optional args, and success/error typing.

## Dependency injection (`uncalled_for`)

Use **`Depends(...)`** from `uncalled_for` in tools **and** resources:

| Route auth | Parameter type | Dependency |
|------------|----------------|------------|
| Public (no Bearer) | `OrderBridgeClientRef` | `Depends(get_apk_api)` |
| Bearer required | `AuthenticatedOrderBridgeRef` | `Depends(get_authenticated_order_bridge)` |

**Do not** inject the generated `Client` directly. Always use `OrderBridgeClientRef` / `AuthenticatedOrderBridgeRef`.

Authenticated handlers pass **`auth.client`** and **`auth.bearer_token`** into the service layer.

## Adding a tool

1. Add `your_feature.py` under `app/app/tools/`.
2. Import it from `app/app/tools/__init__.py`:

```python
from . import your_feature  # noqa: F401
```

3. Implement with `@mcp.tool(name="...", description="...")`, `async def`, return `dict[str, Any]`:

`description=` debe estar en **español** (texto orientado al modelo) e incluir método HTTP, ruta, si es público o Bearer y parámetros clave.

```python
@mcp.tool(
    name="get_order",
    description=(
        "Obtiene el detalle de un pedido (GET /api/order_bridge/orders/{order_id}, Bearer), "
        "incluyendo líneas."
    ),
)
async def get_order(
    order_id: int,
    auth: AuthenticatedOrderBridgeRef = Depends(get_authenticated_order_bridge),
) -> dict[str, Any]:
    return await get_order_detail(auth.client, bearer_token=auth.bearer_token, order_id=order_id)
```

## Adding a resource

Resources expose read-only data that hosts/users can attach as context.

1. Add `your_domain.py` under `app/app/resources/`.
2. Import it from `app/app/resources/__init__.py`.
3. Use URI scheme `apk://<domain>/<resource>[/{param}]`:

**Static resource:**
```python
@mcp.resource(
    uri="apk://catalog/categories",
    name="Catálogo: categorías",
    description="Lista completa de categorías (pública).",
    mime_type="application/json",
)
async def read_catalog_categories(api: OrderBridgeClientRef) -> dict[str, Any]:
    return await list_categories(api.client)

@mcp.resource(...)
async def categories_resource(
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    return await read_catalog_categories(api)
```

**Templated resource** (URI parameters become function args):
```python
@mcp.resource(
    uri="apk://catalog/products/{product_id}",
    name="Catálogo: producto",
    description="Detalle de producto por ID (público).",
    mime_type="application/json",
)
async def read_catalog_product(
    api: OrderBridgeClientRef, *, product_id: int,
) -> dict[str, Any]:
    return await get_product_detail(api.client, product_id=product_id)

@mcp.resource(...)
async def product_resource(
    product_id: int,
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    return await read_catalog_product(api, product_id=product_id)
```

## Adding a tool_resource (ChatGPT-compatible read)

When a resource already exists, **do not duplicate service calls**. Add a thin `@mcp.tool` in `app/app/tools/tool_resources/` that imports the `read_*` handler from the resource module.

1. Ensure the handler exists in `app/app/resources/<domain>.py`.
2. Add `your_domain.py` under `app/app/tools/tool_resources/`.
3. Import it from `app/app/tools/tool_resources/__init__.py`.
4. Use `READ_ONLY` from `tool_resources/_common.py` and name tools `read_<domain>_<resource>`.

```python
from app.resources.catalog import read_catalog_categories
from app.tools.tool_resources._common import READ_ONLY

@mcp.tool(
    name="read_catalog_categories",
    description="... Equivalente al Resource apk://catalog/categories.",
    annotations=READ_ONLY,
)
async def read_catalog_categories_tool(
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    return await read_catalog_categories(api)
```

## Adding a prompt

Prompts are workflow templates for multi-step tasks. **Do not** create 1:1 wrappers over a single tool — they add no value over calling the tool directly.

1. Add `your_domain.py` under `app/app/prompts/`.
2. Import it from `app/app/prompts/__init__.py`.
3. Use `@mcp.prompt(name="...", description="...")`, sync `def`, return `list[Message]`:

```python
from fastmcp.prompts import Message
from app.server import mcp

@mcp.prompt(
    name="place_order",
    description="End-to-end order from natural-language items; handles stock errors.",
)
def place_order(items_text: str) -> list[Message]:
    return [
        Message(
            f"The user wants to order: {items_text}\n\n"
            "1. Call read_catalog_products to resolve product IDs.\n"
            "2. Build lines JSON and call create_order.\n"
            "3. Handle InsufficientStockError: show available qty, ask user to adjust.\n"
            "4. Present the created order summary."
        )
    ]
```

`Message(content, role="user"|"assistant")` — `role` defaults to `"user"`.

## Implement the service function

1. Locate or create **`app/app/services/order_bridge/<area>.py`**.
2. Import the generated API module from `app.generated.order_bridge_client.api.default`.
3. Import the **success response model** for HTTP 200.
4. Call **`client_helper(endpoint_module, client, success_type=..., unexpected_shape_message="...", **kwargs)`**:
   - `kwargs` must match the generated `asyncio_detailed` signature.
   - Optional fields: use `unset_int` / `unset_str` so `None` becomes `UNSET`.
5. Bearer routes: wrap in `async with bearer_authorization(client, bearer_token): ...`.
6. Custom 400 errors (e.g. `InsufficientStockError`): pass a `bad_request_spec` tuple to `client_helper`:

```python
_CREATE_BAD_REQUEST_SPEC = ((InsufficientStockErrorResponse, InsufficientStockError),)

async with bearer_authorization(client, bearer_token):
    return await client_helper(
        order_bridge_orders_create,
        client,
        success_type=OrderCreatedResponse,
        bad_request_spec=_CREATE_BAD_REQUEST_SPEC,
        body=body,
    )
```

## After adding surface

- Update `instructions=` in `app/app/server/server.py`.
- Update `README.md` Tools / Resources / Prompts tables.
- Regenerate the Python client when OpenAPI changes (`pnpm run gen:order-bridge-types`); new endpoints must exist under `generated/order_bridge_client` before wiring.

## Reference implementations

| Domain | Tool (acción) | Tool (lectura) | Resource | Service |
|--------|---------------|----------------|----------|---------|
| Products | — | `tool_resources/catalog.py` (`read_catalog_*`) | `resources/catalog.py` | `services/order_bridge/products.py`, `categories.py` |
| Orders | `tools/orders.py` (checkout, create, cancel, get_last_order) | `tool_resources/orders.py` (`read_orders`, `read_order`) | `resources/orders.py` | `services/order_bridge/orders.py` |
| Profile | `tools/profile.py` (`update_profile`) | `tool_resources/profile.py` (`read_session_profile`) | `resources/profile.py` | `services/order_bridge/profile.py` |
| Device | `tools/device.py` | — | `resources/session.py` | `services/order_bridge/device.py` |
| Locations | — | `tool_resources/locations.py` (`read_locations_municipalities`) | `resources/locations.py` | `services/order_bridge/locations.py` |
| Store | — | `resources/store.py` | `services/order_bridge/store.py` |
| Banners | — | `resources/catalog.py` | `services/order_bridge/banners.py` |
| Push | `tools/push.py` | — | `services/order_bridge/push.py` |
