#!/bin/sh
set -eu

if [ "$#" -ne 2 ]; then
    echo "usage: $0 SOURCE.md OUTPUT.md" >&2
    exit 2
fi

SOURCE_MD=$1
OUTPUT_MD=$2
REPO_ROOT=/Users/zacharygrunenberg/Projects/Enchiridion
PYTHON_BIN=$REPO_ROOT/ocr/.venv/bin/python3

python3 repair_cantor.py apparatus "$OUTPUT_MD" --source "$SOURCE_MD"
python3 repair_cantor.py furniture "$OUTPUT_MD"

python3 "$REPO_ROOT/ocr/3-postprocess/rejoin-split-paragraphs.py" \
    "$OUTPUT_MD" --rule --min-words 4 --apply
python3 - "$OUTPUT_MD" <<'PY'
from pathlib import Path
import sys
count = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines().count("---")
assert count == 63, f"expected 63 unrejoined page rules, found {count}"
PY

python3 repair_cantor.py notation "$OUTPUT_MD"
python3 repair_cantor.py structure "$OUTPUT_MD"
python3 "$REPO_ROOT/ocr/3-postprocess/join-line-wrap-hyphens.py" "$OUTPUT_MD" --apply
python3 repair_cantor.py finishing "$OUTPUT_MD"
python3 repair_cantor.py pagination "$OUTPUT_MD"

"$PYTHON_BIN" "$REPO_ROOT/ocr/verify/lint-math.py" "$OUTPUT_MD"
node "$REPO_ROOT/ocr/verify/check-math.js" "$OUTPUT_MD"
node "$REPO_ROOT/ocr/verify/check-raw-latex.js" "$OUTPUT_MD"
