#!/bin/sh
# Re-derive Hilbert's Mathematical Problems and run its acceptance checks.
set -eu

OCR_ROOT=/Users/zacharygrunenberg/Projects/Enchiridion/ocr
PYTHON="$OCR_ROOT/.venv/bin/python3"
SOURCE=source/pg71655-images-3.epub
RAW=raw-hilbert.md
OUTPUT=hilbert-mathematical-problems.md

"$PYTHON" "$OCR_ROOT/0-recon/recon-epub.py" "$SOURCE"
"$PYTHON" extract-hilbert.py "$SOURCE" "$RAW"
"$PYTHON" stage3-hilbert.py "$RAW" "$OUTPUT"
"$PYTHON" verify-hilbert.py "$SOURCE" "$OUTPUT"
"$PYTHON" "$OCR_ROOT/verify/verify-controls.py" "$OUTPUT"
