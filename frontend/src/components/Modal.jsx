// ============================================
// Modal Component — Reusable overlay dialog
// Props:
//   isOpen   - boolean to show/hide
//   onClose  - callback when modal is closed
//   title    - header text for the modal
//   children - modal body content
// ============================================

export default function Modal({ isOpen, onClose, title, children }) {
  // Don't render anything if the modal is not open
  if (!isOpen) return null;

  return (
    // Overlay backdrop — click to close
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      {/* Dark backdrop with blur */}
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" />

      {/* Modal content — stop propagation to prevent closing when clicking inside */}
      <div
        className="relative bg-white rounded-xl shadow-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header with title and close button */}
        <div className="flex items-center justify-between p-5 border-b border-slate-200">
          <h2 className="text-lg font-semibold text-slate-900">{title}</h2>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 transition-colors text-2xl leading-none"
          >
            ×
          </button>
        </div>

        {/* Body content */}
        <div className="p-5">{children}</div>
      </div>
    </div>
  );
}
