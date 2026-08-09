#!/bin/sh
set -eu

REPO_ROOT=${1:-/Users/zacharygrunenberg/Projects/Enchiridion}
PYTHON="$REPO_ROOT/ocr/.venv/bin/python3"

mkdir -p work
"$PYTHON" "$REPO_ROOT/ocr/2-extract/extract-epub.py" \
  source/pg3600-images-3.epub work/montaigne-raw.md --report
"$PYTHON" build_montaigne.py work/montaigne-raw.md montaigne-essays.md
"$PYTHON" verify_montaigne.py montaigne-essays.md
"$PYTHON" "$REPO_ROOT/ocr/verify/lint-math.py" montaigne-essays.md
node "$REPO_ROOT/ocr/verify/check-math.js" montaigne-essays.md
node "$REPO_ROOT/ocr/verify/check-raw-latex.js" montaigne-essays.md
