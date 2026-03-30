import { NextResponse } from "next/server";
import { execSync } from "child_process";

export async function POST() {
  try {
    execSync("python scripts/run_pipeline.py", { stdio: "pipe" });
    return NextResponse.json({ ok: true, message: "Pipeline completed successfully." });
  } catch (error) {
    return NextResponse.json(
      {
        ok: false,
        error: "Pipeline failed.",
        details: error instanceof Error ? error.message : String(error),
      },
      { status: 500 }
    );
  }
}