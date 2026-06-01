"""
Main Application Entry Point
=============================
This is the heart of the FastAPI application. It:
1. Creates the FastAPI app instance with metadata
2. Configures CORS middleware (Cross-Origin Resource Sharing)
3. Registers all route modules (products, customers, orders, dashboard)
4. Defines the health check endpoint
5. Creates database tables on startup

How to run:
    uvicorn app.main:app --reload --port 8000

The --reload flag enables hot-reloading during development
(server restarts automatically when you save code changes).

API Documentation:
After starting the server, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import create_tables
from app.routes import product, customer, order, dashboard

# --- Create FastAPI Application ---
# title: Shown in the Swagger docs header
# description: Shown below the title in Swagger docs
# version: API version number
app = FastAPI(
    title="Inventory & Order Management System",
    description=(
        "A comprehensive REST API for managing products, customers, and orders. "
        "Built with FastAPI, SQLAlchemy, and PostgreSQL. "
        "Features include inventory tracking, order processing with stock management, "
        "and a dashboard for system overview."
    ),
    version="1.0.0"
)

# --- CORS Middleware Configuration ---
# CORS (Cross-Origin Resource Sharing) allows the frontend (running on a
# different port/domain) to make requests to this API.
#
# In development: We allow ALL origins (*) for easy testing
# In production: Replace ["*"] with your actual frontend domain
#   e.g., ["https://your-frontend.com", "https://admin.your-frontend.com"]
#
# ⚠️  WARNING: allow_origins=["*"] is NOT safe for production!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict this in production!
    allow_credentials=True,
    allow_methods=["*"],     # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],     # Allow all headers
)

# --- Register Route Modules ---
# Each router handles a specific resource (products, customers, orders, dashboard)
# The prefix and tags are defined in each router file
app.include_router(product.router)
app.include_router(customer.router)
app.include_router(order.router)
app.include_router(dashboard.router)


# --- Startup Event ---
# This function runs automatically when the server starts
# It creates all database tables if they don't exist
@app.on_event("startup")
def on_startup():
    """
    Runs when the FastAPI server starts up.
    Creates all database tables based on SQLAlchemy models.
    """
    print("🚀 Starting Inventory & Order Management System...")
    create_tables()
    print("✅ Application started successfully!")


# --- Health Check Endpoint ---
@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Used by:
    - Load balancers to check if the service is alive
    - Monitoring systems to track uptime
    - Docker health checks
    - Simple manual verification
    
    Returns: {"status": "healthy"}
    """
    return {"status": "healthy"}


# --- Root Endpoint ---
@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint - provides basic API information and links.
    
    Returns: Welcome message with useful links
    """
    return {
        "message": "Welcome to the Inventory & Order Management System API",
        "docs": "/docs",
        "health": "/health",
        "version": "1.0.0"
    }
