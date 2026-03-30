import { NextResponse } from "next/server";
import { getEntityAcrossCases } from "@/lib/db";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ name: string }> }
) {
  const { name } = await params;
  const decodedName = decodeURIComponent(name);

  return NextResponse.json({
    ok: true,
    entity: decodedName,
    matches: getEntityAcrossCases(decodedName),
  });
}