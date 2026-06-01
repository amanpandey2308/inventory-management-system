# ===================================
# Dockerfile for Inventory Management Backend
# ===================================
# This Dockerfile packages the FastAPI backend into a Docker container.
#
# How to build and run:
#   docker build -t inventory-backend .
#   docker run -p 8000:8000 --env-file .env inventory-backend
#
# The multi-step approach (COPY requirements first, then code) leverages
# Docker's layer caching: dependencies are only re-installed when
# requirements.txt changes, not when code changes.

# Use Python 3.11 slim image (smaller than full Python image)
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (for Docker layer caching)
# This layer is cached and only re-built when requirements.txt changes
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir reduces image size by not caching pip downloads
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000 (documentation - doesn't actually publish the port)
EXPOSE 8000

# Start the FastAPI server using uvicorn
# --host 0.0.0.0 makes it accessible from outside the container
# --port 8000 matches the EXPOSE directive
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
