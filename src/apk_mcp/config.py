"""Application settings (environment / .env)."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    mcp_port: int = Field(default=7000, ge=1, le=65535)
    mcp_path: str = Field(default="/mcp")

    apk_mcp_tenant_header: str = Field(
        default="X-Apk-Tenant-Id",
        description=(
            "HTTP header that identifies the MCP client for multi-tenant isolation "
            "(same value keys the in-memory device/Bearer token)."
        ),
    )
    apk_mcp_fallback_tenant_id: str = Field(
        default="default",
        description=(
            "Tenant id when the header is absent and APK_MCP_REQUIRE_TENANT_HEADER is false "
            "(local dev / single anonymous client)."
        ),
    )
    apk_mcp_require_tenant_header: bool = Field(
        default=False,
        description="If true, every request must include the tenant header; fallback is ignored.",
    )


def get_settings() -> Settings:
    return Settings()
