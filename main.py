"""Sandbox entry point for the 20 November 2026 entry.

The front page is rendered ahead of time by build_image.py; this
script only delivers the finished PNG to the harness output folder
(MAKEFUN_OUTPUT_DIR, falling back to /output). Fully offline and
deterministic.
"""

import os
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent
RENDERED = BASE / "entry.png"


def destination() -> Path:
    folder = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "entry.png"


def deliver() -> Path:
    target = destination()
    shutil.copyfile(RENDERED, target)
    return target


def main() -> None:
    path = deliver()
    print(f"delivered {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
