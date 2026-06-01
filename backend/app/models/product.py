"""
Product Model
=============
SQLAlchemy model for the 'products' table.

This model represents products in our inventory system.
Each product has a unique SKU (Stock Keeping Unit) for identification,
a price, and a quantity tracking how many units are in stock.

Key Concepts:
- __tablename__: Defines the actual table name in the database
- Column types define the data type for each field in the database
- 'nullable=False' means the field is required (NOT NULL in SQL)
- 'unique=True' adds a UNIQUE constraint preventing duplicate values
- 'default' sets a default value when one isn't provided
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database.connection import Base


class Product(Base):
    """
    Product model - represents items in inventory.
    
    Attributes:
        id: Auto-incrementing primary key (unique identifier)
        name: Product name (e.g., "Wireless Mouse")
        sku: Stock Keeping Unit - unique code for each product (e.g., "WM-001")
        price: Product price in currency units
        quantity_in_stock: How many units are currently available
        created_at: Timestamp when the product was added to the system
    """
    __tablename__ = "products"

    # Primary key - auto-incremented integer ID
    # index=True creates a database index for faster lookups
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # Product name - required, max 200 characters
    name = Column(String(200), nullable=False)

    # SKU (Stock Keeping Unit) - unique identifier for the product
    # Must be unique across all products (e.g., "LAPTOP-001", "MOUSE-002")
    sku = Column(String(50), unique=True, nullable=False, index=True)

    # Product price - must be provided (no default)
    price = Column(Float, nullable=False)

    # Current stock quantity - defaults to 0 if not specified
    quantity_in_stock = Column(Integer, nullable=False, default=0)

    # Timestamp for when the product was created
    # datetime.utcnow is called when a new row is inserted (not when the model is defined)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        """String representation for debugging - shows product name and SKU."""
        return f"<Product(id={self.id}, name='{self.name}', sku='{self.sku}')>"
