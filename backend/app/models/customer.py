"""
Customer Model
==============
SQLAlchemy model for the 'customers' table.

This model represents customers who can place orders in the system.
Each customer has a unique email address and an optional phone number.

Key Concepts:
- Relationships: Customers have a one-to-many relationship with orders
  (one customer can have many orders)
- back_populates: Creates a bidirectional relationship between models
  so you can access customer.orders and order.customer
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database.connection import Base


class Customer(Base):
    """
    Customer model - represents users who place orders.
    
    Attributes:
        id: Auto-incrementing primary key
        full_name: Customer's full name
        email: Unique email address for the customer
        phone: Optional phone number
        created_at: When the customer was registered
        orders: List of orders placed by this customer (relationship)
    """
    __tablename__ = "customers"

    # Primary key - auto-incremented integer ID
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # Customer's full name - required
    full_name = Column(String(200), nullable=False)

    # Email must be unique - used to identify customers and prevent duplicates
    email = Column(String(200), unique=True, nullable=False, index=True)

    # Phone number is optional (nullable=True is the default, but explicit for clarity)
    phone = Column(String(20), nullable=True)

    # Timestamp for when the customer was registered
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship: One customer can have many orders
    # back_populates="customer" links this to the 'customer' attribute in Order model
    # This lets you do: customer.orders to get all orders for a customer
    orders = relationship("Order", back_populates="customer")

    def __repr__(self):
        """String representation for debugging."""
        return f"<Customer(id={self.id}, name='{self.full_name}', email='{self.email}')>"
