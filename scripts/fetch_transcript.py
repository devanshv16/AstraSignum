import json
import os
import re
from urllib.parse import parse_qs, urlparse
from typing import Dict, List, Tuple, Any

from youtube_transcript_api import YouTubeTranscriptApi

VIDEOS_PATH = "data/raw/videos.json"
RAW_TRANSCRIPTS_DIR = "data/raw/transcripts"


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def extract_video_id(url: str) -> str:
    parsed = urlparse(url)

    if parsed.hostname in {"youtu.be", "www.youtu.be"}:
        return parsed.path.lstrip("/")

    if parsed.hostname and "youtube.com" in parsed.hostname:
        query = parse_qs(parsed.query)
        if "v" in query:
            return query["v"][0]

        match = re.search(r"/shorts/([^/?]+)", parsed.path)
        if match:
            return match.group(1)

        match = re.search(r"/embed/([^/?]+)", parsed.path)
        if match:
            return match.group(1)

    raise ValueError(f"Could not extract video id from URL: {url}")


def load_videos() -> List[Dict[str, Any]]:
    if not os.path.exists(VIDEOS_PATH):
        raise FileNotFoundError(f"{VIDEOS_PATH} not found.")

    with open(VIDEOS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(f"{VIDEOS_PATH} must contain a JSON list.")

    valid_videos = []
    for item in data:
        if not isinstance(item, dict):
            continue
        if not item.get("url"):
            continue
        valid_videos.append(item)

    return valid_videos


def fetch_transcript(video_url: str) -> Tuple[str, List[Dict[str, Any]]]:
    video_id = extract_video_id(video_url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return video_id, transcript


def save_transcript(slug: str, transcript: List[Dict[str, Any]]) -> str:
    ensure_dir(RAW_TRANSCRIPTS_DIR)
    output_path = os.path.join(RAW_TRANSCRIPTS_DIR, f"{slug}.json")

    # Save ONLY the raw segment list so it matches clean_transcript.py
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(transcript, f, indent=2, ensure_ascii=False)

    return output_path


def process_video(video: Dict[str, Any]) -> None:
    title = video.get("title", "untitled-video")
    url = video.get("url", "").strip()
    slug = video.get("slug") or slugify(title)

    if not url:
        print(f"[fetch_transcript] Skipping '{title}': missing URL")
        return

    try:
        video_id, transcript = fetch_transcript(url)
        output_path = save_transcript(slug, transcript)
        print(
            f"[fetch_transcript] Saved transcript for '{title}' "
            f"(video_id={video_id}, segments={len(transcript)}) -> {output_path}"
        )
    except Exception as e:
        print(f"[fetch_transcript] Failed for '{title}' ({url}): {e}")


def main() -> None:
    ensure_dir(RAW_TRANSCRIPTS_DIR)
    videos = load_videos()

    if not videos:
        print("[fetch_transcript] No valid videos found in videos.json")
        return

    print(f"[fetch_transcript] Found {len(videos)} video(s).")

    for video in videos:
        process_video(video)


if __name__ == "__main__":
    main()