"""Convert flaws.cloud CloudTrail logs to NDJSON (one event per line).

Each source file is one large JSON object with a "Records" array, which is
awkward to load in parallel. This script rewrites every file so each line is
a single CloudTrail event, gzip-compressed.

Usage (run from inside the prep/ folder):
    python prep.py
"""
import gzip
import json
import glob
import os

RAW_DIR = os.path.join("..", "data", "raw")
OUT_DIR = os.path.join("..", "data", "ndjson")
os.makedirs(OUT_DIR, exist_ok=True)

for path in glob.glob(os.path.join(RAW_DIR, "**", "*.json.gz"), recursive=True):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        records = json.load(f)["Records"]
    out = os.path.join(OUT_DIR, os.path.basename(path))
    with gzip.open(out, "wt", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    print(out, len(records))
