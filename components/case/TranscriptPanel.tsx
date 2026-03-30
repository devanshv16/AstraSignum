export default function TranscriptPanel({
  transcript,
}: {
  transcript: Array<{
    start: number;
    duration: number;
    cleaned_text: string;
  }>;
}) {
  return (
    <div className="card p-6">
      <h2 className="text-xl font-semibold">Transcript Excerpts</h2>
      <div className="mt-4 space-y-4">
        {transcript.length === 0 ? (
          <p className="text-slate-400">No cleaned transcript found yet.</p>
        ) : (
          transcript.slice(0, 20).map((segment, index) => (
            <div key={`${segment.start}-${index}`} className="rounded-xl border border-white/10 p-4">
              <div className="text-xs text-sky-300">t = {segment.start.toFixed(1)}s</div>
              <p className="mt-2 text-sm leading-6 text-slate-300">{segment.cleaned_text}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}