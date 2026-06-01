// ============================================
// Products Page — CRUD for product inventory
// Features: search, low-stock filter, add/edit/delete
// ============================================

import { useState, useEffect } from "react";
import {
  getProducts,
  createProduct,
  updateProduct,
  deleteProduct,
} from "../api/api";
import Modal from "../components/Modal";
import ConfirmDialog from "../components/ConfirmDialog";
import LoadingSpinner from "../components/LoadingSpinner";
import { useToast } from "../components/Toast";

// Default empty form state
const emptyForm = { name: "", sku: "", price: "", quantity_in_stock: "" };

export default function Products() {
  // State
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [lowStock, setLowStock] = useState(false);

  // Modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState(null); // null = creating, object = editing
  const [form, setForm] = useState(emptyForm);
  const [formErrors, setFormErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  // Delete confirmation state
  const [deleteTarget, setDeleteTarget] = useState(null);

  const { addToast } = useToast();

  // Fetch products whenever search or lowStock changes
  useEffect(() => {
    fetchProducts();
  }, [search, lowStock]);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const res = await getProducts(search, lowStock);
      setProducts(res.data);
    } catch (err) {
      addToast("Failed to load products", "error");
    } finally {
      setLoading(false);
    }
  };

  // Validate form fields
  const validate = () => {
    const errors = {};
    if (!form.name.trim()) errors.name = "Name is required";
    if (!form.sku.trim()) errors.sku = "SKU is required";
    if (!form.price || Number(form.price) <= 0)
      errors.price = "Price must be a positive number";
    if (form.quantity_in_stock === "" || Number(form.quantity_in_stock) < 0)
      errors.quantity_in_stock = "Quantity must be 0 or more";
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // Open modal for creating a new product
  const openCreate = () => {
    setEditing(null);
    setForm(emptyForm);
    setFormErrors({});
    setModalOpen(true);
  };

  // Open modal for editing an existing product
  const openEdit = (product) => {
    setEditing(product);
    setForm({
      name: product.name,
      sku: product.sku,
      price: String(product.price),
      quantity_in_stock: String(product.quantity_in_stock),
    });
    setFormErrors({});
    setModalOpen(true);
  };

  // Handle form submission (create or update)
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setSubmitting(true);
    try {
      const payload = {
        name: form.name.trim(),
        sku: form.sku.trim(),
        price: parseFloat(form.price),
        quantity_in_stock: parseInt(form.quantity_in_stock, 10),
      };

      if (editing) {
        // Update existing product
        await updateProduct(editing.id, payload);
        addToast("Product updated successfully!", "success");
      } else {
        // Create new product
        await createProduct(payload);
        addToast("Product created successfully!", "success");
      }

      setModalOpen(false);
      fetchProducts(); // Refresh the list
    } catch (err) {
      // Show the API error message (e.g., "SKU already exists")
      const msg =
        err.response?.data?.detail || "Failed to save product";
      addToast(msg, "error");
    } finally {
      setSubmitting(false);
    }
  };

  // Handle product deletion
  const handleDelete = async () => {
    if (!deleteTarget) return;
    try {
      await deleteProduct(deleteTarget.id);
      addToast("Product deleted successfully!", "success");
      fetchProducts();
    } catch (err) {
      const msg =
        err.response?.data?.detail || "Failed to delete product";
      addToast(msg, "error");
    } finally {
      setDeleteTarget(null);
    }
  };

  // Update a single form field
  const updateField = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (formErrors[field]) {
      setFormErrors((prev) => ({ ...prev, [field]: undefined }));
    }
  };

  return (
    <div>
      {/* Page header with actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Products</h1>
        <button
          onClick={openCreate}
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium text-sm"
        >
          + Add Product
        </button>
      </div>

      {/* Search and filter bar */}
      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        {/* Search input */}
        <div className="flex-1">
          <input
            type="text"
            placeholder="Search by name or SKU..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full px-4 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
        </div>

        {/* Low stock toggle */}
        <button
          onClick={() => setLowStock(!lowStock)}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors border ${
            lowStock
              ? "bg-amber-100 text-amber-800 border-amber-300"
              : "bg-white text-slate-600 border-slate-300 hover:bg-slate-50"
          }`}
        >
          ⚠️ Low Stock Only
        </button>
      </div>

      {/* Products table */}
      {loading ? (
        <LoadingSpinner />
      ) : products.length === 0 ? (
        <div className="bg-white rounded-xl shadow-md p-10 text-center">
          <p className="text-slate-400 text-lg">No products found</p>
          <p className="text-slate-300 text-sm mt-1">
            {search || lowStock
              ? "Try adjusting your filters"
              : "Click 'Add Product' to get started"}
          </p>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-md overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="text-left px-4 py-3 font-semibold text-slate-600">
                    Name
                  </th>
                  <th className="text-left px-4 py-3 font-semibold text-slate-600">
                    SKU
                  </th>
                  <th className="text-right px-4 py-3 font-semibold text-slate-600">
                    Price
                  </th>
                  <th className="text-right px-4 py-3 font-semibold text-slate-600">
                    Stock
                  </th>
                  <th className="text-right px-4 py-3 font-semibold text-slate-600">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                {products.map((product) => (
                  <tr
                    key={product.id}
                    className="border-b border-slate-100 last:border-0 hover:bg-slate-50 transition-colors"
                  >
                    <td className="px-4 py-3 font-medium text-slate-800">
                      {product.name}
                    </td>
                    <td className="px-4 py-3 text-slate-500">{product.sku}</td>
                    <td className="px-4 py-3 text-right text-slate-700">
                      ${Number(product.price).toFixed(2)}
                    </td>
                    <td className="px-4 py-3 text-right">
                      <span
                        className={`px-2 py-0.5 rounded-full text-xs font-semibold ${
                          product.quantity_in_stock < 10
                            ? "bg-red-100 text-red-700"
                            : "bg-emerald-100 text-emerald-700"
                        }`}
                      >
                        {product.quantity_in_stock}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-right">
                      <div className="flex gap-2 justify-end">
                        <button
                          onClick={() => openEdit(product)}
                          className="px-3 py-1 text-xs font-medium text-indigo-600 bg-indigo-50 rounded-md hover:bg-indigo-100 transition-colors"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => setDeleteTarget(product)}
                          className="px-3 py-1 text-xs font-medium text-red-600 bg-red-50 rounded-md hover:bg-red-100 transition-colors"
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Create / Edit Modal */}
      <Modal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editing ? "Edit Product" : "Add New Product"}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Name field */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Product Name *
            </label>
            <input
              type="text"
              value={form.name}
              onChange={(e) => updateField("name", e.target.value)}
              className={`w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 ${
                formErrors.name ? "border-red-400" : "border-slate-300"
              }`}
              placeholder="e.g., Wireless Mouse"
            />
            {formErrors.name && (
              <p className="text-red-500 text-xs mt-1">{formErrors.name}</p>
            )}
          </div>

          {/* SKU field */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              SKU *
            </label>
            <input
              type="text"
              value={form.sku}
              onChange={(e) => updateField("sku", e.target.value)}
              className={`w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 ${
                formErrors.sku ? "border-red-400" : "border-slate-300"
              }`}
              placeholder="e.g., WM-001"
            />
            {formErrors.sku && (
              <p className="text-red-500 text-xs mt-1">{formErrors.sku}</p>
            )}
          </div>

          {/* Price field */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Price ($) *
            </label>
            <input
              type="number"
              step="0.01"
              min="0.01"
              value={form.price}
              onChange={(e) => updateField("price", e.target.value)}
              className={`w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 ${
                formErrors.price ? "border-red-400" : "border-slate-300"
              }`}
              placeholder="e.g., 29.99"
            />
            {formErrors.price && (
              <p className="text-red-500 text-xs mt-1">{formErrors.price}</p>
            )}
          </div>

          {/* Quantity field */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Quantity *
            </label>
            <input
              type="number"
              min="0"
              value={form.quantity_in_stock}
              onChange={(e) => updateField("quantity_in_stock", e.target.value)}
              className={`w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 ${
                formErrors.quantity_in_stock ? "border-red-400" : "border-slate-300"
              }`}
              placeholder="e.g., 100"
            />
            {formErrors.quantity_in_stock && (
              <p className="text-red-500 text-xs mt-1">{formErrors.quantity_in_stock}</p>
            )}
          </div>

          {/* Submit button */}
          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={() => setModalOpen(false)}
              className="flex-1 px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 transition-colors font-medium text-sm"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium text-sm disabled:opacity-50"
            >
              {submitting
                ? "Saving..."
                : editing
                ? "Update Product"
                : "Create Product"}
            </button>
          </div>
        </form>
      </Modal>

      {/* Delete confirmation */}
      <ConfirmDialog
        isOpen={!!deleteTarget}
        onCancel={() => setDeleteTarget(null)}
        onConfirm={handleDelete}
        message={`Are you sure you want to delete "${deleteTarget?.name}"? This action cannot be undone.`}
      />
    </div>
  );
}
