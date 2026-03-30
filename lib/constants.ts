import path from "path";

export const APP_NAME = process.env.NEXT_PUBLIC_APP_NAME || "Astra Signum";

export const ROOT_DIR = process.cwd();
export const DATA_DIR = path.join(ROOT_DIR, "data");
export const RAW_DIR = path.join(DATA_DIR, "raw");
export const PROCESSED_DIR = path.join(DATA_DIR, "processed");

export const VIDEOS_FILE = path.join(RAW_DIR, "videos.json");
export const RAW_TRANSCRIPTS_DIR = path.join(RAW_DIR, "transcripts");
export const CLEANED_TRANSCRIPTS_DIR = path.join(PROCESSED_DIR, "cleaned_transcripts");
export const ENTITIES_DIR = path.join(PROCESSED_DIR, "entities");
export const SUMMARIES_DIR = path.join(PROCESSED_DIR, "summaries");
export const PROFILES_DIR = path.join(PROCESSED_DIR, "profiles");