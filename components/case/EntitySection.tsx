import Link from "next/link";
import { ExtractedEntity, PersonProfile } from "@/lib/types";

export default function EntitySection({
  entities,
  profiles,
}: {
  entities: ExtractedEntity[];
  profiles: PersonProfile[];
}) {
  const topEntities = [...entities].sort((a, b) => b.count - a.count).slice(0, 18);

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <div className="card p-6">
        <h2 className="text-xl font-semibold">Top Entities</h2>
        <div className="mt-4 flex flex-wrap gap-3">
          {topEntities.length === 0 ? (
            <p className="text-slate-400">No entities extracted yet.</p>
          ) : (
            topEntities.map((entity) => (
              <Link
                key={`${entity.label}-${entity.text}`}
                href={`/entities/${encodeURIComponent(entity.text)}`}
                className="rounded-full border border-white/10 px-4 py-2 text-sm text-slate-200 hover:border-sky-300/30"
              >
                {entity.text} · {entity.count}
              </Link>
            ))
          )}
        </div>
      </div>

      <div className="card p-6">
        <h2 className="text-xl font-semibold">Person Profiles</h2>
        <div className="mt-4 space-y-4">
          {profiles.length === 0 ? (
            <p className="text-slate-400">No person profiles built yet.</p>
          ) : (
            profiles.slice(0, 8).map((profile) => (
              <div key={profile.name} className="rounded-xl border border-white/10 p-4">
                <div className="font-medium">{profile.name}</div>
                <p className="mt-2 text-sm text-slate-300">{profile.role_summary}</p>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}