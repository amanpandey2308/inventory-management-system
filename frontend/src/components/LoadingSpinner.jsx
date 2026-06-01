// ============================================
// LoadingSpinner — Shown while data is being fetched
// Centered spinner with a "Loading..." label
// ============================================

export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      {/* Spinning circle */}
      <div className="w-10 h-10 border-4 border-slate-200 border-t-indigo-600 rounded-full animate-spin" />
      {/* Label */}
      <p className="mt-3 text-slate-500 text-sm font-medium">Loading...</p>
    </div>
  );
}
