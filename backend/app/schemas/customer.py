"""
Customer Schemas (Pydantic Models)
==================================
Pydantic schemas for customer request validation and response formatting.

Key Concept - EmailStr:
- EmailStr is a special Pydantic type that validates email format
- It checks that the email has a valid structure (e.g., "user@domain.com")
- Invalid emails like "not-an-email" will be rejected with a clear error message
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerCreate(BaseModel):
    """
    Schema for creating a new customer.
    
    Used in: POST /api/customers
    
    Validation rules:
    - full_name: Required string
    - email: Required valid email address (EmailStr validates format)
    - phone: Optional string for phone number
    """
    full_name: str = Field(..., min_length=1, max_length=200, description="Customer's full name")
    email: EmailStr = Field(..., description="Customer's email address (must be valid format)")
    phone: Optional[str] = Field(None, max_length=20, description="Customer's phone number (optional)")


class CustomerResponse(BaseModel):
    """
    Schema for customer data returned in API responses.
    
    Used in: All customer endpoints that return customer data
    
    Includes all fields plus the auto-generated id and created_at.
    """
    id: int
    full_name: str
    email: str  # Using str here instead of EmailStr for response (already validated on input)
    phone: Optional[str] = None
    created_at: datetime

    # Allows Pydantic to read from SQLAlchemy ORM model attributes
    model_config = ConfigDict(from_attributes=True)
