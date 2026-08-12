#!/bin/sh
set -eu

# Build the OCR input from the supplied 1914 scan.  PDF leaves are 1-indexed.
# Keep Galileo's authorial dedication (21-22) and the complete translated
# dialogue (31-324).  The latter ends with the Fourth Day; leaf 325 is an
# editorial notice that the edition omits Galileo's appendix.

source_pdf="source/cu31924012322701.pdf"
output_dir="prepared/galileo-two-new-sciences"
output_pdf="$output_dir/galileo-two-new-sciences-prepared.pdf"

source_pages=$(qpdf --show-npages "$source_pdf")
test "$source_pages" -eq 340 || {
    echo "expected 340 source pages, found $source_pages" >&2
    exit 1
}

mkdir -p "$output_dir"
mkdir -p raw
qpdf "$source_pdf" --pages . 21-22 . 31-324 -- "$output_pdf"

prepared_pages=$(qpdf --show-npages "$output_pdf")
test "$prepared_pages" -eq 296 || {
    echo "expected 296 prepared pages, found $prepared_pages" >&2
    exit 1
}

echo "prepared $output_pdf ($prepared_pages pages: source 21-22, 31-324)"
