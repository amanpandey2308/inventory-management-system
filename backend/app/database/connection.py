"""
Database Connection Module
==========================
This module handles the database connection setup using SQLAlchemy.
It creates the engine, session factory, and provides a dependency
function (get_db) that FastAPI uses to inject database sessions into routes.

Key Concepts:
- Engine: The core interface to the database (manages connection pool)
- SessionLocal: A factory that creates new database session objects
- Base: The declarative base class that all our models inherit from
- get_db(): A generator function used as a FastAPI dependency to provide
  a database session per request and ensure it's closed after use
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variable, with a default fallback
# Format: postgresql://username:password@host:port/database_name
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/inventory_db"
)

# Create the SQLAlchemy engine
# - The engine manages a pool of database connections
# - echo=False means SQL queries won't be printed to console (set True for debugging)
engine = create_engine(DATABASE_URL, echo=False)

# Create a configured session factory
# - autocommit=False: We manually control when to commit transactions
# - autoflush=False: We manually control when to flush changes to the DB
# - bind=engine: Links this session factory to our database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all our SQLAlchemy models
# Every model (Product, Customer, Order, etc.) will inherit from this
Base = declarative_base()


def get_db():
    """
    Dependency function that provides a database session to each request.
    
    How it works:
    1. Creates a new database session when a request comes in
    2. Yields the session so the route handler can use it
    3. Automatically closes the session when the request is done
    
    Usage in routes:
        @router.get("/")
        def get_items(db: Session = Depends(get_db)):
            ...
    
    The 'yield' keyword makes this a generator - FastAPI knows to run
    the code after yield (db.close()) as cleanup after the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        # Always close the session to release the connection back to the pool
        db.close()


def create_tables():
    """
    Creates all database tables based on the SQLAlchemy models.
    
    This function inspects all classes that inherit from Base and creates
    their corresponding tables in the database if they don't already exist.
    
    Note: We import all models here to ensure they are registered with Base
    before we call create_all(). Without these imports, SQLAlchemy wouldn't
    know about our models and no tables would be created.
    """
    # Import all models so they are registered with Base.metadata
    # These imports are required here even if not used directly
    from app.models import product, customer, order, order_item  # noqa: F401

    # Create all tables that don't exist yet (won't drop/recreate existing ones)
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
