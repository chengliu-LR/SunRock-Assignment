"""FastAPI routes for the Orders resource.

This module wires HTTP handlers to the service layer. It intentionally keeps
logic minimal so that business rules live in the service.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models.orders import Order, OrderCreate, OrderUpdate
from app.repositories.orders import InMemoryOrderRepository
from app.services.orders import OrderService

router = APIRouter()

# Simple dependency injection for repository/service
repo = InMemoryOrderRepository()
service = OrderService(repo)


@router.get("/", response_model=List[Order])
async def list_orders():
    """Return all orders in the system."""
    return service.list()


@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """Return a single order by its id."""
    order = service.get(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(payload: OrderCreate):
    """Create a new order with market alignment and default rules."""
    return service.create(payload)


@router.put("/{order_id}", response_model=Order)
async def update_order(order_id: str, payload: OrderUpdate):
    """Update an existing order, adjusting window if expired."""
    updated = service.update(order_id, payload)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return updated


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: str):
    """Delete an order by id."""
    ok = service.delete(order_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return None
