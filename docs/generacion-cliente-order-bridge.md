# Generación y uso del cliente y modelos order_bridge

Este documento explica cómo regenerar el código a partir del OpenAPI de **order_bridge** y cómo usarlo dentro de **apk-mcp**.

## Qué se genera

Tras ejecutar el comando de generación se crean o actualizan:

| Artefacto | Ruta | Herramienta | Rol |
|-----------|------|-------------|-----|
| **Modelos Pydantic** (esquemas del OpenAPI) | `src/apk_mcp/generated/order_bridge_models.py` | [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator) | Tipos `BaseModel` útiles para validar o documentar datos alineados con el contrato OpenAPI. |
| **Cliente HTTP** (endpoints listos) | `src/apk_mcp/generated/order_bridge_client/` | [openapi-python-client](https://github.com/openapi-generators/openapi-python-client) | Clase `Client` / `AuthenticatedClient` con **httpx**, más un módulo por operación bajo `api/default/`. Los cuerpos y respuestas aquí usan modelos **attrs** generados en `order_bridge_client/models/`. |

La especificación se descarga una vez a **`.cache/order_bridge_openapi.json`** (carpeta ignorada por git). Ese archivo es la entrada común para ambos generadores.

**Importante:** los modelos del **cliente generado** (attrs) y **`order_bridge_models.py`** (Pydantic) **no son la misma clase**: vienen de dos herramientas distintas. Para llamadas HTTP usa el cliente y sus `models`; para Pydantic “puros” según el mismo OpenAPI usa `order_bridge_models`. Evita mezclarlos en el mismo flujo sin una capa de conversión explícita.

## Requisitos previos

1. **Odoo** (o el host que sirva la API) en ejecución y accesible en la URL del OpenAPI (por defecto `http://localhost:8069/order_bridge/static/openapi.json`).
2. **`curl`** en el PATH (el script descarga el JSON con `curl -fsSL`).
3. Dependencias del proyecto: **`pnpm`** en la raíz del repo; para Python, **`uv`** (recomendado) o un entorno **`.venv`** con `pip`.

## Cómo generar todo con un solo comando

Desde la raíz del repositorio:

```bash
pnpm run gen:order-bridge-types
```

Esto ejecuta [`scripts/gen-order-bridge-api.sh`](../scripts/gen-order-bridge-api.sh), que:

1. Descarga el OpenAPI a `.cache/order_bridge_openapi.json`.
2. Regenera `order_bridge_models.py` con `datamodel-codegen`.
3. Regenera el directorio `order_bridge_client/` con `openapi-python-client` y **`--overwrite`** para que las ejecuciones sucesivas actualicen el cliente.

### Otra URL o entorno

Si el OpenAPI no está en el host por defecto:

```bash
OPENAPI_URL=https://mi-servidor.com/order_bridge/static/openapi.json pnpm run gen:order-bridge-types
```

También puedes invocar el script directamente:

```bash
bash scripts/gen-order-bridge-api.sh
```

Con **`uv`** instalado, el script ejecuta `uv sync` y los generadores con `uv run`. Sin `uv`, usa `.venv/bin/python` (o `python3`) e instala las dependencias de desarrollo necesarias con `pip` de forma silenciosa.

## Uso del cliente HTTP en el código

### URL base

El cliente generado concatena rutas relativas del OpenAPI (por ejemplo `/api/order_bridge/products`) con la **`base_url`** que pases al constructor.

Debe coincidir con el origen de la API Odoo **sin** path extra de módulo; suele ser el mismo valor que `APK_API_BASE_URL` en la configuración de apk-mcp (por ejemplo `http://localhost:8069`).

### Importaciones

Con el paquete instalado en modo editable o con `PYTHONPATH` apuntando a `src`:

```python
from apk_mcp.generated.order_bridge_client import Client
from apk_mcp.generated.order_bridge_client.api.default import order_bridge_products
```

### Llamada síncrona

Cada módulo bajo `api/default/` expone funciones como `sync`, `sync_detailed`, `asyncio` y `asyncio_detailed`. `*_detailed` devuelve un objeto `Response` con `status_code`, `headers` y `parsed`.

```python
client = Client(base_url="http://localhost:8069")

# Cuerpo tipado (o None / modelo de error según status)
data = order_bridge_products.sync(client=client, limit=20, offset=0)
if data is not None:
    # data es un modelo attrs generado (p. ej. ProductsPageResponse)
    ...
```

### Llamada asíncrona

```python
client = Client(base_url="http://localhost:8069")

data = await order_bridge_products.asyncio(client=client, limit=20, offset=0)
```

### Autenticación

Para rutas que exigen cabeceras o token según el OpenAPI, el generador expone **`AuthenticatedClient`**. Impórtalo desde el mismo paquete del cliente y pásalo donde el tipo acepte `Client | AuthenticatedClient`.

```python
from apk_mcp.generated.order_bridge_client import AuthenticatedClient

client = AuthenticatedClient(
    base_url="http://localhost:8069",
    token="tu_token_o_device_key",
    prefix="Bearer",  # valor por defecto; cámbialo si la API usa otro esquema
    auth_header_name="Authorization",  # por defecto
)
```

Los campos `token`, `prefix` y `auth_header_name` salen del cliente generado; si el OpenAPI define otra forma de autenticación, revisa `order_bridge_client/client.py` tras regenerar.

### Uso de los modelos Pydantic (`order_bridge_models.py`)

Sirven para tipar o validar datos contra el mismo contrato OpenAPI **sin** pasar por el cliente generado, por ejemplo en tests o en DTOs internos:

```python
from apk_mcp.generated import order_bridge_models

# Ejemplo: instancia o validación según el nombre de clase generado en el archivo
# item = order_bridge_models.Algo(...)
```

Abre `order_bridge_models.py` y usa las clases que correspondan a `components.schemas` del OpenAPI.

## Buenas prácticas

- **No edites a mano** los archivos bajo `generated/`; cualquier cambio se perderá en la próxima generación. Si necesitas adaptadores, colócalos en otro módulo (por ejemplo `apk_mcp/adapters/`).
- Tras cambios en la API Odoo, vuelve a ejecutar `pnpm run gen:order-bridge-types` y revisa el diff en git.
- Si el generador del cliente avisa de **ruff** no encontrado, puedes instalar **ruff** en el entorno virtual; la generación suele completarse igualmente.

## Más contexto

La visión general del servidor MCP y las capas internas está en [arquitectura.md](arquitectura.md). El código generado complementa el cliente manual `http_client.py`; puedes migrar herramientas poco a poco al cliente generado si lo deseas.
