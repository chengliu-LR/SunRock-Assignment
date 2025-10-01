from fastapi.testclient import TestClient
from app.main import app
from app.models.orders import OrderType, MarketType

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_crud_flow():
    payload = {"orderType": OrderType.BUY, "type": MarketType.INTRADAY, "quantity": 3.0}
    res = client.post("/api/v1/orders/", json=payload)
    assert res.status_code == 201
    order = res.json()

    res_get = client.get(f"/api/v1/orders/{order['id']}")
    assert res_get.status_code == 200

    res_list = client.get("/api/v1/orders/")
    assert res_list.status_code == 200
    assert len(res_list.json()) >= 1

    res_delete = client.delete(f"/api/v1/orders/{order['id']}")
    assert res_delete.status_code == 204
