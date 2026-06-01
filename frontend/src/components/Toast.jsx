// ============================================
// Toast Notification System
// Provides context-based toast notifications
// Usage: const { addToast } = useToast();
//        addToast("Message", "success");
// ============================================

import { createContext, useContext, useState, useCallback } from "react";

// Create context for toast notifications
const ToastContext = createContext();

/**
 * Custom hook to access toast notifications
 * @returns {{ addToast: (message: string, type?: "success"|"error"|"info") => void }}
 */
export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error("useToast must be used within a ToastProvider");
  }
  return context;
};

/**
 * Toast Provider — wraps your app to enable toast notifications everywhere
 */
export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  // Add a new toast notification
  const addToast = useCallback((message, type = "info") => {
    const id = Date.now() + Math.random();
    setToasts((prev) => [...prev, { id, message, type }]);

    // Auto-dismiss after 3 seconds
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 3000);
  }, []);

  // Remove a specific toast
  const removeToast = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  // Color mapping for toast types
  const typeStyles = {
    success: "bg-emerald-500 text-white",
    error: "bg-red-500 text-white",
    info: "bg-blue-500 text-white",
  };

  // Icon mapping for toast types
  const typeIcons = {
    success: "✓",
    error: "✕",
    info: "ℹ",
  };

  return (
    <ToastContext.Provider value={{ addToast }}>
      {children}

      {/* Toast container — fixed to top-right of viewport */}
      <div className="fixed top-4 right-4 z-[9999] flex flex-col gap-2">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={`${typeStyles[toast.type]} px-4 py-3 rounded-lg shadow-lg flex items-center gap-3 min-w-[300px] max-w-[400px] animate-slide-in`}
            style={{
              animation: "slideIn 0.3s ease-out",
            }}
          >
            {/* Toast icon */}
            <span className="text-lg font-bold">{typeIcons[toast.type]}</span>
            {/* Toast message */}
            <span className="flex-1 text-sm font-medium">{toast.message}</span>
            {/* Close button */}
            <button
              onClick={() => removeToast(toast.id)}
              className="text-white/80 hover:text-white text-lg font-bold ml-2"
            >
              ×
            </button>
          </div>
        ))}
      </div>

      {/* CSS animation for slide-in effect */}
      <style>{`
        @keyframes slideIn {
          from {
            transform: translateX(100%);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
      `}</style>
    </ToastContext.Provider>
  );
}
