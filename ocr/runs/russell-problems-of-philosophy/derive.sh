#!/bin/sh
set -eu

PYTHON=/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3
OCR_ROOT=/Users/zacharygrunenberg/Projects/Enchiridion/ocr

"$PYTHON" "$OCR_ROOT/2-extract/extract-epub.py" \
  source/pg5827-images-3.epub raw.md --report --no-images
"$PYTHON" build_russell.py raw.md russell-problems-of-philosophy.md \
  --dropped-contents dropped-contents.md \
  --dropped-bibliography dropped-bibliography.md
