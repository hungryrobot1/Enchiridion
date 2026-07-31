#!/bin/bash
# Convert EPUB files to PDF using Calibre's ebook-convert
#
# Usage:
#   ./convert-epub-to-pdf.sh <input.epub>              # convert a single file
#   ./convert-epub-to-pdf.sh --all                     # convert all EPUBs in texts/
#
# Requirements:
#   - Calibre (brew install --cask calibre)
#   - ebook-convert must be in PATH (symlinked from Calibre.app)
#
# Output: PDF file in the same directory as the input EPUB

set -euo pipefail

TEXTS_DIR="$(cd "$(dirname "$0")/../texts" && pwd)"

convert_one() {
  local epub="$1"
  local dir="$(dirname "$epub")"
  local base="$(basename "$epub" .epub)"
  local pdf="$dir/$base.pdf"

  if [ -f "$pdf" ]; then
    echo "  SKIP  $epub (PDF already exists)"
    return
  fi

  echo "  CONVERT  $epub"
  ebook-convert "$epub" "$pdf" \
    --pdf-page-margin-top 72 \
    --pdf-page-margin-bottom 72 \
    --pdf-page-margin-left 72 \
    --pdf-page-margin-right 72 \
    --pdf-serif-family "Times New Roman" \
    --pdf-default-font-size 12 \
    --paper-size letter \
    --pdf-page-numbers \
    > /dev/null 2>&1

  if [ -f "$pdf" ]; then
    echo "  OK     $pdf"
  else
    echo "  FAIL   $epub" >&2
    return 1
  fi
}

if ! command -v ebook-convert &>/dev/null; then
  echo "Error: ebook-convert not found."
  echo ""
  echo "Install Calibre:"
  echo "  brew install --cask calibre"
  echo ""
  echo "Then symlink ebook-convert into PATH:"
  echo "  sudo ln -s /Applications/calibre.app/Contents/MacOS/ebook-convert /usr/local/bin/ebook-convert"
  exit 1
fi

if [ "${1:-}" = "--all" ]; then
  echo "Converting all EPUBs in $TEXTS_DIR..."
  count=0
  fail=0
  while IFS= read -r epub; do
    if convert_one "$epub"; then
      ((count++))
    else
      ((fail++))
    fi
  done < <(find "$TEXTS_DIR" -name "*.epub" -type f | sort)
  echo ""
  echo "Done. Converted: $count, Failed: $fail"
else
  if [ $# -lt 1 ]; then
    echo "Usage: $0 <input.epub> | --all"
    exit 1
  fi
  convert_one "$1"
fi
