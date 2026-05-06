# apk-mcp

Servidor [MCP](https://modelcontextprotocol.io/) (Model Context Protocol) en Python que hace de puente hacia la API REST **Tienda Apk** (`/api/order_bridge/`), usando **FastMCP** con transporte **Streamable HTTP**.

## Requisitos

- Python 3.11+

## Instalación

```bash
cd ApkMCP
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

Si usas [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

## Configuración

Copia `.env.example` a `.env` y ajusta:

| Variable | Descripción |
|----------|-------------|
| `APK_API_BASE_URL` | URL base del host (ej. `https://mi-odoo.com`) |
| `APK_API_TIMEOUT` | Timeout HTTP en segundos |
| `MCP_HOST` / `MCP_PORT` / `MCP_PATH` | Bind y ruta del endpoint MCP (p. ej. `/mcp`) |
| `APK_DEVICE_KEY_STORE_MODE` | `layered` (recomendado), `context`, o `sqlite` |
| `APK_DEVICE_KEY_PERSISTENCE_BACKEND` | Motor del repositorio: `sqlite` (por defecto) o `memory` (pruebas) |
| `APK_DEVICE_KEY_DB_PATH` | Ruta al SQLite cuando el backend es `sqlite` |

### Autenticación (`device_key`)

La API usa `Authorization: Bearer <device_key>` salvo rutas públicas (catálogo, `POST /register`, etc.).

- **Capa de sesión (caché)**: FastMCP guarda estado por sesión MCP (`Context.set_state` / `get_state`).
- **Repositorio genérico**: la persistencia estable va detrás de la interfaz `DeviceKeyRepository` ([`src/apk_mcp/persistence/base.py`](src/apk_mcp/persistence/base.py)). Hoy hay implementaciones **SQLite** y **memoria**; puedes añadir Postgres/Redis implementando el mismo protocolo y registrándolo en [`create_device_key_repository`](src/apk_mcp/persistence/factory.py).

La clave lógica en disco es `resolve_persistence_key` ([`session_store.py`](src/apk_mcp/session_store.py)), en este orden:

1. **OAuth** (conector con login, p. ej. ChatGPT): token de acceso con claim `sub` → clave `oauth:{client_id}|{sub}` (misma idea que el aislamiento de tareas en FastMCP). Así **un nuevo chat del mismo usuario** suele reutilizar el mismo bucket y el `device_key` ya registrado.
2. **`Context.client_id`** del runtime MCP (depende del cliente; puede cambiar entre conversaciones).
3. Cabecera **`X-Client-Id`** (útil si delante del MCP fijas un id estable por usuario).
4. **`default`**: un solo bucket para toda la instancia (single-tenant). También sobrevive a nuevos chats si solo hay un operador.

Modo recomendado: **`APK_DEVICE_KEY_STORE_MODE=layered`**: lectura rápida desde la sesión y escritura/lectura en el repositorio para reconexiones y nuevos chats.

**Expectativas realistas:** si el proveedor MCP no envía OAuth con `sub` estable y tampoco `X-Client-Id`, solo tendrás continuidad fuerte con el bucket `default` (un usuario) o con lo que exponga `Context.client_id`. Para ChatGPT como app con OAuth, configura el servidor MCP con el flujo de auth de FastMCP para maximizar la clave `oauth:…`.

## Ejecución

```bash
python -m apk_mcp
# o
apk-mcp
```

Por defecto el endpoint MCP queda en `http://<MCP_HOST>:<MCP_PORT>/mcp` (FastMCP 3.x, transporte `streamable-http`).

Variables de entorno adicionales de FastMCP (opcionales) están documentadas en [gofastmcp.com](https://gofastmcp.com); este proyecto pasa `host`, `port` y `path` desde `MCP_HOST`, `MCP_PORT` y la ruta configurada en código (`/mcp` por defecto vía `Settings.mcp_path`).

## Uso con ChatGPT / Cursor

1. Despliega este servidor en una URL HTTPS accesible (o túnel tipo Cloudflare Tunnel / ngrok).
2. En el cliente, añade un servidor MCP remoto con la URL `https://tu-host/mcp`.
3. Configura `APK_API_BASE_URL` apuntando a tu instancia con el módulo **order_bridge**.

## Tools implementados

- **`list_products`**: `GET /api/order_bridge/products` (público) — paginación y filtros opcionales.

Más endpoints del contrato OpenAPI se pueden añadir en `src/apk_mcp/tools/` siguiendo el mismo patrón.

## Licencia

Proyecto de ejemplo / uso interno según tu organización.
