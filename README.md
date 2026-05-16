# apk-mcp

Servidor [MCP](https://modelcontextprotocol.io/) (Model Context Protocol) en Python que hace de puente hacia la API REST **Tienda Apk** (`/api/order_bridge/`), usando **FastMCP** con transporte **Streamable HTTP**.

## Requisitos

- Python 3.11+
- Para las herramientas de desarrollo Node ([MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)): Node.js **22.7.5+** y **pnpm** (ver [Desarrollo / MCP Inspector](#desarrollo--mcp-inspector)).


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
| `APK_MCP_TENANT_HEADER` | Cabecera HTTP que identifica al cliente/inquilino (defecto: `X-Apk-Tenant-Id`) |
| `APK_MCP_FALLBACK_TENANT_ID` | Valor de tenant usado si falta la cabecera y no exiges cabecera obligatoria (defecto: `default`) |
| `APK_MCP_REQUIRE_TENANT_HEADER` | Si es `true`, cada petición MCP debe incluir la cabecera de tenant (sin fallback) |

### Autenticación (multi-tenant, Bearer y registro)

La API usa `Authorization: Bearer <token>` salvo rutas públicas (catálogo, `POST /register`, etc.).

El servidor MCP es **multi-tenant**: el cliente debe enviar la cabecera configurada (por defecto **`X-Apk-Tenant-Id`**) en cada petición HTTP al endpoint Streamable HTTP, para aislar dispositivos. Para cada valor de tenant, el proceso genera **en memoria** un token opaco ([`InMemoryTenantCredentialStore`](src/apk_mcp/utils/tenant_credentials.py)) que se usa **tanto** en `POST /register` como `device_key` **como** en el Bearer hacia Tienda Apk. **No hay disco**; al reiniciar el proceso se pierden esas claves (aceptable en desarrollo).

Si no envías cabecera y `APK_MCP_REQUIRE_TENANT_HEADER` es `false`, se usa `APK_MCP_FALLBACK_TENANT_ID` (por defecto `default`), equivalente a un único cliente anónimo en local.

Si Tienda Apk exige que el dispositivo esté registrado en Odoo, un **401** puede indicar que el token aún no está vinculado o aprobado en la API, no un fallo local de “falta token”.

## Ejecución

```bash
python -m apk_mcp
# o
apk-mcp
```

Por defecto el endpoint MCP queda en `http://<MCP_HOST>:<MCP_PORT>/mcp` (FastMCP 3.x, transporte `streamable-http`).

Variables de entorno adicionales de FastMCP (opcionales) están documentadas en [gofastmcp.com](https://gofastmcp.com); este proyecto pasa `host`, `port` y `path` desde `MCP_HOST`, `MCP_PORT` y la ruta configurada en código (`/mcp` por defecto vía `Settings.mcp_path`).

## Desarrollo / MCP Inspector

[Herramienta oficial](https://modelcontextprotocol.io/docs/tools/inspector) para probar y depurar servidores MCP (solo desarrollo local; no forma parte del despliegue en producción).

1. Instala dependencias Node en la raíz del repo: `pnpm install`.
2. Arranca el servidor FastMCP y el Inspector en **un solo terminal**: `pnpm dev` (usa [concurrently](https://www.npmjs.com/package/concurrently) para lanzar `uv run apk-mcp` y el inspector en paralelo).
3. Abre la UI del Inspector (por defecto `http://localhost:6274`). En la consola aparece un **token de sesión** del proxy: úsalo si la UI lo pide (no desactivar la autenticación salvo que entiendas los riesgos descritos en el proyecto [inspector](https://github.com/modelcontextprotocol/inspector)).
4. Conecta con transporte **Streamable HTTP** a la URL del servidor MCP, p. ej. `http://localhost:8000/mcp` (ajusta puerto y ruta si cambiaste `MCP_PORT` o `MCP_PATH`). Atajo con query params: `http://localhost:6274/?transport=streamable-http&serverUrl=http://localhost:8000/mcp`.
5. Opcional: `pnpm run inspector -- --config dev/mcp-inspector.config.json --server apk-mcp-local` para cargar la entrada `streamable-http` hacia `http://127.0.0.1:8000/mcp` (actualiza el JSON si el bind no es el predeterminado).

También puedes ejecutar por separado `pnpm run mcp:server` y `pnpm run inspector` en dos terminales.

## Uso con ChatGPT / Cursor

1. Despliega este servidor en una URL HTTPS accesible (o túnel tipo Cloudflare Tunnel / ngrok).
2. En el cliente, añade un servidor MCP remoto con la URL `https://tu-host/mcp`. Si tu host MCP permite cabeceras personalizadas, configura **`X-Apk-Tenant-Id`** (o el nombre definido en `APK_MCP_TENANT_HEADER`) por usuario o workspace para aislar sesiones.
3. Configura `APK_API_BASE_URL` apuntando a tu instancia con el módulo **order_bridge**.

## VS Code y GitHub Copilot (agentes / Chat)

Este servidor expone **Streamable HTTP**; en VS Code se declara como servidor MCP de tipo **`http`**. El cliente intenta primero el transporte HTTP stream y, si hace falta, compatible con SSE (ver [referencia MCP en VS Code](https://code.visualstudio.com/docs/copilot/reference/mcp-configuration)).

1. Arranca el servidor MCP en local (o detrás de HTTPS si es remoto), p. ej. `python -m apk_mcp`, y anota la URL completa del endpoint (host, puerto y ruta), p. ej. `http://127.0.0.1:7000/mcp`.
2. Abre la configuración MCP del **workspace** o del **usuario**:
   - Paleta de comandos: **“MCP: Open Workspace Folder MCP Configuration”** → crea o edita [`.vscode/mcp.json`](https://code.visualstudio.com/docs/copilot/customization/mcp-servers), o
   - **“MCP: Open User Configuration”** si quieres el mismo servidor en todos los proyectos.
3. Añade una entrada en `servers` con la URL que incluya el path (`/mcp` por defecto). Para multi-tenant, usa `headers` con la misma cabecera que `APK_MCP_TENANT_HEADER` (por defecto `X-Apk-Tenant-Id`):

```json
{
  "servers": {
    "yyMercadoApk": {
      "type": "http",
      "url": "http://127.0.0.1:7000/mcp",
      "headers": {
        "X-Apk-Tenant-Id": "vscode-mi-workspace"
      }
    }
  }
}
```

4. Comprueba que el servidor aparece y puede iniciarse: paleta **“MCP: List Servers”**. Si cambias tools o recursos en el servidor y el IDE no los refleja, prueba **“MCP: Reset Cached Tools”**.
5. Revisa el acceso a MCP en ajustes de VS Code si el servidor no se usa en el chat/agente: [`chat.mcp.access`](https://code.visualstudio.com/docs/copilot/reference/copilot-settings) (documentación de **GitHub Copilot** / MCP en VS Code).

**Nota:** Copilot suele mostrar con claridad las **tools** MCP; **resources** y **prompts** dependen de cómo el host los enlaza al chat o a la ventana de agentes. Para depurar el protocolo sin el IDE, usa la sección [Desarrollo / MCP Inspector](#desarrollo--mcp-inspector).

Más detalle en la documentación de GitHub: [Extender Copilot Chat con servidores MCP](https://docs.github.com/en/copilot/customizing-copilot/extending-copilot-chat-with-mcp?tool=vscode).

## Surface MCP implementada

### Tools

| Nombre | Endpoint | Auth |
|--------|----------|------|
| `list_products` | `GET /products` | Público |
| `get_product` | `GET /products/{id}` | Público |
| `register_device` | `POST /register` | Público |
| `get_device_status` | `GET /status` | Bearer |
| `list_orders` | `GET /orders` | Bearer |
| `get_order` | `GET /orders/{id}` | Bearer |
| `create_order` | `POST /orders` | Bearer |
| `cancel_order` | `POST /orders/{id}/cancel` | Bearer |
| `get_profile` | `GET /profile` | Bearer |
| `update_profile` | `PATCH /profile` | Bearer |
| `replace_profile` | `PUT /profile` | Bearer |
| `register_push_token` | `POST /push/token` | Bearer |
| `update_push_topics` | `PATCH /push/topics` | Bearer |

### Resources

| URI | Descripción | Auth |
|-----|-------------|------|
| `yy-shop://catalog/categories` | Lista de categorías de producto | Público |
| `yy-shop://catalog/banners` | Banners publicitarios activos | Público |
| `yy-shop://catalog/products/{product_id}` | Detalle de producto | Público |
| `yy-shop://store/settings` | Configuración general de la tienda | Público |
| `yy-shop://locations/municipalities` | Municipios y barrios (nomencladores) | Público |
| `yy-shop://session/status` | Estado de validación del dispositivo | Bearer |
| `yy-shop://session/profile` | Perfil del contacto del dispositivo | Bearer |
| `yy-shop://orders/{order_id}` | Detalle de pedido con líneas | Bearer |

### Prompts

| Nombre | Descripción |
|--------|-------------|
| `find_products` | Búsqueda con resolución automática de categoría |
| `place_order` | Carrito en lenguaje natural → `create_order` con manejo de stock |
| `track_order` | Estado y líneas formateadas de un pedido |
| `reorder_last` | Repetir el último pedido con confirmación |
| `update_my_address` | Actualizar dirección resolviendo IDs de municipio/barrio |
| `onboard_device` | Registrar dispositivo (token interno por tenant) y reportar validación |

Añadir nuevos endpoints sigue el patrón en `src/apk_mcp/tools/`, `src/apk_mcp/resources/` y `src/apk_mcp/prompts/`; ver también `.agents/skills/apk-mcp-tools/SKILL.md`.

## Licencia

Proyecto de ejemplo / uso interno según tu organización.
