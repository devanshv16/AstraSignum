import json
import os
from typing import Any, Dict, List, Tuple

ENTITIES_DIR = "data/processed/entities"
OUTPUT_DIR = "data/processed/profiles"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def summarize_mentions(mentions: List[Dict[str, Any]], limit: int = 8) -> List[Dict[str, Any]]:
    mentions = sorted(mentions, key=lambda m: float(m.get("start", 0)))
    trimmed = []
    seen_contexts = set()

    for mention in mentions:
        context = mention.get("context", "").strip()
        if not context or context in seen_contexts:
            continue
        seen_contexts.add(context)
        trimmed.append({
            "start": mention.get("start", 0),
            "context": context
        })
        if len(trimmed) >= limit:
            break

    return trimmed


def build_profile(person_name: str, person_payload: Dict[str, Any]) -> Dict[str, Any]:
    mentions = person_payload.get("mentions", [])
    mention_count = int(person_payload.get("count", 0))
    timeline = summarize_mentions(mentions, limit=10)

    description_parts = []
    if timeline:
        description_parts.append(
            f"{person_name} is mentioned {mention_count} time(s) in this case."
        )
        description_parts.append(
            "The transcript references this person across multiple moments in the story, suggesting they may be an important witness, participant, investigator, official, or recurring figure."
        )

    if timeline:
        description_parts.append(
            "Early and repeated mention contexts include: " +
            " ".join(item["context"] for item in timeline[:3])
        )

    return {
        "name": person_name,
        "mention_count": mention_count,
        "profile_summary": " ".join(description_parts).strip(),
        "timeline_mentions": timeline
    }


def build_profiles_for_case(filename: str) -> Dict[str, Any]:
    entity_path = os.path.join(ENTITIES_DIR, filename)
    entities = load_json(entity_path)

    people = entities.get("people", {})
    profiles = []

    # Only build profiles for people with at least 2 mentions to reduce junk
    sorted_people: List[Tuple[str, Dict[str, Any]]] = sorted(
        people.items(),
        key=lambda item: (-int(item[1].get("count", 0)), item[0].lower())
    )

    for person_name, payload in sorted_people:
        if int(payload.get("count", 0)) < 2:
            continue
        profiles.append(build_profile(person_name, payload))

    return {
        "case_id": filename.replace(".json", ""),
        "people_profiles": profiles
    }


def main() -> None:
    files = [f for f in os.listdir(ENTITIES_DIR) if f.endswith(".json")]
    if not files:
        print("[build_person_profiles] No entity files found.")
        return

    for filename in files:
        payload = build_profiles_for_case(filename)
        output_path = os.path.join(OUTPUT_DIR, filename)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        print(f"[build_person_profiles] Saved: {output_path}")


if __name__ == "__main__":
    main()