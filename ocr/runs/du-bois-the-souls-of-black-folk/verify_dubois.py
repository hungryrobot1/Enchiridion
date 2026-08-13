#!/usr/bin/env python3
"""Independent conservation checks for the Du Bois build; never edits."""
from pathlib import Path
import re

import pymupdf

PDF = Path("source/DuBois-split.pdf")
MARKDOWN = Path("du-bois-the-souls-of-black-folk.md")
IMAGES = Path("images")


def words(text: str) -> list[str]:
    text = text.translate(str.maketrans({"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff"}))
    return re.findall(r"[a-z0-9]+", text.casefold())


def main() -> None:
    doc = pymupdf.open(PDF)
    assert doc.page_count == 178
    md = MARKDOWN.read_text()
    md_stream = " ".join(words(md))

    assert "BURGHARDT AND YOLANDE" in md
    assert "HEREIN IS WRITTEN" not in md  # edition contents page intentionally removed
    checked = 0
    for pno, page in enumerate(doc, 1):
        if pno in (1, 2, 5, 6):
            continue  # normalized title/dedication; edition contents; blank leaf
        candidates: list[list[str]] = []
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                if line["bbox"][1] < 48:  # running head / folio
                    continue
                token_line = words("".join(s["text"] for s in line["spans"]))
                if len(token_line) >= 5:
                    candidates.append(token_line)
        if not candidates:
            raise AssertionError(f"work page {pno} has no five-token text line")
        # At least one of the three longest lines from every evidence-bearing
        # page must survive as an exact normalized phrase in the final text.
        anchors = sorted(candidates, key=len, reverse=True)[:3]
        assert any(" ".join(a) in md_stream for a in anchors), (
            f"page {pno} has no conserved long-line anchor: {anchors}"
        )
        checked += 1

    refs = re.findall(r"\(images/(music-p\d{3}\.png)\)", md)
    files = sorted(p.name for p in IMAGES.glob("music-p*.png"))
    assert len(refs) == len(set(refs)) == 19
    assert sorted(refs) == files
    assert len(re.findall(r"^# [IVX]+\. ", md, re.M)) == 14
    assert md.startswith("# THE SOULS OF BLACK FOLK\n")
    assert md.rstrip().endswith("THE END")
    assert "APPENDIX I" not in md and "EXPLANATORY NOTES" not in md
    print(
        f"PASS: {checked} work pages have conserved text anchors; four declared "
        "title/dedication/contents/blank leaves handled separately; 14 chapters; 19 unique "
        "music references exactly match 19 files"
    )


if __name__ == "__main__":
    main()
