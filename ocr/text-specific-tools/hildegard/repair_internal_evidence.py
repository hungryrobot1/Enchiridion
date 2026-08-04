#!/usr/bin/env python3
"""Apply Hildegard repairs licensed by internal stage-3 evidence.

Licence: each repaired reading is impossible in English (or a character from a
script this English text does not use), and exactly one repair is available.
No printed witness is invoked.  Ambiguous readings are asserted unchanged.

The CLI is dry-run by default.  ``build_hildegard.py`` imports ``repair_text``
and applies it in memory so a clean rebuild includes this pass automatically.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


# These are the words immediately following a standalone ABBYY ``1`` at sites
# where English syntax requires the first-person pronoun.  The set is bound to
# this document by the 150-site census and the per-follower counts below.
DIGIT_I_FOLLOWERS = {
    "again", "also", "am", "can", "commit", "could", "did", "do",
    "dwell", "fear", "further", "had", "have", "heard", "help", "lode",
    "look", "love", "never", "not", "rise", "rose", "saw", "should",
    "tear", "then", "think", "truly", "was", "who", "will", "wish",
    "work",
}
EXPECTED_DIGIT_FOLLOWERS = Counter({
    "saw": 59, "also": 19, "heard": 15, "again": 10, "then": 6,
    "will": 5, "could": 2, "who": 2, "had": 2,
    "am": 1, "can": 1, "commit": 1, "did": 1, "do": 1, "dwell": 1,
    "fear": 1, "further": 1, "have": 1, "help": 1, "lode": 1,
    "look": 1, "love": 1, "never": 1, "not": 1, "rise": 1,
    "rose": 1, "should": 1, "tear": 1, "think": 1, "truly": 1,
    "was": 1, "wish": 1, "work": 1,
})
EXPECTED_GENUINE_DIGIT_FOLLOWERS = Counter({"the": 5, "and": 1})

DIGIT_WORD_RE = re.compile(r"(?<!\d)\b1\s+([A-Za-z]+)")
COMMA_PARAGRAPH = "5.1, however, saw"

SLASH_FOLLOWERS = Counter({
    "will": 2, "be": 1, "was": 1, "never": 1, "am": 1,
    "thundered": 1, "also": 1, "thought": 1, "renewed": 1,
    "placed": 1, "cortfused": 1,
})
SLASH_WORD_RE = re.compile(r"(?<!\w)/\s+([A-Za-z]+)")

# Exact-anchor repairs.  Every source form is impossible in English and the
# replacement is the only available reading; counts prevent scope drift.
EXACT_REPAIRS = [
    ("yourseff", "yourself", 1),
    ("failltful", "faithful", 1),
    ("lheir", "their", 1),
    ("per son", "person", 1),
    ("WILLBE", "WILL BE", 1),
    ("BLESSEDONES", "BLESSED ONES", 1),
    ("THEFACTTHATA", "THE FACT THAT A", 2),
    ("TOMEN", "TO MEN", 1),
    ("cortfused", "confused", 1),
    ("0 Lord", "O Lord", 2),
]

# Word-bounded because ``LUKE`` is a valid name elsewhere in the text.
WORD_REPAIRS = [(re.compile(r"\bUKE\b"), "LIKE", 1)]

CONFUSABLES = [("Ό", "O", 2), ("Ί", "I", 2)]

# The neighbors make exactly one value available; these are sequence repairs,
# not guesses about glyph shape.
SEQUENCE_REPAIRS = [
    ("## S3 THE DEVIL WILL NOT PREVAIL", "## 53 THE DEVIL WILL NOT PREVAIL", 1),
    ("## Ill REPENTANCE CONCERNING MURDER OUT OF NECESSITY", "## 111 REPENTANCE CONCERNING MURDER OUT OF NECESSITY", 1),
    ("## IIS REPENTANCE OF THE MOTHER KILLING THE INFANT BORN FROM HERSELF", "## 115 REPENTANCE OF THE MOTHER KILLING THE INFANT BORN FROM HERSELF", 1),
    ("II. A man who practices robbery", "77. A man who practices robbery", 1),
]

# More than one repair is plausible.  These counts must survive unchanged.
AMBIGUOUS = {
    "Wenks": 1,
    "pilch": 1,
    "Cue": 4,
    "{Hide": 1,
    "creatine": 1,
    "Sdll": 1,
    "it»": 1,
}


def repair_text(text: str) -> tuple[str, dict[str, int]]:
    stats: dict[str, int] = {}
    before_ambiguous = {token: text.count(token) for token in AMBIGUOUS}
    assert before_ambiguous == AMBIGUOUS, before_ambiguous

    # The answered instruction names 99 whitespace-shaped ``number.1``
    # openings.  One additional comma-bearing form has the same unique syntax.
    whitespace_openings = re.findall(r"(?m)^\d+\.1\s+[A-Za-z]+", text)
    assert len(whitespace_openings) == 99, len(whitespace_openings)
    assert text.count(COMMA_PARAGRAPH) == 1
    text = text.replace(COMMA_PARAGRAPH, "5. I, however, saw")
    stats["digit_i_comma_openings"] = 1

    all_digit_sites = list(DIGIT_WORD_RE.finditer(text))
    follower_counts = Counter(m.group(1).lower() for m in all_digit_sites)
    licensed_counts = Counter({
        word: count for word, count in follower_counts.items()
        if word in DIGIT_I_FOLLOWERS
    })
    genuine_counts = follower_counts - licensed_counts
    assert licensed_counts == EXPECTED_DIGIT_FOLLOWERS, licensed_counts
    assert genuine_counts == EXPECTED_GENUINE_DIGIT_FOLLOWERS, genuine_counts
    assert sum(follower_counts.values()) == 150

    changed_digit = 0

    def replace_digit(match: re.Match[str]) -> str:
        nonlocal changed_digit
        follower = match.group(1)
        if follower.lower() not in DIGIT_I_FOLLOWERS:
            return match.group(0)
        changed_digit += 1
        # ``3.1 saw`` needs the space that ABBYY lost between paragraph number
        # and pronoun; ordinary ``and 1 saw`` already has its leading space.
        prefix = " I " if match.start() and text[match.start() - 1] == "." else "I "
        return prefix + follower

    text = DIGIT_WORD_RE.sub(replace_digit, text)
    assert changed_digit == 144, changed_digit
    stats["digit_i_word_sites"] = changed_digit
    stats["digit_i_total"] = changed_digit + 1
    stats["genuine_digit_sites_left"] = sum(genuine_counts.values())

    slash_sites = list(SLASH_WORD_RE.finditer(text))
    slash_counts = Counter(m.group(1).lower() for m in slash_sites)
    assert slash_counts == SLASH_FOLLOWERS, slash_counts
    text, slash_changed = SLASH_WORD_RE.subn(lambda m: "I " + m.group(1), text)
    assert slash_changed == 12
    stats["slash_i_total"] = slash_changed

    exact_total = 0
    for source, replacement, expected in EXACT_REPAIRS:
        count = text.count(source)
        assert count == expected, f"{source!r}: expected {expected}, got {count}"
        text = text.replace(source, replacement)
        exact_total += count

    word_total = 0
    for pattern, replacement, expected in WORD_REPAIRS:
        text, count = pattern.subn(replacement, text)
        assert count == expected, f"{pattern.pattern}: expected {expected}, got {count}"
        word_total += count

    confusable_total = 0
    for source, replacement, expected in CONFUSABLES:
        count = text.count(source)
        assert count == expected, f"{source!r}: expected {expected}, got {count}"
        text = text.replace(source, replacement)
        confusable_total += count

    sequence_total = 0
    for source, replacement, expected in SEQUENCE_REPAIRS:
        count = text.count(source)
        assert count == expected, f"{source!r}: expected {expected}, got {count}"
        text = text.replace(source, replacement)
        sequence_total += count

    stats["exact_word_repairs"] = exact_total + word_total
    stats["confusable_repairs"] = confusable_total
    stats["sequence_repairs"] = sequence_total

    # The instruction's example is absent; assert that this source does not
    # silently acquire a new member of that family without review.
    assert text.count("DIFERENTIATED") == 0

    remaining = Counter(m.group(1).lower() for m in DIGIT_WORD_RE.finditer(text))
    assert remaining == EXPECTED_GENUINE_DIGIT_FOLLOWERS, remaining
    assert COMMA_PARAGRAPH not in text
    assert not SLASH_WORD_RE.search(text)
    for source, _replacement, _expected in EXACT_REPAIRS:
        assert source not in text
    assert not re.search(r"\bUKE\b", text)
    assert "Ό" not in text and "Ί" not in text
    for source, _replacement, _expected in SEQUENCE_REPAIRS:
        assert source not in text
    after_ambiguous = {token: text.count(token) for token in AMBIGUOUS}
    assert after_ambiguous == before_ambiguous, (before_ambiguous, after_ambiguous)
    return text, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    source = args.markdown.read_text(encoding="utf-8")
    repaired, stats = repair_text(source)
    if args.apply:
        args.markdown.write_text(repaired, encoding="utf-8")
    verb = "repaired" if args.apply else "would repair"
    print(
        f"{verb}: digit 1→I {stats['digit_i_total']} (left genuine "
        f"{stats['genuine_digit_sites_left']}), slash→I {stats['slash_i_total']}, "
        f"exact words {stats['exact_word_repairs']}, confusables "
        f"{stats['confusable_repairs']}, sequence repairs "
        f"{stats['sequence_repairs']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
