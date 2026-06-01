"""
Product Service Layer
=====================
This module contains all the business logic for product operations.

Why a service layer?
- Separates business logic from route handlers (clean architecture)
- Makes the code more testable (can test business logic independently)
- Routes stay thin and focused on HTTP concerns (request/response)
- Services focus on data operations and business rules

Pattern:
1. Route receives HTTP request and validates input (using Pydantic schemas)
2. Route calls the appropriate service function
3. Service performs database operations and applies business rules
4. Service returns data or raises custom exceptions
5. Route catches exceptions and returns appropriate HTTP responses
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.exceptions import NotFoundError, DuplicateSKUError


def get_all_products(db: Session, search: str = None, low_stock: bool = False):
    """
    Retrieve all products with optional filtering.
    
    Args:
        db: Database session (injected by FastAPI)
        search: Optional search string - filters products by name OR sku
                Uses SQL ILIKE for case-insensitive partial matching
        low_stock: If True, only returns products with quantity_in_stock < 10
    
    Returns:
        List of Product objects matching the filters
    
    Example:
        get_all_products(db, search="mouse")  → Products with "mouse" in name or SKU
        get_all_products(db, low_stock=True)  → Products with stock < 10
    """
    # Start building the query
    query = db.query(Product)

    # Apply search filter if provided
    # ILIKE is case-insensitive LIKE (PostgreSQL specific)
    # The % wildcards allow partial matching (contains search)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Product.name.ilike(search_pattern),
                Product.sku.ilike(search_pattern)
            )
        )

    # Filter for low stock products (less than 10 units)
    if low_stock:
        query = query.filter(Product.quantity_in_stock < 10)

    # Order by newest first and return all results
    return query.order_by(Product.created_at.desc()).all()


def get_product_by_id(db: Session, product_id: int):
    """
    Retrieve a single product by its ID.
    
    Args:
        db: Database session
        product_id: The ID of the product to find
    
    Returns:
        Product object if found
    
    Raises:
        NotFoundError: If no product exists with the given ID
    """
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise NotFoundError("Product", product_id)

    return product


def create_product(db: Session, product_data: ProductCreate):
    """
    Create a new product in the database.
    
    Business Rules:
    - SKU must be unique across all products
    
    Args:
        db: Database session
        product_data: Validated product data from the request
    
    Returns:
        The newly created Product object
    
    Raises:
        DuplicateSKUError: If a product with the same SKU already exists
    """
    # Check if a product with the same SKU already exists
    existing_product = db.query(Product).filter(Product.sku == product_data.sku).first()
    if existing_product:
        raise DuplicateSKUError(product_data.sku)

    # Create new product instance from the validated data
    # **product_data.model_dump() unpacks the Pydantic model into keyword arguments
    # e.g., Product(name="Mouse", sku="M-001", price=29.99, quantity_in_stock=50)
    new_product = Product(**product_data.model_dump())

    # Add to session, commit to database, and refresh to get generated fields (id, created_at)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    """
    Update an existing product.
    
    Business Rules:
    - Product must exist
    - If SKU is being changed, the new SKU must not already be in use
    - Only provided fields are updated (partial update)
    
    Args:
        db: Database session
        product_id: ID of the product to update
        product_data: Validated update data (only fields to change)
    
    Returns:
        The updated Product object
    
    Raises:
        NotFoundError: If the product doesn't exist
        DuplicateSKUError: If the new SKU conflicts with another product
    """
    # First, find the product
    product = get_product_by_id(db, product_id)

    # Get only the fields that were actually provided (exclude unset/None values)
    # exclude_unset=True means only fields explicitly set in the request are included
    update_data = product_data.model_dump(exclude_unset=True)

    # If SKU is being changed, check for duplicates
    if "sku" in update_data and update_data["sku"] != product.sku:
        existing = db.query(Product).filter(Product.sku == update_data["sku"]).first()
        if existing:
            raise DuplicateSKUError(update_data["sku"])

    # Apply each update to the product
    # setattr(product, "name", "New Name") is equivalent to product.name = "New Name"
    for field, value in update_data.items():
        setattr(product, field, value)

    # Commit changes and refresh from database
    db.commit()
    db.refresh(product)

    return product


def delete_product(db: Session, product_id: int):
    """
    Delete a product from the database.
    
    Args:
        db: Database session
        product_id: ID of the product to delete
    
    Returns:
        dict with success message
    
    Raises:
        NotFoundError: If the product doesn't exist
    """
    product = get_product_by_id(db, product_id)

    db.delete(product)
    db.commit()

    return {"detail": f"Product '{product.name}' (ID: {product_id}) deleted successfully"}
