"""
Dashboard Routes (API Endpoints)
================================
Dashboard endpoint provides a summary/overview of the system.

This is useful for a frontend dashboard page that shows:
- Total products, customers, and orders count
- List of products with low stock (< 10 units)
- Count of low stock products

This endpoint aggregates data from multiple tables in a single API call,
which is more efficient than making multiple separate API calls from the frontend.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.connection import get_db
from app.models.product import Product
from app.models.customer import Customer
from app.models.order import Order


# --- Dashboard Response Schema ---
# Defined here since it's only used by the dashboard endpoint

class LowStockProduct(BaseModel):
    """Schema for low stock product items in the dashboard response."""
    id: int
    name: str
    sku: str
    quantity_in_stock: int

    model_config = {"from_attributes": True}


class TopProduct(BaseModel):
    """Schema for top products in the stock level bar chart."""
    id: int
    name: str
    quantity: int  # mapped from quantity_in_stock for frontend simplicity

    model_config = {"from_attributes": True}


class DashboardResponse(BaseModel):
    """
    Schema for the dashboard summary response.
    
    Provides an at-a-glance overview of the entire system.
    """
    total_products: int
    total_customers: int
    total_orders: int
    low_stock_products: List[LowStockProduct]
    low_stock_count: int
    top_products: List[TopProduct]


# Create router
router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    """
    Get dashboard summary data.
    
    Returns:
    - total_products: Total number of products in the system
    - total_customers: Total number of registered customers
    - total_orders: Total number of orders placed
    - low_stock_products: List of products with stock < 10
    - low_stock_count: Number of products with low stock
    - top_products: Top 10 products by stock level (for bar chart)
    
    This single endpoint replaces the need for multiple API calls
    from the frontend dashboard page.
    """
    try:
        # Count totals using SQLAlchemy's count() - more efficient than len(query.all())
        # count() generates a SQL COUNT query instead of loading all rows into memory
        total_products = db.query(Product).count()
        total_customers = db.query(Customer).count()
        total_orders = db.query(Order).count()

        # Get products with low stock (less than 10 units)
        low_stock_products = db.query(Product).filter(
            Product.quantity_in_stock < 10
        ).order_by(Product.quantity_in_stock.asc()).all()  # Sort by lowest stock first

        # Get top 10 products by stock for the dashboard bar chart
        top_products_raw = db.query(Product).order_by(
            Product.quantity_in_stock.desc()
        ).limit(10).all()

        # Map quantity_in_stock -> quantity for frontend simplicity
        top_products = [
            TopProduct(id=p.id, name=p.name, quantity=p.quantity_in_stock)
            for p in top_products_raw
        ]

        return DashboardResponse(
            total_products=total_products,
            total_customers=total_customers,
            total_orders=total_orders,
            low_stock_products=low_stock_products,
            low_stock_count=len(low_stock_products),
            top_products=top_products
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
