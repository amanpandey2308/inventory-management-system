"""
Order Routes (API Endpoints)
============================
HTTP endpoints for order operations.

Order creation is the most complex endpoint because it:
1. Validates customer and all products exist
2. Checks stock availability for each item
3. Calculates total amount
4. Creates the order with items in a single transaction
5. Reduces stock quantities

Endpoints:
- POST /api/orders      → Create a new order
- GET /api/orders        → List all orders
- GET /api/orders/{id}   → Get an order by ID
- DELETE /api/orders/{id} → Delete an order
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services import order_service
from app.utils.exceptions import NotFoundError, InsufficientStockError

# Create router with prefix and tag
router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order.
    
    Request Body:
    - customer_id: ID of the customer placing the order (required)
    - items: List of items to order (at least 1 required)
      - product_id: ID of the product (required)
      - quantity: Number of units (required, must be > 0)
    
    What happens:
    1. Verifies the customer exists
    2. Verifies each product exists and has enough stock
    3. Calculates total amount (sum of price × quantity for each item)
    4. Creates the order and all order items
    5. Reduces stock for each ordered product
    
    Returns: Created order with customer name, items, and totals
    
    Errors:
    - 400: Insufficient stock for one or more products
    - 404: Customer or product not found
    - 422: Validation error (empty items list, invalid quantity, etc.)
    """
    try:
        return order_service.create_order(db, order_data)
    except NotFoundError as e:
        # 404 - Customer or product doesn't exist
        raise HTTPException(status_code=404, detail=e.detail)
    except InsufficientStockError as e:
        # 400 Bad Request - not enough stock to fulfill the order
        raise HTTPException(status_code=400, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/", response_model=List[OrderResponse])
def get_all_orders(db: Session = Depends(get_db)):
    """
    Get all orders with customer info and items.
    
    Returns: List of all orders with:
    - Customer name (from relationship)
    - Order items with product names
    - Total amount
    
    Orders are sorted by newest first.
    """
    try:
        return order_service.get_all_orders(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """
    Get a single order by ID with full details.
    
    Path Parameters:
    - order_id: The ID of the order to retrieve
    
    Returns: Order with customer name, items, product names, and totals
    
    Errors:
    - 404: Order not found
    """
    try:
        return order_service.get_order_by_id(db, order_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """
    Delete an order and its items.
    
    Path Parameters:
    - order_id: The ID of the order to delete
    
    Returns: Success message
    
    Errors:
    - 404: Order not found
    
    Note: Order items are automatically deleted via cascade.
    Stock quantities are NOT restored (by design).
    """
    try:
        return order_service.delete_order(db, order_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
