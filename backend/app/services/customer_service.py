"""
Customer Service Layer
======================
Business logic for customer operations.

This service handles:
- Listing all customers
- Finding a customer by ID
- Creating new customers with email uniqueness check
- Deleting customers
"""

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate
from app.utils.exceptions import NotFoundError, DuplicateEmailError


def get_all_customers(db: Session):
    """
    Retrieve all customers, ordered by newest first.
    
    Args:
        db: Database session
    
    Returns:
        List of all Customer objects
    """
    return db.query(Customer).order_by(Customer.created_at.desc()).all()


def get_customer_by_id(db: Session, customer_id: int):
    """
    Retrieve a single customer by their ID.
    
    Args:
        db: Database session
        customer_id: The ID of the customer to find
    
    Returns:
        Customer object if found
    
    Raises:
        NotFoundError: If no customer exists with the given ID
    """
    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise NotFoundError("Customer", customer_id)

    return customer


def create_customer(db: Session, customer_data: CustomerCreate):
    """
    Create a new customer in the database.
    
    Business Rules:
    - Email must be unique across all customers
    
    Args:
        db: Database session
        customer_data: Validated customer data from the request
    
    Returns:
        The newly created Customer object
    
    Raises:
        DuplicateEmailError: If a customer with the same email already exists
    """
    # Check if email is already registered
    existing_customer = db.query(Customer).filter(
        Customer.email == customer_data.email
    ).first()

    if existing_customer:
        raise DuplicateEmailError(customer_data.email)

    # Create new customer from validated data
    new_customer = Customer(**customer_data.model_dump())

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


def delete_customer(db: Session, customer_id: int):
    """
    Delete a customer from the database.
    
    Note: This will fail if the customer has existing orders due to
    the foreign key constraint. In a production app, you might want
    to handle this case explicitly.
    
    Args:
        db: Database session
        customer_id: ID of the customer to delete
    
    Returns:
        dict with success message
    
    Raises:
        NotFoundError: If the customer doesn't exist
    """
    customer = get_customer_by_id(db, customer_id)

    db.delete(customer)
    db.commit()

    return {"detail": f"Customer '{customer.full_name}' (ID: {customer_id}) deleted successfully"}
