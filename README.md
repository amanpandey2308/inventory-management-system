# 📦 Inventory & Order Management System

A **full-stack, production-ready** Inventory and Order Management System built with **FastAPI** (Python) and **React** (Vite + Tailwind CSS). Designed with clean architecture, beginner-friendly code, and detailed comments — perfect for **interviews** and **portfolio projects**.

![Tech Stack](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Local Setup (Without Docker)](#-local-setup-without-docker)
- [Docker Setup](#-docker-setup)
- [API Endpoints](#-api-endpoints)
- [Business Logic](#-business-logic)
- [Deployment](#-deployment)
- [Seed Data](#-seed-data)
- [Environment Variables](#-environment-variables)

---

## ✨ Features

### Core Features
- ✅ **Product Management** — Create, read, update, delete products
- ✅ **Customer Management** — Create, read, delete customers
- ✅ **Order Management** — Create orders with multiple items, view details
- ✅ **Dashboard** — Real-time stats with low stock alerts

### Business Rules
- ✅ Unique SKU enforcement (no duplicate product codes)
- ✅ Unique customer email enforcement
- ✅ Non-negative stock validation
- ✅ Insufficient stock prevention on orders
- ✅ Automatic stock reduction when orders are placed
- ✅ Automatic total amount calculation

### Technical Features
- ✅ RESTful API with proper HTTP status codes
- ✅ Request validation using Pydantic
- ✅ Clean error responses with meaningful messages
- ✅ Responsive UI with Tailwind CSS
- ✅ Toast notifications for user feedback
- ✅ Loading states throughout the app
- ✅ Search & filter products
- ✅ Docker containerization
- ✅ Health check endpoint

---

## 🛠 Tech Stack

| Layer             | Technology                          |
|-------------------|-------------------------------------|
| **Frontend**      | React 18, Vite, Tailwind CSS        |
| **Backend**       | Python 3.11, FastAPI, SQLAlchemy    |
| **Database**      | PostgreSQL 15                       |
| **HTTP Client**   | Axios                               |
| **Routing**       | React Router DOM v6                 |
| **Validation**    | Pydantic v2                         |
| **Containerization** | Docker, Docker Compose           |

---

## 📁 Project Structure

```
inventory-management-system/
│
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # App entry point, CORS, routers
│   │   ├── database/
│   │   │   ├── connection.py   # SQLAlchemy engine & session
│   │   │   └── seed.py         # Sample data generator
│   │   ├── models/             # SQLAlchemy ORM models
│   │   │   ├── product.py
│   │   │   ├── customer.py
│   │   │   ├── order.py
│   │   │   └── order_item.py
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   │   ├── product.py
│   │   │   ├── customer.py
│   │   │   └── order.py
│   │   ├── routes/             # API endpoint definitions
│   │   │   ├── product.py
│   │   │   ├── customer.py
│   │   │   ├── order.py
│   │   │   └── dashboard.py
│   │   ├── services/           # Business logic layer
│   │   │   ├── product_service.py
│   │   │   ├── customer_service.py
│   │   │   └── order_service.py
│   │   └── utils/
│   │       └── exceptions.py   # Custom exception classes
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── api/
│   │   │   └── api.js          # Axios API functions
│   │   ├── components/         # Reusable UI components
│   │   │   ├── Layout.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── StatsCard.jsx
│   │   │   ├── Modal.jsx
│   │   │   ├── Toast.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   └── ConfirmDialog.jsx
│   │   ├── pages/              # Page components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Products.jsx
│   │   │   ├── Customers.jsx
│   │   │   └── Orders.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── .env.example
│
├── docker-compose.yml          # Container orchestration
├── .env.example                # Environment variable template
└── README.md                   # This file
```

---

## 🚀 Local Setup (Without Docker)

### Prerequisites
- **Python 3.11+** — [Download](https://www.python.org/downloads/)
- **Node.js 18+** — [Download](https://nodejs.org/)
- **PostgreSQL 15+** — [Download](https://www.postgresql.org/download/)

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd inventory-management-system
```

### Step 2: Setup PostgreSQL Database
```sql
-- Open psql or pgAdmin and run:
CREATE DATABASE inventory_db;
```

### Step 3: Setup Backend
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Edit .env and set your DATABASE_URL:
# DATABASE_URL=postgresql://postgres:your_password@localhost:5432/inventory_db

# Run the backend
uvicorn app.main:app --reload --port 8000
```
The backend will be running at **http://localhost:8000**
API docs available at **http://localhost:8000/docs** (Swagger UI)

### Step 4: Seed Sample Data (Optional)
```bash
# With backend virtual environment activated:
cd backend
python -m app.database.seed
```

### Step 5: Setup Frontend
```bash
cd frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env
# VITE_API_URL=http://localhost:8000

# Run the frontend
npm run dev
```
The frontend will be running at **http://localhost:3000**

---

## 🐳 Docker Setup

### Prerequisites
- **Docker** — [Download](https://www.docker.com/products/docker-desktop)
- **Docker Compose** — (Included with Docker Desktop)

### Start Everything
```bash
# Copy environment file
copy .env.example .env

# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

### Access the Application
| Service    | URL                         |
|------------|-----------------------------|
| Frontend   | http://localhost:3000        |
| Backend    | http://localhost:8000        |
| API Docs   | http://localhost:8000/docs   |
| PostgreSQL | localhost:5432               |

### Stop Everything
```bash
docker-compose down        # Stop containers
docker-compose down -v     # Stop + delete database data
```

---

## 📡 API Endpoints

### Health Check
| Method | Endpoint   | Description    |
|--------|-----------|----------------|
| GET    | `/health` | Health check   |

### Products (`/api/products`)
| Method | Endpoint             | Description         | Status Codes       |
|--------|---------------------|---------------------|-------------------|
| POST   | `/api/products`      | Create a product    | 201, 409, 422     |
| GET    | `/api/products`      | List all products   | 200               |
| GET    | `/api/products/{id}` | Get a product       | 200, 404          |
| PUT    | `/api/products/{id}` | Update a product    | 200, 404, 409     |
| DELETE | `/api/products/{id}` | Delete a product    | 200, 404          |

**Query Parameters for GET /api/products:**
- `search` (string) — Filter by name or SKU
- `low_stock` (boolean) — Show only products with stock < 10

### Customers (`/api/customers`)
| Method | Endpoint               | Description          | Status Codes    |
|--------|------------------------|----------------------|-----------------|
| POST   | `/api/customers`       | Create a customer    | 201, 409, 422   |
| GET    | `/api/customers`       | List all customers   | 200             |
| GET    | `/api/customers/{id}`  | Get a customer       | 200, 404        |
| DELETE | `/api/customers/{id}`  | Delete a customer    | 200, 404        |

### Orders (`/api/orders`)
| Method | Endpoint            | Description       | Status Codes         |
|--------|--------------------|--------------------|----------------------|
| POST   | `/api/orders`      | Create an order    | 201, 400, 404, 422   |
| GET    | `/api/orders`      | List all orders    | 200                  |
| GET    | `/api/orders/{id}` | Get order details  | 200, 404             |
| DELETE | `/api/orders/{id}` | Delete an order    | 200, 404             |

### Dashboard (`/api/dashboard`)
| Method | Endpoint          | Description         |
|--------|-------------------|---------------------|
| GET    | `/api/dashboard`  | Get dashboard stats |

**Dashboard Response:**
```json
{
  "total_products": 10,
  "total_customers": 5,
  "total_orders": 3,
  "low_stock_count": 2,
  "low_stock_products": [
    { "id": 1, "name": "Widget A", "sku": "WDG-001", "quantity_in_stock": 3 }
  ]
}
```

---

## 🧠 Business Logic

### 1. Unique SKU Enforcement
- When creating or updating a product, the system checks if the SKU already exists
- Returns **409 Conflict** with message: `"Product with SKU 'XXX' already exists"`

### 2. Unique Email Enforcement
- When creating a customer, the system checks if the email is already registered
- Returns **409 Conflict** with message: `"Customer with email 'xxx@example.com' already exists"`

### 3. Non-Negative Stock
- Product `quantity_in_stock` must be >= 0
- Validated by Pydantic schema (frontend validation too)
- Returns **422 Unprocessable Entity** if negative

### 4. Order Creation — Stock Check
When an order is created:
1. Verify the **customer exists** (404 if not)
2. For each item, verify the **product exists** (404 if not)
3. Check that **stock >= requested quantity** for each product (400 if insufficient)
4. **Calculate total amount** = sum of (product.price × quantity) for all items
5. **Create the order** and order items in the database
6. **Reduce stock** for each product automatically

### 5. Error Response Format
All errors follow a consistent format:
```json
{
  "detail": "Human-readable error message"
}
```

---

## 🚢 Deployment

### Deploy Frontend to Vercel

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com) and sign in with GitHub
3. Click **"New Project"** → Import your repository
4. Set the **Root Directory** to `frontend`
5. Vercel will auto-detect Vite — no config needed
6. Add environment variable:
   - `VITE_API_URL` = `https://your-backend-url.onrender.com`
7. Click **Deploy**

### Deploy Backend to Render

1. Go to [render.com](https://render.com) and sign in with GitHub
2. Create a **New PostgreSQL** database:
   - Copy the **Internal Database URL**
3. Create a **New Web Service**:
   - Connect your GitHub repo
   - Set **Root Directory** to `backend`
   - Set **Build Command**: `pip install -r requirements.txt`
   - Set **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add environment variable:
     - `DATABASE_URL` = the PostgreSQL URL from step 2
4. Click **Deploy**

### Post-Deployment
- Update your Vercel frontend's `VITE_API_URL` to point to the Render backend URL
- Update CORS in `backend/app/main.py` to allow your Vercel domain

---

## 🌱 Seed Data

A seed script is included to populate the database with sample data for testing:

```bash
# If running locally:
cd backend
python -m app.database.seed

# If running with Docker:
docker exec -it ims_backend python -m app.database.seed
```

This creates:
- 10 sample products (electronics, office supplies)
- 5 sample customers
- 3 sample orders with items

---

## 🔐 Environment Variables

### Backend (`backend/.env`)
| Variable       | Description                    | Example                                                      |
|---------------|--------------------------------|--------------------------------------------------------------|
| `DATABASE_URL` | PostgreSQL connection string   | `postgresql://postgres:postgres@localhost:5432/inventory_db`  |
| `PORT`         | Server port                    | `8000`                                                       |

### Frontend (`frontend/.env`)
| Variable        | Description          | Example                    |
|----------------|----------------------|----------------------------|
| `VITE_API_URL`  | Backend API base URL | `http://localhost:8000`    |

> ⚠️ **Never commit `.env` files to Git!** Use `.env.example` as a template.

---

## 🏗 Architecture Overview (For Interviews)

```
┌──────────────┐     HTTP      ┌──────────────┐     SQL       ┌──────────────┐
│   React UI   │ ──────────►   │   FastAPI     │ ──────────►   │  PostgreSQL  │
│   (Vite)     │   Axios       │   Backend     │  SQLAlchemy   │   Database   │
│  Port 3000   │ ◄──────────   │  Port 8000    │ ◄──────────   │  Port 5432   │
└──────────────┘    JSON       └──────────────┘    ORM         └──────────────┘
```

### Backend Layers (Clean Architecture)
```
Routes (API endpoints)
  ↓ calls
Services (Business logic)
  ↓ uses
Models (Database tables via SQLAlchemy)
  ↓ maps to
PostgreSQL (Actual data storage)
```

- **Routes** — Define HTTP endpoints, handle request/response
- **Schemas** — Validate incoming data with Pydantic
- **Services** — Contain all business logic (stock checks, calculations)
- **Models** — Define database table structure with SQLAlchemy ORM
- **Database** — Connection setup and session management

This separation makes the code **testable**, **maintainable**, and **easy to explain**.

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
