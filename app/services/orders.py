"""Business logic for electricity orders.

The service enforces market rules independent of persistence:
- Start times align to the next quarter-hour boundary
- DAH vs Intra-Day default windows
- Update auto-adjustment if an order's end time is already past
"""

from datetime import datetime, timedelta, timezone
import uuid
from typing import Optional

from app.models.orders import (
    Order,
    OrderCreate,
    OrderUpdate,
    PRODUCT_TYPE,
    MarketType,
)
from app.repositories.orders import OrderRepository
from app.utils.time import align_to_next_quarter, ms

FIFTEEN_MINUTES = 15 * 60 * 1000


class OrderService:
    """Coordinate validation, defaulting, and alignment for orders."""

    def __init__(self, repo: OrderRepository) -> None:
        self.repo = repo

    def _default_start_end(self, market_type: Optional[MarketType]) -> tuple[int, int]:
        """Compute default window [start, end) in ms based on market type."""
        now = datetime.now(timezone.utc)
        if market_type == MarketType.DAH:
            start_base = datetime(now.year, now.month, now.day, tzinfo=timezone.utc) + timedelta(days=1)
        else:
            start_base = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
        start_aligned = align_to_next_quarter(now if market_type != MarketType.DAH else start_base)
        start_ms = ms(start_aligned)
        end_ms = start_ms + FIFTEEN_MINUTES
        return start_ms, end_ms

    def create(self, data: OrderCreate) -> Order:
        """Create a new order, applying alignment and default duration rules."""
        start = data.start
        end = data.end
        if start is None or end is None:
            start, end = self._default_start_end(data.type)
        else:
            dt_start = datetime.fromtimestamp(start / 1000, tz=timezone.utc)
            aligned = align_to_next_quarter(dt_start)
            start = ms(aligned)
            if end <= start:
                end = start + FIFTEEN_MINUTES

        order = Order(
            id=str(uuid.uuid4()),
            orderType=data.orderType,
            productType=PRODUCT_TYPE,
            type=data.type,
            quantity=data.quantity,
            created=ms(datetime.now(timezone.utc)),
            start=start,
            end=end,
        )
        return self.repo.create(data, order)

    def list(self) -> list[Order]:
        """Return all orders."""
        return self.repo.list()

    def get(self, order_id: str) -> Optional[Order]:
        """Return a single order by id or None if not found."""
        return self.repo.get(order_id)

    def update(self, order_id: str, data: OrderUpdate) -> Optional[Order]:
        """Update an order, adjusting time window when necessary.

        - If ``end`` is in the past, set ``start = now`` and ``end = start + 15m``.
        - Otherwise, ensure ``start`` is aligned and ``end > start``.
        """
        existing = self.repo.get(order_id)
        if not existing:
            return None
        orderType = data.orderType or existing.orderType
        type_ = data.type or existing.type
        quantity = data.quantity if data.quantity is not None else existing.quantity
        start = data.start if data.start is not None else existing.start
        end = data.end if data.end is not None else existing.end

        now_ms = ms(datetime.now(timezone.utc))
        if end < now_ms:
            start = now_ms
            end = now_ms + FIFTEEN_MINUTES
        else:
            aligned_start = ms(
                align_to_next_quarter(datetime.fromtimestamp(start / 1000, tz=timezone.utc))
            )
            if aligned_start != start:
                start = aligned_start
            if end <= start:
                end = start + FIFTEEN_MINUTES

        updated = Order(
            id=existing.id,
            orderType=orderType,
            productType=PRODUCT_TYPE,
            type=type_,
            quantity=quantity,
            created=existing.created,
            start=start,
            end=end,
        )
        return self.repo.update(order_id, data, updated)

    def delete(self, order_id: str) -> bool:
        """Delete an order and return True if it existed."""
        return self.repo.delete(order_id)
