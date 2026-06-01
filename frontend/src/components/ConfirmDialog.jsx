// ============================================
// ConfirmDialog — Confirmation modal for destructive actions
// Props:
//   isOpen    - boolean to show/hide
//   onConfirm - callback when user confirms the action
//   onCancel  - callback when user cancels
//   message   - the question to display (e.g., "Delete this product?")
// ============================================

export default function ConfirmDialog({ isOpen, onConfirm, onCancel, message }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Dark backdrop */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onCancel}
      />

      {/* Dialog box */}
      <div className="relative bg-white rounded-xl shadow-2xl w-full max-w-sm p-6">
        {/* Warning icon */}
        <div className="flex justify-center mb-4">
          <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
            <span className="text-red-600 text-2xl">⚠</span>
          </div>
        </div>

        {/* Message */}
        <p className="text-center text-slate-700 font-medium mb-6">{message}</p>

        {/* Action buttons */}
        <div className="flex gap-3 justify-center">
          <button
            onClick={onCancel}
            className="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 transition-colors font-medium"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}
