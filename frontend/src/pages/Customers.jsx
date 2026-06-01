// ============================================
// Customers Page — Manage customer records
// Features: list, add, delete customers
// ============================================

import { useState, useEffect } from "react";
import { getCustomers, createCustomer, deleteCustomer } from "../api/api";
import Modal from "../components/Modal";
import ConfirmDialog from "../components/ConfirmDialog";
import LoadingSpinner from "../components/LoadingSpinner";
import { useToast } from "../components/Toast";

// Default empty form state
const emptyForm = { full_name: "", email: "", phone: "" };

export default function Customers() {
  // State
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);

  // Modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState(emptyForm);
  const [formErrors, setFormErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  // Delete confirmation state
  const [deleteTarget, setDeleteTarget] = useState(null);

  const { addToast } = useToast();

  // Fetch customers on mount
  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      setLoading(true);
      const res = await getCustomers();
      setCustomers(res.data);
    } catch (err) {
      addToast("Failed to load customers", "error");
    } finally {
      setLoading(false);
    }
  };

  // Validate form fields
  const validate = () => {
    const errors = {};
    if (!form.full_name.trim()) errors.full_name = "Full name is required";
    if (!form.email.trim()) {
      errors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
      errors.email = "Invalid email format";
    }
    // Phone is optional but validate format if provided
    if (form.phone && form.phone.trim().length < 7) {
      errors.phone = "Phone number seems too short";
    }
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // Open create modal
  const openCreate = () => {
    setForm(emptyForm);
    setFormErrors({});
    setModalOpen(true);
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setSubmitting(true);
    try {
      const payload = {
        full_name: form.full_name.trim(),
        email: form.email.trim(),
        phone: form.phone.trim() || null,
      };

      await createCustomer(payload);
      addToast("Customer created successfully!", "success");
      setModalOpen(false);
      fetchCustomers();
    } catch (err) {
      // Show API error (e.g., "Email already exists")
      const msg =
        err.response?.data?.detail || "Failed to create customer";
      addToast(msg, "error");
    } finally {
      setSubmitting(false);
    }
  };

  // Handle customer deletion
  const handleDelete = async () => {
    if (!deleteTarget) return;
    try {
      await deleteCustomer(deleteTarget.id);
      addToast("Customer deleted successfully!", "success");
      fetchCustomers();
    } catch (err) {
      const msg =
        err.response?.data?.detail || "Failed to delete customer";
      addToast(msg, "error");
    } finally {
      setDeleteTarget(null);
    }
  };

  // Update a single form field
  const updateField = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
    if (formErrors[field]) {
      setFormErrors((prev) => ({ ...prev, [field]: undefined }));
    }
  };

  return (
    <div>
      {/* Page header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Customers</h1>
        <button
          onClick={openCreate}
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium text-sm"
        >
          + Add Customer
        </button>
      </div>

      {/* Customers table */}
      {loading ? (
        <LoadingSpinner />
      ) : customers.length === 0 ? (
        <div className="bg-white rounded-xl shadow-md p-10 text-center">
          <p className="text-slate-400 text-lg">No customers found</p>
          <p className="text-slate-300 text-sm mt-1">
            Click &apos;Add Customer&apos; to get started
          </p>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-md overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="text-left px-4 py-3 font-semibold text-slate-600">
                    ID
                  </th>
                  <th className="text-left px-4 py-3 font-semibold text-slate-600">
                    Full Name
                  </th>
                  <th className="text-left px-4 py-3 font-semibold text-slate-600">
                    Email
                  </th>
                  <th className="text-left px-4 py-3 font-semibold text-slate-600">
                    Phone
                  </th>
                  <th className="text-right px-4 py-3 font-semibold text-slate-600">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                {customers.map((customer) => (
                  <tr
                    key={customer.id}
                    className="border-b border-slate-100 last:border-0 hover:bg-slate-50 transition-colors"
                  >
                    <td className="px-4 py-3 text-slate-400">#{customer.id}</td>
                    <td className="px-4 py-3 font-medium text-slate-800">
                      {customer.full_name}
                    </td>
                    <td className="px-4 py-3 text-slate-600">
                      {customer.email}
                    </td>
                    <td className="px-4 py-3 text-slate-500">
                      {customer.phone || "—"}
                    </td>
                    <td className="px-4 py-3 text-right">
                      <button
                        onClick={() => setDeleteTarget(customer)}
                        className="px-3 py-1 text-xs font-medium text-red-600 bg-red-50 rounded-md hover:bg-red-100 transition-colors"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Create Modal */}
      <Modal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        title="Add New Customer"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Name field */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Full Name *
            </label>
            <input
              type="text"
              value={form.full_name}
              onChange={(e) => updateField("full_name", e.target.value)}
              className={`w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 ${
                formErrors.full_name ? "border-red-400" : "border-slate-300"
              }`}
              placeholder="e.g., John Doe"
            />
            {formErrors.full_name && (
              <p className="text-red-500 text-xs mt-1">{formErrors.full_name}</p>
            )}
          </div>

          {/* Email field */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Email *
            </label>
            <input
              type="email"
              value={form.email}
              onChange={(e) => updateField("email", e.target.value)}
              className={`w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 ${
                formErrors.email ? "border-red-400" : "border-slate-300"
              }`}
              placeholder="e.g., john@example.com"
            />
            {formErrors.email && (
              <p className="text-red-500 text-xs mt-1">{formErrors.email}</p>
            )}
          </div>

          {/* Phone field */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Phone
            </label>
            <input
              type="text"
              value={form.phone}
              onChange={(e) => updateField("phone", e.target.value)}
              className={`w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 ${
                formErrors.phone ? "border-red-400" : "border-slate-300"
              }`}
              placeholder="e.g., +1 555-0123"
            />
            {formErrors.phone && (
              <p className="text-red-500 text-xs mt-1">{formErrors.phone}</p>
            )}
          </div>

          {/* Submit buttons */}
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
              {submitting ? "Creating..." : "Create Customer"}
            </button>
          </div>
        </form>
      </Modal>

      {/* Delete confirmation */}
      <ConfirmDialog
        isOpen={!!deleteTarget}
        onCancel={() => setDeleteTarget(null)}
        onConfirm={handleDelete}
        message={`Are you sure you want to delete "${deleteTarget?.full_name}"? This action cannot be undone.`}
      />
    </div>
  );
}
