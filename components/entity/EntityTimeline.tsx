export default function EntityTimeline({ facts }: { facts: string[] }) {
  return (
    <div className="card p-6">
      <h2 className="text-xl font-semibold">Timeline Notes</h2>
      <ul className="mt-4 list-disc space-y-2 pl-6 text-slate-300">
        {facts.map((fact) => (
          <li key={fact}>{fact}</li>
        ))}
      </ul>
    </div>
  );
}