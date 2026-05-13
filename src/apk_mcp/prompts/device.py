"""Device prompts — guided onboarding flow."""

from __future__ import annotations

from fastmcp.prompts import Message

from apk_mcp.server import mcp


@mcp.prompt(
    name="onboard_device",
    description=(
        "Register a new device and report its validation status. "
        "Calls register_device then get_device_status and presents a clear summary "
        "including whether human approval is still pending."
    ),
)
def onboard_device(
    device_key: str,
    phone: str | None = None,
) -> list[Message]:
    phone_line = f"  Phone: {phone}\n" if phone else ""
    return [
        Message(
            "The user wants to register a new device with the following details:\n"
            f"  Device key: {device_key}\n"
            f"{phone_line}\n"
            "Follow these steps:\n"
            "1. Call register_device with device_key and phone (if provided).\n"
            "2. Present the result: whether it was newly created (created flag), "
            "the partner_id, and whether it is validated.\n"
            "3. Call get_device_status to confirm the current validation state.\n"
            "4. If validated is false, clearly explain to the user that the device "
            "registration is pending approval in the store backend (Odoo) and that "
            "authenticated features (orders, profile) will be available once approved.\n"
            "5. If validated is true, confirm that the device is fully active and ready "
            "to use all features."
        )
    ]
