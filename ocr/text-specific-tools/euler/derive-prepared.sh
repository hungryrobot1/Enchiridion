#!/bin/sh
set -eu

OCR_ROOT=/Users/zacharygrunenberg/Projects/Enchiridion/ocr
"$OCR_ROOT/.venv/bin/python3" prepare_euler.py
"$OCR_ROOT/.venv/bin/python3" "$OCR_ROOT/1-prepare/check-duplicate-leaves.py" \
  prepared/euler-elements-of-algebra/euler-elements-of-algebra-ocr-ready.pdf \
  --expected-pages 462 --positive-page 2
