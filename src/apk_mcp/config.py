"""Application settings (environment / .env)."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

DeviceKeyStoreMode = Literal["context", "sqlite", "layered"]
DeviceKeyPersistenceBackend = Literal["sqlite", "memory"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    apk_api_base_url: str = Field(
        default="http://localhost:8069",
        description="Base URL of the Odoo / API host (no trailing path).",
    )
    apk_api_timeout: float = Field(default=30.0, ge=1.0)
    mcp_host: str = Field(default="0.0.0.0")
    mcp_port: int = Field(default=8000, ge=1, le=65535)
    mcp_path: str = Field(default="/mcp")

    device_key_store_mode: DeviceKeyStoreMode = Field(
        default="layered",
        description="context = session only; sqlite = repository only; layered = cache + repository.",
    )
    device_key_persistence_backend: DeviceKeyPersistenceBackend = Field(
        default="sqlite",
        description="Repository implementation: sqlite (file) or memory (tests).",
    )
    device_key_db_path: Path = Field(default=Path("./data/device_keys.sqlite"))


def get_settings() -> Settings:
    return Settings()
