"""
Models Package
==============
This file imports all SQLAlchemy models so they can be easily accessed
from other parts of the application.

Why import models here?
- It ensures all models are registered with SQLAlchemy's Base.metadata
- It allows convenient imports like: from app.models import Product, Customer
- It's required for create_tables() to know about all the models
"""

from app.models.product import Product
from app.models.customer import Customer
from app.models.order import Order
from app.models.order_item import OrderItem

# This list makes it explicit which models are available when importing from this package
__all__ = ["Product", "Customer", "Order", "OrderItem"]
