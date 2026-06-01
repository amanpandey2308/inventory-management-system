// ============================================
// API Layer — All backend communication goes here
// We use Axios to make HTTP requests to our FastAPI backend
// The base URL comes from environment variable VITE_API_URL
// ============================================

import axios from "axios";

// Create an Axios instance with the backend URL
// In development: http://localhost:8000
// In production: your deployed backend URL
const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

// ---- Product APIs ----
export const getProducts = (search = "", lowStock = false) =>
  API.get("/api/products", { params: { search, low_stock: lowStock } });
export const getProduct = (id) => API.get(`/api/products/${id}`);
export const createProduct = (data) => API.post("/api/products", data);
export const updateProduct = (id, data) => API.put(`/api/products/${id}`, data);
export const deleteProduct = (id) => API.delete(`/api/products/${id}`);

// ---- Customer APIs ----
export const getCustomers = () => API.get("/api/customers");
export const getCustomer = (id) => API.get(`/api/customers/${id}`);
export const createCustomer = (data) => API.post("/api/customers", data);
export const deleteCustomer = (id) => API.delete(`/api/customers/${id}`);

// ---- Order APIs ----
export const getOrders = () => API.get("/api/orders");
export const getOrder = (id) => API.get(`/api/orders/${id}`);
export const createOrder = (data) => API.post("/api/orders", data);
export const deleteOrder = (id) => API.delete(`/api/orders/${id}`);

// ---- Dashboard API ----
export const getDashboard = () => API.get("/api/dashboard");

export default API;
