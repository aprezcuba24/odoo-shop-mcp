# Arquitectura de apk-mcp

## Rol

Servidor **MCP** (FastMCP, transporte **Streamable HTTP**) que expone *tools* al cliente (ChatGPT, Cursor, etc.) y las traduce en llamadas HTTP a la API REST **Tienda Apk** bajo `/api/order_bridge/`.

## Capas

| Capa | Ubicación | Función |
|------|-----------|---------|
| **Entrada MCP** | `server.py`, `tools/` | Lifespan, registro de tools, `mcp.run(...)`. |
| **Orquestación** | `tools/*.py` | Parámetros del tool → llamada al cliente HTTP → respuesta validada (Pydantic). |
| **Cliente REST** | `http_client.py` | `httpx.AsyncClient`, errores HTTP → excepciones tipadas (`exceptions.py`). |
| **Auth Tienda Apk** | `tenant_credentials.py`, `tenant_resolution.py` | Mapa **en memoria** `tenant_id → token` (`secrets.token_urlsafe`); el token se usa como `device_key` en `POST /register` y como Bearer en rutas autenticadas. |
| **Modelos** | `models/` | Espejo parcial del OpenAPI (respuestas/errores usados por los tools). |
| **Config** | `config.py` | Variables de entorno / `.env` (`pydantic-settings`). |

## Flujo resumido

1. El cliente abre sesión MCP sobre HTTP (`/mcp`).
2. El lifespan crea `httpx.AsyncClient` con `APK_API_BASE_URL` y un [`InMemoryTenantCredentialStore`](src/apk_mcp/utils/tenant_credentials.py).
3. Cada petición HTTP al MCP lleva (según configuración) una cabecera de tenant; [`resolve_tenant_id`](src/apk_mcp/server/tenant_resolution.py) la lee vía [`get_http_request`](https://gofastmcp.com) de FastMCP.
4. Un tool (p. ej. `list_products`) usa `app_state.api` → `GET /api/order_bridge/products` (público).
5. Rutas Bearer llaman a `ensure_device_token(tenant_id)` para el tenant actual y aplican `bearer_authorization` al cliente generado.

## Credenciales en memoria (multi-tenant)

- Implementación: [`InMemoryTenantCredentialStore`](src/apk_mcp/utils/tenant_credentials.py) — un token estable por `tenant_id` mientras viva el proceso.
- **No hay persistencia en disco**: al reiniciar el proceso MCP las claves por tenant se pierden.
- Identidad MCP: cabecera configurable (`APK_MCP_TENANT_HEADER`, defecto `X-Apk-Tenant-Id`); si falta y no se exige, se usa `APK_MCP_FALLBACK_TENANT_ID` (defecto `default`).
- La API de Tienda Apk puede seguir exigiendo registro en Odoo; un 401 remoto no equivale a “falta token local”.

## Extensión

Nuevos endpoints del OpenAPI: añadir modelos en `models/`, tool en `tools/` y registrarlo desde el lifespan o un módulo de registro compartido con `catalog.py`.
