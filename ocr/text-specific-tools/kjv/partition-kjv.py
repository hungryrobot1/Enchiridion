#!/usr/bin/env python3
"""Partition the King James Bible with Apocrypha (DaVince Tools PDF, 2001/2004).

The PDF is text-native (built from the public-domain KJV text), so this is a
pure extraction — no OCR. The sibling kjv.txt (a lossier conversion of the same
PDF) serves as the reconciliation witness.

Geometry: two columns split at x=306; running heads ("Page N" + book name) live
in a header zone y<50 and are dropped positionally. Psalms (printed pp.309–394)
is the one book set single-column, one verse per line with hanging-indent
continuations; everything else is two-column wrapped prose whose blocks are
paragraphs.

Structure: Book = h1 (81 books; short canonical names, the edition's full title
line kept as an italic first body line). Chapter = h2, promoted at each {C:1}
verse marker (single-chapter books get no chapter heading). Psalms nests its
canonical fivefold division: Book I–V = h2, Psalm N = h3 (promoted from the
edition's own "Psalm N" lines; the "Book N" label is typeset BELOW the psalm
heading it precedes and is reordered above it). Verse markers {C:V} become bold
verse numbers (**V**); the chapter half is carried by the heading. KJV
supplied-word brackets ([was], [is]) are the translators' own and stay.

Apparatus stripped: both PDF prefaces, the ToC, running heads, and the
"The Apocrypha" / "New Testament" divider pages. The 1611 edition's own front
matter inside books (Susanna's headnote, Sirach's prologues, psalm
superscriptions) is text and stays.

Validation: verses must increment by 1 within a chapter, chapters by 1 within
a book, per-book chapter totals are checked against canonical counts, and any
brace surviving marker transformation is reported (a malformed marker).

Usage:
    python3 partition-kjv.py SOURCE.pdf OUT.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf

OFFSET = 20                    # printed page N = PDF index N + 20
HEADER_Y = 50                  # running-head zone
COL_X = 306                    # two-column split
MARKER_RE = re.compile(r"\{\s*(\d+)\s*:\s*(\d+)\s*\}")
PSALM_LINE_RE = re.compile(r"^Psalm (\d+)$")
PSBOOK_RE = re.compile(r"^Book ([IVX]+)$")

# (short name, printed start page, expected chapters or None to just report)
BOOKS = [
    ("Genesis", 1, 50), ("Exodus", 31, 40), ("Leviticus", 57, 27),
    ("Numbers", 77, 36), ("Deuteronomy", 103, 34), ("Joshua", 125, 24),
    ("Judges", 141, 21), ("Ruth", 157, 4), ("1 Samuel", 159, 31),
    ("2 Samuel", 179, 24), ("1 Kings", 195, 22), ("2 Kings", 215, 25),
    ("1 Chronicles", 233, 29), ("2 Chronicles", 251, 36), ("Ezra", 273, 10),
    ("Nehemiah", 279, 13), ("Esther", 289, 10), ("Job", 295, 42),
    ("Psalms", 309, 150), ("Proverbs", 395, 31), ("Ecclesiastes", 407, 12),
    ("Song of Solomon", 413, 8), ("Isaiah", 417, 66), ("Jeremiah", 447, 52),
    ("Lamentations", 479, 5), ("Ezekiel", 483, 48), ("Daniel", 513, 12),
    ("Hosea", 523, 14), ("Joel", 527, 3), ("Amos", 529, 9),
    ("Obadiah", 533, 1), ("Jonah", 535, 4), ("Micah", 537, 7),
    ("Nahum", 541, 3), ("Habakkuk", 543, 3), ("Zephaniah", 545, 3),
    ("Haggai", 547, 2), ("Zechariah", 549, 14), ("Malachi", 555, 4),
    # "Esther (Greek)" (printed 579–584) is EXCLUDED: word-for-word identical
    # to canonical Esther (5,804 words, zero diff hunks) — the PDF duplicated
    # the Hebrew Esther there instead of the Greek additions ("The Rest of
    # Esther"), which this source simply does not contain.
    ("Tobit", 559, 14), ("Judith", 567, 16),
    ("Wisdom", 585, 19), ("Sirach", 599, 51), ("Baruch", 635, 5),
    ("Letter of Jeremiah", 639, 1), ("Prayer of Azariah", 641, 1),
    ("Susanna", 643, 1), ("Bel and the Dragon", 645, 1),
    ("1 Maccabees", 647, 16), ("2 Maccabees", 675, 15),
    ("1 Esdras", 693, 9), ("2 Esdras", 707, 16),
    ("Prayer of Manasseh", 731, 1),
    ("Matthew", 733, 28), ("Mark", 753, 16), ("Luke", 765, 24),
    ("John", 785, 21), ("Acts", 801, 28), ("Romans", 821, 16),
    ("1 Corinthians", 829, 16), ("2 Corinthians", 837, 13),
    ("Galatians", 843, 6), ("Ephesians", 847, 6), ("Philippians", 851, 4),
    ("Colossians", 853, 4), ("1 Thessalonians", 855, 5),
    ("2 Thessalonians", 857, 3), ("1 Timothy", 859, 6), ("2 Timothy", 861, 4),
    ("Titus", 863, 3), ("Philemon", 865, 1), ("Hebrews", 867, 13),
    ("James", 873, 5), ("1 Peter", 875, 5), ("2 Peter", 877, 3),
    ("1 John", 879, 5), ("2 John", 881, 1), ("3 John", 883, 1),
    ("Jude", 885, 1), ("Revelation", 887, 22),
]
LAST_PRINTED = 895              # Revelation's last printed page
# "The Apocrypha" / "New Testament" divider pages, plus the duplicated-Esther
# pages (see the BOOKS comment) so they don't get absorbed into Judith's span.
DIVIDER_PAGES = {558, 732} | set(range(579, 585))

# The Letter of Jeremiah is printed as Baruch chapter 6 (the 1611 convention),
# so its markers run {6:1}–{6:73}; it is still its own single-chapter book.
START_CHAPTER = {"Letter of Jeremiah": 6}

# The source PDF omits the final benediction verse of exactly these four books
# (verified absent from the PDF pages themselves; every other canonical book
# matches the canonical KJV verse count exactly). Restored with the standard
# KJV text, supplied words bracketed in this edition's style.
RESTORED = {
    "Philippians":
        "{4:23} The grace of our Lord Jesus Christ [be] with you all. Amen.",
    "1 Thessalonians":
        "{5:28} The grace of our Lord Jesus Christ [be] with you. Amen.",
    "Hebrews": "{13:25} Grace [be] with you all. Amen.",
    "Revelation":
        "{22:21} The grace of our Lord Jesus Christ [be] with you all. Amen.",
}

# Canonical KJV verse counts for the 66 books — a total oracle: any extraction
# slip that survives the marker-sequence check (e.g. a dropped final verse)
# fails here. Apocrypha counts vary by edition and are not enforced.
VERSE_COUNTS = {
    "Genesis": 1533, "Exodus": 1213, "Leviticus": 859, "Numbers": 1288,
    "Deuteronomy": 959, "Joshua": 658, "Judges": 618, "Ruth": 85,
    "1 Samuel": 810, "2 Samuel": 695, "1 Kings": 816, "2 Kings": 719,
    "1 Chronicles": 942, "2 Chronicles": 822, "Ezra": 280, "Nehemiah": 406,
    "Esther": 167, "Job": 1070, "Psalms": 2461, "Proverbs": 915,
    "Ecclesiastes": 222, "Song of Solomon": 117, "Isaiah": 1292,
    "Jeremiah": 1364, "Lamentations": 154, "Ezekiel": 1273, "Daniel": 357,
    "Hosea": 197, "Joel": 73, "Amos": 146, "Obadiah": 21, "Jonah": 48,
    "Micah": 105, "Nahum": 47, "Habakkuk": 56, "Zephaniah": 53, "Haggai": 38,
    "Zechariah": 211, "Malachi": 55,
    "Matthew": 1071, "Mark": 678, "Luke": 1151, "John": 879, "Acts": 1007,
    "Romans": 433, "1 Corinthians": 437, "2 Corinthians": 257,
    "Galatians": 149, "Ephesians": 155, "Philippians": 104, "Colossians": 95,
    "1 Thessalonians": 89, "2 Thessalonians": 47, "1 Timothy": 113,
    "2 Timothy": 83, "Titus": 46, "Philemon": 25, "Hebrews": 303,
    "James": 108, "1 Peter": 105, "2 Peter": 61, "1 John": 105, "2 John": 13,
    "3 John": 14, "Jude": 25, "Revelation": 404,
}

# The PDF fuses a few subtitle "or"s onto the previous word; repaired exactly.
TITLE_FIXES = {
    "The Book of Wisdomor The Wisdom of Solomon":
        "The Book of Wisdom, or The Wisdom of Solomon",
    "The Wisdom of Jesus the Son of Sirach,or Ecclesiasticus":
        "The Wisdom of Jesus the Son of Sirach, or Ecclesiasticus",
    "The Prayer of Manassehor, The Prayer of Manasses King of Judah":
        "The Prayer of Manasseh, or The Prayer of Manasses King of Judah",
    "Ecclesiastesor, the Preacher": "Ecclesiastes, or the Preacher",
}

# 1611 front-matter styling inside books: the two Sirach prologue headings are
# bolded; the Susanna/Bel headnotes (the translators' own italic notes) are
# italicized. Everything else in a book's front stays plain.
FRONT_BOLD = {
    "A Prologue made by an uncertain Author",
    "The Prologue of the Wisdom of Jesus the Son of Sirach.",
}
FRONT_ITALIC_PREFIX = (
    "Set apart from the beginning of Daniel,",
    "The History of the Destruction of Bel and the Dragon,",
)


def page_lines(page) -> list[tuple[float, float, str]]:
    """Body lines in reading order: (x0, y0, raw text with leading spaces
    kept). Header-zone and whitespace-only lines are dropped."""
    out = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0 or b["bbox"][1] < HEADER_Y:
            continue
        for l in b["lines"]:
            t = "".join(s["text"] for s in l["spans"])
            if t.strip():
                out.append((b["bbox"][0], l["bbox"][1], t.rstrip()))
    out.sort(key=lambda r: (r[0] >= COL_X, r[1], r[0]))
    return out


# Wrap-hyphen healing must not eat the KJV's hyphenated proper names
# (Beer-sheba, Padan-aram, Jehovah-nissi …) when the line happens to break at
# the name's own hyphen. Two lexica, built in a pre-pass over the whole span,
# arbitrate: tokens seen hyphenated mid-line keep the hyphen; words seen whole
# elsewhere drop it; a capitalized head (the KJV name convention) breaks ties.
HYPHEN_LEX: set[str] = set()
PLAIN_LEX: set[str] = set()


def build_lexica(doc) -> None:
    hy = re.compile(r"[A-Za-z]+-[A-Za-z]+")
    word = re.compile(r"[A-Za-z]+")
    for i, (_, start, _) in enumerate(BOOKS):
        end = BOOKS[i + 1][1] - 1 if i + 1 < len(BOOKS) else LAST_PRINTED
        for p in range(start, end + 1):
            if p in DIVIDER_PAGES:
                continue
            for line in doc[p + OFFSET].get_text().split("\n"):
                line = line.strip()
                for m in hy.finditer(line):
                    if m.end() < len(line):        # hyphen not at line end
                        HYPHEN_LEX.add(m.group(0).lower())
                PLAIN_LEX.update(w.lower() for w in word.findall(line))


def heal(a: str, b: str) -> str:
    """Join continuation b onto a; decide a trailing wrap hyphen's fate."""
    if not (a.endswith("-") and b[:1].islower()):
        return a + " " + b
    head = a[:-1].rsplit(None, 1)[-1] if " " in a else a[:-1]
    tail = re.match(r"[A-Za-z]+", b)
    tail = tail.group(0) if tail else ""
    if f"{head}-{tail}".lower() in HYPHEN_LEX:
        return a + b                    # hard hyphen: Beer- + sheba
    if (head + tail).lower() in PLAIN_LEX:
        return a[:-1] + b               # soft wrap: perad- + venture
    return a + b if head[:1].isupper() else a[:-1] + b


def page_paragraphs(page) -> list[str]:
    """Prose pages: blocks are paragraphs. Lines within a block are joined
    with wrap hyphens healed; column order is left then right."""
    paras = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0 or b["bbox"][1] < HEADER_Y:
            continue
        text = ""
        for l in b["lines"]:
            t = "".join(s["text"] for s in l["spans"]).strip()
            if not t:
                continue
            text = heal(text, t) if text else t
        if text:
            paras.append((b["bbox"][0] >= COL_X, b["bbox"][1], text))
    paras.sort(key=lambda r: (r[0], r[1]))
    return [re.sub(r"\s+", " ", t).strip() for _, _, t in paras]


def tidy(s: str) -> str:
    """Collapse whitespace and heal the edition's split-bracket bug
    ('[saying,' / ']' on the next line -> '[saying,]')."""
    s = re.sub(r"\s+", " ", s).strip()
    return re.sub(r"\s+\]", "]", s)


class BookBuilder:
    """Accumulates one book's output: transforms {C:V} markers to bold verse
    numbers, promotes {C:1} to a chapter heading (unless suppressed), and
    sequence-validates chapters and verses."""

    def __init__(self, name: str, expected: int | None, warnings: list[str],
                 emit_headings: bool = True):
        self.name = name
        self.expected = expected
        self.warnings = warnings
        # single-chapter books get no chapter heading at all
        self.emit = emit_headings and expected != 1
        self.first = START_CHAPTER.get(name, 1)
        self.chapter = self.first - 1
        self.verse = 0
        self.verses = 0
        self.out: list[str] = []

    @property
    def chapters(self) -> int:
        return self.chapter - (self.first - 1)

    def feed(self, para: str) -> None:
        """One paragraph: split at chapter starts, bold the verses."""
        pos = 0
        cur: list[str] = []
        for m in MARKER_RE.finditer(para):
            c, v = int(m.group(1)), int(m.group(2))
            cur.append(para[pos:m.start()])
            pos = m.end()
            if v == 1 and c == self.chapter + 1:
                text = tidy("".join(cur))
                if text:
                    self.out.append(text)
                cur = []
                self.chapter, self.verse = c, 0
                if self.emit:
                    self.out.append(f"## Chapter {c}")
            elif c != self.chapter or v != self.verse + 1:
                self.warnings.append(
                    f"{self.name}: marker {{{c}:{v}}} after "
                    f"{{{self.chapter}:{self.verse}}}")
                self.chapter, self.verse = c, v - 1
            self.verse += 1
            self.verses += 1
            cur.append(f"**{v}** ")
        cur.append(para[pos:])
        text = tidy("".join(cur))
        if text:
            self.out.append(text)

    def close(self) -> None:
        if self.expected is not None and self.chapters != self.expected:
            self.warnings.append(
                f"{self.name}: {self.chapters} chapters "
                f"(expected {self.expected})")
        want = VERSE_COUNTS.get(self.name)
        if want is not None and self.verses != want:
            self.warnings.append(
                f"{self.name}: {self.verses} verses (canonical {want})")


def build_prose_book(doc, name, span, expected, warnings):
    """A two-column prose book -> (front lines, output parts, builder)."""
    bb = BookBuilder(name, expected, warnings)
    front: list[str] = []
    seen_marker = False
    for pno in span:
        for para in page_paragraphs(doc[pno]):
            if not seen_marker and not MARKER_RE.search(para):
                front.append(tidy(para))
                continue
            seen_marker = True
            if para.startswith("]") and bb.out and not bb.out[-1].startswith("#"):
                # split-bracket bug: the ']' closes the previous paragraph
                bb.out[-1] += "]"
                para = para[1:].strip()
                if not para:
                    continue
            if MARKER_RE.match(para):
                bb.feed(para)
            elif bb.out and not bb.out[-1].startswith("#"):
                # a non-marker-opening paragraph is a continuation of the
                # previous one across a column/page break; the tail may hold
                # more markers, so rejoin and re-feed (bolded **V** in the
                # already-transformed head pass through untouched)
                prev = bb.out.pop()
                bb.feed(heal(prev, para))
            else:
                bb.feed(para)
    if name in RESTORED:
        bb.feed(RESTORED[name])
    bb.close()
    return front, bb.out, bb


def build_psalms(doc, span, warnings):
    """Psalms: single column, verse per line, hanging-indent continuations.
    Book I–V = h2 (reordered above the psalm heading each is typeset under),
    Psalm N = h3 from the edition's own lines, superscriptions italic,
    all-caps section words (Psalm 119's ALEPH…) bold."""
    bb = BookBuilder("Psalms", 150, warnings, emit_headings=False)
    front: list[str] = []
    out: list[str] = []
    cur_verse: str | None = None
    psalm_no = 0

    def flush():
        nonlocal cur_verse
        if cur_verse is not None:
            bb.feed(cur_verse)
            out.extend(bb.out)
            bb.out = []
            cur_verse = None

    for pno in span:
        for _, _, raw in page_lines(doc[pno]):
            line = raw.strip()
            indented = raw[:1] == " " and not line.startswith("{")
            m = PSBOOK_RE.match(line)
            if m:
                flush()
                h2 = f"## Book {m.group(1)}"
                # typeset below the psalm heading it governs — reorder above
                if out and out[-1].startswith("### Psalm"):
                    out.insert(len(out) - 1, h2)
                else:
                    out.append(h2)
                continue
            m = PSALM_LINE_RE.match(line)
            if m:
                flush()
                n = int(m.group(1))
                if n != psalm_no + 1:
                    warnings.append(f"Psalms: 'Psalm {n}' after {psalm_no}")
                psalm_no = n
                out.append(f"### Psalm {n}")
                continue
            if psalm_no == 0:
                front.append(tidy(line))
                continue
            if line.startswith("]") and cur_verse is not None:
                cur_verse += "]"          # split-bracket bug: ']' opens a line
                line = line[1:].strip()
                if not line:
                    continue
            if MARKER_RE.match(line):
                flush()
                cur_verse = line
            elif indented and cur_verse is not None:
                cur_verse += " " + line
            else:
                flush()
                if line.isupper():
                    out.append(f"**{line.title()}**")   # ALEPH. BETH. …
                else:
                    out.append(f"*{tidy(line)}*")        # superscription
    flush()
    if psalm_no != 150:
        warnings.append(f"Psalms: {psalm_no} psalm headings (expected 150)")
    bb.close()
    return front, out, bb


def main() -> int:
    src, out_path = Path(sys.argv[1]), Path(sys.argv[2])
    doc = pymupdf.open(src)
    build_lexica(doc)
    warnings: list[str] = []
    parts: list[str] = [
        "# The Holy Bible",
        "*The King James Version of 1611, with Apocrypha. Modern spelling.*",
    ]
    total_verses = 0

    for i, (name, start, expected) in enumerate(BOOKS):
        end = BOOKS[i + 1][1] - 1 if i + 1 < len(BOOKS) else LAST_PRINTED
        span = [p + OFFSET for p in range(start, end + 1)
                if p not in DIVIDER_PAGES]
        if name == "Psalms":
            front, body, bb = build_psalms(doc, span, warnings)
        else:
            front, body, bb = build_prose_book(doc, name, span, expected,
                                               warnings)

        parts.append(f"# {name}")
        for j, f in enumerate(front):
            f = TITLE_FIXES.get(f, f)
            if j == 0:
                if f.lower() != name.lower():       # skip bare-name repeats
                    parts.append(f"*{f}*")
            elif f in FRONT_BOLD:
                parts.append(f"**{f}**")
            elif f.startswith(FRONT_ITALIC_PREFIX):
                parts.append(f"*{f}*")
            else:
                parts.append(f)
        parts.extend(body)
        total_verses += bb.verses
        exp = "" if expected is None else f"/{expected}"
        extra = f"   front: {front[0][:50]!r}" if front else "   front: —"
        if len(front) > 1:
            extra += f" (+{len(front) - 1} more lines)"
        print(f"  {name:20s} ch {bb.chapters:3d}{exp:5s} vv {bb.verses:5d}{extra}")

    text = "\n\n".join(parts) + "\n"
    # anything brace-like surviving transformation is a malformed marker
    for m in re.finditer(r"[{}]", text):
        warnings.append(
            f"stray brace: …{text[max(0, m.start() - 60):m.start() + 20]!r}…")
    out_path.write_text(text)

    print(f"\nbooks: {len(BOOKS)}   verses: {total_verses:,}")
    print(f"output: {out_path} ({out_path.stat().st_size:,} bytes)")
    print(f"warnings: {len(warnings)}")
    for w in warnings[:60]:
        print("  ⚠ " + w)
    if len(warnings) > 60:
        print(f"  … and {len(warnings) - 60} more")
    return 0 if not warnings else 1


if __name__ == "__main__":
    main()
