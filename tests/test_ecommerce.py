import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_list_products():
    res = client.get("/api/v1/orders/products")
    assert res.status_code == 200
    assert len(res.json()) >= 4

def test_successful_checkout():
    payload = {"product_id": 101, "quantity": 2}
    res = client.post("/api/v1/orders/checkout", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "CONFIRMED"
    assert data["quantity"] == 2
    assert data["remaining_stock"] == 23

def test_insufficient_stock_rejection():
    # Product 102 only has 10 in stock, requesting 15 should trigger a 400 Bad Request
    payload = {"product_id": 102, "quantity": 15}
    res = client.post("/api/v1/orders/checkout", json=payload)
    assert res.status_code == 400
