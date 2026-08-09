#!/bin/sh
# Re-derive the final Lovelace text and rerun its structural and renderer checks.
set -eu

OCR_ROOT=/Users/zacharygrunenberg/Projects/Enchiridion/ocr
PYTHON="$OCR_ROOT/.venv/bin/python3"
SOURCE=source/pg75107-images-3.epub
RAW=raw-lovelace.md
OUTPUT=lovelace-sketch-of-the-analytical-engine.md

"$PYTHON" "$OCR_ROOT/0-recon/recon-epub.py" "$SOURCE"
"$PYTHON" extract-lovelace.py "$SOURCE" "$RAW"
"$PYTHON" stage3-lovelace.py "$RAW" "$OUTPUT"
"$PYTHON" audit-epub-tables.py "$SOURCE"
"$PYTHON" verify-lovelace.py "$SOURCE" "$OUTPUT"
"$PYTHON" "$OCR_ROOT/verify/verify-controls.py" "$OUTPUT"
