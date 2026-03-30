export default function CaseHeader({
  title,
  slug,
}: {
  title: string;
  slug: string;
}) {
  return (
    <div className="card p-6">
      <div className="text-sm text-sky-300">Case File</div>
      <h1 className="mt-2 text-3xl font-bold">{title}</h1>
      <p className="mt-2 text-sm text-slate-400">Slug: {slug}</p>
    </div>
  );
}