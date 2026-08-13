#!/bin/sh
set -eu

# Reproduce the stage-1 PDF handed to manual OCR. The source hash makes this
# fail loudly if the edition is replaced beneath the recorded crop decision.
ROOT=/Users/zacharygrunenberg/Projects/Enchiridion
PYTHON="$ROOT/ocr/.venv/bin/python3"
SOURCE=source/rspa.1928.0023.pdf
OUTDIR=ocr-input/dirac-quantum-theory-of-the-electron
OUTPUT="$OUTDIR/dirac-quantum-theory-of-the-electron-prepared.pdf"
EXPECTED_SHA=d97c12ac75ef9cca8a183719a03b46ff18de57e5c851b5c3e8de334f95a1c3b4

actual_sha=$(shasum -a 256 "$SOURCE" | awk '{print $1}')
test "$actual_sha" = "$EXPECTED_SHA"
mkdir -p "$OUTDIR"

"$PYTHON" "$ROOT/ocr/1-prepare/crop-pdf.py" \
  "$SOURCE" "$OUTPUT" --margins 0 0 25 0

pages=$(qpdf --show-npages "$OUTPUT")
test "$pages" -eq 15

"$PYTHON" "$ROOT/ocr/1-prepare/check-duplicate-leaves.py" \
  "$OUTPUT" --expected-pages 15 --positive-page 3

echo "Prepared and verified: $OUTPUT"

