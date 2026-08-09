#!/usr/bin/env python3
"""Remove the critical apparatus from the Copernicus OCR extraction.

This script implements the received-text decision recorded in ANSWER.md:
rejected and alternate authorial passages are edition apparatus and are
removed; passages labelled ``Printed text`` or ``Printed version`` are the
received text and survive after their labels are removed.

No endpoint is inferred.  Every removal has a unique literal start and a
unique literal retained anchor.  The four prose-form labels use boundaries
read on printed pp. 25, 26, 78, and 80 of the prepared witness.  The script is
bound to the immutable OCR by SHA-256 and writes both the working Markdown and
an audit report.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


RAW = Path("raw/copernicus-revolutions-ocr.md")
OUTPUT = Path("copernicus-revolutions.md")
REPORT = Path("apparatus-report.txt")
RAW_SHA256 = "51ada54d022e11fd80648bb9334838b0ee2d39882a1822057827542452602dec"
EXPECTED_CHARS = 962_467
EXPECTED_PAGES = 328
PAGE_RULE = "\n\n---\n\n"


def assert_once(text: str, anchor: str, description: str) -> None:
    count = text.count(anchor)
    if count != 1:
        raise AssertionError(
            f"{description}: expected one anchor, found {count}: {anchor[:100]!r}"
        )


def remove_to(
    text: str,
    start: str,
    retained: str,
    description: str,
) -> tuple[str, str]:
    """Remove from unique *start* up to, but not including, unique *retained*."""
    assert_once(text, start, description + " start")
    assert_once(text, retained, description + " retained boundary")
    begin = text.index(start)
    end = text.index(retained)
    if end <= begin:
        raise AssertionError(f"{description}: retained boundary precedes start")
    removed = text[begin:end]
    return text[:begin] + text[end:], removed


def remove_exact(text: str, target: str, description: str) -> tuple[str, str]:
    assert_once(text, target, description)
    return text.replace(target, ""), target


def paired_bracket_spans(text: str) -> int:
    """Count matched square-bracket pairs with a simple nesting stack.

    This deliberately includes Markdown image alt brackets, translator
    interpolations, editorial labels, and mathematical explanatory brackets:
    the requested census is of *all* square-bracket spans, not a semantic
    subset.  Unmatched delimiters are reported separately.
    """
    depth = 0
    pairs = 0
    for char in text:
        if char == "[":
            depth += 1
        elif char == "]" and depth:
            depth -= 1
            pairs += 1
    return pairs


def delimiter_census(text: str) -> tuple[int, int, int]:
    return paired_bracket_spans(text), text.count("["), text.count("]")


def main() -> None:
    raw_bytes = RAW.read_bytes()
    digest = hashlib.sha256(raw_bytes).hexdigest()
    if digest != RAW_SHA256:
        raise AssertionError(f"raw OCR hash changed: {digest}")
    original = raw_bytes.decode("utf-8")
    if len(original) != EXPECTED_CHARS:
        raise AssertionError(
            f"expected {EXPECTED_CHARS} OCR characters, found {len(original)}"
        )
    if len(original.split(PAGE_RULE)) != EXPECTED_PAGES:
        raise AssertionError("expected 328 OCR page segments")
    if original.count("![img-") != 140:
        raise AssertionError("expected 140 raw image references")

    # Freeze the full label vocabulary before making any changes.  Similar
    # looking but unauthorized forms cause a failure instead of being folded
    # into a broad pattern.
    expected_label_forms = {
        "[Earlier draft:": 4,
        "[Printed text:": 4,
        "[Deleted version:": 1,
        "[In the autograph,": 1,
        "[Earlier version:": 7,
        "[Earlier version of the beginning of V, 1:": 1,
        "[Earlier version of the concluding paragraph of V, 23:": 1,
        "[Printed version:": 6,
        "[Deleted in the autograph:": 1,
    }
    actual_label_forms = {label: original.count(label) for label in expected_label_forms}
    if actual_label_forms != expected_label_forms:
        raise AssertionError(f"critical label vocabulary changed: {actual_label_forms}")
    if original.count("# Earlier draft:") != 1:
        raise AssertionError("expected one OCR-demoted [Earlier draft:] label")

    text = original
    removed_chunks: list[str] = []
    counts: Counter[str] = Counter()

    def cut(start: str, retained: str, category: str, description: str) -> None:
        nonlocal text
        text, removed = remove_to(text, start, retained, description)
        removed_chunks.append(removed)
        counts[category] += 1

    def drop(target: str, category: str, description: str) -> None:
        nonlocal text
        text, removed = remove_exact(text, target, description)
        removed_chunks.append(removed)
        counts[category] += 1

    def strip_label(label: str, following: str, category: str, description: str) -> None:
        """Remove a label only, with following received text as a unique guard."""
        nonlocal text
        guarded = label + following
        assert_once(text, guarded, description)
        text = text.replace(guarded, following)
        removed_chunks.append(label)
        counts[category] += 1

    # Four prose-form apparatus labels.  Their endpoints were read on the
    # printed pages, not inferred from the next heading or label.
    cut(
        "[Here Copernicus originally planned to include a little more than two handwritten pages",
        "[The foregoing letter, the true nature of which was not suspected by Copernicus",
        "prose label: Here Copernicus originally planned",
        "printed p. 25 deleted Book-I ending",
    )
    cut(
        "[The foregoing letter, the true nature of which was not suspected by Copernicus",
        "[The rest of the material deleted here in the autograph",
        "prose label: The foregoing letter",
        "printed p. 26 deleted Book-II introduction",
    )
    cut(
        "[An earlier version of the latter part of II, 12 survives in the autograph",
        "## THE RISING AND SETTING OF THE HEAVENLY BODIES",
        "prose label: An earlier version of II, 12",
        "printed p. 78 earlier II,12 ending",
    )
    drop(
        "[The beginning of a new book, according to Copernicus' original plan; an earlier draft of the first two-thirds of this Chapter survives in the autograph, folio 46$^{v}$ – 47$^{v}$, without any indication that it was superseded; where this earlier draft is somewhat more explicit than the printed text, it too is translated here].\n\n",
        "prose label: The beginning of a new book",
        "printed p. 80 introductory apparatus label",
    )

    # Standalone notices that actually introduce rejected passages lose the
    # notice and the passage.  Original-plan chapter notices identify received
    # text, so only their bracketed editorial labels are removed.
    cut(
        "[The rest of the material deleted here in the autograph",
        "[As the heading of I, 12, the first edition introduced",
        "standalone notice + rejected passage: rest deleted in autograph",
        "printed p. 26 deleted I,12 opening",
    )
    cut(
        "[As the heading of I, 12, the first edition introduced",
        "## STRAIGHT LINES SUBTENDED IN A CIRCLE Chapter 12",
        "standalone notice + rejected passage: I,12 heading/autograph continuation",
        "printed pp. 26-27 superseded I,12 material",
    )
    for chapter in (1, 2, 3):
        drop(
            f"[Book II, Chapter {chapter}, according to Copernicus' original plan]\n\n",
            "standalone original-plan chapter notice",
            f"Book II original-plan notice {chapter}",
        )
    drop(
        "[Marginal note, inserted in the wrong place, and later deleted, but restored by the editors: The proof is exactly the same, if the earth were at rest in F, and the sun moved in the circumference ABC, as in Ptolemy and other authors.]\n\n",
        "standalone restored marginal notice",
        "restored editorial marginal note",
    )

    # Explicit draft/received pairs and self-delimited rejected variants.
    cut(
        "[Earlier draft:\n\nNow that I have expounded",
        "[Printed text:\n\n20\n\nThis opinion",
        "[Earlier draft:]",
        "first printed-p.80 earlier draft",
    )
    strip_label(
        "[Printed text:\n\n", "20\n\nThis opinion", "[Printed text:]",
        "first printed-text label",
    )
    cut(
        "[Earlier draft:\n\nOf course I acknowledge",
        "[Printed text:\n\nBut we shall do much better",
        "[Earlier draft:]",
        "second printed-p.80 earlier draft",
    )
    strip_label(
        "[Printed text:\n\n", "But we shall do much better", "[Printed text:]",
        "second printed-text label",
    )
    # Printed pp. 82-83 visibly use the same authorized bracket convention,
    # but Mistral lost the opening bracket and promoted the label to an h1.
    # The edition itself supplies the explicit closing notice.
    cut(
        "# Earlier draft:\n\nAfter these rings have been arranged in this way",
        "For example, in the 2nd year of the emperor Antoninus Pius",
        "[Earlier draft:]",
        "astrolabe earlier draft, OCR-demoted label",
    )

    cut(
        "[In the autograph, fol. 75$^{2}$, Chapter 4 originally ended",
        "[Printed text:\n\n15\n\nTherefore it is clear",
        "[In the autograph ...:]",
        "autograph ending of III,4",
    )
    strip_label(
        "[Printed text:\n\n", "15\n\nTherefore it is clear", "[Printed text:]",
        "third printed-text label",
    )
    cut(
        "[Earlier draft:\n\nIn the year 1460 A. D.",
        "---\n\nHere again it is absolutely clear",
        "[Earlier draft:]",
        "standalone earlier obliquity draft",
    )
    cut(
        "[Earlier draft: Originally Copernicus began III, 7",
        "[Printed text:\n\nThe mean motions having been set forth",
        "[Earlier draft:]",
        "earlier beginning of III,7",
    )
    strip_label(
        "[Printed text:\n\n", "The mean motions having been set forth", "[Printed text:]",
        "fourth printed-text label",
    )
    cut(
        "[Deleted version:\n\nIts nonuniformity, however",
        "The sun's [motion], however, is demonstrably nonuniform",
        "[Deleted version:]",
        "deleted solar-motion version",
    )

    cut(
        "[Earlier version of the beginning of V, 1:",
        "[Printed version:\n\nIn Plato's *Timaeus*",
        "[Earlier version of beginning V,1:]",
        "earlier beginning of V,1",
    )
    strip_label(
        "[Printed version:\n\n", "In Plato's *Timaeus*", "[Printed version:]",
        "first printed-version label",
    )
    cut(
        "[Deleted in the autograph:\n\nCombined in this way",
        "I say that the motion in parallax is nothing but the difference",
        "[Deleted in the autograph:]",
        "deleted V,1 autograph passage",
    )
    cut(
        "[Earlier version:\n\nOne was the work of Ptolemy",
        "---\n\nOne was the work of Timocharis",
        "[Earlier version:]",
        "earlier V,23 observation",
    )
    cut(
        "[Earlier version of the concluding paragraph of V, 23:",
        "## THE PLACES OF VENUS' ANOMALY",
        "[Earlier version concluding V,23:]",
        "earlier conclusion of V,23",
    )
    cut(
        "[Earlier version:\n\nTHE PLACES OF VENUS' MEAN ANOMALY",
        "[Printed version:\n\nFrom the 1st Olympiad",
        "[Earlier version:]",
        "earlier V,24 passage",
    )
    strip_label(
        "[Printed version:\n\n", "From the 1st Olympiad", "[Printed version:]",
        "second printed-version label",
    )
    cut(
        "[Earlier version:\n\nThe whole of EA = 16580",
        "[Printed version:\n\nHowever, with $DE = 60^p$",
        "[Earlier version:]",
        "first earlier V,36 computation",
    )
    strip_label(
        "[Printed version:\n\n", "However, with $DE = 60^p$", "[Printed version:]",
        "third printed-version label",
    )
    cut(
        "[Earlier version:\n\nBut according to the computations executed for the greatest distance",
        "[Printed version:\n\nFor other places the procedure is similar",
        "[Earlier version:]",
        "second earlier V,36 computation",
    )
    strip_label(
        "[Printed version:\n\n", "For other places the procedure is similar", "[Printed version:]",
        "fourth printed-version label",
    )
    cut(
        "[Earlier version:\n\nThus, when the line of the sun's mean motion",
        "To make the foregoing remarks likewise easier to understand",
        "[Earlier version:]",
        "earlier VI,2 sentence",
    )
    cut(
        "[Earlier version:\n\nNow as an example I shall use Mars",
        "[Printed version:\n\nFor each planet the ratio of EG",
        "[Earlier version:]",
        "earlier VI,3 computation",
    )
    strip_label(
        "[Printed version:\n\n", "For each planet the ratio of EG", "[Printed version:]",
        "fifth printed-version label",
    )
    cut(
        "[Earlier version:\n\nNevertheless, if anybody wishes to scrutinize",
        "[Printed version:\n\nNevertheless, if anybody is not wearied",
        "[Earlier version:]",
        "earlier VI,8 ending",
    )
    strip_label(
        "[Printed version:\n\n", "Nevertheless, if anybody is not wearied", "[Printed version:]",
        "sixth printed-version label",
    )

    # Every authorized label form must be absent; ordinary translator
    # interpolations are protected by exact sentinel counts.
    for label in expected_label_forms:
        if label in text:
            raise AssertionError(f"critical label survived: {label!r}")
    if "# Earlier draft:" in text:
        raise AssertionError("OCR-demoted earlier-draft label survived")
    sentinels = {
        "[The sphere of the fixed stars]": (1, 1),
        "[Al-Zarkali's]": (1, 1),
        "[is given]": (1, 1),
        "[from the earth's center]": (1, 1),
        # One instance belongs to the rejected VI,8 variant; the independent
        # received-text interpolation must remain.
        "[after V, 33]": (2, 1),
    }
    for span, expected in sentinels.items():
        before = original.count(span)
        after = text.count(span)
        if (before, after) != expected:
            raise AssertionError(
                f"ordinary bracket sentinel changed: {span!r}: {before} -> {after}"
            )

    before_brackets = delimiter_census(original)
    after_brackets = delimiter_census(text)
    removed_openers = sum(chunk.count("[") for chunk in removed_chunks)
    removed_closers = sum(chunk.count("]") for chunk in removed_chunks)
    if before_brackets[1] - after_brackets[1] != removed_openers:
        raise AssertionError("square-bracket opener accounting failed")
    if before_brackets[2] - after_brackets[2] != removed_closers:
        raise AssertionError("square-bracket closer accounting failed")

    refs = re.findall(r"!\[img-(\d+)\.jpeg\]\(images/img-\1\.jpeg\)", text)
    removed_refs = sorted(
        set(re.findall(r"!\[img-(\d+)\.jpeg\]", original)) - set(refs),
        key=int,
    )
    if len(refs) != 138 or len(set(refs)) != 138:
        raise AssertionError(
            f"expected 138 unique received-text image refs, found {len(refs)}; "
            f"removed={removed_refs}"
        )
    if removed_refs != ["113", "128"]:
        raise AssertionError(f"unexpected apparatus-only images: {removed_refs}")

    report_lines = [
        "Copernicus critical-apparatus removal",
        f"raw sha256: {digest}",
        "",
        "Removals by label form:",
    ]
    for category, count in sorted(counts.items()):
        report_lines.append(f"- {category}: {count}")
    report_lines += [
        "",
        "Square-bracket census (matched pairs / openers / closers):",
        f"- before: {before_brackets[0]} / {before_brackets[1]} / {before_brackets[2]}",
        f"- after: {after_brackets[0]} / {after_brackets[1]} / {after_brackets[2]}",
        f"- difference: {before_brackets[0] - after_brackets[0]} / "
        f"{before_brackets[1] - after_brackets[1]} / {before_brackets[2] - after_brackets[2]}",
        f"- removed chunks contain: {removed_openers} openers / {removed_closers} closers",
        "",
        "Witnessed prose boundaries:",
        "- printed p. 25, 'Here Copernicus originally planned ...': rejected text ends 'you are dead.'; first final received prose kept afterward: 'In accordance with the common practice of'.",
        "- printed p. 26, 'The foregoing letter ...': rejected text ends 'science of the stars.'; first final received prose kept afterward: 'In accordance with the common practice of'.",
        "- printed p. 78, 'An earlier version of ... II, 12': rejected text ends 'which I discussed only as examples.'; first six prose words kept: 'The risings and settings of the'.",
        "- printed p. 80, 'The beginning of a new book ...': the introductory label alone is removed; after the explicitly delimited earlier draft, the first six received words kept are 'This opinion, I believe, should be'.",
        "- printed pp. 82-83, '[Earlier draft:]' (OCR rendered '# Earlier draft:'): the explicit end notice is '[The earlier draft ends abruptly here].'; first six words kept are 'For example, in the 2nd year'.",
        "",
        "Images:",
        "- raw references: 140",
        "- received-text references: 138",
        "- apparatus-only references removed: img-113.jpeg, img-128.jpeg",
        "- the source files remain in images/ so the raw extraction is reproducible",
    ]
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(text):,} characters")
    print(f"wrote {REPORT}")
    print(f"removed labelled blocks/notices: {sum(counts.values())}")
    print(f"bracket pairs: {before_brackets[0]} -> {after_brackets[0]}")
    print("received-text image references: 138 (2 apparatus-only references removed)")


if __name__ == "__main__":
    main()
