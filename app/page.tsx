import Link from "next/link";
import { getAllVideos, getCaseSummary } from "@/lib/db";
import { slugify } from "@/lib/slugify";

export default function HomePage() {
  const videos = getAllVideos();

  return (
    <div className="space-y-8">
      <section className="space-y-4">
        <span className="badge">UFO Case Explorer</span>
        <h1 className="text-4xl font-bold tracking-tight">Astra Signum</h1>
        <p className="max-w-3xl text-slate-300">
          Explore long-form UFO case transcripts through summaries, recurring entities,
          timeline references, and case-level profiles.
        </p>
      </section>

      <section className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        {videos.map((video) => {
          const slug = video.slug || slugify(video.title);
          const summary = getCaseSummary(slug);

          return (
            <Link
              key={slug}
              href={`/cases/${slug}`}
              className="card block p-5 transition hover:-translate-y-1 hover:border-sky-300/30"
            >
              <div className="mb-2 text-sm text-sky-300">{video.category.toUpperCase()}</div>
              <h2 className="text-xl font-semibold">{video.title}</h2>
              <p className="mt-3 text-sm text-slate-300">
                {summary?.short_summary || "No summary generated yet. Run the pipeline first."}
              </p>
            </Link>
          );
        })}
      </section>
    </div>
  );
}