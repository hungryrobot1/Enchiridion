#!/bin/bash
# Update metadata.json files after EPUB-to-PDF conversion
#
# For each text directory that contains both an EPUB and a converted PDF:
#   - Updates "format" from "epub" to "pdf"
#   - Updates "filename" to the new PDF filename
#
# Usage:
#   ./update-metadata-after-conversion.sh              # dry run (shows changes)
#   ./update-metadata-after-conversion.sh --apply      # apply changes

set -euo pipefail

TEXTS_DIR="$(cd "$(dirname "$0")/../texts" && pwd)"
DRY_RUN=true

if [ "${1:-}" = "--apply" ]; then
  DRY_RUN=false
fi

count=0

while IFS= read -r metadata; do
  dir="$(dirname "$metadata")"

  # Check if metadata says format is epub
  current_format=$(python3 -c "import json; print(json.load(open('$metadata'))['format'])" 2>/dev/null || echo "")
  if [ "$current_format" != "epub" ]; then
    continue
  fi

  current_filename=$(python3 -c "import json; print(json.load(open('$metadata'))['filename'])" 2>/dev/null || echo "")
  pdf_filename="${current_filename%.epub}.pdf"

  # Check if the converted PDF exists
  if [ ! -f "$dir/$pdf_filename" ]; then
    echo "  SKIP  $metadata (no PDF found: $pdf_filename)"
    continue
  fi

  if $DRY_RUN; then
    echo "  WOULD UPDATE  $metadata"
    echo "    format: epub -> pdf"
    echo "    filename: $current_filename -> $pdf_filename"
  else
    python3 -c "
import json
with open('$metadata', 'r') as f:
    data = json.load(f)
data['format'] = 'pdf'
data['filename'] = '$pdf_filename'
with open('$metadata', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')
"
    echo "  UPDATED  $metadata"
  fi
  ((count++))

done < <(find "$TEXTS_DIR" -name "metadata.json" -type f | sort)

echo ""
if $DRY_RUN; then
  echo "Dry run complete. $count files would be updated."
  echo "Run with --apply to make changes."
else
  echo "Done. Updated $count metadata files."
fi
