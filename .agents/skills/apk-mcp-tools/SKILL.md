---
name: apk-mcp-tools
description: >-
  Defines how to add FastMCP tools to ApkMCP: module layout, @mcp.tool wiring,
  Depends(get_apk_api | get_authenticated_order_bridge), and thin services that
  call the generated order_bridge Client via client_helper. Use when adding or
  changing MCP tools under src/apk_mcp/tools, wiring Tienda Apk order_bridge
  endpoints, or mirroring catalog.py / orders.py patterns.
---

# ApkMCP: adding new tools

## Architecture (keep this separation)

1. **`src/apk_mcp/tools/`** — MCP-facing surface: `@mcp.tool`, docstrings shown to the model, parameters typed for the MCP schema. **No** raw HTTP or response parsing here beyond delegating to services.
2. **`src/apk_mcp/services/order_bridge/`** — One module per domain area; calls the **generated** `openapi-python-client` (`apk_mcp.generated.order_bridge_client`) and uses **`client_helper`** / **`bearer_authorization`** from `apk_mcp.utils.openapi_detailed`.
3. **`src/apk_mcp/server/app_state.py`** — Lifespan singletons: shared `Client`, `BearerTokenStore`. Exposes **`get_apk_api`** (public routes) and **`get_authenticated_order_bridge`** (Bearer).

Tools stay thin; services own endpoint selection, `UNSET` optional args, and success/error typing.

## Register a new tool module

1. Add `your_feature.py` under `src/apk_mcp/tools/`.
2. Import it from `src/apk_mcp/tools/__init__.py` (same pattern as `catalog` / `orders`) so import side effects run:

```python
from . import your_feature  # noqa: F401
```

Registration happens because `apk_mcp/server/__init__.py` already does `import apk_mcp.tools`.

## Implement the MCP tool function

- Import **`mcp`** from `apk_mcp.server` (not from `server.server` directly in new code—use the package exports).
- Decorate with **`@mcp.tool(name="...", description="...")`**:
  - **`name`**: stable snake_case identifier for clients.
  - **`description`**: mention HTTP method/path, auth (public vs Bearer), and main parameters (pagination, filters).
- Use **`async def`**.
- Return **`dict[str, Any]`** (service functions return `success_model.to_dict()` via `client_helper`).

### Dependency injection (`uncalled_for`)

Use **`Depends(...)`** from `uncalled_for`:

| Route auth | Parameter type | Dependency |
|------------|----------------|------------|
| Public (no Bearer) | `OrderBridgeClientRef` | `Depends(get_apk_api)` |
| Bearer required | `AuthenticatedOrderBridgeRef` | `Depends(get_authenticated_order_bridge)` |

**Do not** inject the generated **`Client`** directly as a FastMCP dependency: it behaves like an async context manager and conflicts with the lifespan-managed `httpx.AsyncClient`. Always use **`OrderBridgeClientRef`** / **`AuthenticatedOrderBridgeRef`** from `app_state`.

Authenticated tools pass **`auth.client`** and **`auth.bearer_token`** into the service layer.

## Implement the service function

1. Locate or create **`src/apk_mcp/services/order_bridge/<area>.py`**.
2. Import the generated API module from **`apk_mcp.generated.order_bridge_client.api.default`** (e.g. `order_bridge_products`, `order_bridge_orders_list`).
3. Import the **success response model** for HTTP 200 (e.g. `ProductsPageResponse`).
4. Call **`client_helper(endpoint_module, client, success_type=..., unexpected_shape_message="...", **kwargs)`**:
   - **`kwargs`** must match the generated `asyncio_detailed` signature.
   - Optional query/body fields: use **`unset_int`** / **`unset_str`** so `None` becomes **`UNSET`** (`apk_mcp.generated.order_bridge_client.types`).
5. If the route requires Bearer auth, wrap the **`client_helper`** call in:

```python
async with bearer_authorization(client, bearer_token):
    return await client_helper(...)
```

6. Prefer **`unexpected_shape_message`** text that names the operation (see existing products/orders modules).

For non-200 handling, rely on **`client_helper`** defaults unless the OpenAPI error models differ; extend **`openapi_detailed`** only when needed.

## After adding a tool

- If the tool is user-visible and central, extend **`instructions=`** on **`FastMCP`** in `src/apk_mcp/server/server.py` so MCP clients get accurate capability hints.
- Regenerate the Python client when OpenAPI changes (follow project README/scripts); new endpoints must exist under **`generated/order_bridge_client`** before wiring.

## Reference implementations

- Public catalog-style tool: `src/apk_mcp/tools/catalog.py` + `src/apk_mcp/services/order_bridge/products.py`
- Authenticated list tool: `src/apk_mcp/tools/orders.py` + `src/apk_mcp/services/order_bridge/orders.py`
