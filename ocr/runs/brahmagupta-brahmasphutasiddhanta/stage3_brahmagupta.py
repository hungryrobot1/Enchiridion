#!/usr/bin/env python3
"""Count-asserted stage-3 transformations for Brahmagupta's two chapters.

The untouched OCR is `source/raw.md`.  Every pass either initializes the working
markdown from that source or transforms the existing working markdown after
asserting the exact input condition it expects.  This keeps each editorial
operation separately reviewable and lets the diagnostic triad run between
passes.

Usage:
    ocr/.venv/bin/python3 stage3_brahmagupta.py initialize
    ocr/.venv/bin/python3 stage3_brahmagupta.py macrons-to-acutes
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


RAW = Path("source/raw.md")
OUTPUT = Path("brahmagupta-brahmasphutasiddhanta.md")
RAW_SHA256 = "647b5808fc8ac00e3945ffa2e8d4210c963a0b8619a9868d9ec57cd381d6005c"
PAGE_SEPARATOR = "\n\n---\n\n"
MACRON_TO_ACUTE = str.maketrans(
    {"ā": "á", "ī": "í", "ō": "ó", "ū": "ú", "Ā": "Á", "Ī": "Í", "Ō": "Ó", "Ū": "Ú"}
)
EXPECTED_MACRONS = {"ā": 55, "ī": 18, "ō": 3, "ū": 3, "Ā": 15, "Ī": 5, "Ō": 0, "Ū": 2}

# These are continuation paragraphs of numbered Brahmagupta verses.  Their
# page-local indices were checked against the immediately adjacent verse; all
# other non-heading, non-numbered paragraphs belong to the printed note zone.
BODY_CONTINUATIONS = {
    2: {0}, 3: {0}, 8: {2}, 10: {0, 1}, 12: {0}, 17: {0}, 18: {0},
    20: {0}, 24: {0}, 27: {0}, 31: {0}, 35: {0}, 37: {0}, 45: {0},
    46: {0}, 47: {0}, 50: {0}, 53: {0}, 55: {0}, 57: {0}, 58: {0},
    64: {0}, 66: {0}, 90: {0}, 92: {0}, 93: {0}, 101: {0}, 102: {0},
}
RULE_START = re.compile(
    r"^(?:\d+(?:\s*[—–-]\s*\d+)?\.|Rule:|Rules,|Interpretation|FINIS)", re.I
)
NUMBERED_NOTE_START = re.compile(r"^(?:[¹²³⁴⁵⁶⁷⁸⁹⁰ᵃ]|\$\^\{|\d+\s+(?=[A-Z]))")
STAR_NOTE_START = re.compile(r"^(?:[*†‡]|\\\*)")
CERTAIN_COMMENTATOR_SIGNATURE = re.compile(
    r"(?i)(?<![A-Za-z])(?:ch|c(?:ii|11|₁₁|₁1|1₁)|com)\."
    r"(?![A-Za-z])|\bCHATURVÉDA\."
)
OTHER_SIGNATURE = re.compile(
    r"(?i)(?<![A-Za-z-])(?:ib|cn|gan)\.\s*$"
)
COMMENTATOR_SIGNATURE = re.compile(
    r"(?i)(?<![A-Za-z])(?:ch|c(?:ii|11|₁₁|₁1|1₁)|com)\."
    r"(?![A-Za-z])|\bCHATURVÉDA\.|(?<![A-Za-z-])(?:ib|cn|gan)\.\s*$"
)


def read_checked(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if len(text.split(PAGE_SEPARATOR)) != 102:
        raise AssertionError(f"{path}: expected 102 OCR page segments")
    if text.count("![") != 36:
        raise AssertionError(f"{path}: expected 36 image references")
    return text


def initialize() -> None:
    raw = read_checked(RAW)
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    if digest != RAW_SHA256:
        raise AssertionError(f"raw OCR digest changed: {digest}")
    OUTPUT.write_text(raw, encoding="utf-8")
    print(f"initialized {OUTPUT} from immutable OCR: {len(raw)} characters")


def macrons_to_acutes() -> None:
    text = read_checked(OUTPUT)
    actual = {mark: text.count(mark) for mark in EXPECTED_MACRONS}
    if actual != EXPECTED_MACRONS:
        raise AssertionError(f"unexpected macron census: {actual}")
    revised = text.translate(MACRON_TO_ACUTE)
    changed = sum(actual.values())
    if sum(revised.count(mark) for mark in EXPECTED_MACRONS) != 0:
        raise AssertionError("macron replacement was incomplete")
    OUTPUT.write_text(revised, encoding="utf-8")
    print(f"replaced {changed} OCR macrons with the edition's acute long-vowel mark")


def remaining_macrons_to_acutes() -> None:
    """Repair the four e-macrons on audited pages omitted from the first table."""
    text = read_checked(OUTPUT)
    actual = {"ē": text.count("ē"), "Ē": text.count("Ē")}
    if actual != {"ē": 2, "Ē": 2}:
        raise AssertionError(f"unexpected remaining macron census: {actual}")
    revised = text.translate(str.maketrans({"ē": "é", "Ē": "É"}))
    OUTPUT.write_text(revised, encoding="utf-8")
    print("replaced 4 OCR e-macrons on the audited printed pages")


def shape_headings() -> None:
    text = read_checked(OUTPUT)
    replacements = {
        "# GANITÁD'HYAYA, ON ARITHMETIC;": ("# BRAHME-SPHUTA-SIDD'HÁNTA, CHAPTERS XII AND XVIII\n\n## GANITÁD'HYAYA, ON ARITHMETIC;", 1),
        "# CHAPTER XII.": ("# CHAPTER XII.", 1),
        "# SECTION I.": ("## SECTION I.", 2),
        "# CUTTACAD'HYAYA, ON ALGEBRA;": ("## CUTTACAD'HYAYA, ON ALGEBRA;", 1),
        "# CHAPTER XVIII.": ("# CHAPTER XVIII.", 1),
        "### SECTION III.": ("## SECTION III.", 2),
        "#### TRIANGLE and QUADRILATERAL.": ("### TRIANGLE and QUADRILATERAL.", 1),
    }
    revised = text
    counts = {}
    for old, (new, expected) in replacements.items():
        counts[old] = revised.count(old)
        if counts[old] != expected:
            raise AssertionError(f"heading anchor count {old!r}: {counts[old]}")
        revised = revised.replace(old, new)
    # All section headings are h2 and their descriptive titles h3.
    revised, section_promotions = re.subn(r"^### (SECTION [IVX]+\.)$", r"## \1", revised, flags=re.M)
    if section_promotions != 0:
        raise AssertionError(f"unexpected additional h3 section headings: {section_promotions}")
    OUTPUT.write_text(revised, encoding="utf-8")
    print(f"shaped heading hierarchy using {len(replacements)} asserted anchors")


def paragraph_records(text: str):
    records = []
    pages = text.split(PAGE_SEPARATOR)
    for page_no, page in enumerate(pages, 1):
        paras = [p for p in re.split(r"\n\s*\n", page.strip()) if p.strip()]
        for index, para in enumerate(paras):
            one_line = para.replace("\n", " ")
            body = (
                para.startswith("#")
                or (page_no == 1 and index <= 10)  # title matter plus added document h1
                or (page_no == 49 and index <= 7)  # chapter XVIII title leaf
                or bool(RULE_START.match(one_line))
                or index in BODY_CONTINUATIONS.get(page_no, set())
            )
            records.append({
                "page": page_no, "index": index, "text": para,
                "one": one_line, "body": body, "role": "body" if body else "note",
            })
    return records


def voice_separation() -> None:
    """Remove unsigned editorial groups and blockquote signed commentary."""
    text = read_checked(OUTPUT)
    records = paragraph_records(text)
    note_records = [r for r in records if not r["body"]]

    # Star/dagger asides are nested inside numbered note streams in this OCR.
    # Classify each as its own note so it cannot terminate the surrounding one.
    main_notes = [r for r in note_records if not STAR_NOTE_START.match(r["one"])]
    star_notes = [r for r in note_records if STAR_NOTE_START.match(r["one"])]

    groups = []
    current = []
    for rec in main_notes:
        if NUMBERED_NOTE_START.match(rec["one"]) and current:
            groups.append(current)
            current = []
        current.append(rec)
    if current:
        groups.append(current)

    signed = [g for g in groups if COMMENTATOR_SIGNATURE.search(" ".join(r["one"] for r in g))]
    unsigned = [g for g in groups if g not in signed]
    certain_signed = [g for g in signed if CERTAIN_COMMENTATOR_SIGNATURE.search(" ".join(r["one"] for r in g))]
    uncertain_signed = [g for g in signed if g not in certain_signed]
    signed_stars = [r for r in star_notes if COMMENTATOR_SIGNATURE.search(r["one"])]
    unsigned_stars = [r for r in star_notes if r not in signed_stars]
    actual = (len(groups), len(signed), len(unsigned), len(star_notes), len(signed_stars), len(unsigned_stars))
    expected = (194, 126, 68, 38, 4, 34)
    if actual != expected:
        raise AssertionError(f"unexpected voice census {actual}, expected {expected}")
    if (len(certain_signed), len(uncertain_signed)) != (122, 4):
        raise AssertionError("unexpected certain/uncertain signature split")

    group_number = {}
    group_label = {}
    for number, group in enumerate(signed, 1):
        for rec in group:
            rec["role"] = "commentary"
            group_number[id(rec)] = number
            group_label[id(rec)] = "commentary" if group in certain_signed else "uncertain"
    for group in unsigned:
        for rec in group:
            rec["role"] = "drop"
    for rec in signed_stars:
        rec["role"] = "commentary"
        group_number[id(rec)] = len(signed) + signed_stars.index(rec) + 1
        group_label[id(rec)] = "commentary"
    for rec in unsigned_stars:
        rec["role"] = "drop"

    # A single signed note can continue below one or more intervening page-top
    # verses.  Gather it at its first occurrence so the reader sees the whole
    # note before the next verse, exactly as the page zones imply.  Only joins
    # across an actual page turn are collapsed; ordinary note paragraphs stay
    # separate.
    gathered_note_continuations = 0
    for group in signed:
        first = group[0]
        assembled = first["text"]
        previous = first
        for rec in group[1:]:
            if rec["page"] != previous["page"] and (
                assembled.rstrip().endswith("-") or rec["text"].lstrip()[:1].islower()
            ):
                assembled = assembled.rstrip()
                if assembled.endswith("-"):
                    assembled = assembled[:-1]
                    separator = ""
                else:
                    separator = " "
                assembled += separator + rec["text"].lstrip()
            else:
                assembled += "\n\n" + rec["text"]
            rec["role"] = "merged"
            previous = rec
            gathered_note_continuations += 1
        first["text"] = assembled
        first["one"] = assembled.replace("\n", " ")

    # Restore the numbered verses before emitting the note apparatus: the scan
    # puts lower-page notes between a verse broken at a page turn and its next
    # leaf continuation.  Append each asserted continuation to the preceding
    # numbered body paragraph, removing a wrap hyphen when present.
    merged_continuations = 0
    for rec in records:
        if rec["index"] not in BODY_CONTINUATIONS.get(rec["page"], set()):
            continue
        prior = next(
            (candidate for candidate in reversed(records[:records.index(rec)])
             if candidate["body"] and RULE_START.match(candidate["one"])),
            None,
        )
        if prior is None:
            raise AssertionError(f"no preceding verse for continuation on OCR page {rec['page']}")
        joiner = "" if prior["text"].rstrip().endswith("-") else " "
        prior["text"] = prior["text"].rstrip()
        if not joiner:
            prior["text"] = prior["text"][:-1]
        prior["text"] += joiner + rec["text"].lstrip()
        prior["one"] = prior["text"].replace("\n", " ")
        rec["role"] = "merged"
        merged_continuations += 1

    # Remove each dropped note's printed reference marker from the nearest
    # preceding retained paragraph. Superscript/dagger markers are unambiguous;
    # asterisk markers are removed only from paragraphs with odd star parity,
    # which distinguishes them from paired Markdown emphasis.
    unresolved = []
    retained_so_far = []
    dropped_starts = [g[0] for g in unsigned] + unsigned_stars
    dropped_ids = {id(r) for g in unsigned for r in g} | {id(r) for r in unsigned_stars}
    starts_by_id = {id(r): r for r in dropped_starts}
    removed_markers = 0
    for rec in records:
        if id(rec) in starts_by_id:
            marker = rec["one"][0]
            if marker == "\\":
                marker = "*"
            found = False
            for prior in reversed(retained_so_far):
                candidate = prior["text"]
                if marker == "*":
                    if candidate.count("*") % 2 == 0:
                        continue
                elif marker not in candidate:
                    continue
                pos = candidate.rfind(marker)
                prior["text"] = candidate[:pos] + candidate[pos + 1:]
                prior["one"] = prior["text"].replace("\n", " ")
                removed_markers += 1
                found = True
                break
            if not found:
                unresolved.append((rec["page"] + 276, marker, rec["one"][:60]))
        if id(rec) not in dropped_ids:
            retained_so_far.append(rec)

    out_pages = [[] for _ in range(102)]
    introduced = set()
    for rec in records:
        if rec["role"] in {"drop", "merged"}:
            continue
        para = rec["text"]
        if rec["role"] == "commentary":
            number = group_number[id(rec)]
            label = (
                "*Pṛthūdaka commentary:*"
                if group_label[id(rec)] == "commentary"
                else "*Signed note retained for review:*"
            )
            if number not in introduced:
                if not introduced and group_label[id(rec)] == "commentary":
                    label += " Colebrooke attributes these worked examples to the commentator, but says that attribution is probable rather than certain."
                para = label + "\n\n" + para
                introduced.add(number)
            para = "\n".join("> " + line if line else ">" for line in para.splitlines())
        out_pages[rec["page"] - 1].append(para)
    revised = "\n\n".join(para for page in out_pages for para in page)
    if revised.count("*Pṛthūdaka commentary:*") != 126:
        raise AssertionError("certain commentary label count changed")
    if revised.count("*Signed note retained for review:*") != 4:
        raise AssertionError("uncertain signed-note label count changed")
    OUTPUT.write_text(revised + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    Path("voice-separation-report.txt").write_text(
        "Voice separation\n"
        f"signed numbered groups kept: {len(signed)}\n"
        f"certain Ch./Com. numbered groups: {len(certain_signed)}\n"
        f"other-signature numbered groups retained neutrally: {len(uncertain_signed)}\n"
        f"unsigned numbered groups dropped: {len(unsigned)}\n"
        f"signed star/dagger asides kept: {len(signed_stars)}\n"
        f"unsigned star/dagger asides dropped: {len(unsigned_stars)}\n"
        f"reference markers removed: {removed_markers}\n"
        f"page-turn verse continuations merged: {merged_continuations}\n"
        f"signed-note continuation paragraphs gathered: {gathered_note_continuations}\n"
        f"unresolved reference markers: {len(unresolved)}\n" +
        "".join(f"printed p.{p}: {m!r} before {sample}\n" for p, m, sample in unresolved),
        encoding="utf-8",
    )
    print(
        f"kept and marked {len(signed) + len(signed_stars)} signed note groups; "
        f"dropped {len(unsigned) + len(unsigned_stars)} unsigned editorial groups; "
        f"removed {removed_markers} markers; {len(unresolved)} unresolved"
    )


def repair_internal_splits() -> None:
    """Repair uniquely determined OCR layout splits inside retained prose."""
    text = OUTPUT.read_text(encoding="utf-8")
    literal = {
        "BRAHME-SPHUÚA-SIDD'HÁNTA": "BRAHME-SPHUTA-SIDD'HÁNTA",
        "> dropped, they are 1 2 3 4 The number given is 87. It is the profit (§ 16). Deduct-\n> 12 30 20 15\n>\n> ing the sum":
            "> dropped, they are 1 2 3 4 The number given is 87. It is the profit (§ 16). Deducting the sum\n>\n> 12 30 20 15",
        "> the honey-jar, 6 ⅛. So water in the water-jar 31 ⅓; in the honey-jar, 12 ⅓; in the butter-\n> jar":
            "> the honey-jar, 6 ⅛. So water in the water-jar 31 ⅓; in the honey-jar, 12 ⅓; in the butter-jar",
        "> Where the common increase is unknown; divide in like manner the sum by the period, the quotient is the mean amount. Double it; and subtract twice the initial term: the quotient of the re-\n>\n> § Ibid. mainder":
            "> Where the common increase is unknown; divide in like manner the sum by the period, the quotient is the mean amount. Double it; and subtract twice the initial term: the quotient of the remainder",
        "> Diameter 10, multiplied by three, 30; this is the gross circum-\n>\n> ference.":
            "> Diameter 10, multiplied by three, 30; this is the gross circumference.",
    }
    revised = text
    for old, new in literal.items():
        if revised.count(old) != 1:
            raise AssertionError(f"internal-split anchor count {old[:60]!r}: {revised.count(old)}")
        revised = revised.replace(old, new)

    pattern = re.compile(
        r"> ru 9 Now, from the abso-\n>\n(?P<equation>> ya v 1 ya 10)\n>\n> lute number"
    )
    revised, count = pattern.subn(
        lambda m: "> ru 9 Now, from the absolute number\n>\n" + m.group("equation"), revised
    )
    if count != 1:
        raise AssertionError(f"absolute-number layout split count: {count}")

    pattern = re.compile(
        r"> the\] factum and absolute number is 90\. With the product \[of the coeffi-\n>\n"
        r"(?P<middle>> The multiplication of absolute number.*?Thence the rest is to be done as above directed\. Con\.) "
        r"cients\] of the unknown, namely 12, added, it becomes 102\.",
        re.S,
    )
    revised, count = pattern.subn(
        lambda m: (
            "> the] factum and absolute number is 90. With the product [of the coefficients] "
            "of the unknown, namely 12, added, it becomes 102.\n>\n" + m.group("middle")
        ),
        revised,
    )
    if count != 1:
        raise AssertionError(f"coefficient layout split count: {count}")

    OUTPUT.write_text(revised, encoding="utf-8")
    print("repaired 7 uniquely determined OCR/layout splits using asserted anchors")


def proofread_census_reading() -> None:
    """Apply the one final census reading settled from printed p.316."""
    text = OUTPUT.read_text(encoding="utf-8")
    old = "solid cubits or c'háris of Magad'ha"
    new = "solid cubits or c'hárís of Magad'ha"
    if text.count(old) != 1 or text.count(new) != 0:
        raise AssertionError(
            f"printed-p.316 anchor changed: old={text.count(old)}, new={text.count(new)}"
        )
    OUTPUT.write_text(text.replace(old, new), encoding="utf-8")
    print("repaired c'háris -> c'hárís at printed p.316 from the printed witness")


def final_structure() -> None:
    text = OUTPUT.read_text(encoding="utf-8")
    old = "#### SIMPLE EQUATION."
    new = "### SIMPLE EQUATION."
    lines = text.splitlines()
    if lines.count(old) != 1 or lines.count(new) != 0:
        raise AssertionError(f"simple-equation heading anchor: old={lines.count(old)}, new={lines.count(new)}")
    OUTPUT.write_text(text.replace(old, new), encoding="utf-8")
    print("normalized the final subsection heading with one asserted anchor")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "pass_name",
        choices=("initialize", "macrons-to-acutes", "remaining-macrons-to-acutes", "shape-headings", "voice-separation", "repair-internal-splits", "proofread-census-reading", "final-structure"),
    )
    args = parser.parse_args()
    if args.pass_name == "initialize":
        initialize()
    elif args.pass_name == "macrons-to-acutes":
        macrons_to_acutes()
    elif args.pass_name == "remaining-macrons-to-acutes":
        remaining_macrons_to_acutes()
    elif args.pass_name == "shape-headings":
        shape_headings()
    elif args.pass_name == "voice-separation":
        voice_separation()
    elif args.pass_name == "repair-internal-splits":
        repair_internal_splits()
    elif args.pass_name == "proofread-census-reading":
        proofread_census_reading()
    else:
        final_structure()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
