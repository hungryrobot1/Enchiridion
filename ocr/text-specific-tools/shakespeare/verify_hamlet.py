#!/usr/bin/env python3
"""Read-only structural verification for this Hamlet derivation."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown", type=Path)
    parser.add_argument("toc", type=Path)
    args = parser.parse_args()

    text = args.markdown.read_text(encoding="utf-8")
    toc = json.loads(args.toc.read_text(encoding="utf-8"))
    headings = re.findall(r"^(#{1,6}) (.+)$", text, re.MULTILINE)
    heading_titles = [title for _, title in headings]

    assert heading_titles[0] == "THE TRAGEDY OF HAMLET, PRINCE OF DENMARK"
    assert sum(level == "#" for level, _ in headings) == 6  # title + five acts
    assert sum(level == "##" for level, _ in headings) == 22  # cast, setting, 20 scenes
    assert text.count("**CLAUDIUS:**") == 102
    assert text.count("**GERTRUDE:**") == 69
    assert len(re.findall(r"^\*\*[A-Z][A-Z ]+:\*\*", text, re.MULTILINE)) == 1137
    assert "\x00" not in text
    assert "Project Gutenberg" not in text
    assert "Transcriber’s Notes" not in text
    assert 'href="#' not in text
    assert not re.search(r"&(?:amp|lt|gt|quot|apos|#\d+|#x[0-9A-Fa-f]+);", text)
    assert text.count("```") == 0

    toc_titles = [section["title"] for section in toc["sections"]]
    assert toc["title"] == "Hamlet"
    assert toc_titles == heading_titles[1:], "ToC does not exactly mirror document headings"

    # Known verse and prose controls prove the local line-shape assertions can
    # distinguish both cases instead of treating a zero as evidence.
    verse = "**HAMLET:** To be, or not to be, that is the question:  \nWhether ’tis nobler"
    prose = "**HAMLET:** Get thee to a nunnery. Why wouldst thou be a breeder of sinners?"
    assert verse in text, "known verse hard break was lost"
    assert prose in text, "known prose control was lost"
    assert "sinners?  \nI am myself" not in text, "prose was falsely line-broken"

    print(
        f"ok: {len(text.split()):,} words; {len(headings)} headings; "
        "1,137 speaker tags; mixed verse/prose controls pass"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
