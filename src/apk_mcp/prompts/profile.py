"""Profile prompts — address update with municipality/neighborhood ID resolution."""

from __future__ import annotations

from fastmcp.prompts import Message

from apk_mcp.server import mcp


@mcp.prompt(
    name="update_my_address",
    description=(
        "Update the user's delivery address: resolves municipality and neighborhood names "
        "to IDs using the locations nomenclator, calls update_profile (PATCH), then "
        "confirms the change with get_profile."
    ),
)
def update_my_address(
    street: str,
    state: str,
    municipality_name: str,
    neighborhood_name: str,
) -> list[Message]:
    return [
        Message(
            "The user wants to update their delivery address with the following details:\n"
            f"  Street: {street}\n"
            f"  State/Province: {state}\n"
            f"  Municipality: {municipality_name}\n"
            f"  Neighborhood: {neighborhood_name}\n\n"
            "Follow these steps:\n"
            "1. Read the resource apk://locations/municipalities to get the full "
            "list of municipalities and their neighborhoods.\n"
            f'2. Find the municipality whose name best matches "{municipality_name}" '
            "(case-insensitive). Note its id as municipality_id.\n"
            f'3. Within that municipality, find the neighborhood whose name best matches '
            f'"{neighborhood_name}". Note its id as neighborhood_id.\n'
            "4. If either cannot be found, show the available options to the user and ask "
            "them to choose.\n"
            "5. Call update_profile with:\n"
            f'   street="{street}", state="{state}", '
            "municipality_id=<id>, neighborhood_id=<id>.\n"
            "6. Call get_profile to verify the saved address and confirm the change to "
            "the user in a friendly summary."
        )
    ]
