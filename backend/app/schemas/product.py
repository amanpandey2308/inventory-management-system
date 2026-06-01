"""
Product Schemas (Pydantic Models)
=================================
Pydantic schemas for request validation and response serialization of products.

Why separate schemas from SQLAlchemy models?
- SQLAlchemy models define the DATABASE structure (what's stored)
- Pydantic schemas define the API structure (what's sent/received)
- This separation gives us control over what data the API accepts and returns
- Pydantic automatically validates incoming data and returns clear error messages

Schema Types:
- ProductCreate: Validates data when creating a new product (POST request body)
- ProductUpdate: Validates data when updating a product (PUT request body)
- ProductResponse: Formats the data sent back to the client (API response)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    """
    Schema for creating a new product.
    
    Used in: POST /api/products
    
    Validation rules:
    - name: Required string (product name)
    - sku: Required string (unique stock keeping unit code)
    - price: Required float, must be greater than 0
    - quantity_in_stock: Required int, must be >= 0 (can't have negative stock)
    """
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    sku: str = Field(..., min_length=1, max_length=50, description="Unique SKU code")
    price: float = Field(..., gt=0, description="Product price (must be > 0)")
    quantity_in_stock: int = Field(0, ge=0, description="Current stock quantity (must be >= 0)")


class ProductUpdate(BaseModel):
    """
    Schema for updating an existing product.
    
    Used in: PUT /api/products/{id}
    
    All fields are optional - only provide the fields you want to change.
    This is called a "partial update" pattern.
    
    Example: To update only the price, send: {"price": 29.99}
    """
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="Product name")
    sku: Optional[str] = Field(None, min_length=1, max_length=50, description="Unique SKU code")
    price: Optional[float] = Field(None, gt=0, description="Product price (must be > 0)")
    quantity_in_stock: Optional[int] = Field(None, ge=0, description="Stock quantity (must be >= 0)")


class ProductResponse(BaseModel):
    """
    Schema for product data returned in API responses.
    
    Used in: All product endpoints that return product data
    
    model_config with from_attributes=True tells Pydantic to read data
    from SQLAlchemy model attributes (e.g., product.name) instead of
    expecting a dictionary. This is required for ORM model → Pydantic conversion.
    """
    id: int
    name: str
    sku: str
    price: float
    quantity_in_stock: int
    created_at: datetime

    # This config allows Pydantic to read data from SQLAlchemy ORM objects
    # Without this, Pydantic wouldn't know how to convert a Product model instance
    model_config = ConfigDict(from_attributes=True)
