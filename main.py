"""News-image entry for make.fun news-image-01.

The program copies the artwork shipped beside it (entry.png) to the
grader's output directory. It uses only the Python standard library,
writes the same bytes on every run, and needs no network.

Run locally with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT.mkdir(parents=True, exist_ok=True)
source = HERE / "entry.png"
if not source.is_file():
    raise SystemExit("entry.png missing beside main.py")
shutil.copyfile(source, OUT / "entry.png")
