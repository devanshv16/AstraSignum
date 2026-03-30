import subprocess
import sys
from typing import List

PIPELINE_SCRIPTS: List[str] = [
    "scripts/seed_videos.py",
    "scripts/ingest_video.py",
    "scripts/extract_entities.py",
    "scripts/build_case_summary.py",
    "scripts/build_person_profiles.py",
]


def run_script(script_path: str) -> None:
    cmd = [sys.executable, script_path]
    print(f"[run_pipeline] Running: {' '.join(cmd)}")

    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Pipeline failed at: {script_path}")


def main() -> None:
    for script in PIPELINE_SCRIPTS:
        run_script(script)

    print("[run_pipeline] Pipeline completed successfully.")


if __name__ == "__main__":
    main()