"""
Order Schemas (Pydantic Models)
===============================
Pydantic schemas for order request validation and response formatting.

Order creation is the most complex operation in the system:
1. Client sends customer_id and a list of items (product_id + quantity)
2. Server validates everything, calculates totals, and creates the order
3. Response includes the full order with customer name and item details

Key Concepts:
- Nested schemas: OrderCreate contains a list of OrderItemCreate objects
- Computed fields: OrderResponse includes customer_name and product_name
  which are looked up from related tables (not stored in the order itself)
- min_length=1 on the items list ensures at least one item is in the order
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    """
    Schema for a single item in a new order.
    
    Used in: POST /api/orders (nested inside OrderCreate)
    
    Example: {"product_id": 1, "quantity": 3}
    This means: "Order 3 units of product with ID 1"
    """
    product_id: int = Field(..., description="ID of the product to order")
    quantity: int = Field(..., gt=0, description="Number of units to order (must be > 0)")


class OrderItemResponse(BaseModel):
    """
    Schema for order item data in API responses.
    
    Includes the product_name for convenience so the frontend doesn't
    need to make a separate API call to get the product name.
    """
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: float  # Price at the time of purchase (snapshot)
    product_name: Optional[str] = None  # Populated from the related Product

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    """
    Schema for creating a new order.
    
    Used in: POST /api/orders
    
    Validation rules:
    - customer_id: Required (must reference an existing customer)
    - items: At least one item must be provided (min_length=1)
    
    Example request body:
    {
        "customer_id": 1,
        "items": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 3, "quantity": 1}
        ]
    }
    """
    customer_id: int = Field(..., description="ID of the customer placing the order")
    items: List[OrderItemCreate] = Field(
        ...,
        min_length=1,
        description="List of items to order (at least 1 required)"
    )


class OrderResponse(BaseModel):
    """
    Schema for order data returned in API responses.
    
    Includes nested items list and customer_name for convenience.
    The total_amount is calculated server-side as sum(item.price * item.quantity).
    """
    id: int
    customer_id: int
    customer_name: Optional[str] = None  # Populated from the related Customer
    total_amount: float
    created_at: datetime
    items: List[OrderItemResponse] = []  # List of items in the order

    model_config = ConfigDict(from_attributes=True)
