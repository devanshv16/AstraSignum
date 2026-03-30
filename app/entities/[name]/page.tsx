import Link from "next/link";
import { getEntityAcrossCases } from "@/lib/db";

export default async function EntityPage({
  params,
}: {
  params: Promise<{ name: string }>;
}) {
  const { name } = await params;
  const decodedName = decodeURIComponent(name);
  const matches = getEntityAcrossCases(decodedName);

  return (
    <div className="space-y-6">
      <div className="card p-6">
        <div className="text-sm text-sky-300">Entity</div>
        <h1 className="mt-2 text-3xl font-bold">{decodedName}</h1>
        <p className="mt-3 text-slate-300">
          This page shows where the entity appears across processed cases.
        </p>
      </div>

      <div className="card p-6">
        <h2 className="text-xl font-semibold">Case Mentions</h2>
        <div className="mt-4 space-y-3">
          {matches.length === 0 ? (
            <p className="text-slate-400">No case mentions found yet.</p>
          ) : (
            matches.map((match) => (
              <Link
                key={`${match.slug}-${match.label}`}
                href={`/cases/${match.slug}`}
                className="block rounded-xl border border-white/10 p-4 hover:border-sky-300/30"
              >
                <div className="font-medium">{match.title}</div>
                <div className="mt-1 text-sm text-slate-300">
                  Type: {match.label} · Mentions: {match.count}
                </div>
              </Link>
            ))
          )}
        </div>
      </div>
    </div>
  );
}