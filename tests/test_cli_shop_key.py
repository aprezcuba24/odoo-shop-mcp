"""Unit tests for apk-mcp-shop-key CLI."""

from __future__ import annotations

from app.cli.shop_key import main
from app.utils.shop_key_codec import SHOP_KEY_BEARER_PREFIX, shop_context_from_encoded


def test_cli_prints_bearer_encoded_shop_key(capsys) -> None:
    code = main(["http://localhost:8069|test-token"])
    captured = capsys.readouterr()

    assert code == 0
    encoded = captured.out.strip()
    assert encoded.startswith(SHOP_KEY_BEARER_PREFIX)

    ctx = shop_context_from_encoded(encoded)
    assert ctx.base_url == "http://localhost:8069"
    assert ctx.bearer_token == "Bearer test-token"


def test_cli_verbose_prints_debug_on_stderr(capsys) -> None:
    code = main(
        ["https://shop.example.com|device-uuid", "--verbose"],
    )
    captured = capsys.readouterr()

    assert code == 0
    assert "base_url: https://shop.example.com" in captured.err
    assert "bearer_token: Bearer device-uuid" in captured.err
