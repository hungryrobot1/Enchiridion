#!/bin/sh
set -eu

workspace_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
raw="$workspace_dir/prepared/napier-construction-of-the-wonderful-canon-of-logarithms/napier-construction-of-the-wonderful-canon-of-logarithms.md"
final="$workspace_dir/napier-construction-of-the-wonderful-canon-of-logarithms.md"
python_bin=/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3
ocr_root=/Users/zacharygrunenberg/Projects/Enchiridion/ocr

"$python_bin" "$workspace_dir/build_napier.py" "$raw" "$final"
"$python_bin" "$ocr_root/3-postprocess/join-line-wrap-hyphens.py" "$final" --apply
"$python_bin" "$workspace_dir/verify_napier.py" "$final"
"$python_bin" "$ocr_root/verify/verify-controls.py" "$final"
