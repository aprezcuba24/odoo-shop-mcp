"""``python -m apk_mcp`` entrypoint."""

from __future__ import annotations

from apk_mcp.server import run


def main() -> None:
    run()


if __name__ == "__main__":
    main()
