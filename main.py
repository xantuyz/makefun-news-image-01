"""News-image entry for make.fun news-image-01.

The program copies the artwork shipped beside it (entry.png) to the
grader's output directory. It uses only the Python standard library,
writes the same bytes on every run, and needs no network.

Run locally with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


OUT.mkdir(parents=True, exist_ok=True)
source = HERE / "entry.png"
if not source.is_file():
    raise SystemExit("entry.png missing beside main.py")
target = OUT / "entry.png"
shutil.copyfile(source, target)
if target.stat().st_size != source.stat().st_size:
    raise SystemExit(
        "copy failed: entry.png size mismatch "
        f"({target.stat().st_size} != {source.stat().st_size} bytes)"
    )
if _sha256(target) != _sha256(source):
    raise SystemExit("copy failed: entry.png sha256 mismatch")
