#!/usr/bin/env python3
"""Reproducibly post-process the published Alfarabi transcription.

This is deliberately tied to the known corpus input.  It refuses a different
file rather than making a plausible-looking edit against shifted anchors.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import re
import tempfile
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parent
DEFAULT_TEXT = WORKSPACE / "source" / "al-farabi-philosophy-of-plato-and-aristotle.md"
OCR_ROOT = Path("/Users/zacharygrunenberg/Projects/Enchiridion/ocr")
EXPECTED_SOURCE_SHA256 = "3a2dcb52f16d0fbd288ea354e14285724206f1dbbc5c5bd99365bc15138403eb"

SUPERSCRIPTS = "⁰¹²³⁴⁵⁶⁷⁸⁹"
SUP_TO_ASCII = str.maketrans(SUPERSCRIPTS, "0123456789")

PART_II_BLOCK = """Part II

The Philosophy of Plato

---

3
# THE PHILOSOPHY OF PLATO,
## ITS PARTS, THE RANKS OF ORDER
### OF ITS PARTS, FROM THE BEGINNING
#### TO THE END

i"""

PART_III_BLOCK = """# Part III

## The Philosophy of Aristotle

---

59
# THE PHILOSOPHY OF ARISTOTLE,

## THE PARTS OF HIS PHILOSOPHY,

### THE RANKS OF ORDER OF ITS PARTS,

### THE POSITION FROM WHICH HE

### STARTED AND THE ONE HE REACHED

#### i"""

MAIN_END = "\n132\nNotes\n\n---\n\n133\n\n# Part I: THE ATTAINMENT OF HAPPINESS"

MISSING_PAGE_127_ANCHOR = """there is here a certain intellect, uncom-

---

128
ALFARABI

these things belong to man so that he may attain this rank of being."""

MISSING_PAGE_127_REPAIR = """there is here a certain intellect, uncompounded and in act, that has engendered the primary intelligibles in the potential intellect and has equipped it by nature to receive all the other intelligibles.

## xix

98 When he investigated this intellect, he found that it is an intellect in act, had never been potential, and has always been and will always be (what has never been potential is not in a material, its substance and act are identical or close to being identical); when the human intellect achieves its ultimate perfection, its substance comes close to being the substance of this intellect. He called this intellect the *Active Intellect*. And it became evident to him that in achieving the perfection of its substance, the human intellect follows the example of this Intellect. This Intellect is the end because its example is followed in this manner, it is the most perfect end, and it is the agent. It is thus the principle of man as the agent, ultimately, of that which renders man substantial insofar as he is man. It is the end because it is that which gave him a principle with which to labor toward perfection and an example to follow in what he labors at, until he comes as close to it as he possibly can. It is, then, his agent, it is his end, and it is the perfection the substance of which man attempts to approach. Hence, it is a principle in three respects: as an agent, as an end, and as the perfection that man attempts to approach. It is therefore a separate form of man, a separate end and a prior end, and a separate agent; in some manner, man becomes united with it when it is intellected by him. And it became evident that the thing whose very substance and nature are nothing but mind can be intellected and can exist outside the intellect—there is no difference between these two modes of its existence. Hence it became clear that it is intellected by man only when he is not separated from it by an intermediary. In this way, the soul of man itself becomes this Intellect. Since the human soul is for the sake of this Intellect, the nature by which man acquires what is natural to him is for the sake of the soul only, and the soul is for the sake of the theoretical intellect in its highest perfection, it follows that all these things belong to man so that he may attain this rank of being."""

RUNNING_HEADER_RE = re.compile(
    r"^(?:\d+\s+)?(?:ALFARABI|THE ATTAINMENT OF HAPPINESS|"
    r"THE PHILOSOPHY OF PLATO|THE PHILOSOPHY OF ARISTOTLE)$"
)
BARE_NUMBER_RE = re.compile(r"^\d+$")
ROMAN_HEADING_RE = re.compile(r"(?m)^#{0,6}[ \t]*([ivxlcdm]+)[ \t]*$")


def require_count(text: str, anchor: str, expected: int, label: str) -> None:
    actual = text.count(anchor)
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected} occurrence(s), found {actual}")


def load_helper(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load helper: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(source: str) -> tuple[str, dict[str, int], str]:
    source_hash = hashlib.sha256(source.encode("utf-8")).hexdigest()
    if source_hash != EXPECTED_SOURCE_SHA256:
        raise AssertionError(
            "input SHA-256 differs from the reviewed corpus transcription: "
            f"expected {EXPECTED_SOURCE_SHA256}, found {source_hash}"
        )

    require_count(source, "# Part I\n## The Attainment of Happiness", 1, "main start")
    require_count(source, MAIN_END, 1, "main end")
    require_count(source, PART_II_BLOCK, 1, "Part II title block")
    require_count(source, PART_III_BLOCK, 1, "Part III title block")
    require_count(source, MISSING_PAGE_127_ANCHOR, 1, "omitted page 127 passage")

    start = source.index("# Part I\n## The Attainment of Happiness")
    end = source.index(MAIN_END)
    main = source[start:end]

    require_count(main, "## i\n\n1. The human things", 1, "Part I opening")
    main = main[main.index("## i\n\n1. The human things") :]
    main = "# PHILOSOPHY OF PLATO AND ARISTOTLE\n\n# PART I: THE ATTAINMENT OF HAPPINESS\n\n" + main
    main = main.replace(PART_II_BLOCK, "# PART II: THE PHILOSOPHY OF PLATO\n\n## i")
    main = main.replace(PART_III_BLOCK, "# PART III: THE PHILOSOPHY OF ARISTOTLE\n\n## i")
    main = main.replace(MISSING_PAGE_127_ANCHOR, MISSING_PAGE_127_REPAIR)

    leading_superscript_sections = 0

    def normalize_section_number(match: re.Match[str]) -> str:
        nonlocal leading_superscript_sections
        leading_superscript_sections += 1
        return match.group(1).translate(SUP_TO_ASCII) + " "

    main = re.sub(rf"(?m)^([{SUPERSCRIPTS}]+) (?=[A-Z])", normalize_section_number, main)
    if leading_superscript_sections != 6:
        raise AssertionError(
            f"leading section numerals: expected 6, found {leading_superscript_sections}"
        )

    footnote_markers = len(re.findall(rf"[{SUPERSCRIPTS}]+", main))
    main = re.sub(rf"[{SUPERSCRIPTS}]+", "", main)

    removed_furniture = 0
    kept_lines: list[str] = []
    for line in main.splitlines():
        stripped = line.strip()
        if (
            BARE_NUMBER_RE.fullmatch(stripped)
            or re.fullmatch(r"\d+\s+[a-z]", stripped)
            or RUNNING_HEADER_RE.fullmatch(stripped)
        ):
            removed_furniture += 1
            continue
        kept_lines.append(line)
    main = "\n".join(kept_lines) + "\n"

    roman_headings = len(ROMAN_HEADING_RE.findall(main))
    main = ROMAN_HEADING_RE.sub(lambda m: f"## {m.group(1)}", main)

    rules_before_rejoin = len(re.findall(r"(?m)^---\s*$", main))

    rejoin = load_helper(
        OCR_ROOT / "3-postprocess" / "rejoin-split-paragraphs.py", "enchiridion_rejoin"
    )
    hyphens = load_helper(
        OCR_ROOT / "3-postprocess" / "join-line-wrap-hyphens.py", "enchiridion_hyphens"
    )

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", dir=WORKSPACE / "tmp", encoding="utf-8", delete=False
    ) as handle:
        handle.write(main)
        temp_path = Path(handle.name)

    try:
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture):
            rejoin.process(
                temp_path,
                apply=True,
                do_rule=True,
                do_blank=False,
                verse=False,
                categories=None,
                min_words=0,
            )
        rejoin_report = capture.getvalue()
        match = re.search(r"rejoin (\d+) paragraph pair", rejoin_report)
        if not match:
            raise AssertionError(f"could not read rejoin count from:\n{rejoin_report}")
        rejoined = int(match.group(1))
        main = temp_path.read_text(encoding="utf-8")
        remaining_lines = main.splitlines()
        remaining_rule_contexts: list[str] = []
        remaining_mask = rejoin.build_structural_mask(remaining_lines)
        for index, line in enumerate(remaining_lines):
            if line.strip() == "---":
                prev_index = rejoin.find_neighbor(remaining_lines, index, -1)
                next_index = rejoin.find_neighbor(remaining_lines, index, 1)
                prev_line = remaining_lines[prev_index] if prev_index >= 0 else "<NONE>"
                next_line = remaining_lines[next_index] if next_index >= 0 else "<NONE>"
                category = rejoin.classify_pair(prev_line, next_line)
                remaining_rule_contexts.append(
                    f"category={category!r} mask=({remaining_mask[prev_index]},"
                    f"{remaining_mask[index]},{remaining_mask[next_index]}) "
                    f"PREV={prev_line[-100:]} NEXT={next_line[:100]}"
                )
        if remaining_rule_contexts:
            rejoin_report += "\nREMAINING RULE CONTEXTS:\n" + "\n".join(remaining_rule_contexts) + "\n"
    finally:
        temp_path.unlink(missing_ok=True)

    forced_page_joins = (
        (r"could not lead us to\n(?:[ \t]*\n)*---[ \t]*\n(?:[ \t]*\n)*different convictions", "could not lead us to different convictions"),
        (r"a certain way of life\.\n(?:[ \t]*\n)*---[ \t]*\n(?:[ \t]*\n)*All this", "a certain way of life. All this"),
        (r"has priority,\n(?:[ \t]*\n)*---[ \t]*\n(?:[ \t]*\n)*and the speech", "has priority, and the speech"),
        (r"those four things\.\n(?:[ \t]*\n)*---[ \t]*\n(?:[ \t]*\n)*And although men", "those four things. And although men"),
        (r"belonging to man;\n(?:[ \t]*\n)*---[ \t]*\n(?:[ \t]*\n)*however, they", "belonging to man; however, they"),
    )
    forced_rejoined = 0
    for pattern, replacement in forced_page_joins:
        main, count = re.subn(pattern, replacement, main)
        if count != 1:
            raise AssertionError(f"forced page join {pattern!r}: expected 1, found {count}")
        forced_rejoined += count

    main, hyphens_joined, hyphens_kept, _decisions = hyphens.join(main)
    rules_remaining = len(re.findall(r"(?m)^---\s*$", main))
    main = re.sub(r"(?m)^---\s*\n?", "", main)
    main = re.sub(r"\n{3,}", "\n\n", main).strip() + "\n"

    counts = {
        "apparatus_prefix_chars_removed": start,
        "apparatus_suffix_chars_removed": len(source) - end,
        "leading_section_numerals_normalized": leading_superscript_sections,
        "footnote_markers_removed": footnote_markers,
        "page_furniture_lines_removed": removed_furniture,
        "roman_subheadings_normalized": roman_headings,
        "page_split_paragraphs_rejoined": rejoined,
        "page_split_paragraphs_force_rejoined": forced_rejoined,
        "line_wrap_hyphens_joined": hyphens_joined,
        "compound_hyphens_kept": hyphens_kept,
        "scan_break_rules_removed": rules_before_rejoin,
        "scan_break_rules_rejoined": rejoined,
        "scan_break_rules_stripped_after_rejoin": rules_remaining,
    }

    # Acceptance assertions derived from this exact, reviewed input.
    expected = {
        "leading_section_numerals_normalized": 6,
        "footnote_markers_removed": 281,
        "page_furniture_lines_removed": 212,
        "roman_subheadings_normalized": 31,
        "page_split_paragraphs_rejoined": 46,
        "page_split_paragraphs_force_rejoined": 5,
        "line_wrap_hyphens_joined": 9,
        "compound_hyphens_kept": 0,
        "scan_break_rules_removed": 56,
        "scan_break_rules_rejoined": 46,
        "scan_break_rules_stripped_after_rejoin": 5,
    }
    for key, value in expected.items():
        if counts[key] != value:
            raise AssertionError(
                f"{key}: expected {value}, found {counts[key]}; all counts={counts}"
            )

    forbidden = {
        "horizontal rules": r"(?m)^---\s*$",
        "bare page/margin numbers": r"(?m)^\d+\s*$",
        "running headers": r"(?m)^(?:\d+\s+)?(?:ALFARABI|THE ATTAINMENT OF HAPPINESS|THE PHILOSOPHY OF PLATO|THE PHILOSOPHY OF ARISTOTLE)\s*$",
        "superscript note markers": rf"[{SUPERSCRIPTS}]",
        "scholarly notes": r"(?m)^# Notes|^Notes$|^# INDEX$",
    }
    for label, pattern in forbidden.items():
        if re.search(pattern, main):
            raise AssertionError(f"residual {label}")

    if main.count("# PHILOSOPHY OF PLATO AND ARISTOTLE") != 1:
        raise AssertionError("document title must occur exactly once")
    if len(re.findall(r"(?m)^# PART (?:I|II|III):", main)) != 3:
        raise AssertionError("expected exactly three part headings")

    part_starts = [main.index(f"# PART {label}:") for label in ("I", "II", "III")]
    part_ends = part_starts[1:] + [len(main)]
    expected_sections = [list(range(1, 65)), list(range(1, 39)), list(range(1, 100))]
    for label, start_at, end_at, expected_numbers in zip(
        ("I", "II", "III"), part_starts, part_ends, expected_sections
    ):
        numbers = [
            int(number)
            for number in re.findall(r"(?m)^(\d+)(?:\.|\s)", main[start_at:end_at])
        ]
        if numbers != expected_numbers:
            raise AssertionError(
                f"Part {label} numbered-section sequence differs: "
                f"expected {expected_numbers}, found {numbers}"
            )

    return main, counts, rejoin_report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", nargs="?", type=Path, default=DEFAULT_TEXT)
    parser.add_argument("--apply", action="store_true", help="write the repaired markdown")
    args = parser.parse_args()

    source = args.text.read_text(encoding="utf-8")
    result, counts, _report = build(source)

    for key, value in counts.items():
        print(f"{key}: {value}")
    print(f"output_lines: {len(result.splitlines())}")
    print(f"output_words: {len(result.split())}")
    print(f"output_sha256: {hashlib.sha256(result.encode('utf-8')).hexdigest()}")

    if args.apply:
        args.text.write_text(result, encoding="utf-8")
        print(f"wrote {args.text}")
    else:
        print("dry-run; pass --apply to write")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
