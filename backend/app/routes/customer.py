"""
Customer Routes (API Endpoints)
===============================
HTTP endpoints for customer operations.

Endpoints:
- POST /api/customers      → Create a new customer
- GET /api/customers        → List all customers
- GET /api/customers/{id}   → Get a customer by ID
- DELETE /api/customers/{id} → Delete a customer
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services import customer_service
from app.utils.exceptions import NotFoundError, DuplicateEmailError

# Create router with prefix and tag for Swagger grouping
router = APIRouter(prefix="/api/customers", tags=["Customers"])


@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(customer_data: CustomerCreate, db: Session = Depends(get_db)):
    """
    Create a new customer.
    
    Request Body:
    - full_name: Customer's name (required)
    - email: Valid email address (required, must be unique)
    - phone: Phone number (optional)
    
    Returns: Created customer with ID and timestamp
    
    Errors:
    - 409: Email already registered
    - 422: Validation error (invalid email format, etc.)
    """
    try:
        return customer_service.create_customer(db, customer_data)
    except DuplicateEmailError as e:
        # 409 Conflict - email already exists
        raise HTTPException(status_code=409, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/", response_model=List[CustomerResponse])
def get_all_customers(db: Session = Depends(get_db)):
    """
    Get all customers.
    
    Returns: List of all customers ordered by newest first
    """
    try:
        return customer_service.get_all_customers(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Get a single customer by ID.
    
    Path Parameters:
    - customer_id: The ID of the customer to retrieve
    
    Returns: Customer details
    
    Errors:
    - 404: Customer not found
    """
    try:
        return customer_service.get_customer_by_id(db, customer_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Delete a customer by ID.
    
    Path Parameters:
    - customer_id: The ID of the customer to delete
    
    Returns: Success message
    
    Errors:
    - 404: Customer not found
    
    Note: Will fail if customer has existing orders (foreign key constraint)
    """
    try:
        return customer_service.delete_customer(db, customer_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
