import { NextResponse } from "next/server";
import { getCaseEntities, getCaseProfiles, getCaseSummary, getCaseTranscript } from "@/lib/db";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ slug: string }> }
) {
  const { slug } = await params;
  const summary = getCaseSummary(slug);

  if (!summary) {
    return NextResponse.json({ ok: false, error: "Case not found" }, { status: 404 });
  }

  return NextResponse.json({
    ok: true,
    case: {
      summary,
      entities: getCaseEntities(slug),
      transcript: getCaseTranscript(slug),
      profiles: getCaseProfiles(slug),
    },
  });
}