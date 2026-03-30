export default function TimelinePanel({ years }: { years: string[] }) {
  return (
    <div className="card p-6">
      <h2 className="text-xl font-semibold">Timeline References</h2>
      <div className="mt-4 flex flex-wrap gap-3">
        {years.length === 0 ? (
          <p className="text-slate-400">No timeline references found yet.</p>
        ) : (
          years.map((year) => (
            <span key={year} className="badge">
              {year}
            </span>
          ))
        )}
      </div>
    </div>
  );
}