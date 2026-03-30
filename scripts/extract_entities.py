import json
import os
import re
from collections import Counter, defaultdict
from typing import Dict, List, Any

import spacy

CLEAN_DIR = "data/processed/cleaned_transcripts"
OUTPUT_DIR = "data/processed/entities"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load spaCy English model
# Make sure you install it:
# python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

ENTITY_LABEL_MAP = {
    "PERSON": "people",
    "GPE": "places",
    "LOC": "places",
    "ORG": "organizations",
    "DATE": "dates",
    "EVENT": "events",
}

STOPLIKE_ENTITY_VALUES = {
    "today", "tomorrow", "yesterday", "monday", "tuesday", "wednesday",
    "thursday", "friday", "saturday", "sunday"
}


def normalize_entity_name(name: str) -> str:
    name = name.strip()
    name = re.sub(r"\s+", " ", name)
    return name


def extract_years(text: str) -> List[str]:
    return re.findall(r"\b(18\d{2}|19\d{2}|20\d{2}|21\d{2})\b", text)


def load_cleaned_transcript(filepath: str) -> List[Dict[str, Any]]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(f"{filepath} does not contain a list.")

    return data


def empty_entity_bucket() -> Dict[str, Any]:
    return {
        "count": 0,
        "mentions": []
    }


def add_mention(bucket: Dict[str, Any], text: str, start: float) -> None:
    bucket["count"] += 1
    bucket["mentions"].append({
        "start": start,
        "context": text
    })


def sort_entities(entity_map: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return dict(
        sorted(
            entity_map.items(),
            key=lambda item: (-item[1]["count"], item[0].lower())
        )
    )


def build_case_entities(chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    grouped_entities = {
        "people": defaultdict(empty_entity_bucket),
        "places": defaultdict(empty_entity_bucket),
        "organizations": defaultdict(empty_entity_bucket),
        "dates": defaultdict(empty_entity_bucket),
        "events": defaultdict(empty_entity_bucket),
    }

    year_counter = Counter()
    all_text = []

    for chunk in chunks:
        text = chunk.get("text", "").strip()
        start = float(chunk.get("start", 0))
        if not text:
            continue

        all_text.append(text)
        doc = nlp(text)

        for ent in doc.ents:
            mapped_type = ENTITY_LABEL_MAP.get(ent.label_)
            if not mapped_type:
                continue

            entity_name = normalize_entity_name(ent.text)
            if not entity_name:
                continue

            if entity_name.lower() in STOPLIKE_ENTITY_VALUES:
                continue

            add_mention(grouped_entities[mapped_type][entity_name], text, start)

        # Extra year extraction because DATE NER is often fuzzy
        years = extract_years(text)
        for year in years:
            year_counter[year] += 1
            add_mention(grouped_entities["dates"][year], text, start)

    result = {}
    for category, entity_map in grouped_entities.items():
        result[category] = sort_entities(entity_map)

    result["year_frequency"] = dict(sorted(year_counter.items(), key=lambda item: item[0]))
    result["transcript_stats"] = {
        "chunk_count": len(chunks),
        "word_count": sum(len(t.split()) for t in all_text),
        "character_count": sum(len(t) for t in all_text),
    }

    return result


def process_file(filename: str) -> None:
    filepath = os.path.join(CLEAN_DIR, filename)
    chunks = load_cleaned_transcript(filepath)
    case_entities = build_case_entities(chunks)

    output_path = os.path.join(OUTPUT_DIR, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(case_entities, f, indent=2, ensure_ascii=False)

    print(f"[extract_entities] Saved: {output_path}")


def main() -> None:
    files = [f for f in os.listdir(CLEAN_DIR) if f.endswith(".json")]
    if not files:
        print("[extract_entities] No cleaned transcripts found.")
        return

    for filename in files:
        process_file(filename)


if __name__ == "__main__":
    main()