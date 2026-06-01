// ============================================
// Sidebar Component — Navigation menu
// Displays the app logo and navigation links
// Props:
//   isOpen   - boolean for mobile visibility
//   onClose  - callback to close sidebar on mobile
// ============================================

import { NavLink } from "react-router-dom";

// Navigation items configuration
const navItems = [
  { to: "/dashboard", label: "Dashboard", icon: "📊" },
  { to: "/products", label: "Products", icon: "📦" },
  { to: "/customers", label: "Customers", icon: "👥" },
  { to: "/orders", label: "Orders", icon: "🛒" },
];

export default function Sidebar({ isOpen, onClose }) {
  return (
    <>
      {/* Mobile overlay — shown when sidebar is open on small screens */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-20 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar panel */}
      <aside
        className={`
          fixed top-0 left-0 z-30 h-full w-64 bg-slate-800 text-white
          transform transition-transform duration-300 ease-in-out
          lg:translate-x-0 lg:static lg:z-auto
          ${isOpen ? "translate-x-0" : "-translate-x-full"}
        `}
      >
        {/* Logo / App name */}
        <div className="p-5 border-b border-slate-700">
          <h1 className="text-xl font-bold tracking-wide flex items-center gap-2">
            <span className="text-2xl">📋</span>
            Inventory MS
          </h1>
          <p className="text-slate-400 text-xs mt-1">Management System</p>
        </div>

        {/* Navigation links */}
        <nav className="p-3 flex flex-col gap-1 mt-2">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              onClick={onClose} // Close sidebar on mobile after clicking
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-indigo-600 text-white shadow-md"
                    : "text-slate-300 hover:bg-slate-700 hover:text-white"
                }`
              }
            >
              <span className="text-lg">{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>

        {/* Bottom section */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-slate-700">
          <p className="text-xs text-slate-500 text-center">
            © 2026 Inventory MS
          </p>
        </div>
      </aside>
    </>
  );
}
