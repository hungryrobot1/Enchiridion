#!/bin/sh
set -eu

PY=/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3
OCR=/Users/zacharygrunenberg/Projects/Enchiridion/ocr
TEXT=bayes-essay-towards-solving-a-problem-in-doctrine-of-chances.md

"$PY" prepare_bayes.py
"$PY" build_bayes.py
"$PY" verify_bayes.py
"$PY" "$OCR/verify/verify-controls.py" "$TEXT"
"$PY" "$OCR/verify/math-vocab-census.py" "$TEXT" > math-vocab.txt
