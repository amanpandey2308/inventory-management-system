// ============================================
// StatsCard Component — Displays a single dashboard metric
// Props:
//   title - label for the stat (e.g., "Total Products")
//   value - the number to display
//   icon  - emoji or icon string
//   color - Tailwind color class for the accent (e.g., "bg-indigo-500")
// ============================================

export default function StatsCard({ title, value, icon, color = "bg-indigo-500" }) {
  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden">
      {/* Colored top accent bar */}
      <div className={`h-1 ${color}`} />

      <div className="p-5 flex items-center gap-4">
        {/* Icon container with colored background */}
        <div className={`${color} text-white w-12 h-12 rounded-lg flex items-center justify-center text-2xl shrink-0`}>
          {icon}
        </div>

        {/* Text content */}
        <div>
          <p className="text-sm text-slate-500 font-medium">{title}</p>
          <p className="text-2xl font-bold text-slate-900">{value ?? "—"}</p>
        </div>
      </div>
    </div>
  );
}
