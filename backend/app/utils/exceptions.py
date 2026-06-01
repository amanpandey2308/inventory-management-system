"""
Custom Exception Classes
========================
These custom exceptions are used in the service layer to represent
specific business logic errors. The route layer catches these exceptions
and converts them into appropriate HTTP error responses.

Why custom exceptions?
- They make the code more readable and self-documenting
- They separate business logic errors from generic Python errors
- They allow routes to return specific HTTP status codes (404, 409, 400)
- They carry meaningful error messages that help API consumers debug issues

Pattern:
1. Service layer raises custom exception (e.g., DuplicateSKUError)
2. Route layer catches it and returns HTTP 409 with error message
"""


class NotFoundError(Exception):
    """
    Raised when a requested resource (product, customer, order) is not found.
    
    Maps to HTTP 404 Not Found.
    
    Example usage:
        raise NotFoundError("Product", product_id)
        → "Product with ID 5 not found"
    """
    def __init__(self, resource_name: str, resource_id: int):
        self.message = f"{resource_name} with ID {resource_id} not found"
        self.detail = self.message
        super().__init__(self.message)


class DuplicateSKUError(Exception):
    """
    Raised when trying to create/update a product with a SKU that already exists.
    
    Maps to HTTP 409 Conflict.
    
    Example usage:
        raise DuplicateSKUError("LAPTOP-001")
        → "Product with SKU 'LAPTOP-001' already exists"
    """
    def __init__(self, sku: str):
        self.message = f"Product with SKU '{sku}' already exists"
        self.detail = self.message
        super().__init__(self.message)


class DuplicateEmailError(Exception):
    """
    Raised when trying to create a customer with an email that already exists.
    
    Maps to HTTP 409 Conflict.
    
    Example usage:
        raise DuplicateEmailError("john@example.com")
        → "Customer with email 'john@example.com' already exists"
    """
    def __init__(self, email: str):
        self.message = f"Customer with email '{email}' already exists"
        self.detail = self.message
        super().__init__(self.message)


class InsufficientStockError(Exception):
    """
    Raised when an order requests more units than are available in stock.
    
    Maps to HTTP 400 Bad Request.
    
    Example usage:
        raise InsufficientStockError("Wireless Mouse", available=5, requested=10)
        → "Insufficient stock for 'Wireless Mouse'. Available: 5, Requested: 10"
    """
    def __init__(self, product_name: str, available: int, requested: int):
        self.message = (
            f"Insufficient stock for '{product_name}'. "
            f"Available: {available}, Requested: {requested}"
        )
        self.detail = self.message
        super().__init__(self.message)
