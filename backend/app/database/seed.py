"""
Database Seed Script
====================
This script populates the database with sample data for testing and development.

It creates:
- 10 sample products across different categories
- 5 sample customers
- 3 sample orders with multiple items each

How to run:
    python -m app.database.seed

Note: Run this AFTER the database tables have been created
(they are created automatically when the server starts).

The script checks for existing data to avoid duplicates when run multiple times.
"""

import sys
import os

# Add the project root to Python path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database.connection import SessionLocal, create_tables
from app.models.product import Product
from app.models.customer import Customer
from app.models.order import Order
from app.models.order_item import OrderItem


def seed_products(db):
    """Create 10 sample products if the products table is empty."""

    # Check if products already exist
    existing_count = db.query(Product).count()
    if existing_count > 0:
        print(f"⏭️  Skipping products - {existing_count} already exist")
        return

    # Sample products spanning different categories
    products = [
        Product(name="Wireless Mouse", sku="MOUSE-001", price=29.99, quantity_in_stock=50),
        Product(name="Mechanical Keyboard", sku="KB-001", price=89.99, quantity_in_stock=30),
        Product(name="USB-C Hub", sku="HUB-001", price=49.99, quantity_in_stock=25),
        Product(name="27\" Monitor", sku="MON-001", price=349.99, quantity_in_stock=15),
        Product(name="Laptop Stand", sku="STAND-001", price=39.99, quantity_in_stock=40),
        Product(name="Webcam HD 1080p", sku="CAM-001", price=59.99, quantity_in_stock=20),
        Product(name="Noise-Cancelling Headphones", sku="HP-001", price=199.99, quantity_in_stock=8),
        Product(name="Wireless Charger", sku="CHG-001", price=24.99, quantity_in_stock=5),
        Product(name="Desk Lamp LED", sku="LAMP-001", price=34.99, quantity_in_stock=3),
        Product(name="Ethernet Cable 10ft", sku="CABLE-001", price=9.99, quantity_in_stock=100),
    ]

    db.add_all(products)
    db.commit()
    print(f"✅ Created {len(products)} sample products")


def seed_customers(db):
    """Create 5 sample customers if the customers table is empty."""

    existing_count = db.query(Customer).count()
    if existing_count > 0:
        print(f"⏭️  Skipping customers - {existing_count} already exist")
        return

    customers = [
        Customer(full_name="Alice Johnson", email="alice@example.com", phone="+1-555-0101"),
        Customer(full_name="Bob Smith", email="bob@example.com", phone="+1-555-0102"),
        Customer(full_name="Carol Williams", email="carol@example.com", phone="+1-555-0103"),
        Customer(full_name="David Brown", email="david@example.com", phone=None),
        Customer(full_name="Eve Davis", email="eve@example.com", phone="+1-555-0105"),
    ]

    db.add_all(customers)
    db.commit()
    print(f"✅ Created {len(customers)} sample customers")


def seed_orders(db):
    """Create 3 sample orders with items if the orders table is empty."""

    existing_count = db.query(Order).count()
    if existing_count > 0:
        print(f"⏭️  Skipping orders - {existing_count} already exist")
        return

    # Get existing products and customers to reference
    products = db.query(Product).all()
    customers = db.query(Customer).all()

    if len(products) < 3 or len(customers) < 3:
        print("⚠️  Not enough products or customers to create sample orders")
        return

    # --- Order 1: Alice orders a Mouse and Keyboard ---
    order1_items = [
        {"product": products[0], "quantity": 2},  # 2x Wireless Mouse
        {"product": products[1], "quantity": 1},  # 1x Mechanical Keyboard
    ]
    order1_total = sum(item["product"].price * item["quantity"] for item in order1_items)

    order1 = Order(customer_id=customers[0].id, total_amount=round(order1_total, 2))
    db.add(order1)
    db.flush()  # Get the order ID

    for item in order1_items:
        db.add(OrderItem(
            order_id=order1.id,
            product_id=item["product"].id,
            quantity=item["quantity"],
            price=item["product"].price
        ))
        # Reduce stock
        item["product"].quantity_in_stock -= item["quantity"]

    # --- Order 2: Bob orders a Monitor and USB-C Hub ---
    order2_items = [
        {"product": products[3], "quantity": 1},  # 1x Monitor
        {"product": products[2], "quantity": 2},  # 2x USB-C Hub
    ]
    order2_total = sum(item["product"].price * item["quantity"] for item in order2_items)

    order2 = Order(customer_id=customers[1].id, total_amount=round(order2_total, 2))
    db.add(order2)
    db.flush()

    for item in order2_items:
        db.add(OrderItem(
            order_id=order2.id,
            product_id=item["product"].id,
            quantity=item["quantity"],
            price=item["product"].price
        ))
        item["product"].quantity_in_stock -= item["quantity"]

    # --- Order 3: Carol orders Headphones and a Webcam ---
    order3_items = [
        {"product": products[6], "quantity": 1},  # 1x Headphones
        {"product": products[5], "quantity": 1},  # 1x Webcam
        {"product": products[4], "quantity": 1},  # 1x Laptop Stand
    ]
    order3_total = sum(item["product"].price * item["quantity"] for item in order3_items)

    order3 = Order(customer_id=customers[2].id, total_amount=round(order3_total, 2))
    db.add(order3)
    db.flush()

    for item in order3_items:
        db.add(OrderItem(
            order_id=order3.id,
            product_id=item["product"].id,
            quantity=item["quantity"],
            price=item["product"].price
        ))
        item["product"].quantity_in_stock -= item["quantity"]

    # Commit all orders and stock changes
    db.commit()
    print(f"✅ Created 3 sample orders with items")


def run_seed():
    """Main function to run all seed operations."""
    print("🌱 Starting database seed...")
    print("=" * 50)

    # Ensure tables exist before seeding
    create_tables()

    # Create a database session
    db = SessionLocal()

    try:
        seed_products(db)
        seed_customers(db)
        seed_orders(db)

        print("=" * 50)
        print("🎉 Database seeding completed successfully!")
        print("\nSummary:")
        print(f"  Products:  {db.query(Product).count()}")
        print(f"  Customers: {db.query(Customer).count()}")
        print(f"  Orders:    {db.query(Order).count()}")
        print(f"  OrderItems:{db.query(OrderItem).count()}")

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


# Allow running as: python -m app.database.seed
if __name__ == "__main__":
    run_seed()
