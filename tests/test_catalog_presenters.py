from app.services.order_bridge.catalog_presenters import (
    present_fetch_product,
    present_search_results,
)


def test_present_search_results_maps_products():
    page = {
        "items": [
            {"id": 42, "name": "Arroz 1kg", "list_price": 120.0},
            {"id": 7, "name": "Frijoles", "list_price": 95.0},
        ],
        "total": 2,
    }
    out = present_search_results(page)
    assert out == {
        "results": [
            {"id": "42", "title": "Arroz 1kg", "url": "apk://catalog/products/42"},
            {"id": "7", "title": "Frijoles", "url": "apk://catalog/products/7"},
        ]
    }


def test_present_fetch_product_wraps_detail():
    detail = {"id": 42, "name": "Arroz 1kg", "list_price": 120.0}
    out = present_fetch_product(detail, product_id=42)
    assert out["id"] == "42"
    assert out["title"] == "Arroz 1kg"
    assert out["url"] == "apk://catalog/products/42"
    assert '"Arroz 1kg"' in out["text"]
    assert out["metadata"] == {"type": "product"}
