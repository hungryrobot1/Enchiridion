#!/usr/bin/env python3
"""Prepare the complete 1903 work from the supplied 2007 Oxford edition.

Keeps PDF pages 38--215 inclusive: the work's title leaf through its
After-Thought. Removes Oxford's introduction, note on the text, bibliography,
chronology, three appended separately published Du Bois pieces, and explanatory
notes. Boundary text and counts are asserted before the deterministic split.
"""
from pathlib import Path
import subprocess

import pymupdf

SOURCE = Path("source/DuBois.pdf")
OUTPUT = Path("source/DuBois-split.pdf")
FIRST = 38
LAST = 215
EXPECTED_SOURCE_PAGES = 260
EXPECTED_KEPT_PAGES = 178


def main() -> None:
    doc = pymupdf.open(SOURCE)
    assert doc.page_count == EXPECTED_SOURCE_PAGES
    assert "THE SOULS\nOF BLACK FOLK" in doc[FIRST - 1].get_text()
    assert "THE AFTER-THOUGHT" in doc[LAST - 1].get_text()
    assert "APPENDIX I" in doc[LAST].get_text()
    assert LAST - FIRST + 1 == EXPECTED_KEPT_PAGES
    subprocess.run(
        ["qpdf", str(SOURCE), "--pages", ".", f"{FIRST}-{LAST}", "--", str(OUTPUT)],
        check=True,
    )
    prepared = pymupdf.open(OUTPUT)
    assert prepared.page_count == EXPECTED_KEPT_PAGES
    assert "THE SOULS\nOF BLACK FOLK" in prepared[0].get_text()
    assert "THE AFTER-THOUGHT" in prepared[-1].get_text()
    print(
        f"wrote {OUTPUT}: {prepared.page_count} pages; kept source PDF "
        f"{FIRST}-{LAST}, dropped 1-{FIRST-1} and {LAST+1}-{doc.page_count}"
    )


if __name__ == "__main__":
    main()
