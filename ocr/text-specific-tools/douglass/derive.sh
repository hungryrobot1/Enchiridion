#!/bin/sh
set -eu

PYTHON=/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3
OCR=/Users/zacharygrunenberg/Projects/Enchiridion/ocr

"$PYTHON" "$OCR/2-extract/extract-epub.py" \
  source/pg23-images-3.epub raw.md --report
"$PYTHON" build_douglass.py raw.md \
  douglass-narrative-of-the-life-of-frederick-douglass.md \
  --removed-text removed-frontmatter.txt
