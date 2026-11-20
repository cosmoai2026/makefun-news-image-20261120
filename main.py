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

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def output_dir():
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    return Path(override) if override else Path("/output")


def copy_entry():
    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    return target


def main():
    target = copy_entry()
    print(f"entry written to {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
