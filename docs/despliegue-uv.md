# Despliegue y uso con uv

[uv](https://docs.astral.sh/uv/) gestiona el intérprete, el entorno virtual y las dependencias a partir de `pyproject.toml`.

## Requisitos

- [uv instalado](https://docs.astral.sh/uv/getting-started/installation/) (una vez en la máquina o en la imagen CI).

## Proyecto local

```bash
cd ApkMCP
cp .env.example .env   # edita APK_API_TIMEOUT y bind MCP
uv sync
```

`uv sync` crea/actualiza `.venv`, instala dependencias y el paquete en modo editable.

## Ejecutar el servidor MCP

```bash
uv run python -m apk_mcp
# o
uv run apk-mcp
```

Por defecto escucha en `http://0.0.0.0:8000/mcp` (ajustable con `MCP_HOST`, `MCP_PORT`, `MCP_PATH` en `.env`).

## Comandos útiles

| Comando | Uso |
|---------|-----|
| `uv sync` | Alinear entorno con `pyproject.toml` tras cambiar dependencias. |
| `uv add nombre-paquete` | Añadir dependencia y actualizar el lockfile si usas `uv lock`. |
| `uv run <comando>` | Ejecutar en el venv del proyecto sin activarlo manualmente. |

## Despliegue (idea general)

1. Clonar/copiar el repo en el servidor o construir una imagen que ejecute `uv sync` (o `uv sync --frozen` si versionas `uv.lock`).
2. Variables de entorno o `.env` con bind MCP (`MCP_HOST`, `MCP_PORT`, `MCP_PATH`) y carrito (`CART_STORE_BACKEND`, `DYNAMODB_CART_TABLE` en Lambda). El backend Odoo va en `shop-key` (`Bearer` + base64 `URL|user_token`).
3. Proceso bajo systemd, Docker o PaaS ejecutando `uv run apk-mcp` (o el binario equivalente en tu imagen).
4. Exponer **HTTPS** hacia el endpoint `/mcp` si el cliente es remoto (p. ej. ChatGPT).

Para generar lockfile reproducible: `uv lock` en el repo y en CI/despliegue `uv sync --frozen`.
