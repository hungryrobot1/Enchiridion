#!/bin/sh
set -eu

OCR_ROOT=/Users/zacharygrunenberg/Projects/Enchiridion/ocr
"$OCR_ROOT/.venv/bin/python3" prepare_euler.py
"$OCR_ROOT/.venv/bin/python3" "$OCR_ROOT/1-prepare/check-duplicate-leaves.py" \
  prepared/euler-elements-of-algebra/euler-elements-of-algebra-ocr-ready.pdf \
  --expected-pages 462 --positive-page 2
"$OCR_ROOT/.venv/bin/python3" build_euler.py
"$OCR_ROOT/.venv/bin/python3" "$OCR_ROOT/3-postprocess/collapse-inline-display.py" \
  --max-len 1000 euler-elements-of-algebra.md > collapse-report.txt
tail -n 1 collapse-report.txt
"$OCR_ROOT/.venv/bin/python3" finalize_euler.py
"$OCR_ROOT/.venv/bin/python3" "$OCR_ROOT/verify/verify-controls.py" \
  euler-elements-of-algebra.md
