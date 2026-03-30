import json
import os
from typing import Dict, Any, List, Tuple

CLEAN_DIR = "data/processed/cleaned_transcripts"
ENTITIES_DIR = "data/processed/entities"
OUTPUT_DIR = "data/processed/summaries"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def top_items(entity_map: Dict[str, Dict[str, Any]], limit: int = 5) -> List[Tuple[str, int]]:
    items = []
    for name, payload in entity_map.items():
        count = int(payload.get("count", 0))
        items.append((name, count))
    items.sort(key=lambda x: (-x[1], x[0].lower()))
    return items[:limit]


def get_overview_from_chunks(chunks: List[Dict[str, Any]], max_chunks: int = 5) -> str:
    texts = []
    for chunk in chunks[:max_chunks]:
        text = chunk.get("text", "").strip()
        if text:
            texts.append(text)

    return " ".join(texts)


def build_summary_payload(filename: str) -> Dict[str, Any]:
    clean_path = os.path.join(CLEAN_DIR, filename)
    entity_path = os.path.join(ENTITIES_DIR, filename)

    chunks = load_json(clean_path)
    entities = load_json(entity_path)

    people = top_items(entities.get("people", {}), limit=8)
    places = top_items(entities.get("places", {}), limit=8)
    organizations = top_items(entities.get("organizations", {}), limit=8)
    dates = top_items(entities.get("dates", {}), limit=10)

    narrative_overview = get_overview_from_chunks(chunks, max_chunks=6)

    summary = {
        "case_id": filename.replace(".json", ""),
        "title_guess": filename.replace(".json", "").replace("_", " ").replace("-", " ").title(),
        "overview": narrative_overview,
        "structured_summary": {
            "top_people": [{"name": name, "mentions": count} for name, count in people],
            "top_places": [{"name": name, "mentions": count} for name, count in places],
            "top_organizations": [{"name": name, "mentions": count} for name, count in organizations],
            "top_dates": [{"name": name, "mentions": count} for name, count in dates],
        },
        "timeline_hint": [name for name, _ in dates[:10]],
        "stats": entities.get("transcript_stats", {}),
    }

    # Add a lightweight human-readable paragraph
    readable_bits = []

    if people:
        readable_bits.append(
            "Key people mentioned include " +
            ", ".join(name for name, _ in people[:5]) + "."
        )

    if places:
        readable_bits.append(
            "The story is tied to places such as " +
            ", ".join(name for name, _ in places[:5]) + "."
        )

    if organizations:
        readable_bits.append(
            "Organizations referenced include " +
            ", ".join(name for name, _ in organizations[:5]) + "."
        )

    if dates:
        readable_bits.append(
            "Important dates or years mentioned include " +
            ", ".join(name for name, _ in dates[:6]) + "."
        )

    summary["readable_summary"] = " ".join(readable_bits).strip()

    return summary


def main() -> None:
    files = [f for f in os.listdir(CLEAN_DIR) if f.endswith(".json")]
    if not files:
        print("[build_case_summary] No cleaned transcripts found.")
        return

    for filename in files:
        entity_path = os.path.join(ENTITIES_DIR, filename)
        if not os.path.exists(entity_path):
            print(f"[build_case_summary] Skipping {filename}: missing entities file.")
            continue

        payload = build_summary_payload(filename)
        output_path = os.path.join(OUTPUT_DIR, filename)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        print(f"[build_case_summary] Saved: {output_path}")


if __name__ == "__main__":
    main()