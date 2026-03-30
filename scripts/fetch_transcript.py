import json
import os
import re
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi

RAW_TRANSCRIPTS_DIR = "data/raw/transcripts"


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def extract_video_id(url: str) -> str:
    parsed = urlparse(url)

    if parsed.hostname in {"youtu.be"}:
        return parsed.path.lstrip("/")

    if parsed.hostname and "youtube.com" in parsed.hostname:
        query = parse_qs(parsed.query)
        if "v" in query:
            return query["v"][0]

        match = re.search(r"/shorts/([^/?]+)", parsed.path)
        if match:
            return match.group(1)

    raise ValueError(f"Could not extract video id from URL: {url}")


def fetch_transcript(video_url: str):
    video_id = extract_video_id(video_url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return video_id, transcript


def save_transcript(slug: str, video_id: str, transcript) -> str:
    ensure_dir(RAW_TRANSCRIPTS_DIR)
    output_path = os.path.join(RAW_TRANSCRIPTS_DIR, f"{slug}.json")

    payload = {
        "video_id": video_id,
        "segments": transcript,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    return output_path