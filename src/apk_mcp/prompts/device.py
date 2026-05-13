"""Prompts de dispositivo — flujo guiado de registro (onboarding)."""

from __future__ import annotations

from fastmcp.prompts import Message

from apk_mcp.server import mcp


@mcp.prompt(
    name="onboard_device",
    description=(
        "Registra un dispositivo nuevo e informa de su estado de validación. "
        "Llama a register_device y luego get_device_status y resume de forma clara "
        "si falta aprobación humana."
    ),
)
def onboard_device(
    device_key: str,
    phone: str | None = None,
) -> list[Message]:
    phone_line = f"  Teléfono: {phone}\n" if phone else ""
    return [
        Message(
            "El usuario quiere registrar un dispositivo nuevo con estos datos:\n"
            f"  Clave de dispositivo: {device_key}\n"
            f"{phone_line}\n"
            "Sigue estos pasos:\n"
            "1. Llama a register_device con device_key y phone (si se proporcionó).\n"
            "2. Presenta el resultado: si es registro nuevo (created), el partner_id y si está validado.\n"
            "3. Llama a get_device_status para confirmar el estado de validación actual.\n"
            "4. Si validated es false, explica con claridad que el registro está pendiente de aprobación "
            "en la tienda (Odoo) y que las funciones con autenticación (pedidos, perfil) estarán "
            "disponibles cuando se apruebe.\n"
            "5. Si validated es true, confirma que el dispositivo está activo y listo para usar todas las funciones."
        )
    ]
