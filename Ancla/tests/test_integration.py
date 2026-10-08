"""Integration check: Lovable origin -> FastAPI (/api/loans, /api/collateral) and Pulse import map.

Run with the API up: python test_integration.py   (or: pytest test_integration.py)
"""
import importlib
import os

import requests

BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8001")
LOVABLE = "https://preview--anchor-lend-connect.lovable.app"


def test_pulse_import_path():
    module = importlib.import_module("peer_lending_backend.src.routers.loans")
    paths = {r.path for r in module.router.routes}
    assert "/api/loans" in paths and "/api/loans/{loan_id}/approve" in paths


def test_health():
    assert requests.get(f"{BASE}/health", timeout=5).status_code == 200


def test_cors_preflight_for_lovable():
    for path in ("/api/loans", "/api/collateral"):
        r = requests.options(
            f"{BASE}{path}",
            headers={"Origin": LOVABLE, "Access-Control-Request-Method": "GET"},
            timeout=5,
        )
        assert r.status_code == 200
        assert r.headers.get("access-control-allow-origin") == LOVABLE


def test_loans_and_collateral_routes():
    headers = {"Origin": LOVABLE}
    for path in ("/api/loans?status=pending", "/api/collateral"):
        r = requests.get(f"{BASE}{path}", headers=headers, timeout=10)
        assert r.status_code == 200, f"{path}: {r.status_code} {r.text}"
        assert isinstance(r.json(), list)
        assert r.headers.get("access-control-allow-origin") == LOVABLE


if __name__ == "__main__":
    import sys

    import pytest

    sys.exit(pytest.main([__file__, "-v"]))
