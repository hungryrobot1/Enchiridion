#!/usr/bin/env python3
"""Source-specific acceptance assertions for the Bayes transcription."""

from pathlib import Path
import re


RAW = Path("source/raw.md")
FINAL = Path("bayes-essay-towards-solving-a-problem-in-doctrine-of-chances.md")


def main() -> None:
    raw = RAW.read_text(encoding="utf-8")
    pages = raw.split("\n\n---\n\n")
    assert len(pages) == 49, f"expected 49 OCR page blocks, found {len(pages)}"
    assert min(map(len, pages)) >= 200, "unexpected thin OCR page block"

    text = FINAL.read_text(encoding="utf-8")
    assert text.startswith("# AN ESSAY TOWARDS SOLVING A PROBLEM IN THE DOCTRINE OF CHANCES\n")
    assert text.count("## RICHARD PRICE — COVERING LETTER") == 1
    assert text.count("## THOMAS BAYES — ESSAY") == 1
    assert text.count("## RICHARD PRICE — APPENDIX") == 1
    assert "\n\n---\n\n" not in text
    assert not re.search(r"<a\s|href=|id=", text, re.I), "in-page link markup survived"

    refs = re.findall(r"!\[[^]]*\]\((images/[^)]+)\)", text)
    assert refs == ["images/img-0.jpeg", "images/img-1.jpeg"], refs
    for ref in refs:
        assert Path(ref).is_file(), f"missing image: {ref}"

    furniture = re.compile(r"^(?:# \[|VOL\. LIII|Hhh|F f f|G g g|Eee|\d+$)", re.M)
    assert not furniture.search(text), "page furniture survived"
    print(
        f"source-specific checks clean: {len(pages)} page blocks, "
        f"{len(text):,} output chars, {len(refs)} images, attributed voices"
    )


if __name__ == "__main__":
    main()
