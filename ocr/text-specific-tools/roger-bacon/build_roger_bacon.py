#!/usr/bin/env python3
"""Build one reader-ready Opus Majus from Burke's two OCR intermediates.

This is an asserted, reproducible stage-3 transformation.  It:

* verifies the 425/412-page OCR shapes and both work boundaries;
* drops both binding half-titles and supplies one work title;
* removes page-position running heads (including fuzzy OCR variants), page
  separators, folios, and Burke editorial footnotes and markers;
* joins only page-boundary continuations licensed by internal syntax;
* normalizes Parts I-VII and their subordinate headings;
* namespaces and copies all 80 extracted images into one sibling directory.

It does not adjudicate ambiguous readings against a printed page.

Usage:
    ocr/.venv/bin/python3 build_roger_bacon.py
"""

from __future__ import annotations

import html
import re
import shutil
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VOLUME_1 = ROOT / "ocr-output" / "prepared.md"
VOLUME_2 = ROOT / "ocr-output-volume-2" / "prepared.md"
OUTPUT = ROOT / "roger-bacon-opus-majus.md"
IMAGE_OUTPUT = ROOT / "images"
PAGE_SEPARATOR = "\n\n---\n\n"

EXPECTED_PAGES = {1: 425, 2: 412}
EXPECTED_IMAGES = {1: 28, 2: 52}
EXPECTED_RUNNING_HEADERS = {1: 409, 2: 384}
EXPECTED_FOOTNOTE_BODIES = {1: 13, 2: 108}

RUNNING_HEADERS = (
    "opus majus",
    "causes of error",
    "philosophy",
    "study of tongues",
    "mathematics",
    "optical science",
    "experimental science",
    "moral philosophy",
)

PART_RE = re.compile(
    r"^PART\s+(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN)(?:\s+OF\s+THIS\s+PLEA)?$",
    re.I,
)
DISTINCTION_RE = re.compile(
    r"^(?:FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH|EIGHTH|NINTH|TENTH|LAST)\s+DISTINCTION$",
    re.I,
)
CHAPTER_RE = re.compile(r"^CHAPTER(?:\s+.+)?$", re.I)
SUBPART_RE = re.compile(
    r"^(?:SECOND PART OF PERSPECTIVE|PART THREE OF PERSPECTIVE|"
    r"MORAL PHILOSOPHY: (?:FIRST|SECOND|THIRD) PART|"
    r"FOURTH PART OF MORAL PHILOSOPHY)$",
    re.I,
)
OTHER_SECTION_RE = re.compile(
    r"^(?:THE APPLICATION OF MATHEMATICS TO SACRED SUBJECTS\.?|"
    r"EXPLANATION OF THE TABLE\.?|"
    r"CHAPTER ON THE (?:SECOND PREROGATIVE OF EXPERIMENTAL SCIENCE|"
    r"THIRD PREROGATIVE OR THE DIGNITY OF THE EXPERIMENTAL ART)|"
    r"Example [IVX]+)$",
    re.I,
)
BARE_FOLIO_RE = re.compile(r"^\[\s*\d{1,4}\s*\]$")
IMAGE_RE = re.compile(r"!\[([^]]*)\]\(images/(img-\d+\.jpeg)\)")


def canonical(value: str) -> str:
    value = re.sub(r"^#+\s*", "", value.strip()).casefold()
    return re.sub(r"[^a-z]+", " ", value).strip()


def is_running_header(line: str) -> bool:
    if not re.match(r"^#{1,3}\s+", line.strip()):
        return False
    candidate = canonical(line)
    if not candidate:
        return False
    return any(
        candidate == target
        or (
            len(candidate) >= 7
            and SequenceMatcher(None, candidate, target, autojunk=False).ratio() >= 0.78
        )
        for target in RUNNING_HEADERS
    )


def strip_first_running_header(page: str) -> tuple[str, str | None]:
    lines = page.splitlines()
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        if is_running_header(line):
            removed = line.strip()
            del lines[index]
            return "\n".join(lines).strip(), removed
        return page.strip(), None
    return "", None


def strip_editorial_footnotes(page: str) -> tuple[str, int]:
    lines = page.splitlines()
    kept: list[str] = []
    removed = 0
    for line in lines:
        # Mistral represents Burke's page-bottom editorial notes as `* `.
        # Italic section summaries are `*text*` with no space and stay.
        if line.startswith(("* ", "† ", "‡ ", "§ ", "|| ")) or re.match(
            r"^\\\((?:\\?dagger|\\?ddagger)\\\)\s+", line
        ):
            removed += 1
            continue
        kept.append(line)
    return "\n".join(kept).strip(), removed


EMPHASIS_RE = re.compile(r"(?<![\w\\])\*(?!\s)([^*\n]+?)(?<!\s)\*(?!\w)")


def strip_editorial_markers(text: str) -> tuple[str, Counter[str]]:
    """Remove footnote symbols without disturbing valid Markdown emphasis."""
    protected: list[str] = []

    def protect(match: re.Match[str]) -> str:
        protected.append(match.group(0))
        return f"\x00EMPH{len(protected)-1}\x00"

    text = EMPHASIS_RE.sub(protect, text)
    counts: Counter[str] = Counter()
    text, counts["escaped stars"] = re.subn(r"\\\*", "", text)
    text, counts["stars"] = re.subn(r"(?<!\*)\*(?!\*)", "", text)
    text, counts["daggers"] = re.subn("†", "", text)
    text, counts["double daggers"] = re.subn("‡", "", text)
    for index, value in enumerate(protected):
        text = text.replace(f"\x00EMPH{index}\x00", value)
    return text, counts


def rewrite_images(text: str, volume: int) -> tuple[str, int]:
    seen: set[str] = set()

    def replace(match: re.Match[str]) -> str:
        alt, name = match.groups()
        seen.add(name)
        return f"![{alt}](images/v{volume}-{name})"

    return IMAGE_RE.sub(replace, text), len(seen)


def structural_start(text: str) -> bool:
    s = text.lstrip()
    return (
        not s
        or s.startswith(("#", "![", "|", "$$", "```", "<", ">"))
        or bool(re.match(r"^(?:[-+*]|\d+[.)])\s", s))
    )


def boundary_join_kind(left: str, right: str) -> str | None:
    if not left.strip() or structural_start(right):
        return None
    last_line = left.rstrip().splitlines()[-1].rstrip()
    first_line = right.lstrip().splitlines()[0].lstrip()
    if structural_start(last_line) or not first_line:
        return None
    if last_line.endswith("-") and first_line[0].isalpha():
        return "hyphen"
    if last_line[-1] in ",(—–" or last_line[-1].isalnum():
        return "continuation"
    return None


def join_pages(pages: list[str]) -> tuple[str, Counter[str]]:
    out = ""
    counts: Counter[str] = Counter()
    for page in pages:
        page = page.strip()
        if not page:
            counts["blank pages"] += 1
            continue
        if not out:
            out = page
            continue
        kind = boundary_join_kind(out, page)
        if kind == "hyphen":
            out = out.rstrip()[:-1] + page.lstrip()
            counts[kind] += 1
        elif kind == "continuation":
            out = out.rstrip() + " " + page.lstrip()
            counts[kind] += 1
        else:
            out = out.rstrip() + "\n\n" + page.lstrip()
    return out, counts


def normalize_headings(text: str) -> tuple[str, Counter[str]]:
    out: list[str] = []
    counts: Counter[str] = Counter()
    distinction_active = False
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped.startswith("#"):
            out.append(raw)
            continue
        title = re.sub(r"^#+\s*", "", stripped).strip()
        if title == "THE OPUS MAJUS OF ROGER BACON":
            out.append(f"# {title}")
            counts["title"] += 1
        elif PART_RE.fullmatch(title):
            out.append(f"# {title}")
            distinction_active = False
            counts["parts"] += 1
        elif SUBPART_RE.fullmatch(title):
            out.append(f"## {title}")
            distinction_active = False
            counts["subparts"] += 1
        elif DISTINCTION_RE.fullmatch(title):
            out.append(f"## {title}")
            distinction_active = True
            counts["distinctions"] += 1
        elif CHAPTER_RE.fullmatch(title):
            level = "###" if distinction_active else "##"
            out.append(f"{level} {title}")
            counts["chapters"] += 1
        elif OTHER_SECTION_RE.fullmatch(title):
            out.append(f"## {title}")
            distinction_active = False
            counts["other sections"] += 1
        else:
            # Preserve uncommon OCR headings, but never let them create a new
            # lazy top-level section accidentally.
            old_level = len(stripped) - len(stripped.lstrip("#"))
            out.append(f"{'#' * max(2, old_level)} {title}")
            counts["preserved uncommon"] += 1
    return "\n".join(out), counts


def normalize_blanks(text: str) -> str:
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def apply_page_verified_repairs(text: str) -> tuple[str, list[str]]:
    """Apply only readings directly adjudicated against Burke's printed page."""
    repairs = [
        (
            "from $\\mathfrak{E}$ in Greek, which is sex in Latin",
            "from ἕξ in Greek, which is sex in Latin",
            "Volume I printed p.182 (source PDF p.204): printed Greek ἕξ, not fraktur E",
        ),
    ]
    report: list[str] = []
    for old, new, citation in repairs:
        count = text.count(old)
        if count != 1:
            raise AssertionError(
                f"page-verified repair anchor expected once, found {count}: {old!r}"
            )
        text = text.replace(old, new)
        report.append(citation)
    return text, report


def apply_internal_repairs(text: str) -> tuple[str, list[str]]:
    """Repair uniquely determined OCR/wrap damage using internal evidence."""
    repairs = [
        ("pas-\n\nsage", "passage"),
        ("con-\n\ntaining", "containing"),
        ("propo-\n\nsition", "proposition"),
        ("oppositio- nis", "oppositionis"),
        ("computa- tionem", "computationem"),
        ("differ-\n\nent", "different"),
        ("as-\n\nsign", "assign"),
        ("re-\n\nspect", "respect"),
        ("dif-\n\nference", "difference"),
        ("pyra-\n\nmid", "pyramid"),
        ("rea-\n\nson", "reason"),
        ("dis- please", "displease"),
        ("condemna- tion", "condemnation"),
        ("more ele-\n\nelevated than it", "more elevated than it"),
        (
            "angles of inci-\n\nincidence and reflection",
            "angles of incidence and reflection",
        ),
    ]
    report: list[str] = []
    for old, new in repairs:
        count = text.count(old)
        if count != 1:
            raise AssertionError(
                f"internal repair anchor expected once, found {count}: {old!r}"
            )
        text = text.replace(old, new)
        report.append(f"{old!r} -> {new!r}")
    return text, report


def copy_images() -> None:
    IMAGE_OUTPUT.mkdir(exist_ok=True)
    for volume, count in EXPECTED_IMAGES.items():
        source = ROOT / ("ocr-output" if volume == 1 else "ocr-output-volume-2") / "images"
        files = sorted(source.glob("img-*.jpeg"))
        if len(files) != count:
            raise AssertionError(
                f"Volume {volume}: expected {count} image files, found {len(files)}"
            )
        for path in files:
            shutil.copy2(path, IMAGE_OUTPUT / f"v{volume}-{path.name}")


def process_volume(path: Path, volume: int) -> tuple[str, dict[str, object]]:
    raw = path.read_text(encoding="utf-8")
    pages = raw.split(PAGE_SEPARATOR)
    if len(pages) != EXPECTED_PAGES[volume]:
        raise AssertionError(
            f"Volume {volume}: expected {EXPECTED_PAGES[volume]} OCR pages, found {len(pages)}"
        )
    if "THE OPUS MAJUS OF" not in pages[0] or "ROGER BACON" not in pages[0]:
        raise AssertionError(f"Volume {volume}: half-title anchor missing")
    if volume == 1:
        if "PART ONE" not in pages[1] or "unable to write more" not in pages[-1]:
            raise AssertionError("Volume I boundary anchor failed")
    else:
        if "PART FIVE OF THIS PLEA" not in pages[1] or "manuscript breaks off abruptly" not in pages[-1]:
            raise AssertionError("Volume II boundary anchor failed")

    # Both half-titles are binding furniture.  The final output supplies one
    # synthetic work title before the unified Part I-Part VII structure.
    pages = pages[1:]
    removed_headers: Counter[str] = Counter()
    footnote_bodies = 0
    cleaned: list[str] = []
    for page in pages:
        page, header = strip_first_running_header(page)
        if header:
            removed_headers[header] += 1
        page, removed = strip_editorial_footnotes(page)
        footnote_bodies += removed
        # A footer folio escaped OCR footer handling on one Volume-I leaf.
        page = "\n".join(
            line for line in page.splitlines() if not BARE_FOLIO_RE.fullmatch(line.strip())
        )
        cleaned.append(page)

    if sum(removed_headers.values()) != EXPECTED_RUNNING_HEADERS[volume]:
        raise AssertionError(
            f"Volume {volume}: expected {EXPECTED_RUNNING_HEADERS[volume]} running heads, "
            f"removed {sum(removed_headers.values())}: {dict(removed_headers)}"
        )
    if footnote_bodies != EXPECTED_FOOTNOTE_BODIES[volume]:
        raise AssertionError(
            f"Volume {volume}: expected {EXPECTED_FOOTNOTE_BODIES[volume]} footnote bodies, "
            f"removed {footnote_bodies}"
        )

    joined, joins = join_pages(cleaned)
    joined, image_refs = rewrite_images(joined, volume)
    if image_refs != EXPECTED_IMAGES[volume]:
        raise AssertionError(
            f"Volume {volume}: expected {EXPECTED_IMAGES[volume]} image refs, found {image_refs}"
        )
    return joined, {
        "headers": removed_headers,
        "footnote bodies": footnote_bodies,
        "joins": joins,
        "image refs": image_refs,
    }


def main() -> int:
    volume_1, report_1 = process_volume(VOLUME_1, 1)
    volume_2, report_2 = process_volume(VOLUME_2, 2)
    combined = "# THE OPUS MAJUS OF ROGER BACON\n\n" + volume_1 + "\n\n" + volume_2
    combined, marker_counts = strip_editorial_markers(combined)
    combined = html.unescape(combined)
    combined, heading_counts = normalize_headings(combined)
    combined, internal_repair_report = apply_internal_repairs(combined)
    combined, repair_report = apply_page_verified_repairs(combined)
    combined = normalize_blanks(combined)

    if combined.count("\n# PART ") != 7:
        raise AssertionError("unified text does not contain exactly Parts I-VII as top-level headings")
    if re.search(r"^---$", combined, re.M):
        raise AssertionError("page separator survived the join")
    if re.search(r"^# (?:Opus|Mathematics|Philosophy|Study|Causes|Optical|Experimental|Moral)", combined, re.M):
        raise AssertionError("running header survived as a top-level heading")
    final_image_refs = re.findall(
        r"!\[[^]]*\]\(images/v[12]-img-\d+\.jpeg\)", combined
    )
    if len(final_image_refs) != sum(EXPECTED_IMAGES.values()):
        raise AssertionError("image reference count changed")
    if not combined.rstrip().endswith("*Here the manuscript breaks off abruptly.*"):
        raise AssertionError("final manuscript-break statement was not preserved")

    copy_images()
    OUTPUT.write_text(combined, encoding="utf-8")

    for volume, report in ((1, report_1), (2, report_2)):
        print(f"Volume {volume}:")
        print(f"  running headers removed: {sum(report['headers'].values())}")
        for header, count in sorted(report["headers"].items()):
            print(f"    {count:3} {header}")
        print(f"  editorial footnote bodies removed: {report['footnote bodies']}")
        print(f"  page joins: {dict(report['joins'])}")
        print(f"  image references: {report['image refs']}")
    print(f"Editorial markers removed: {dict(marker_counts)}")
    print(f"Headings normalized: {dict(heading_counts)}")
    print(f"Internally licensed repairs: {len(internal_repair_report)}")
    for repair in internal_repair_report:
        print(f"  {repair}")
    for repair in repair_report:
        print(f"Page-verified repair: {repair}")
    print(f"Written {OUTPUT.name}: {len(combined):,} characters")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
