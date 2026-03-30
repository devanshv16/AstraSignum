import os
import json
import re

RAW_DIR = "data/raw/transcripts"
CLEAN_DIR = "data/processed/cleaned_transcripts"

os.makedirs(CLEAN_DIR, exist_ok=True)


# -----------------------------
# Patterns to REMOVE
# -----------------------------
SPONSOR_PATTERNS = [
    r"this video is sponsored by",
    r"thanks to our sponsor",
    r"check out .*\.com",
    r"use code .* for discount",
]

OUTRO_PATTERNS = [
    r"thanks for watching",
    r"like and subscribe",
    r"see you next time",
]

FILLER_PATTERNS = [
    r"uh+",
    r"um+",
    r"you know",
    r"i mean",
]

# combine all
REMOVE_PATTERNS = SPONSOR_PATTERNS + OUTRO_PATTERNS


# -----------------------------
# Utility cleaning functions
# -----------------------------
def normalize_text(text):
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def is_noise(text):
    """
    Decide if a line is useless
    """
    if len(text) < 5:
        return True

    for pattern in REMOVE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


def clean_line(text):
    """
    Clean individual line
    """
    text = normalize_text(text)

    # remove filler words
    for pattern in FILLER_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    # remove weird characters
    text = re.sub(r"[^\w\s.,!?'-]", "", text)

    text = normalize_text(text)

    return text


# -----------------------------
# Main cleaning function
# -----------------------------
def clean_transcript_file(filename):
    raw_path = os.path.join(RAW_DIR, filename)

    with open(raw_path, "r", encoding="utf-8") as f:
        transcript = json.load(f)

    cleaned = []

    for chunk in transcript:
        text = chunk.get("text", "")
        start = chunk.get("start", 0)

        text = clean_line(text)

        if is_noise(text):
            continue

        cleaned.append({
            "text": text,
            "start": start
        })

    # save cleaned output
    output_path = os.path.join(CLEAN_DIR, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2)

    print(f"Cleaned transcript saved: {output_path}")


# -----------------------------
# Run for all files
# -----------------------------
def main():
    files = os.listdir(RAW_DIR)

    for file in files:
        if file.endswith(".json"):
            clean_transcript_file(file)


if __name__ == "__main__":
    main()