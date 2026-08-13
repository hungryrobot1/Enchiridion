#!/bin/sh
set -eu

ROOT=/Users/zacharygrunenberg/Projects/Enchiridion
PY="$ROOT/ocr/.venv/bin/python3"
EPUB=source/pg4280-images-3.epub
RAW=raw.md
OUT=kant-critique-of-pure-reason.md

"$PY" "$ROOT/ocr/2-extract/extract-epub.py" "$EPUB" "$RAW" --report
"$PY" build_kant.py "$RAW" "$OUT" --epub "$EPUB"
