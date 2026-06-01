"""
OrderItem Model
===============
SQLAlchemy model for the 'order_items' table.

This is a junction/detail table that connects orders to products.
Each row represents one line item in an order (e.g., "2x Wireless Mouse at $29.99").

Key Concepts:
- This table has TWO foreign keys: one to orders and one to products
- The 'price' field stores the price at the time of purchase (snapshot)
  because product prices can change over time
- This is a common pattern in e-commerce: store the price at purchase time
  rather than looking it up from the product table each time
"""

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base


class OrderItem(Base):
    """
    OrderItem model - represents a single product line in an order.
    
    Example: If an order has 2 Mice and 1 Keyboard, there would be
    2 OrderItem rows for that order.
    
    Attributes:
        id: Auto-incrementing primary key
        order_id: Foreign key to the order this item belongs to
        product_id: Foreign key to the product being ordered
        quantity: How many units of the product were ordered
        price: Price per unit at the time of purchase (snapshot price)
        order: The parent Order object (relationship)
        product: The Product object (relationship)
    """
    __tablename__ = "order_items"

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # Foreign key to orders table - which order this item belongs to
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    # Foreign key to products table - which product was ordered
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    # Quantity of the product ordered (e.g., 3 units)
    quantity = Column(Integer, nullable=False)

    # Price per unit at the time of purchase
    # We store this separately because the product price might change later
    # but we want to keep a record of what the customer actually paid
    price = Column(Float, nullable=False)

    # Relationship to Order - each item belongs to one order
    order = relationship("Order", back_populates="items")

    # Relationship to Product - each item references one product
    # No back_populates needed since we don't need product.order_items navigation
    product = relationship("Product")

    def __repr__(self):
        """String representation for debugging."""
        return f"<OrderItem(id={self.id}, product_id={self.product_id}, qty={self.quantity})>"
