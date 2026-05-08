# Arquitectura de apk-mcp

## Rol

Servidor **MCP** (FastMCP, transporte **Streamable HTTP**) que expone *tools* al cliente (ChatGPT, Cursor, etc.) y las traduce en llamadas HTTP a la API REST **Tienda Apk** bajo `/api/order_bridge/`.

## Capas

| Capa | Ubicación | Función |
|------|-----------|---------|
| **Entrada MCP** | `server.py`, `tools/` | Lifespan, registro de tools, `mcp.run(...)`. |
| **Orquestación** | `tools/*.py` | Parámetros del tool → llamada al cliente HTTP → respuesta validada (Pydantic). |
| **Cliente REST** | `http_client.py` | `httpx.AsyncClient`, errores HTTP → excepciones tipadas (`exceptions.py`). |
| **Auth Tienda Apk** | `session_store.py`, `persistence/` | `device_key`: caché por sesión (`Context`) + repositorio intercambiable (`DeviceKeyRepository`; SQLite por defecto). |
| **Modelos** | `models/` | Espejo parcial del OpenAPI (respuestas/errores usados por los tools). |
| **Config** | `config.py` | Variables de entorno / `.env` (`pydantic-settings`). |

## Flujo resumido

1. El cliente abre sesión MCP sobre HTTP (`/mcp`).
2. El lifespan crea `httpx.AsyncClient` con `APK_API_BASE_URL` y el `DeviceKeyStore` configurado.
3. Un tool (p. ej. `list_products`) usa `app_state.api` → `GET /api/order_bridge/products`.
4. Rutas que exijan Bearer leen el `device_key` del store (memoria + disco según modo); los tools autenticados usan `Depends(get_authenticated_order_bridge)` en lugar de repetir esa lógica.

## Persistencia del `device_key`

- **`DeviceKeyRepository`** (`persistence/base.py`): contrato genérico (`get` / `set` / `delete` / `aclose`).
- Implementaciones: **SQLite** (`persistence/sqlite_backend.py`), **memoria** (`memory_backend.py`). Nuevos backends: misma interfaz + registro en `persistence/factory.py`.
- La clave lógica en disco es `resolve_persistence_key` en `session_store.py` (OAuth `sub`, `Context.client_id`, `X-Client-Id` o `default`).

## Extensión

Nuevos endpoints del OpenAPI: añadir modelos en `models/`, tool en `tools/` y registrarlo desde el lifespan o un módulo de registro compartido con `catalog.py`.
