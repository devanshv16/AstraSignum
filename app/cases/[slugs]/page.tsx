import { notFound } from "next/navigation";
import { getCaseEntities, getCaseProfiles, getCaseSummary, getCaseTranscript } from "@/lib/db";
import CaseHeader from "@/components/case/CaseHeader";
import CaseSummary from "@/components/case/CaseSummary";
import EntitySection from "@/components/case/EntitySection";
import TimelinePanel from "@/components/case/TimelinePanel";
import TranscriptPanel from "@/components/case/TranscriptPanel";

export default async function CasePage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;

  const summary = getCaseSummary(slug);
  if (!summary) return notFound();

  const entities = getCaseEntities(slug);
  const transcript = getCaseTranscript(slug);
  const profiles = getCaseProfiles(slug);

  return (
    <div className="space-y-6">
      <CaseHeader title={summary.title} slug={slug} />
      <CaseSummary summary={summary} />
      <EntitySection entities={entities} profiles={profiles} />
      <TimelinePanel years={summary.timeline_years} />
      <TranscriptPanel transcript={transcript} />
    </div>
  );
}