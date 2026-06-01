"""
Order Service Layer
===================
Business logic for order operations.

This is the most complex service because creating an order involves:
1. Validating the customer exists
2. Validating all products exist and have sufficient stock
3. Calculating the total amount
4. Creating the order and order items in a single transaction
5. Reducing stock quantities for each product

Key Concepts:
- Eager Loading: Using joinedload() to load related data in a single query
  instead of making separate queries for each relationship (N+1 problem)
- Transaction Safety: All changes (order creation + stock reduction) happen
  in one commit() so if anything fails, nothing is saved (atomicity)
"""

from sqlalchemy.orm import Session, joinedload

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.customer import Customer
from app.schemas.order import OrderCreate
from app.utils.exceptions import NotFoundError, InsufficientStockError


def get_all_orders(db: Session):
    """
    Retrieve all orders with their customer and items eagerly loaded.
    
    Eager Loading Explained:
    Without joinedload, accessing order.customer would trigger a separate
    SQL query for EACH order (N+1 problem). With joinedload, all related
    data is fetched in one query using SQL JOINs.
    
    Args:
        db: Database session
    
    Returns:
        List of Order objects with customer and items pre-loaded
    """
    orders = db.query(Order).options(
        # Load the customer relationship in the same query
        joinedload(Order.customer),
        # Load the items relationship, and for each item, load its product
        joinedload(Order.items).joinedload(OrderItem.product)
    ).order_by(Order.created_at.desc()).all()

    # Enrich each order with computed fields for the response
    return [_enrich_order(order) for order in orders]


def get_order_by_id(db: Session, order_id: int):
    """
    Retrieve a single order by ID with all related data.
    
    Args:
        db: Database session
        order_id: The ID of the order to find
    
    Returns:
        Enriched Order object with customer_name and product_names
    
    Raises:
        NotFoundError: If no order exists with the given ID
    """
    order = db.query(Order).options(
        joinedload(Order.customer),
        joinedload(Order.items).joinedload(OrderItem.product)
    ).filter(Order.id == order_id).first()

    if not order:
        raise NotFoundError("Order", order_id)

    return _enrich_order(order)


def create_order(db: Session, order_data: OrderCreate):
    """
    Create a new order with items.
    
    This is the most important function in the system. Here's the flow:
    
    Step 1: Verify the customer exists
    Step 2: For each item in the order:
            - Verify the product exists
            - Check there's enough stock
            - Calculate the line total (price × quantity)
    Step 3: Create the order with the calculated total
    Step 4: Create order items with the price snapshot
    Step 5: Reduce stock for each product
    Step 6: Commit everything in one transaction
    
    Args:
        db: Database session
        order_data: Validated order data with customer_id and items list
    
    Returns:
        The created order with all related data
    
    Raises:
        NotFoundError: If customer or any product doesn't exist
        InsufficientStockError: If any product doesn't have enough stock
    """
    # Step 1: Verify customer exists
    customer = db.query(Customer).filter(Customer.id == order_data.customer_id).first()
    if not customer:
        raise NotFoundError("Customer", order_data.customer_id)

    # Step 2: Validate all items and calculate total
    total_amount = 0.0
    validated_items = []  # Store validated items with their products

    for item in order_data.items:
        # Check if the product exists
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise NotFoundError("Product", item.product_id)

        # Check if there's enough stock
        if product.quantity_in_stock < item.quantity:
            raise InsufficientStockError(
                product_name=product.name,
                available=product.quantity_in_stock,
                requested=item.quantity
            )

        # Calculate line total and add to order total
        line_total = product.price * item.quantity
        total_amount += line_total

        # Save the validated item info for creating order items later
        validated_items.append({
            "product": product,
            "quantity": item.quantity,
            "price": product.price  # Snapshot the current price
        })

    # Step 3: Create the order
    new_order = Order(
        customer_id=order_data.customer_id,
        total_amount=round(total_amount, 2)  # Round to 2 decimal places
    )
    db.add(new_order)
    db.flush()  # Flush to get the order ID without committing

    # Step 4 & 5: Create order items and reduce stock
    for item_data in validated_items:
        # Create the order item with the snapshot price
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item_data["product"].id,
            quantity=item_data["quantity"],
            price=item_data["price"]
        )
        db.add(order_item)

        # Reduce the product's stock quantity
        item_data["product"].quantity_in_stock -= item_data["quantity"]

    # Step 6: Commit all changes in one transaction
    # If anything fails, all changes are rolled back (atomicity)
    db.commit()
    db.refresh(new_order)

    # Return the order with all related data loaded
    return get_order_by_id(db, new_order.id)


def delete_order(db: Session, order_id: int):
    """
    Delete an order and its items from the database.
    
    Note: The cascade="all, delete-orphan" on the Order model's items
    relationship means order items are automatically deleted when the
    order is deleted.
    
    Note: This implementation does NOT restore stock quantities.
    In a production system, you might want to add stock back when
    an order is cancelled/deleted.
    
    Args:
        db: Database session
        order_id: ID of the order to delete
    
    Returns:
        dict with success message
    
    Raises:
        NotFoundError: If the order doesn't exist
    """
    # We need a simple query here, not the enriched version
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise NotFoundError("Order", order_id)

    db.delete(order)
    db.commit()

    return {"detail": f"Order (ID: {order_id}) deleted successfully"}


def _enrich_order(order: Order):
    """
    Helper function to add computed fields to an order for the response.
    
    This adds:
    - customer_name: The name of the customer (from the relationship)
    - product_name: The name of each product in the order items
    
    We set these as attributes on the SQLAlchemy objects so Pydantic
    can access them when building the response schema.
    
    Args:
        order: The Order object to enrich
    
    Returns:
        The same Order object with additional attributes set
    """
    # Add customer name from the loaded relationship
    if order.customer:
        order.customer_name = order.customer.full_name
    else:
        order.customer_name = None

    # Add product name to each order item
    for item in order.items:
        if item.product:
            item.product_name = item.product.name
        else:
            item.product_name = None

    return order
