#!/usr/bin/env python3
r"""Rejoin paragraphs that were split by OCR artifacts.

Two split patterns occur in OCR'd markdown:

  (a) Stray `---` rules from page breaks, Stephanus markers, or other layout
      artifacts that the OCR converter reified as horizontal rules.
  (b) Blank-line splits with no rule between them — when a page break,
      footnote-body intrusion, or in-line image was stripped during
      post-processing, the surrounding prose was left as two paragraphs.

This script handles both, with separate modes:

  --rule        Look at `---` separators (legacy behavior). Useful for
                non-math texts where `---` rarely appears in tables.
  --blank       Look at blank-line separators where the previous line ends
                mid-clause (no terminal punctuation) and the next line
                looks like a continuation (lowercase, opens with an
                editorial `[`, etc.). Better fit for math-heavy texts.

By default neither mode is on — pass at least one. Dry-run is the default;
add `--apply` to write changes.

Continuation-friendly endings (signal that prev wants to continue):
  - last char is a letter or digit (mid-word OR ends without punctuation)
  - last char is one of `, ( — –` (comma, open paren, em/en dash)

Real-boundary signals (suppress the join):
  - prev ends with terminal punctuation `.!?:;` or closing quote `"'”’)]`
  - next starts with a structural marker:
      * markdown heading (`#`)
      * list item (`-`, `*`, `+`, or `<digit>.`)
      * blockquote (`>`)
      * speaker tag (all-caps NAME:)
      * table row (`|`)
      * image (`![`)
      * code fence (` ``` `)
      * display math (`$$`)
  - either line is inside a code fence or display-math region

Note: the heuristic does not attempt to handle "ends with `.` but the
next paragraph is a continuation" cases. Those need eyeball triage —
review the dry-run report rather than encoding more rules.

For verse texts, pass `--verse` to join with a newline instead of a space
so the verse-line boundary is preserved for the layout="verse" renderer.

Usage:
    python3 ocr/rejoin-split-paragraphs.py <markdown> --blank
    python3 ocr/rejoin-split-paragraphs.py <markdown> --rule --apply
    python3 ocr/rejoin-split-paragraphs.py <markdown> --rule --blank
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


RULE_RE = re.compile(r"^\s*---\s*$")
SPEAKER_RE = re.compile(r"^[A-Z][A-Z' ]+:")
LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+\.|\d+\\\.)\s")
FENCE_RE = re.compile(r"^\s*```")
DISPLAY_MATH_RE = re.compile(r"^\s*\$\$")
# Figure-caption lines (`Fig. 5.13`, `Fig. B`, `Fig. M`, `Fig. Q`, etc.).
# These are short standalone lines that label an image and must not be
# merged with whatever follows.
FIGURE_CAPTION_RE = re.compile(r"^\s*Fig\.\s+[A-Z0-9][A-Za-z0-9.,\s()]*$")
# Bracketed-letter list items (`[a]`, `[b]`, `[ii]`, `[M.T. I]`, etc.).
# Used in classical-math editions as an enumeration mechanism. Treat the
# opener as a list-item boundary so the lead-in sentence isn't merged.
BRACKET_ENUM_RE = re.compile(r"^\s*\[[a-z]\]\s|^\s*\[[ivx]+\]\s|^\s*\[[A-Z]\]\s")
# Classical-proof discourse markers: short declarative lines that
# introduce a theorem statement or display equation. These should remain
# their own paragraph so the rendered text reads:
#   I say that
#   [display math block]
# rather than getting merged with the equation back into one line.
PROOF_INTRO_RE = re.compile(
    r"^\s*(?:"
    r"I say(?:,| that)|"
    r"We say(?:,| that)|"
    r"Then I say(?:,| that)|"
    r"I claim(?:,| that)|"
    r"We claim(?:,| that)|"
    r"\[?Proof:\]?"
    r")\b"
)
TERMINAL_PUNCT = set(".!?:;\"'”’)]")
# `-` : a paragraph ending in a hyphen is a mid-word page-break split
# (`παραλ-` / `ληλόγραμμον`); unambiguous continuation.
CONTINUATION_PUNCT = set(",(—–-")


def is_blank(line: str) -> bool:
    return line.strip() == ""


def starts_structural(nxt: str) -> bool:
    """True if `nxt` opens with something that's a hard paragraph boundary."""
    s = nxt.lstrip()
    if not s:
        return True
    if s.startswith("#"):
        return True
    if s.startswith("<"):
        # HTML tag or comment (interlinear divs, page markers) — never a
        # prose continuation.
        return True
    if s.startswith(">"):
        return True
    if LIST_RE.match(s):
        return True
    if SPEAKER_RE.match(s):
        return True
    if s.startswith("|"):
        return True
    if s.startswith("!["):
        return True
    if s.startswith("```"):
        return True
    if s.startswith("$$"):
        return True
    if FIGURE_CAPTION_RE.match(s):
        return True
    if BRACKET_ENUM_RE.match(s):
        return True
    return False


def is_structural_line(line: str) -> bool:
    """True if this line itself is a structural element (heading, table row,
    figure caption, image, etc.) and must not be merged with neighbors."""
    s = line.strip()
    if not s:
        return True
    if s.startswith("#"):
        return True
    if s.startswith("<"):
        return True
    if s.startswith("|"):
        return True
    if s.startswith("!["):
        return True
    if s.startswith("```"):
        return True
    if FIGURE_CAPTION_RE.match(s):
        return True
    if LIST_RE.match(s):
        return True
    return False


def prev_wants_continuation(prev: str) -> bool:
    """True if prev's last char suggests the sentence isn't done."""
    p = prev.rstrip()
    if not p:
        return False
    if RULE_RE.match(p):
        # A `---` page-break rule ends with '-' but is never a wrapped
        # word; --rule mode owns these.
        return False
    last = p[-1]
    if last in TERMINAL_PUNCT:
        return False
    if last in CONTINUATION_PUNCT:
        return True
    # Mid-word / no-punctuation ending: letters, digits, closing markdown
    # emphasis, etc. all count as "wants continuation".
    if last.isalnum():
        return True
    return False


def next_looks_like_continuation(nxt: str) -> bool:
    """True if nxt's leading content looks like a sentence continuation."""
    s = nxt.lstrip()
    if not s:
        return False
    if starts_structural(s):
        return False
    # Editorial bracket continuation: `[these falling objects] were not …`
    if s.startswith("["):
        return True
    # Lowercase opener is the canonical continuation signal.
    if s[0].islower():
        return True
    # Capitalized opener: could be a proper noun continuing the prior clause,
    # or could be a new sentence. We allow it; triage in dry-run.
    return True


def classify_pair(prev: str, nxt: str, min_words: int = 0) -> str | None:
    """Return a category label if the pair looks rejoinable, else None.

    `min_words`: if > 0, pairs where either prev or next has fewer words
    than the threshold get a `-short` suffix on the category, so they
    can be triaged/filtered separately. Default 0 means no bucketing.
    """
    if is_structural_line(prev):
        return None
    if is_structural_line(nxt):
        return None
    if not prev_wants_continuation(prev):
        return None
    if starts_structural(nxt):
        return None
    if not next_looks_like_continuation(nxt):
        return None
    # Suppress proof-intro discourse markers: `I say that` lines and similar
    # should remain their own paragraph so the rendered output reads as a
    # discourse marker followed by a display equation, not as one prose run.
    if PROOF_INTRO_RE.match(prev):
        return None

    p = prev.rstrip()
    s = nxt.lstrip()
    last = p[-1]
    first = s[0]

    if last in CONTINUATION_PUNCT:
        cat = f"continuation-punct-{last!r}"
    elif first == "[":
        cat = "next-opens-bracket"
    elif first.islower():
        cat = "next-lowercase"
    elif last.isalnum() and first.isupper():
        cat = "midword-then-capital"
    else:
        cat = "other"

    if min_words > 0:
        prev_words = len(prev.split())
        next_words = len(nxt.split())
        if prev_words < min_words or next_words < min_words:
            cat = f"{cat}-short"

    return cat


def build_structural_mask(lines: list[str]) -> list[bool]:
    """Mark each line that lives inside a code fence or display-math block.
    These lines must never be merged with anything."""
    mask = [False] * len(lines)
    in_fence = False
    in_math = False
    for i, ln in enumerate(lines):
        stripped = ln.strip()
        if not in_fence and not in_math and FENCE_RE.match(stripped):
            in_fence = True
            mask[i] = True
            continue
        if in_fence:
            mask[i] = True
            if FENCE_RE.match(stripped):
                in_fence = False
            continue
        # Display math: a line starting with $$ either opens or closes a
        # block. A line containing only `$$` toggles state; a one-liner
        # `$$ ... $$` is also possible but we treat the whole line as math.
        if DISPLAY_MATH_RE.match(stripped):
            mask[i] = True
            # If the line opens-and-closes on the same line ($$ … $$), don't
            # enter math state. Count $$ occurrences.
            occurrences = stripped.count("$$")
            if occurrences % 2 == 1:
                in_math = not in_math
            continue
        if in_math:
            mask[i] = True
            if "$$" in stripped:
                in_math = False
    return mask


def find_neighbor(lines: list[str], idx: int, direction: int) -> int:
    i = idx + direction
    while 0 <= i < len(lines):
        if not is_blank(lines[i]):
            return i
        i += direction
    return -1


def process(
    markdown_path: Path,
    apply: bool,
    do_rule: bool,
    do_blank: bool,
    verse: bool,
    categories: set[str] | None,
    min_words: int,
) -> int:
    text = markdown_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    all_report: list[tuple[str, int, str, str]] = []
    # We collect all candidates first; only those whose category is in
    # `categories` (or all, if categories is None) get materialized into drop/replace.
    pending: list[tuple[str, int, str, str, int, int]] = []
    # (mode, line_no_1based, category, merged, prev_i, next_i)

    if do_rule:
        structural = build_structural_mask(lines)
        for idx, ln in enumerate(lines):
            if not RULE_RE.match(ln):
                continue
            if structural[idx]:
                continue
            prev_i = find_neighbor(lines, idx, -1)
            next_i = find_neighbor(lines, idx, +1)
            if prev_i < 0 or next_i < 0:
                continue
            if structural[prev_i] or structural[next_i]:
                continue
            cat = classify_pair(lines[prev_i], lines[next_i], min_words)
            if cat is None:
                continue
            sep = "\n" if verse else " "
            merged = lines[prev_i].rstrip() + sep + lines[next_i].lstrip()
            pending.append(("rule", idx + 1, cat, merged, prev_i, next_i))

    if do_blank:
        structural = build_structural_mask(lines)
        sep = "\n" if verse else " "
        n = len(lines)
        i = 0
        while i < n:
            if is_blank(lines[i]) or structural[i]:
                i += 1
                continue
            j = i + 1
            saw_blank = False
            while j < n and is_blank(lines[j]):
                saw_blank = True
                j += 1
            if j >= n:
                break
            if not saw_blank or structural[j]:
                i = j
                continue
            if any(RULE_RE.match(lines[k]) for k in range(i + 1, j)):
                i = j
                continue
            cat = classify_pair(lines[i], lines[j], min_words)
            if cat is None:
                i = j
                continue
            merged = lines[i].rstrip() + sep + lines[j].lstrip()
            pending.append(("blank", i + 1, cat, merged, i, j))
            i = j + 1

    # Group for report.
    by_category: dict[str, list[tuple[str, int, str]]] = {}
    for mode, line_no, cat, merged, _p, _n in pending:
        by_category.setdefault(cat, []).append((mode, line_no, merged))

    for cat in sorted(by_category):
        entries = by_category[cat]
        marker = " (selected)" if categories and cat in categories else ""
        print(f"\n== {cat}  ({len(entries)}){marker} ==")
        for mode, line_no, merged in entries:
            preview = merged.replace("\n", " ⏎ ")
            if len(preview) > 140:
                preview = preview[:137] + "…"
            print(f"  [{mode}] L{line_no}: {preview}")

    drop: set[int] = set()
    replace: dict[int, str] = {}
    applied_count = 0
    for mode, line_no, cat, merged, prev_i, next_i in pending:
        if categories is not None and cat not in categories:
            continue
        replace[prev_i] = merged
        for k in range(prev_i + 1, next_i + 1):
            drop.add(k)
        applied_count += 1

    out: list[str] = []
    for i, ln in enumerate(lines):
        if i in drop:
            continue
        out.append(replace.get(i, ln))

    if apply:
        trailing_nl = "\n" if text.endswith("\n") else ""
        markdown_path.write_text("\n".join(out) + trailing_nl, encoding="utf-8")

    verb = "would " if not apply else ""
    print()
    if categories is not None:
        print(
            f"{verb}rejoin {applied_count} of {len(pending)} candidate(s) "
            f"(categories: {', '.join(sorted(categories))})"
        )
    else:
        print(f"{verb}rejoin {len(pending)} paragraph pair(s)")
    if not apply and (applied_count or len(pending)):
        print("(dry-run — pass --apply to write changes)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--apply", action="store_true", help="Write changes (default: dry-run)")
    parser.add_argument("--rule", action="store_true", help="Rejoin across stray `---` rules")
    parser.add_argument("--blank", action="store_true", help="Rejoin across blank-line gaps")
    parser.add_argument("--verse", action="store_true", help="Join with newline instead of space")
    parser.add_argument(
        "--categories",
        type=str,
        default=None,
        help=(
            "Semicolon-separated category names to apply (others are still reported "
            "but not merged). Categories: continuation-punct-',', next-lowercase, "
            "next-opens-bracket, midword-then-capital, other. If omitted, all "
            "categories are applied."
        ),
    )
    parser.add_argument(
        "--min-words",
        type=int,
        default=0,
        help=(
            "If set, candidates where either prev or next has fewer words than N "
            "get a `-short` suffix added to their category, so they can be "
            "filtered/inspected separately. Default 0 means no bucketing."
        ),
    )
    args = parser.parse_args()

    if not args.markdown.exists():
        print(f"error: {args.markdown} does not exist", file=sys.stderr)
        return 2

    if not args.rule and not args.blank:
        print("error: pass at least one of --rule or --blank", file=sys.stderr)
        return 2

    categories: set[str] | None = None
    if args.categories:
        categories = {c.strip() for c in args.categories.split(";") if c.strip()}

    return process(
        args.markdown, args.apply, args.rule, args.blank, args.verse, categories, args.min_words
    )


if __name__ == "__main__":
    sys.exit(main())
