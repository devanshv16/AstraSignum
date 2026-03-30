export default function EntityHeader({ name }: { name: string }) {
  return (
    <div className="card p-6">
      <div className="text-sm text-sky-300">Entity</div>
      <h1 className="mt-2 text-3xl font-bold">{name}</h1>
    </div>
  );
}