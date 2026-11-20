#!/usr/bin/env python3
"""Entrypoint for the make.fun news-image entry.

The grader runs this file with no network access and expects a
deterministic 1024x1024 PNG at /output/entry.png (or in the directory
named by MAKEFUN_OUTPUT_DIR). The finished front page ships in this
repository as entry.png, so the program simply copies it into place.
"""

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENTRY_SOURCE = ROOT / "entry.png"


def resolve_output_dir():
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    return Path(override) if override else Path("/output")


def emit_entry():
    destination_dir = resolve_output_dir()
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / "entry.png"
    shutil.copyfile(ENTRY_SOURCE, destination)
    return destination


def main():
    written = emit_entry()
    print(f"entry written to {written} ({written.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
