#!/bin/sh
set -eu

PY=/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3
OCR=/Users/zacharygrunenberg/Projects/Enchiridion/ocr
TEXT=lobachevsky-theory-of-parallels.md

cp lobachevsky-theory-of-parallels.raw.md "$TEXT"
"$PY" "$OCR/3-postprocess/join-line-wrap-hyphens.py" "$TEXT" --apply
"$PY" "$OCR/3-postprocess/rejoin-split-paragraphs.py" "$TEXT" --rule --apply --min-words 5
"$PY" repair_lobachevsky.py "$TEXT" --stage 3
"$PY" "$OCR/3-postprocess/collapse-inline-display.py" "$TEXT"
"$PY" "$OCR/verify/verify-controls.py" "$TEXT"
"$PY" repair_lobachevsky.py "$TEXT" --stage 4
"$PY" "$OCR/verify/verify-controls.py" "$TEXT"
