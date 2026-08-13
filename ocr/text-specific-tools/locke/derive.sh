#!/bin/sh
set -eu

OCR_ROOT=/Users/zacharygrunenberg/Projects/Enchiridion/ocr
PYTHON="$OCR_ROOT/.venv/bin/python3"

"$PYTHON" "$OCR_ROOT/2-extract/extract-epub.py" \
  source/pg7370-images-3.epub source/raw.md --report
"$PYTHON" scripts/process_locke.py \
  source/raw.md locke-second-treatise-of-government.md
