import { CaseSummary as CaseSummaryType } from "@/lib/types";

export default function CaseSummary({
  summary,
}: {
  summary: CaseSummaryType;
}) {
  return (
    <div className="card p-6">
      <h2 className="text-xl font-semibold">Summary</h2>
      <p className="mt-4 leading-7 text-slate-300">{summary.short_summary}</p>

      <div className="mt-6">
        <h3 className="font-medium">Key Points</h3>
        <ul className="mt-3 list-disc space-y-2 pl-6 text-slate-300">
          {summary.key_points.map((point) => (
            <li key={point}>{point}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}