"""
Product Routes (API Endpoints)
==============================
This module defines all the HTTP endpoints for product operations.

Route Layer Responsibilities:
- Define HTTP methods and URL paths
- Handle request/response serialization via Pydantic schemas
- Catch service layer exceptions and return appropriate HTTP error responses
- Keep business logic OUT of routes (delegate to service layer)

Error Handling Pattern:
- Each route wraps service calls in try/except blocks
- Custom exceptions (NotFoundError, DuplicateSKUError) are caught
  and converted to HTTPException with the right status code
- Unexpected errors return 500 Internal Server Error

HTTP Status Codes Used:
- 200: Success (GET, PUT, DELETE)
- 201: Created (POST)
- 404: Not Found
- 409: Conflict (duplicate SKU)
- 422: Validation Error (automatic from Pydantic)
- 500: Internal Server Error
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services import product_service
from app.utils.exceptions import NotFoundError, DuplicateSKUError

# Create a router with a URL prefix and tag
# - prefix: All routes in this file start with "/api/products"
# - tags: Groups these endpoints together in the Swagger docs
router = APIRouter(prefix="/api/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product.
    
    Request Body (ProductCreate):
    - name: Product name (required)
    - sku: Unique SKU code (required)
    - price: Price > 0 (required)
    - quantity_in_stock: Stock count >= 0 (optional, defaults to 0)
    
    Returns: Created product with ID and timestamp
    
    Errors:
    - 409: SKU already exists
    - 422: Validation error (invalid price, missing fields, etc.)
    """
    try:
        return product_service.create_product(db, product_data)
    except DuplicateSKUError as e:
        # 409 Conflict - SKU already exists in the database
        raise HTTPException(status_code=409, detail=e.detail)
    except Exception as e:
        # 500 Internal Server Error - catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/", response_model=List[ProductResponse])
def get_all_products(
    search: Optional[str] = Query(None, description="Search by product name or SKU"),
    low_stock: bool = Query(False, description="Filter products with stock < 10"),
    db: Session = Depends(get_db)
):
    """
    Get all products with optional filtering.
    
    Query Parameters:
    - search: Filter by name or SKU (partial, case-insensitive match)
    - low_stock: If true, only show products with quantity_in_stock < 10
    
    Returns: List of products matching the filters
    
    Examples:
    - GET /api/products → All products
    - GET /api/products?search=mouse → Products containing "mouse"
    - GET /api/products?low_stock=true → Low stock products
    """
    try:
        return product_service.get_all_products(db, search=search, low_stock=low_stock)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get a single product by ID.
    
    Path Parameters:
    - product_id: The ID of the product to retrieve
    
    Returns: Product details
    
    Errors:
    - 404: Product not found
    """
    try:
        return product_service.get_product_by_id(db, product_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing product.
    
    Path Parameters:
    - product_id: The ID of the product to update
    
    Request Body (ProductUpdate - all fields optional):
    - name: New product name
    - sku: New SKU code
    - price: New price
    - quantity_in_stock: New stock count
    
    Returns: Updated product
    
    Errors:
    - 404: Product not found
    - 409: New SKU conflicts with another product
    """
    try:
        return product_service.update_product(db, product_id, product_data)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except DuplicateSKUError as e:
        raise HTTPException(status_code=409, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product by ID.
    
    Path Parameters:
    - product_id: The ID of the product to delete
    
    Returns: Success message
    
    Errors:
    - 404: Product not found
    """
    try:
        return product_service.delete_product(db, product_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
