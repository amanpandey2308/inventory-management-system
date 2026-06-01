"""
Order Model
============
SQLAlchemy model for the 'orders' table.

This model represents customer orders. Each order belongs to a customer
and contains one or more order items (the products they purchased).

Key Concepts:
- ForeignKey: Creates a link to another table (customers table in this case)
- cascade="all, delete-orphan": When an order is deleted, all its order items
  are automatically deleted too (prevents orphan records)
- Relationships define how models are connected and enable navigation
  between related records (e.g., order.customer, order.items)
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base


class Order(Base):
    """
    Order model - represents a customer's order.
    
    Attributes:
        id: Auto-incrementing primary key
        customer_id: Foreign key linking to the customer who placed the order
        total_amount: Total cost of all items in the order
        created_at: When the order was placed
        customer: The Customer object (loaded via relationship)
        items: List of OrderItem objects in this order (loaded via relationship)
    """
    __tablename__ = "orders"

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # Foreign key to customers table - links each order to a customer
    # "customers.id" refers to the 'id' column in the 'customers' table
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    # Total amount for the entire order (sum of all item prices * quantities)
    # Defaults to 0.0 and gets calculated when items are added
    total_amount = Column(Float, nullable=False, default=0.0)

    # When the order was placed
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to Customer - many orders belong to one customer
    # back_populates="orders" links to the 'orders' attribute in Customer model
    customer = relationship("Customer", back_populates="orders")

    # Relationship to OrderItem - one order has many items
    # cascade="all, delete-orphan" means:
    #   - When we delete an order, all its items are automatically deleted
    #   - If an item is removed from order.items, it gets deleted from DB
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        """String representation for debugging."""
        return f"<Order(id={self.id}, customer_id={self.customer_id}, total={self.total_amount})>"
