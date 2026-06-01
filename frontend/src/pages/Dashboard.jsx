// ============================================
// Dashboard Page — Overview of inventory stats
// Displays StatsCards + Low Stock table + Stock level bar chart
// ============================================

import { useState, useEffect } from "react";
import { getDashboard } from "../api/api";
import StatsCard from "../components/StatsCard";
import LoadingSpinner from "../components/LoadingSpinner";
import { useToast } from "../components/Toast";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const { addToast } = useToast();

  // Fetch dashboard data on mount
  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      const res = await getDashboard();
      setStats(res.data);
    } catch (err) {
      const msg =
        err.response?.data?.detail || "Failed to load dashboard data";
      addToast(msg, "error");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;

  // Find the max stock value for the bar chart scaling
  const topProducts = stats?.top_products || [];
  const maxStock = Math.max(...topProducts.map((p) => p.quantity), 1);

  return (
    <div>
      {/* Page heading */}
      <h1 className="text-2xl font-bold text-slate-900 mb-6">Dashboard</h1>

      {/* Stats cards grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatsCard
          title="Total Products"
          value={stats?.total_products ?? 0}
          icon="📦"
          color="bg-indigo-500"
        />
        <StatsCard
          title="Total Customers"
          value={stats?.total_customers ?? 0}
          icon="👥"
          color="bg-emerald-500"
        />
        <StatsCard
          title="Total Orders"
          value={stats?.total_orders ?? 0}
          icon="🛒"
          color="bg-blue-500"
        />
        <StatsCard
          title="Low Stock Items"
          value={stats?.low_stock_count ?? 0}
          icon="⚠️"
          color="bg-amber-500"
        />
      </div>

      {/* Two-column layout for chart and table */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Stock level bar chart */}
        <div className="bg-white rounded-xl shadow-md p-5">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">
            Top Products by Stock
          </h2>
          {topProducts.length === 0 ? (
            <p className="text-slate-400 text-sm">No products yet.</p>
          ) : (
            <div className="space-y-3">
              {topProducts.map((product) => (
                <div key={product.id}>
                  {/* Product name and stock count */}
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-slate-700 font-medium truncate mr-2">
                      {product.name}
                    </span>
                    <span className="text-slate-500 shrink-0">
                      {product.quantity}
                    </span>
                  </div>
                  {/* Bar */}
                  <div className="w-full bg-slate-100 rounded-full h-3">
                    <div
                      className="bg-indigo-500 h-3 rounded-full transition-all duration-500"
                      style={{
                        width: `${(product.quantity / maxStock) * 100}%`,
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Low stock products table */}
        <div className="bg-white rounded-xl shadow-md p-5">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">
            ⚠️ Low Stock Products
          </h2>
          {(stats?.low_stock_products ?? []).length === 0 ? (
            <p className="text-slate-400 text-sm">
              All products are well stocked! 🎉
            </p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left border-b border-slate-200">
                    <th className="pb-2 font-semibold text-slate-600">Name</th>
                    <th className="pb-2 font-semibold text-slate-600">SKU</th>
                    <th className="pb-2 font-semibold text-slate-600 text-right">
                      Stock
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {stats.low_stock_products.map((product) => (
                    <tr
                      key={product.id}
                      className="border-b border-slate-100 last:border-0"
                    >
                      <td className="py-2 text-slate-700">{product.name}</td>
                      <td className="py-2 text-slate-500">{product.sku}</td>
                      <td className="py-2 text-right">
                        <span className="px-2 py-0.5 bg-red-100 text-red-700 rounded-full text-xs font-semibold">
                          {product.quantity_in_stock}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
