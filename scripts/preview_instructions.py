#!/usr/bin/env python3
"""Preview MCP server instructions as rendered for the client.

Run from repo root:
  pnpm run instructions:preview
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load_instructions_module():
    path = Path(__file__).resolve().parent.parent / "app" / "server" / "instructions.py"
    spec = importlib.util.spec_from_file_location("apk_mcp_instructions", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load instructions from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = _load_instructions_module()
    text: str = module.instructions
    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")
    print(
        f"--- {len(text.splitlines())} lines, {len(text)} chars ---",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
