from datetime import datetime, timezone, timedelta

from app.models.orders import OrderCreate, OrderType, MarketType
from app.repositories.orders import InMemoryOrderRepository
from app.services.orders import OrderService, FIFTEEN_MINUTES


def make_service():
    return OrderService(InMemoryOrderRepository())


def test_create_defaults_intraday_aligns():
    svc = make_service()
    order = svc.create(OrderCreate(orderType=OrderType.BUY, type=MarketType.INTRADAY, quantity=1.0))
    assert order.end - order.start == FIFTEEN_MINUTES


def test_create_with_custom_start_aligns_and_end_defaults():
    svc = make_service()
    now = datetime.now(timezone.utc)
    custom_start = int(now.timestamp() * 1000)
    order = svc.create(
        OrderCreate(orderType=OrderType.SELL, type=MarketType.INTRADAY, quantity=2.5, start=custom_start, end=custom_start)
    )
    assert order.end - order.start == FIFTEEN_MINUTES


def test_update_expired_adjusts_window():
    svc = make_service()
    created = svc.create(OrderCreate(orderType=OrderType.BUY, type=MarketType.INTRADAY, quantity=1.0))
    past_end = int((datetime.now(timezone.utc) - timedelta(hours=1)).timestamp() * 1000)
    updated = svc.update(created.id, type("U", (), {"orderType": None, "type": None, "quantity": None, "start": None, "end": past_end})())
    assert updated is not None
    assert updated.end - updated.start == FIFTEEN_MINUTES
    assert updated.start <= updated.end
