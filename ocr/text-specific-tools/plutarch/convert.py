#!/usr/bin/env python3
"""Convert Plutarch's Lives (Dryden, rev. Clough) to markdown.

Source: Project Gutenberg #674, the Dryden translation as corrected and
revised by Arthur Hugh Clough, from the sibling EPUB (`pg674-images-3.epub`).
Clean structured XHTML — one file per Life and per Comparison, PG boilerplate
isolated in the first two and last files — so we extract from it directly (the
Frontinus/Tacitus/Thucydides HTML-convert pattern).

Structure the source gives us:
  - 68 sections (files 2..69): 46 Lives interleaved with their 22 surviving
    Comparisons (synkriseis), each a `<h2>NAME</h2>` followed by flat prose.
    Dryden's is continuous prose — NO numbered sections (so the Life itself is
    the citable unit, matching how these are recommended: whole).
  - occasional `<p class="poem">` verse quotation (with `<br/>` line breaks) ->
    blockquoted hardbreak verse, the reader's `breaks:false` convention.
  - `noindent` is a paragraph style, not structure -> ordinary paragraph.
  - zero footnotes in the edition.
  - NB: Alexander (file 48) and Caesar (file 49) have no Comparison between
    them — no synkrisis for that pair survives; Plutarch pairs them in
    Alexander's own opening sentence instead.

Outputs (this one script):
  1. the whole volume `plutarch-lives.md` — every Life/Comparison as a '# '
     section (68 h1s give the lazy reader per-Life parsing on a ~1M-word file);
  2. three standalone single-Life texts for the Grand Tour — Marcellus (23),
     Alexander (48), Caesar (49) — each its own text dir + metadata, the
     Heath-Archimedes split pattern. The Comparisons are volume-only (each
     references a Life we don't ship standalone).

Apparatus policy: drop PG front matter (files 0-1) and license (70); keep the
text and the Life/Comparison headings; strip the transcription's 'THE END'.

Validation (hard asserts): exactly 68 volume sections; each split yields
exactly one Life with the expected name.

--apply writes all four files + split metadata; else scratchpad review copies.
"""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path

import lxml.html

ROOT = Path("/Users/zacharygrunenberg/Projects/Enchiridion")
BASE = ROOT / "texts/2-rome-late-antiquity/plutarch-lives"
EPUB = BASE / "pg674-images-3.epub"
OUT_MD = BASE / "plutarch-lives.md"
SCRATCH = Path("/private/tmp/claude-501/-Users-zacharygrunenberg-Projects-"
               "Enchiridion/20baf1b8-79d2-483b-a98f-3c6fdfda67ae/scratchpad")
VOLUME_TITLE = "PLUTARCH'S LIVES"

# file index -> (standalone text-id, life title, one-line description)
SPLITS = {
    23: ("plutarch-marcellus", "Marcellus",
         "Life of the Roman general Marcus Claudius Marcellus, conqueror of "
         "Syracuse — at whose sack Archimedes was killed"),
    48: ("plutarch-alexander", "Alexander",
         "Life of Alexander the Great, pupil of Aristotle and conqueror of the "
         "Persian empire — paired by Plutarch with Caesar"),
    49: ("plutarch-caesar", "Caesar",
         "Life of Gaius Julius Caesar, from his rise under Sylla to the Ides "
         "of March — paired by Plutarch with Alexander"),
}

report: list[str] = []


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def epub_files() -> dict[int, bytes]:
    zf = zipfile.ZipFile(EPUB)
    out = {}
    for info in zf.namelist():
        m = re.search(r"674-h-(\d+)\.htm", info)
        if m:
            out[int(m.group(1))] = zf.read(info)
    return out


def render_poem(el) -> str:
    html = lxml.html.tostring(el, encoding="unicode")
    inner = re.sub(r"</?p[^>]*>", "", html)
    lines = [norm(re.sub(r"<[^>]+>", "", ln)) for ln in re.split(r"<br\s*/?>", inner)]
    return "\n".join(f"> {ln}  " for ln in lines if ln)


def render_file(raw: bytes, heading_level: str) -> tuple[str, str]:
    """Render one Life/Comparison file. Returns (section_name, markdown)."""
    root = lxml.html.fromstring(raw)
    name = None
    body: list[str] = []
    for el in root.iter("h2", "p"):
        if el.tag == "h2":
            name = norm(el.text_content())
            body.append(f"{heading_level} {name}")
        elif (el.get("class") or "") == "poem":
            body.append(render_poem(el))
        else:
            t = norm(el.text_content())
            if t and t != "THE END":
                body.append(t)
    assert name, "file with no h2 heading"
    return name, "\n\n".join(body)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    files = epub_files()

    # ── whole volume: files 2..69 as '# ' sections ───────────────────────
    sections = [f"# {VOLUME_TITLE}"]
    names = []
    for i in range(2, 70):
        name, md = render_file(files[i], "#")
        sections.append(md)
        names.append(name)
    assert len(names) == 68, f"expected 68 sections, got {len(names)}"
    volume = "\n\n".join(sections) + "\n"
    report.append(f"volume: {len(names)} sections, {len(volume.split())} words")

    # ── three standalone Lives: single-h1 texts ──────────────────────────
    splits_md = {}
    for idx, (tid, title, _desc) in SPLITS.items():
        name, md = render_file(files[idx], "#")
        assert name.upper() == title.upper(), f"{tid}: got {name!r} not {title!r}"
        splits_md[tid] = md + "\n"
        report.append(f"split {tid}: {len(md.split())} words")

    print("\n".join(report))

    SCRATCH.mkdir(parents=True, exist_ok=True)
    (SCRATCH / "plutarch-lives-review.md").write_text(volume)
    for tid, md in splits_md.items():
        (SCRATCH / f"{tid}-review.md").write_text(md)
    print(f"review copies in {SCRATCH}")

    if args.apply:
        OUT_MD.write_text(volume)
        print(f"wrote {OUT_MD}")
        for idx, (tid, title, desc) in SPLITS.items():
            d = ROOT / "texts/2-rome-late-antiquity" / tid
            d.mkdir(exist_ok=True)
            (d / f"{tid}.md").write_text(splits_md[tid])
            meta = {
                "title": f"Life of {title}",
                "author": "Plutarch",
                "translator": "John Dryden, revised by Arthur Hugh Clough",
                "year_written": "~100",
                "year_translated": 1859,
                "language": "English",
                "original_language": "Greek",
                "format": "markdown",
                "filename": f"{tid}.md",
                "description": desc,
                "topics": ["history", "biography"],
                "era": "rome-late-antiquity",
                "prerequisites": [],
                "ocr_status": "complete",
            }
            (d / "metadata.json").write_text(
                json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
            print(f"wrote {d}/ ({tid}.md + metadata.json)")
    return 0


if __name__ == "__main__":
    main()
