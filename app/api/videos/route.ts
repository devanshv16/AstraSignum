import { NextResponse } from "next/server";
import { getAllVideos } from "@/lib/db";

export async function GET() {
  return NextResponse.json({
    ok: true,
    videos: getAllVideos(),
  });
}