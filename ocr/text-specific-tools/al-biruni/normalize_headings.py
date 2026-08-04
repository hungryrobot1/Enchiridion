#!/usr/bin/env python3
"""Normalize reader hierarchy and remove OCR-promoted running headings."""

from pathlib import Path


TEXT = Path("source/al-biruni-india-ii.md")


def main() -> None:
    lines = TEXT.read_text(encoding="utf-8").splitlines()
    assert sum(line == "# ALBERUNI'S INDIA." for line in lines) == 3
    assert sum(line == "# ALBERÛNÌ'S INDIA." for line in lines) == 1
    assert sum(line == "# ANNOTATIONS." for line in lines) == 4
    assert sum(line.startswith("# CHAPTER ") for line in lines) == 31

    out: list[str] = []
    title_seen = False
    annotations_seen = 0
    body = True
    removed = 0
    promoted = 0
    demoted = 0

    for line in lines:
        if line in {"# ALBERUNI'S INDIA.", "# ALBERÛNÌ'S INDIA."}:
            if not title_seen:
                out.append("# ALBERUNI'S INDIA.")
                title_seen = True
            else:
                removed += 1
            continue

        if line == "# ANNOTATIONS.":
            annotations_seen += 1
            # Occurrences 2 and 4 are OCR-promoted running headers. The
            # first opens vol. I notes; the third opens vol. II notes.
            if annotations_seen in {2, 4}:
                removed += 1
                continue
            body = False
            out.append(line)
            continue

        if body and line.startswith("# CHAPTER "):
            if line == "# CHAPTER I.":
                # PDF leaf 16, printed p. 15, reads CHAPTER L.
                line = "# CHAPTER L."
            out.append("#" + line)
            demoted += 1
            continue

        if body and line.startswith("## ") and not line.startswith("## CHAPTER "):
            out.append("#" + line)
            promoted += 1
            continue

        out.append(line)

    assert (removed, demoted, promoted) == (5, 31, 28)
    TEXT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("removed 5 running headings; normalized 31 chapters and 28 body subheads")


if __name__ == "__main__":
    main()
