#!/bin/sh
# Re-derive Wollstonecraft's Vindication and run its acceptance checks.
set -eu

OCR_ROOT=/Users/zacharygrunenberg/Projects/Enchiridion/ocr
PYTHON="$OCR_ROOT/.venv/bin/python3"
EPUB=source/pg3420-images-3.epub
RAW=raw.md
OUTPUT=wollstonecraft-vindication-of-the-rights-of-woman.md
DROPPED=dropped-text.txt

"$PYTHON" "$OCR_ROOT/0-recon/recon-epub.py" "$EPUB"
"$PYTHON" "$OCR_ROOT/2-extract/extract-epub.py" \
  "$EPUB" "$RAW" --report --no-images 2>extract-report.txt
"$PYTHON" build_wollstonecraft.py "$RAW" "$OUTPUT" \
  --dropped-text "$DROPPED"
"$PYTHON" "$OCR_ROOT/verify/check-completeness.py" --self-test
"$PYTHON" "$OCR_ROOT/verify/check-completeness.py" \
  "$EPUB" "$OUTPUT" --dropped-text "$DROPPED"
"$PYTHON" "$OCR_ROOT/verify/verify-controls.py" "$OUTPUT"
