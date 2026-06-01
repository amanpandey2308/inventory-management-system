// ============================================
// Orders Page — Create and manage customer orders
// Features: order list, create order with dynamic items,
//           view order details, delete orders
// ============================================

import { useState, useEffect } from "react";
import {
  getOrders,
  getOrder,
  createOrder,
  deleteOrder,
  getProducts,
  getCustomers,
} from "../api/api";
import Modal from "../components/Modal";
import ConfirmDialog from "../components/ConfirmDialog";
import LoadingSpinner from "../components/LoadingSpinner";
import { useToast } from "../components/Toast";

export default function Orders() {
  // State
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  // Create order modal state
  const [createModalOpen, setCreateModalOpen] = useState(false);
  const [customers, setCustomers] = useState([]);
  const [products, setProducts] = useState([]);
  const [selectedCustomer, setSelectedCustomer] = useState("");
  const [orderItems, setOrderItems] = useState([
    { product_id: "", quantity: 1 },
  ]);
  const [submitting, setSubmitting] = useState(false);

  // View details modal state
  const [detailsModalOpen, setDetailsModalOpen] = useState(false);
  const [orderDetails, setOrderDetails] = useState(null);
  const [loadingDetails, setLoadingDetails] = useState(false);

  // Delete confirmation state
  const [deleteTarget, setDeleteTarget] = useState(null);

  const { addToast } = useToast();

  // Fetch orders on mount
  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const res = await getOrders();
      setOrders(res.data);
    } catch (err) {
      addToast("Failed to load orders", "error");
    } finally {
      setLoading(false);
    }
  };

  // Open create order modal — also fetches customers and products
  const openCreate = async () => {
    try {
      const [custRes, prodRes] = await Promise.all([
        getCustomers(),
        getProducts(),
      ]);
      setCustomers(custRes.data);
      setProducts(prodRes.data);
      setSelectedCustomer("");
      setOrderItems([{ product_id: "", quantity: 1 }]);
      setCreateModalOpen(true);
    } catch (err) {
      addToast("Failed to load form data", "error");
    }
  };

  // Add a new item row to the order
  const addItem = () => {
    setOrderItems((prev) => [...prev, { product_id: "", quantity: 1 }]);
  };

  // Remove an item row
  const removeItem = (index) => {
    setOrderItems((prev) => prev.filter((_, i) => i !== index));
  };

  // Update a specific item field
  const updateItem = (index, field, value) => {
    setOrderItems((prev) =>
      prev.map((item, i) =>
        i === index ? { ...item, [field]: value } : item
      )
    );
  };

  // Calculate the price for a single order item line
  const getLineTotal = (item) => {
    const product = products.find((p) => p.id === Number(item.product_id));
    if (!product || !item.quantity) return 0;
    return product.price * item.quantity;
  };

  // Calculate the total order amount
  const getOrderTotal = () => {
    return orderItems.reduce((sum, item) => sum + getLineTotal(item), 0);
  };

  // Handle order creation submission
  const handleCreateOrder = async (e) => {
    e.preventDefault();

    // Validate
    if (!selectedCustomer) {
      addToast("Please select a customer", "error");
      return;
    }

    // Filter out empty items and validate
    const validItems = orderItems.filter(
      (item) => item.product_id && item.quantity > 0
    );
    if (validItems.length === 0) {
      addToast("Please add at least one product", "error");
      return;
    }

    setSubmitting(true);
    try {
      const payload = {
        customer_id: Number(selectedCustomer),
        items: validItems.map((item) => ({
          product_id: Number(item.product_id),
          quantity: Number(item.quantity),
        })),
      };

      await createOrder(payload);
      addToast("Order created successfully!", "success");
      setCreateModalOpen(false);
      fetchOrders();
    } catch (err) {
      // Show API error (e.g., "Insufficient stock for Product X")
      const msg = err.response?.data?.detail || "Failed to create order";
      addToast(msg, "error");
    } finally {
      setSubmitting(false);
    }
  };

  // View order details
  const viewDetails = async (orderId) => {
    try {
      setLoadingDetails(true);
      setDetailsModalOpen(true);
      const res = await getOrder(orderId);
      setOrderDetails(res.data);
    } catch (err) {
      addToast("Failed to load order details", "error");
      setDetailsModalOpen(false);
    } finally {
      setLoadingDetails(false);
    }
  };

  // Handle order deletion
  const handleDelete = async () => {
    if (!deleteTarget) return;
    try {
      await deleteOrder(deleteTarget.id);
      addToast("Order deleted successfully!", "success");
      fetchOrders();
    } catch (err) {
      const msg = err.response?.data?.detail || "Failed to delete order";
      addToast(msg, "error");
    } finally {
      setDeleteTarget(null);
    }
  };

  // Format date string nicely
  const formatDate = (dateStr) => {
    if (!dateStr) return "—";
    return new Date(dateStr).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div>
      {/* Page header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Orders</h1>
        <button
          onClick={openCreate}
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium text-sm"
        >
          + Create Order
        </button>
      </div>

      {/* Orders table */}
      {loading ? (
        <LoadingSpinner />
      ) : orders.length === 0 ? (
        <div className="bg-white rounded-xl shadow-md p-10 text-center">
          <p className="text-slate-400 text-lg">No orders yet</p>
          <p className="text-slate-300 text-sm mt-1">
            Click &apos;Create Order&apos; to place the first order
          </p>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-md overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="text-left px-4 py-3 font-semibold text-slate-600">
                    Order ID
                  </th>
                  <th className="text-left px-4 py-3 font-semibold text-slate-600">
                    Customer
                  </th>
                  <th className="text-right px-4 py-3 font-semibold text-slate-600">
                    Total Amount
                  </th>
                  <th className="text-left px-4 py-3 font-semibold text-slate-600">
                    Date
                  </th>
                  <th className="text-right px-4 py-3 font-semibold text-slate-600">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                {orders.map((order) => (
                  <tr
                    key={order.id}
                    className="border-b border-slate-100 last:border-0 hover:bg-slate-50 transition-colors"
                  >
                    <td className="px-4 py-3 font-medium text-slate-800">
                      #{order.id}
                    </td>
                    <td className="px-4 py-3 text-slate-600">
                      {order.customer_name || order.customer?.name || "—"}
                    </td>
                    <td className="px-4 py-3 text-right font-semibold text-slate-800">
                      ${Number(order.total_amount).toFixed(2)}
                    </td>
                    <td className="px-4 py-3 text-slate-500">
                      {formatDate(order.created_at)}
                    </td>
                    <td className="px-4 py-3 text-right">
                      <div className="flex gap-2 justify-end">
                        <button
                          onClick={() => viewDetails(order.id)}
                          className="px-3 py-1 text-xs font-medium text-indigo-600 bg-indigo-50 rounded-md hover:bg-indigo-100 transition-colors"
                        >
                          View
                        </button>
                        <button
                          onClick={() => setDeleteTarget(order)}
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

      {/* ======================================= */}
      {/* Create Order Modal */}
      {/* ======================================= */}
      <Modal
        isOpen={createModalOpen}
        onClose={() => setCreateModalOpen(false)}
        title="Create New Order"
      >
        <form onSubmit={handleCreateOrder} className="space-y-4">
          {/* Customer dropdown */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Customer *
            </label>
            <select
              value={selectedCustomer}
              onChange={(e) => setSelectedCustomer(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
            >
              <option value="">Select a customer...</option>
              {customers.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.full_name} ({c.email})
                </option>
              ))}
            </select>
          </div>

          {/* Order items */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Order Items *
            </label>

            <div className="space-y-3">
              {orderItems.map((item, index) => (
                <div
                  key={index}
                  className="flex gap-2 items-start p-3 bg-slate-50 rounded-lg"
                >
                  {/* Product dropdown */}
                  <div className="flex-1">
                    <select
                      value={item.product_id}
                      onChange={(e) =>
                        updateItem(index, "product_id", e.target.value)
                      }
                      className="w-full px-2 py-1.5 border border-slate-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
                    >
                      <option value="">Select product...</option>
                      {products.map((p) => (
                        <option key={p.id} value={p.id}>
                          {p.name} — ${Number(p.price).toFixed(2)} (Stock:{" "}
                          {p.quantity_in_stock})
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Quantity input */}
                  <div className="w-20">
                    <input
                      type="number"
                      min="1"
                      value={item.quantity}
                      onChange={(e) =>
                        updateItem(index, "quantity", e.target.value)
                      }
                      className="w-full px-2 py-1.5 border border-slate-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      placeholder="Qty"
                    />
                  </div>

                  {/* Line total */}
                  <div className="w-20 text-right text-sm font-medium text-slate-700 py-1.5">
                    ${getLineTotal(item).toFixed(2)}
                  </div>

                  {/* Remove button (only if more than 1 item) */}
                  {orderItems.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeItem(index)}
                      className="text-red-400 hover:text-red-600 text-lg py-1"
                    >
                      ✕
                    </button>
                  )}
                </div>
              ))}
            </div>

            {/* Add another item button */}
            <button
              type="button"
              onClick={addItem}
              className="mt-2 text-sm text-indigo-600 hover:text-indigo-700 font-medium"
            >
              + Add Another Item
            </button>
          </div>

          {/* Order total */}
          <div className="flex justify-between items-center py-3 border-t border-slate-200 font-semibold text-slate-800">
            <span>Total:</span>
            <span className="text-lg">${getOrderTotal().toFixed(2)}</span>
          </div>

          {/* Submit buttons */}
          <div className="flex gap-3">
            <button
              type="button"
              onClick={() => setCreateModalOpen(false)}
              className="flex-1 px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 transition-colors font-medium text-sm"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium text-sm disabled:opacity-50"
            >
              {submitting ? "Placing Order..." : "Place Order"}
            </button>
          </div>
        </form>
      </Modal>

      {/* ======================================= */}
      {/* View Order Details Modal */}
      {/* ======================================= */}
      <Modal
        isOpen={detailsModalOpen}
        onClose={() => {
          setDetailsModalOpen(false);
          setOrderDetails(null);
        }}
        title={`Order #${orderDetails?.id || ""} Details`}
      >
        {loadingDetails ? (
          <LoadingSpinner />
        ) : orderDetails ? (
          <div className="space-y-4">
            {/* Order info */}
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <p className="text-slate-500">Customer</p>
                <p className="font-medium text-slate-800">
                  {orderDetails.customer_name ||
                    orderDetails.customer?.name ||
                    "—"}
                </p>
              </div>
              <div>
                <p className="text-slate-500">Date</p>
                <p className="font-medium text-slate-800">
                  {formatDate(orderDetails.created_at)}
                </p>
              </div>
            </div>

            {/* Order items table */}
            <div>
              <h3 className="text-sm font-semibold text-slate-700 mb-2">
                Items
              </h3>
              <div className="bg-slate-50 rounded-lg overflow-hidden">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-slate-200">
                      <th className="text-left px-3 py-2 text-slate-600 font-medium">
                        Product
                      </th>
                      <th className="text-right px-3 py-2 text-slate-600 font-medium">
                        Qty
                      </th>
                      <th className="text-right px-3 py-2 text-slate-600 font-medium">
                        Price
                      </th>
                      <th className="text-right px-3 py-2 text-slate-600 font-medium">
                        Total
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {(orderDetails.items || []).map((item, i) => (
                      <tr
                        key={i}
                        className="border-b border-slate-200 last:border-0"
                      >
                        <td className="px-3 py-2 text-slate-700">
                          {item.product_name || item.product?.name || "—"}
                        </td>
                        <td className="px-3 py-2 text-right text-slate-600">
                          {item.quantity}
                        </td>
                        <td className="px-3 py-2 text-right text-slate-600">
                          ${Number(item.price_at_time || item.price || 0).toFixed(2)}
                        </td>
                        <td className="px-3 py-2 text-right font-medium text-slate-800">
                          ${(
                            Number(item.quantity) *
                            Number(item.price_at_time || item.price || 0)
                          ).toFixed(2)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Total */}
            <div className="flex justify-between items-center pt-2 border-t border-slate-200 font-semibold text-slate-800">
              <span>Total Amount:</span>
              <span className="text-lg">
                ${Number(orderDetails.total_amount).toFixed(2)}
              </span>
            </div>
          </div>
        ) : null}
      </Modal>

      {/* Delete confirmation */}
      <ConfirmDialog
        isOpen={!!deleteTarget}
        onCancel={() => setDeleteTarget(null)}
        onConfirm={handleDelete}
        message={`Are you sure you want to delete Order #${deleteTarget?.id}? This action cannot be undone.`}
      />
    </div>
  );
}
