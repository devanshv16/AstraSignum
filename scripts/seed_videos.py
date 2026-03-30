import json
import os
from typing import List, Dict

VIDEOS_PATH = "data/raw/videos.json"


def ensure_parent_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def load_existing_videos() -> List[Dict]:
    if not os.path.exists(VIDEOS_PATH):
        return []

    try:
        with open(VIDEOS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def dedupe_videos(videos: List[Dict]) -> List[Dict]:
    seen = set()
    deduped = []

    for video in videos:
        url = video.get("url", "").strip()
        if not url or url in seen:
            continue
        seen.add(url)
        deduped.append(video)

    return deduped


def seed_default_videos() -> None:
    """
    Creates videos.json if it doesn't exist.
    If it exists, preserves existing entries and appends sample placeholders only if empty.
    """
    ensure_parent_dir(VIDEOS_PATH)
    existing = load_existing_videos()

    if existing:
        print(f"[seed_videos] {VIDEOS_PATH} already has {len(existing)} video(s). No changes made.")
        return

    starter_videos = [
        {
            "title": "Roswell Incident",
            "url": "https://www.youtube.com/watch?v=REPLACE_WITH_VIDEO_ID",
            "category": "ufo",
            "source": "youtube",
            "notes": "Replace with an actual UFO-related video URL."
        },
        {
            "title": "Rendlesham Forest Incident",
            "url": "https://www.youtube.com/watch?v=REPLACE_WITH_VIDEO_ID_2",
            "category": "ufo",
            "source": "youtube",
            "notes": "Replace with an actual UFO-related video URL."
        }
    ]

    starter_videos = dedupe_videos(starter_videos)

    with open(VIDEOS_PATH, "w", encoding="utf-8") as f:
        json.dump(starter_videos, f, indent=2, ensure_ascii=False)

    print(f"[seed_videos] Seeded {len(starter_videos)} starter video(s) into {VIDEOS_PATH}")


if __name__ == "__main__":
    seed_default_videos()