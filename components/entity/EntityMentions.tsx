export default function EntityMentions({
  mentions,
}: {
  mentions: Array<{ caseTitle: string; count: number }>;
}) {
  return (
    <div className="card p-6">
      <h2 className="text-xl font-semibold">Mentions</h2>
      <div className="mt-4 space-y-3">
        {mentions.map((mention) => (
          <div key={mention.caseTitle} className="rounded-xl border border-white/10 p-4">
            <div className="font-medium">{mention.caseTitle}</div>
            <div className="mt-1 text-sm text-slate-300">Mentions: {mention.count}</div>
          </div>
        ))}
      </div>
    </div>
  );
}