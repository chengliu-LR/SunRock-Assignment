"""Repository abstraction and in-memory implementation for orders.

The repository interface enables swapping storage backends (e.g. Postgres,
MongoDB, Redis) without changing business logic in the service layer.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from app.models.orders import Order, OrderCreate, OrderUpdate


class OrderRepository(ABC):
    """Storage interface for orders."""

    @abstractmethod
    def list(self) -> List[Order]: ...

    @abstractmethod
    def get(self, order_id: str) -> Optional[Order]: ...

    @abstractmethod
    def create(self, data: OrderCreate, order: Order) -> Order: ...

    @abstractmethod
    def update(self, order_id: str, data: OrderUpdate, order: Order) -> Optional[Order]: ...

    @abstractmethod
    def delete(self, order_id: str) -> bool: ...


class InMemoryOrderRepository(OrderRepository):
    """Simple dictionary-backed repository for development and tests."""

    def __init__(self) -> None:
        self._db: Dict[str, Order] = {}

    def list(self) -> List[Order]:
        return list(self._db.values())

    def get(self, order_id: str) -> Optional[Order]:
        return self._db.get(order_id)

    def create(self, data: OrderCreate, order: Order) -> Order:
        self._db[order.id] = order
        return order

    def update(self, order_id: str, data: OrderUpdate, order: Order) -> Optional[Order]:
        if order_id not in self._db:
            return None
        self._db[order_id] = order
        return order

    def delete(self, order_id: str) -> bool:
        return self._db.pop(order_id, None) is not None
