# Arquitectura de apk-mcp

## Rol

Servidor **MCP** (FastMCP, transporte **Streamable HTTP**) que expone *tools* al cliente (ChatGPT, Cursor, etc.) y las traduce en llamadas HTTP a la API REST **Tienda Apk** bajo `/api/order_bridge/`.

## Capas

| Capa | Ubicación | Función |
|------|-----------|---------|
| **Entrada MCP** | `server.py`, `tools/` | Lifespan, registro de tools, `mcp.run(...)`. |
| **Orquestación** | `tools/*.py` | Parámetros del tool → llamada al cliente HTTP → respuesta validada (Pydantic). |
| **Cliente REST** | `http_client.py` | `httpx.AsyncClient`, errores HTTP → excepciones tipadas (`exceptions.py`). |
| **Auth Tienda Apk** | `bearer_token_store.py` | Un único token Bearer **en memoria** por proceso; se genera en el primer uso y se reutiliza hasta reiniciar el servidor. |
| **Modelos** | `models/` | Espejo parcial del OpenAPI (respuestas/errores usados por los tools). |
| **Config** | `config.py` | Variables de entorno / `.env` (`pydantic-settings`). |

## Flujo resumido

1. El cliente abre sesión MCP sobre HTTP (`/mcp`).
2. El lifespan crea `httpx.AsyncClient` con `APK_API_BASE_URL` y un `InMemoryBearerTokenStore`.
3. Un tool (p. ej. `list_products`) usa `app_state.api` → `GET /api/order_bridge/products`.
4. Rutas que exijan Bearer obtienen el token con `ensure_token()` (generación automática si aún no existe); los tools autenticados usan `Depends(get_authenticated_order_bridge)` en lugar de repetir esa lógica.

## Token Bearer en memoria

- Implementación: [`InMemoryBearerTokenStore`](src/apk_mcp/utils/bearer_token_store.py) (`secrets.token_urlsafe` en el primer `ensure_token`).
- **No hay persistencia en disco**: al reiniciar el proceso MCP el token cambia.
- La API de Tienda Apk puede seguir exigiendo registro en Odoo; un 401 remoto no equivale a “falta token local”.

## Extensión

Nuevos endpoints del OpenAPI: añadir modelos en `models/`, tool en `tools/` y registrarlo desde el lifespan o un módulo de registro compartido con `catalog.py`.
