#!/usr/bin/env python3
"""Stage-3 repair for Rosen's 1831 translation of al-Khwarizmi.

The supplied markdown is the library's existing IA/Mistral transcription, not
an extraction input.  This script narrows that transcription to the English
authorial text and removes only mechanically identified edition apparatus:

* everything before ``THE AUTHOR'S PREFACE`` and from ``NOTES`` onward;
* Rosen's marker-led editorial footnotes, page by page, and their body calls;
* printed page numbers, Arabic-text marginal page references, printer's
  signatures, one Google scan stamp, and scan page separators;
* one stray code fence which hid most of the work from the markdown renderer;
* two OCR-made approximations of printed diagrams on pp. 15 and 85.

The separate ``extract_figures.py`` recreates the 18 diagram files referenced
here from printed pp. 15-16, 18, 20, 32-33, 75-85.  The Arabic original after the
English and Rosen's preface/endnotes are excluded under ocr/README.md's
pedagogical apparatus and bilingual-edition policies.

Every destructive class has an exact count.  A changed upstream transcription
causes refusal instead of a plausible-looking partial repair.

Usage:
    python3 repair_al_khwarizmi.py                 # dry run
    python3 repair_al_khwarizmi.py --preview PATH  # write disposable preview
    python3 repair_al_khwarizmi.py --apply         # replace source markdown
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TEXT = ROOT / "source/al-khwarizmi-algebra.md"

START = "# THE AUTHOR'S PREFACE."
END = "\n# NOTES."
TITLE = "# THE ALGEBRA OF MOHAMMED BEN MUSA."
PAGE_BREAK = "\n\n---\n\n"

FOOT_LEAD = re.compile(r"^(?:[*†‡§∥¶]\s|\|\s*[*†‡§∥¶]\s)")
SPACED_PAGE = re.compile(r"(?m)^\(\s*\d{1,3}\s*\)$")
MARGIN_PAGE = re.compile(r"\(\d{1,3}\)")

SIGNATURES = [
    "B", "C", "D", "E", "F", "G", "H", "I", "K.", "L", "M", "N",
    "o", "P", "R", "T", "U", "x", "y",
]

STRAY_FENCE = "```\n* 10² = x² × 2½"
ASCII_FIGURE = "```\n10     10\n6     6\n3½    4½    3¾\n```"
TABLE_FIGURE = "| D | G |\n| --- | --- |\n| C | A |\n| B | K |\n| T | H |"

# Editorial footnotes which continue on a later printed page do not repeat
# their marker.  Each tuple is (raw segment index, first footer paragraph,
# asserted prefix).  These 26 runs were identified at the bottom of the page
# and checked against the printed layout; they account for the markerless
# algebraic displays that otherwise survive a marker-led cut.
CONTINUED_FOOTERS = [
    (14, 4, "$$4 \\times"),
    (25, 5, "$$\n\\begin{aligned}"),
    (27, 5, "$$*(10 + x)"),
    (32, 7, "$$\n\\begin{aligned}"),
    (42, 4, "$$\n\\begin{array}"),
    (49, 5, "$$\n\\begin{array}"),
    (51, 3, "$$\n\\begin{aligned}"),
    (52, 2, "If $x$ is the price of the barley"),
    (56, 3, "$$\n\\begin{align*}"),
    (62, 0, "$$ \\left[ x -"),
    (69, 3, "$$\n\\begin{align*}"),
    (72, 4, "$$\n\\begin{aligned}"),
    (102, 2, "$$ \\frac{2}{3}"),
    (110, 2, "If she has bequeathed as much as the share"),
    (113, 2, "Let $x$ be the stranger's legacy"),
    (126, 2, "$$ \\frac{1 - x - y}"),
    (130, 2, "value of the son's share"),
    (137, 2, "the capital to be equal to 24 dirhems"),
    (146, 2, "$$\n\\begin{aligned}"),
    (156, 2, "$$ s - d - 2x"),
    (163, 2, "are to be taken for 1 given"),
    (166, 2, "Let $x$ be that which the master gives"),
    (177, 2, "Hence, according to the author"),
    (179, 2, "Hence, according to the author"),
    (194, 3, "But the reasons for reducing the question"),
    (198, 2, "It is arbitrary how he shall apportion"),
]


def require_count(text: str, needle: str, expected: int, label: str) -> None:
    found = text.count(needle)
    if found != expected:
        raise ValueError(f"{label}: expected {expected}, found {found}")


def strip_footnotes(segments: list[str]) -> tuple[list[str], int, int]:
    """Cut each marker-led editorial footer from its first paragraph onward."""
    out: list[str] = []
    hit_segments = 0
    dropped = 0
    continuation_map = {seg: (cut, prefix) for seg, cut, prefix in CONTINUED_FOOTERS}
    continuation_dropped = 0
    for seg_index, segment in enumerate(segments):
        paras = segment.split("\n\n")
        hits = [i for i, p in enumerate(paras) if FOOT_LEAD.match(p.strip())]
        if hits:
            hit_segments += 1
            cut = hits[0]
            dropped += len(paras) - cut
            paras = paras[:cut]
        if seg_index in continuation_map:
            cut, prefix = continuation_map[seg_index]
            if cut >= len(paras) or not paras[cut].startswith(prefix):
                got = paras[cut][:70] if cut < len(paras) else "<missing>"
                raise ValueError(
                    f"continued footer segment {seg_index}: expected "
                    f"{prefix!r}, found {got!r}"
                )
            continuation_dropped += len(paras) - cut
            paras = paras[:cut]
        cleaned = "\n\n".join(paras).strip()
        if cleaned:
            out.append(cleaned)
    if (hit_segments, dropped) != (114, 401):
        raise ValueError(
            "editorial footnotes: expected 114 segments / 401 paragraphs, "
            f"found {hit_segments} / {dropped}"
        )
    if continuation_dropped != 108:
        raise ValueError(
            f"continued footnotes: expected 108 paragraphs, found "
            f"{continuation_dropped}"
        )
    return out, hit_segments, dropped


def strip_page_furniture(segment: str, counts: dict[str, int]) -> str:
    segment, n = SPACED_PAGE.subn("", segment)
    counts["printed page numbers"] += n
    segment, n = MARGIN_PAGE.subn("", segment)
    counts["Arabic marginal page references"] += n

    for sig in SIGNATURES:
        pattern = re.compile(rf"(?m)^{re.escape(sig)}$")
        segment, n = pattern.subn("", segment)
        counts["printer signatures"] += n

    segment, n = re.subn(r"(?m)^Digitized by Google$", "", segment)
    counts["scan stamps"] += n
    return re.sub(r"\n{3,}", "\n\n", segment).strip()


def structural(paragraph: str) -> bool:
    s = paragraph.lstrip()
    return s.startswith(("#", "![", "|", "```", "$$"))


def merge_segments(segments: list[str]) -> tuple[str, dict[str, int]]:
    """Join only across former scan boundaries, never within a source page."""
    joins = {"hyphen": 0, "lowercase": 0, "open punctuation": 0,
             "incomplete": 0, "kept": 0}
    paras: list[str] = []
    for segment in segments:
        incoming = [p for p in segment.split("\n\n") if p.strip()]
        if not incoming:
            continue
        if not paras:
            paras.extend(incoming)
            continue

        left = paras[-1].rstrip()
        right = incoming[0].lstrip()
        can_join = not structural(left) and not structural(right)
        kind = None
        glue = " "
        if can_join and left.endswith("-") and re.match(r"[a-z]", right):
            kind, glue = "hyphen", ""
            left = left[:-1]
        elif can_join and re.match(r"[a-z]", right):
            kind = "lowercase"
        elif can_join and left.endswith((",", ";", "—", "-", ":")):
            kind = "open punctuation"
        elif can_join and not re.search(r"[.!?…][\"'’”)]?$", left):
            kind = "incomplete"

        if kind:
            paras[-1] = left + glue + right
            incoming = incoming[1:]
            joins[kind] += 1
        else:
            joins["kept"] += 1
        paras.extend(incoming)
    return "\n\n".join(paras), joins


def strip_calls(text: str) -> tuple[str, dict[str, int]]:
    """Remove footnote calls while preserving real Markdown emphasis."""
    daggers = len(re.findall(r"[†‡§∥¶]", text))
    text = re.sub(r"[†‡§∥¶]", "", text)
    protected: list[str] = []

    def keep(match: re.Match[str]) -> str:
        protected.append(match.group(0))
        return f"\x00EM{len(protected) - 1}\x00"

    # Protect strong emphasis first, then ordinary emphasis.  A printed
    # footnote call is followed by whitespace/punctuation and cannot open one
    # of these spans.
    text = re.sub(r"\*\*[^*\n]+\*\*", keep, text)
    text = re.sub(r"(?<!\*)\*[^*\n\s][^*\n]*?\*(?!\*)", keep, text)
    stars = text.count("*")
    text = text.replace("*", "")
    text = re.sub(
        r"\x00EM(\d+)\x00", lambda m: protected[int(m.group(1))], text
    )
    return text, {"non-asterisk calls": daggers, "asterisk calls": stars}


def build(raw: str) -> tuple[str, dict[str, object]]:
    require_count(raw, START, 1, "authorial start anchor")
    require_count(raw, END, 1, "endnotes anchor")
    require_count(raw, STRAY_FENCE, 1, "stray code fence")
    require_count(raw, ASCII_FIGURE, 1, "p. 85 ASCII figure")
    require_count(raw, TABLE_FIGURE, 1, "p. 15 table figure")
    require_count(raw, "![img-", 33, "raw image references")
    require_count(raw, "Digitized by Google", 1, "embedded Google scan stamp")

    start = raw.index(START)
    end = raw.index(END, start)
    core = raw[start:end]
    if len(core.split(PAGE_BREAK)) != 200:
        raise ValueError("expected 200 scan-delimited English segments")
    if core.count("![img-") != 16:
        raise ValueError("expected 16 supplied figure references in English span")

    core = core.replace(STRAY_FENCE, "* 10² = x² × 2½")
    core = core.replace(TABLE_FIGURE, "![Figure on printed page 15](images/img-0.png)")
    core = core.replace(ASCII_FIGURE, "![Figure on printed page 85](images/img-17.png)")
    core = re.sub(
        r"!\[img-(\d+)\.jpeg\]\(images/img-\1\.jpeg\)",
        lambda m: f"![Figure from the printed edition](images/img-{int(m.group(1)) + 1}.png)",
        core,
    )

    segments, foot_segments, foot_paras = strip_footnotes(
        core.split(PAGE_BREAK)
    )
    counts = {
        "printed page numbers": 0,
        "Arabic marginal page references": 0,
        "printer signatures": 0,
        "scan stamps": 0,
    }
    segments = [strip_page_furniture(s, counts) for s in segments]
    segments = [s for s in segments if s]
    expected = {
        "printed page numbers": 175,
        "Arabic marginal page references": 77,
        "printer signatures": 5,
        "scan stamps": 0,
    }
    if counts != expected:
        raise ValueError(f"page furniture counts changed: {counts} != {expected}")

    core, joins = merge_segments(segments)

    # Printed pp. 169-170 (PDF 193-194): the page turn is "Com-" / "putation".
    # The OCR lost the first syllable with the footer; restore the witnessed
    # word by a unique post-merge anchor.
    seam = 'deducted?"* putation:'
    require_count(core, seam, 1, "printed pp. 169-170 Computation seam")
    core = core.replace(seam, 'deducted?" Computation:')

    core, calls = strip_calls(core)

    # Heading tiers: the work is >100 KB, so its four large divisions are h1
    # sections; the repeated headings inside ON LEGACIES are h2 subsections.
    # OCR decorated the same printed tier four different ways.
    heading_repairs = [
        ("Sixth Problem.", "## Sixth Problem.", 1),
        ("## Demonstrations. ", "## Demonstrations.", 1),
        ("# On another Species of Legacy.", "## On another Species of Legacy.", 1),
        ("# On another Species of Legacies.", "## On another Species of Legacies.", 1),
        ("On another Species of Legacies.", "## On another Species of Legacies.", 1),
        ("**On another Species of Legacies.**", "## On another Species of Legacies.", 1),
        ("On the Legacy with a Dirhem.", "## On the Legacy with a Dirhem.", 1),
        ("On Completement.", "## On Completement.", 1),
        ("**On Emancipation in Illness.**", "## On Emancipation in Illness.", 1),
        ("# On return of the Dowry.", "## On return of the Dowry.", 1),
        ("# On Surrender in Illness.", "## On Surrender in Illness.", 1),
    ]
    for old, new, expected_count in heading_repairs:
        pattern = re.compile(rf"(?m)^{re.escape(old)}$")
        core, found = pattern.subn(new, core)
        if found != expected_count:
            raise ValueError(
                f"heading {old}: expected {expected_count}, found {found}"
            )

    core = re.sub(r"[ \t]+([,.;:!?])", r"\1", core)
    core = re.sub(r"[ \t]{2,}", " ", core)
    core = re.sub(r"\n{3,}", "\n\n", core).strip()
    core = "\n\n".join(p.strip() for p in core.split("\n\n"))
    # One separator is adjacent to a removed footer in the raw stream and is
    # exposed only after the paragraph deletion, so it is not consumed by the
    # canonical blank-line page delimiter above.
    core, exposed_rules = re.subn(r"(?m)^---\n?", "", core)
    if exposed_rules != 1:
        raise ValueError(f"expected 1 exposed scan rule, found {exposed_rules}")
    result = TITLE + "\n\n" + core + "\n"

    if result.count("![") != 18:
        raise ValueError("expected exactly 18 authorial figure references")
    if re.search(r"(?m)^---$", result):
        lines = [i for i, line in enumerate(result.splitlines(), 1) if line == "---"]
        raise ValueError(f"scan page rule survived at result lines {lines}")
    if "Digitized by" in result or "# NOTES." in result:
        raise ValueError("edition/scan apparatus survived")
    if re.search(r"[†‡§∥¶]", result):
        survived = sorted(set(re.findall(r"[†‡§∥¶]", result)))
        raise ValueError(f"editorial footnote call survived: {survived}")
    if result.count("```") != 0:
        raise ValueError("stray code fence survived")

    report: dict[str, object] = {
        "source chars": len(raw),
        "result chars": len(result),
        "footnote segments": foot_segments,
        "footnote paragraphs": foot_paras,
        **counts,
        **calls,
        "page-seam joins": joins,
        "figures": result.count("!["),
    }
    return result, report


def main() -> int:
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--apply", action="store_true")
    group.add_argument("--preview", type=Path)
    args = ap.parse_args()

    raw = TEXT.read_text(encoding="utf-8")
    try:
        result, report = build(raw)
    except ValueError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1

    for key, value in report.items():
        print(f"{key}: {value}")
    if args.preview:
        args.preview.write_text(result, encoding="utf-8")
        print(f"preview written: {args.preview}")
    elif args.apply:
        TEXT.write_text(result, encoding="utf-8")
        print(f"written: {TEXT}")
    else:
        print("dry run: pass --apply to replace the markdown")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
