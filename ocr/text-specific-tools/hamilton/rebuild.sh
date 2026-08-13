#!/bin/sh
set -eu

PY=/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3
OCR=/Users/zacharygrunenberg/Projects/Enchiridion/ocr

"$PY" "$OCR/0-recon/recon-epub.py" source/pg18-images-3.epub
"$PY" "$OCR/2-extract/extract-epub.py" source/pg18-images-3.epub raw.md --report
"$PY" build_federalist.py raw.md hamilton-madison-jay-federalist-papers.md
"$PY" verify_federalist.py hamilton-madison-jay-federalist-papers.md
"$PY" "$OCR/verify/lint-math.py" hamilton-madison-jay-federalist-papers.md
node "$OCR/verify/check-math.js" hamilton-madison-jay-federalist-papers.md
node "$OCR/verify/check-raw-latex.js" hamilton-madison-jay-federalist-papers.md
