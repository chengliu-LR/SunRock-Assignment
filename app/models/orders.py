"""Pydantic schemas and enums for the electricity order domain.

These models define the external API contract and validate inputs:
- Enforce valid ``orderType`` and fixed ``productType`` (ELECTRICITY)
- Validate positive ``quantity``
"""

from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class OrderType(str, Enum):
    """Whether its purchase or sale for the order."""

    BUY = "BUY"
    SELL = "SELL"


class MarketType(str, Enum):
    """Market category.

    DAH (Day-Ahead) uses tomorrow as base day; Intra-Day uses today.
    """

    DAH = "DAH"
    INTRADAY = "Intra-Day"


PRODUCT_TYPE = "ELECTRICITY"


class OrderBase(BaseModel):
    """Base fields shared by create/update/response models."""

    orderType: OrderType
    productType: str = Field(default=PRODUCT_TYPE)
    type: Optional[MarketType] = None
    quantity: float

    @field_validator("productType")
    @classmethod
    def validate_product_type(cls, v: str) -> str:
        """Ensure only ELECTRICITY is accepted for productType."""
        if v != PRODUCT_TYPE:
            raise ValueError("productType must be ELECTRICITY")
        return v

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v: float) -> float:
        """Quantity must be strictly positive in MWh."""
        if v <= 0:
            raise ValueError("quantity must be positive")
        return v


class OrderCreate(OrderBase):
    """Payload for creating a new order.

    ``start``/``end`` are miliseconds. If omitted, service will set defaults
    per market rules and 15-minute duration.
    """

    start: Optional[int] = None
    end: Optional[int] = None


class OrderUpdate(BaseModel):
    """Partial update payload.

    If ``end`` is in the past, the service will auto-adjust the window.
    """

    orderType: Optional[OrderType] = None
    type: Optional[MarketType] = None
    quantity: Optional[float] = None
    start: Optional[int] = None
    end: Optional[int] = None


class Order(OrderBase):
    """Order representation returned by the API."""

    id: str
    created: int
    start: int
    end: int
