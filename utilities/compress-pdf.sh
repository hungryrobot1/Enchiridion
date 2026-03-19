#!/bin/bash
# Compress PDF files using Ghostscript
#
# Usage:
#   ./compress-pdf.sh <input.pdf>                      # compress a single file (in-place)
#   ./compress-pdf.sh --all                            # compress all PDFs in texts/
#
# Requirements:
#   - Ghostscript (brew install ghostscript)
#
# Uses /screen quality (72 dpi images) for aggressive compression.
# Original files are replaced with compressed versions.

set -euo pipefail

TEXTS_DIR="$(cd "$(dirname "$0")/../texts" && pwd)"

compress_one() {
  local pdf="$1"
  local tmp="${pdf}.tmp"

  local size_before=$(stat -f%z "$pdf" 2>/dev/null || stat -c%s "$pdf" 2>/dev/null)

  gs -sDEVICE=pdfwrite \
    -dCompatibilityLevel=1.4 \
    -dPDFSETTINGS=/screen \
    -dNOPAUSE -dBATCH -dQUIET \
    -sOutputFile="$tmp" \
    "$pdf"

  if [ -f "$tmp" ]; then
    local size_after=$(stat -f%z "$tmp" 2>/dev/null || stat -c%s "$tmp" 2>/dev/null)

    if [ "$size_after" -lt "$size_before" ]; then
      mv "$tmp" "$pdf"
      local saved=$((size_before - size_after))
      local pct=$((saved * 100 / size_before))
      echo "  OK  $pdf  $(numfmt_kb $size_before) -> $(numfmt_kb $size_after) (-${pct}%)"
    else
      rm "$tmp"
      echo "  SKIP  $pdf  $(numfmt_kb $size_before) (compressed would be larger)"
    fi
  else
    echo "  FAIL  $pdf" >&2
    return 1
  fi
}

numfmt_kb() {
  local bytes=$1
  echo "$((bytes / 1024))KB"
}

if ! command -v gs &>/dev/null; then
  echo "Error: Ghostscript (gs) not found."
  echo "Install: brew install ghostscript"
  exit 1
fi

if [ "${1:-}" = "--all" ]; then
  echo "Compressing all PDFs in $TEXTS_DIR..."
  count=0
  fail=0
  while IFS= read -r pdf; do
    if compress_one "$pdf"; then
      ((count++))
    else
      ((fail++))
    fi
  done < <(find "$TEXTS_DIR" -name "*.pdf" -type f | sort)
  echo ""
  echo "Done. Compressed: $count, Failed: $fail"
else
  if [ $# -lt 1 ]; then
    echo "Usage: $0 <input.pdf> | --all"
    exit 1
  fi
  compress_one "$1"
fi
