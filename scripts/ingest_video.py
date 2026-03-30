import json
import os
import subprocess
import sys
from typing import Dict, List

VIDEOS_PATH = "data/raw/videos.json"


def load_videos() -> List[Dict]:
    if not os.path.exists(VIDEOS_PATH):
        raise FileNotFoundError(
            f"{VIDEOS_PATH} not found. Create it first or run seed_videos.py."
        )

    with open(VIDEOS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(f"{VIDEOS_PATH} must contain a JSON list.")

    valid = []
    for item in data:
        if not isinstance(item, dict):
            continue
        if item.get("url"):
            valid.append(item)

    return valid


def run_script(script_path: str, args: List[str] | None = None) -> None:
    args = args or []
    cmd = [sys.executable, script_path] + args
    print(f"[ingest_video] Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)

    if result.returncode != 0:
        raise RuntimeError(f"Script failed: {script_path}")


def ingest_all() -> None:
    videos = load_videos()
    if not videos:
        print("[ingest_video] No videos found in videos.json")
        return

    print(f"[ingest_video] Found {len(videos)} video(s) to ingest.")

    # Assumes fetch_transcript.py reads videos.json and fetches all listed videos
    run_script("scripts/fetch_transcript.py")

    # Assumes clean_transcript.py cleans all raw transcripts
    run_script("scripts/clean_transcript.py")

    print("[ingest_video] Ingestion complete.")


if __name__ == "__main__":
    ingest_all()