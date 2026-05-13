---
name: apk-mcp-tools
description: >-
  Defines how to add FastMCP tools, resources and prompts to ApkMCP: module
  layout, @mcp.tool / @mcp.resource / @mcp.prompt wiring,
  Depends(get_apk_api | get_authenticated_order_bridge), and thin services that
  call the generated order_bridge Client via client_helper. Use when adding or
  changing MCP surface under src/apk_mcp/tools, src/apk_mcp/resources or
  src/apk_mcp/prompts, wiring Tienda Apk order_bridge endpoints, or mirroring
  existing patterns.
---

# ApkMCP: adding tools, resources and prompts

## Architecture (keep this separation)

1. **`src/apk_mcp/tools/`** — MCP tools: `@mcp.tool`, descriptions shown to the model, typed parameters. No raw HTTP.
2. **`src/apk_mcp/resources/`** — MCP resources: `@mcp.resource`, static or templated URIs. Read-only, browseable by hosts/users.
3. **`src/apk_mcp/prompts/`** — MCP prompts: `@mcp.prompt`, multi-step workflow templates that return `list[Message]`.
4. **`src/apk_mcp/services/order_bridge/`** — One module per domain; calls the **generated** `openapi-python-client` and uses **`client_helper`** / **`bearer_authorization`** from `apk_mcp.utils.openapi_detailed`.
5. **`src/apk_mcp/server/app_state.py`** — Lifespan singletons: `Client`, `BearerTokenStore`. Exposes **`get_apk_api`** (public) and **`get_authenticated_order_bridge`** (Bearer).

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

1. Add `your_feature.py` under `src/apk_mcp/tools/`.
2. Import it from `src/apk_mcp/tools/__init__.py`:

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

1. Add `your_domain.py` under `src/apk_mcp/resources/`.
2. Import it from `src/apk_mcp/resources/__init__.py`.
3. Use URI scheme `apk://<domain>/<resource>[/{param}]`:

**Static resource:**
```python
@mcp.resource(
    uri="apk://catalog/categories",
    name="Catálogo: categorías",
    description="Lista completa de categorías (pública).",
    mime_type="application/json",
)
async def categories_resource(
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    return await list_categories(api.client)
```

**Templated resource** (URI parameters become function args):
```python
@mcp.resource(
    uri="apk://catalog/products/{product_id}",
    name="Catálogo: producto",
    description="Detalle de producto por ID (público).",
    mime_type="application/json",
)
async def product_resource(
    product_id: int,
    api: OrderBridgeClientRef = Depends(get_apk_api),
) -> dict[str, Any]:
    return await get_product_detail(api.client, product_id=product_id)
```

## Adding a prompt

Prompts are workflow templates for multi-step tasks. **Do not** create 1:1 wrappers over a single tool — they add no value over calling the tool directly.

1. Add `your_domain.py` under `src/apk_mcp/prompts/`.
2. Import it from `src/apk_mcp/prompts/__init__.py`.
3. Use `@mcp.prompt(name="...", description="...")`, sync `def`, return `list[Message]`:

```python
from fastmcp.prompts import Message
from apk_mcp.server import mcp

@mcp.prompt(
    name="place_order",
    description="End-to-end order from natural-language items; handles stock errors.",
)
def place_order(items_text: str) -> list[Message]:
    return [
        Message(
            f"The user wants to order: {items_text}\n\n"
            "1. Call list_products to resolve product IDs.\n"
            "2. Build lines JSON and call create_order.\n"
            "3. Handle InsufficientStockError: show available qty, ask user to adjust.\n"
            "4. Present the created order summary."
        )
    ]
```

`Message(content, role="user"|"assistant")` — `role` defaults to `"user"`.

## Implement the service function

1. Locate or create **`src/apk_mcp/services/order_bridge/<area>.py`**.
2. Import the generated API module from `apk_mcp.generated.order_bridge_client.api.default`.
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

- Update `instructions=` in `src/apk_mcp/server/server.py`.
- Update `README.md` Tools / Resources / Prompts tables.
- Regenerate the Python client when OpenAPI changes (`pnpm run gen:order-bridge-types`); new endpoints must exist under `generated/order_bridge_client` before wiring.

## Reference implementations

| Domain | Tool | Resource | Service |
|--------|------|----------|---------|
| Products | `tools/catalog.py` | `resources/catalog.py` | `services/order_bridge/products.py` |
| Orders | `tools/orders.py` | `resources/orders.py` | `services/order_bridge/orders.py` |
| Profile | `tools/profile.py` | `resources/session.py` | `services/order_bridge/profile.py` |
| Device | `tools/device.py` | `resources/session.py` | `services/order_bridge/device.py` |
| Locations | — | `resources/locations.py` | `services/order_bridge/locations.py` |
| Store | — | `resources/store.py` | `services/order_bridge/store.py` |
| Banners | — | `resources/catalog.py` | `services/order_bridge/banners.py` |
| Push | `tools/push.py` | — | `services/order_bridge/push.py` |
