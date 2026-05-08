"""Typed errors for REST bridge."""

from __future__ import annotations

from typing import Any


class ApkMcpError(Exception):
    """Base error for this package."""


class ApkApiError(ApkMcpError):
    """REST API returned an error response."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class UnauthorizedError(ApkApiError):
    """401 — invalid or missing device Bearer token."""


class ValidationApiError(ApkApiError):
    """400 — validation or business rule (often Pydantic-style payload)."""


class NotFoundError(ApkApiError):
    """404 — resource not found."""


class MessageApiError(ApkApiError):
    """400 with structured error + message."""
