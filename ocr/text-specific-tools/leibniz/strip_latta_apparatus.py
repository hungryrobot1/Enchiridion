#!/usr/bin/env python3
"""Remove Robert Latta's apparatus from the Leibniz OCR by page geometry.

Latta's notes are a smaller-type block below Leibniz's text.  The supplied IA
text layer is too inaccurate to publish, but it retains line positions and font
sizes, so it is a better instrument for locating that boundary than guessing
from prose.  For each page this script finds the body-to-note type transition,
aligns the IA tokens to Mistral's OCR tokens, and cuts at the corresponding OCR
position.  It then removes Latta's seven full-size PREFATORY NOTE blocks by
asserted work/body anchors, removes OCR-created running-head headings, and drops
the superscript navigation markers belonging to the discarded notes.

The output retains exact page separators for stage-2/stage-3 auditing.  A later
script rejoins prose across them.
"""

from __future__ import annotations

import difflib
import re
import statistics
from pathlib import Path

import pymupdf

RAW = Path("source.md")
PDF = Path("source/leibniz-works-selected.pdf")
PREPARED = Path("source/leibniz-works-prepared.pdf")
OUT = Path("leibniz-pages.md")
REPORT = Path("latta-apparatus-report.txt")
PAGE_SEPARATOR = "\n\n---\n\n"
TOKEN_RE = re.compile(r"[^\W\d_]+", re.UNICODE)

# These pages contain a work-opening prefatory block and no safely useful
# body-to-note boundary.  The asserted anchor pass below owns their apparatus.
NO_GEOMETRIC_CUT = {1, 2, 3, 58, 96, 126, 127, 176}

# On these pages the IA layer sees the typographic note boundary, but Mistral
# has not transcribed enough text on both sides for token alignment.  Each cut
# is therefore asserted against the exact last words of Leibniz's body text.
# The following source page continues the same sentence in every case.
PAGE_END_ANCHORS = {
    19: "29. But it is the knowledge of necessary and eternal truths that distinguishes us from the mere animals and gives us Reason and the sciences, raising us to the knowledge of ourselves and of God ⁴⁸. And it is this in us that is called the rational soul or mind [esprit].",
    22: "When a truth is necessary, its reason can be found by analysis, resolving it into more simple ideas and truths, until we come to those which are primary ⁵⁴. (Théod. 170, 174, 189, 280-282, 367. Abrégé, Object. 3.)",
    24: "38. Thus the final reason of things must be in a necessary substance, in which the variety of particular changes exists only eminently ⁶¹, as in its source; and this substance we call God. (Théod. 7.)",
    25: "40. We may also hold that this supreme substance, which is unique, universal⁶³ and necessary, nothing out-",
    27: "43. It is farther true that in God there is not only the source of existences but also that of essences, in so far as they are real, that is to say, the source of what is real in the possible⁶⁷. For the understanding of God is the region of eternal truths or of the ideas on which they depend⁶⁸, and without Him there would be nothing real in the possibilities of things, and not only would there be nothing in existence, but nothing would even be possible. (Théod. 20.)",
    34: "according to the special point of view of each Monad⁸⁹. (Théod. 147.)",
    35: "and this Monsieur Bayle recognized when, in his Dictionary (article Rorarius ⁹¹), he raised objections to it, in which",
    38: "that which is there represented distinctly; it cannot all at once unroll everything that is enfolded in it⁹⁸, for its complexity is infinite⁹⁹.",
    45: "74. Philosophers have been much perplexed about the origin of forms ¹¹⁶, entelechies, or souls; but nowadays",
    46: "but always come from seeds, in which there was undoubtedly some pre-formation ¹¹⁷; and it is held that not only the organic",
    56: "recognizing that if we could sufficiently under-",
    61: "Charity is universal benevolence, and benevolence is the habit of loving or esteeming [amandi sive diligendi] ¹¹. But to love",
    72: "And indeed in the commonwealth civil Right receives its force from him who has the supreme power⁵⁵:",
    80: "which in my opinion are to be found everywhere ²⁷, and",
    111: "book; and those who will think out what I have formerly published will perhaps find that they already have the means of making this answer.",
    147: "and the use of this law in physics is very considerable: it is to the effect that we always pass from",
    155: "Quietists¹¹⁹, who imagine an absorption of the soul and its reunion with the ocean of divinity, a notion",
    156: "although this able author goes so far as to think that the rigidity or cohesion of its particles constitutes the essence of the body. Space must rather be conceived as full of an ultimately fluid matter,",
    164: "The Bishop of Worcester might have added that from the fact that the general idea of substance is in body and in spirit, it does not follow that their differences are",
    174: "who found a ground for phenomena [apparences] by inventing for this purpose occult qualities or faculties, which were pictured as being like little sprites or elves ¹⁹³,",
    186: "And this ultimate reason of things is called God ⁴⁰.",
    187: "but any imperfection that remains in them comes from the essential and original limitation of the created thing ⁴⁴.",
    188: "There is conserved the same quantity of total and absolute force, or of activity [action], also the same quantity of relative force or of reaction, and finally the same quantity of force of direction⁴⁸. Further,",
}

FOOTNOTE_PARAGRAPH = re.compile(
    r"(?m)(?:\A|\n\n)(?:[⁰¹²³⁴⁵⁶⁷⁸⁹]+|\$\^\{\d+\}\$)"
)


def token_spans(text: str):
    return [(m.group(0).casefold(), m.start(), m.end()) for m in TOKEN_RE.finditer(text)]


def page_lines(page):
    lines = []
    for block in page.get_text("dict")["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            text = "".join(s["text"] for s in line["spans"]).strip()
            sizes = []
            for span in line["spans"]:
                sizes.extend([span["size"]] * max(1, len(span["text"].strip())))
            if text and sizes:
                lines.append((line["bbox"][1], line["bbox"][3],
                              statistics.median(sizes), text))
    return sorted(lines)


def note_boundary(lines):
    """Return the y coordinate of the small-type note block, or None."""
    for i in range(2, len(lines) - 2):
        previous, current = lines[i - 1], lines[i]
        if current[0] < 80:
            continue
        before = statistics.median(x[2] for x in lines[max(0, i - 4):i])
        after = statistics.median(x[2] for x in lines[i:i + 4])
        gap = current[0] - previous[1]
        # Take the first sustained transition from the roughly 10-point body
        # to the roughly 9-point notes.  Maximising the size delta chose a
        # later transition *inside* the notes on several crowded pages; a
        # looser body threshold also classified the last small-looking body
        # line as apparatus and deleted complete numbered sections.
        if (current[2] <= 9.65 and before >= 9.85 and after <= 9.65 and
                before - after >= 0.35 and gap >= 2):
            return current[0]
    return None


def aligned_cut(ocr: str, lines, boundary: float):
    pdf_before = " ".join(x[3] for x in lines if 45 < x[0] < boundary)
    pdf_after = " ".join(x[3] for x in lines if x[0] >= boundary)
    before_tokens = [x[0] for x in token_spans(pdf_before)]
    after_tokens = [x[0] for x in token_spans(pdf_after)]
    ocr_spans = token_spans(ocr)
    ocr_tokens = [x[0] for x in ocr_spans]
    matcher = difflib.SequenceMatcher(None, before_tokens, ocr_tokens, autojunk=False)
    blocks = [b for b in matcher.get_matching_blocks() if b.size]
    if not blocks:
        return None

    # OCR preserves reading order as body followed by notes, but frequently
    # fuses the first note continuation into the last body paragraph. Locate
    # the final body block and the first substantial note block after it.
    last = max(blocks, key=lambda b: b.a + b.size)
    body_ocr_end = last.b + last.size
    note_blocks = [
        b for b in difflib.SequenceMatcher(
            None, after_tokens, ocr_tokens, autojunk=False
        ).get_matching_blocks()
        if b.size >= 8 and b.b >= body_ocr_end
    ]
    if not note_blocks:
        # An explicit-marker cut may already have removed the entire note, or
        # the prepared crop may contain no transcribed note text.
        return None
    first_note = min(note_blocks, key=lambda b: b.b)
    return ocr_spans[first_note.b][1]


def strip_prefatory(text: str):
    spans = [
        ("# THE MONADOLOGY¹. 1714.", "1. The Monad, of which we shall here speak"),
        ("# ON THE NOTIONS OF RIGHT AND JUSTICE. 1693.",
         "The doctrine of right, confined by nature within narrow limits"),
        ("# NEW SYSTEM OF THE NATURE OF SUBSTANCES", "1. Several years ago I conceived this system"),
        ("# EXPLANATION OF THE NEW SYSTEM OF THE COMMUNICATION BETWEEN SUBSTANCES",
         "I recollect, Sir, that in compliance with what I understood to be your desire"),
        ("# ON THE ULTIMATE ORIGINATION OF THINGS. 1697.", "BESIDES the world or the aggregate"),
        ("# NEW ESSAYS ON THE HUMAN¹ UNDER-STANDING. 1704.", "# INTRODUCTION."),
        ("# PRINCIPLES OF NATURE AND OF GRACE, FOUNDED ON REASON. 1714.",
         "1. Substance is a being capable of action"),
    ]
    for title_prefix, body_anchor in spans:
        start = text.find(title_prefix)
        assert start >= 0, title_prefix
        title_end = text.find("\n", start)
        body = text.find(body_anchor, title_end)
        assert body >= 0, body_anchor
        text = text[:title_end] + "\n\n" + text[body:]
    return text


def main():
    raw = RAW.read_text()
    pages = raw.split(PAGE_SEPARATOR)
    doc = pymupdf.open(PDF)
    prepared = pymupdf.open(PREPARED)
    assert len(pages) == doc.page_count == prepared.page_count == 195
    report = []
    cut_count = 0
    anchored_cut_count = 0
    marker_paragraph_cut_count = 0
    for number, (page, pdf_page, prepared_page) in enumerate(zip(pages, doc, prepared), 1):
        if number in PAGE_END_ANCHORS:
            anchor = PAGE_END_ANCHORS[number]
            assert page.count(anchor) == 1, (number, page.count(anchor))
            cut = page.index(anchor) + len(anchor)
            removed = re.sub(r"\s+", " ", page[cut:]).strip()
            assert removed, number
            pages[number - 1] = page[:cut]
            report.append(
                f"p{number:03}: asserted body-end anchor, removed={removed[:100]!r}"
            )
            anchored_cut_count += 1
            continue
        marker_start = FOOTNOTE_PARAGRAPH.search(page)
        if marker_start:
            marker_cut = marker_start.start()
            removed = re.sub(r"\s+", " ", page[marker_cut:]).strip()
            assert removed, number
            page = page[:marker_cut].rstrip()
            pages[number - 1] = page
            report.append(
                f"p{number:03}: explicit footnote paragraph, removed={removed[:100]!r}"
            )
            marker_paragraph_cut_count += 1
        lines = page_lines(pdf_page)
        boundary = None if number in NO_GEOMETRIC_CUT else note_boundary(lines)
        if boundary is None:
            report.append(f"p{number:03}: no geometric cut")
            continue
        # A transition at the lower edge is useful to the cropper but does not
        # mean note text survived into the OCR.  The 40-point guard retains the
        # final two or three body lines when their measured font happens to dip.
        if prepared_page.rect.height <= boundary + 40:
            report.append(f"p{number:03}: notes already outside prepared crop")
            continue
        try:
            cut = aligned_cut(page, lines, boundary)
        except AssertionError as error:
            raise AssertionError(f"page {number}: {error}") from error
        if cut is None:
            report.append(f"p{number:03}: no note-side OCR match")
            continue
        removed = re.sub(r"\s+", " ", page[cut:]).strip()
        pages[number - 1] = page[:cut].rstrip()
        report.append(f"p{number:03}: y={boundary:.1f}, removed={removed[:100]!r}")
        cut_count += 1
    assert marker_paragraph_cut_count == 51, marker_paragraph_cut_count
    assert cut_count == 22, cut_count
    assert anchored_cut_count == 23, anchored_cut_count
    text = PAGE_SEPARATOR.join(pages)
    text = strip_prefatory(text)

    # OCR promoted repeated running heads to headings. Opening dated titles and
    # the genuine Third Explanation/Introduction headings are not in this set.
    running = re.compile(
        r"(?m)^# (?:THE MONADOLOGY|ON THE NOTIONS OF RIGHT AND JUSTICE|NEW SYSTEM|"
        r"PRINCIPLES OF NATURE AND GRACE)\s*$\n*"
    )
    text, running_count = running.subn("", text)
    assert running_count == 15, running_count

    # These superscripts point exclusively to Latta's discarded notes. Section
    # numerals and mathematical notation in this edition use ordinary glyphs.
    text, marker_count = re.subn(r"[⁰¹²³⁴⁵⁶⁷⁸⁹]+", "", text)
    assert marker_count == 604, marker_count
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    OUT.write_text(text)
    REPORT.write_text("\n".join(report) + "\n")
    print(f"wrote {OUT}: {len(text)} chars; {marker_paragraph_cut_count} explicit-note cuts, "
          f"{cut_count} aligned note-zone cuts, "
          f"{anchored_cut_count} asserted note-zone cuts, "
          f"{running_count} running heads, {marker_count} note markers removed")


if __name__ == "__main__":
    main()
