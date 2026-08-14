#!/usr/bin/env python3
"""Build the proposed Leibniz volume from the OCR and asserted repairs."""

from __future__ import annotations

import re
import importlib.util
from pathlib import Path

import strip_latta_apparatus


PAGES = Path("leibniz-pages.md")
OUT = Path("leibniz-monadology-and-other-philosophical-writings.md")
REJOIN = Path(
    "/Users/zacharygrunenberg/Projects/Enchiridion/ocr/3-postprocess/"
    "rejoin-split-paragraphs.py"
)
RULE = "\n\n---\n\n"


def replace_once(text: str, before: str, after: str) -> str:
    assert text.count(before) == 1, (before, text.count(before))
    return text.replace(before, after)


def sequential_rule_rejoin(text: str) -> tuple[str, int]:
    """Apply the shipped rejoiner's classifier without overlapping rewrites."""
    spec = importlib.util.spec_from_file_location("pipeline_rejoin", REJOIN)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    count = 0
    while True:
        changed = False
        for match in re.finditer(r"([^\n]+)\n\n---\n\n([^\n]+)", text):
            previous, following = match.group(1), match.group(2)
            if not module.prev_wants_continuation(previous):
                continue
            if not module.next_looks_like_continuation(following):
                continue
            text = text[:match.start()] + previous.rstrip() + " " + following.lstrip() + text[match.end():]
            count += 1
            changed = True
            break
        if not changed:
            return text, count


def main() -> None:
    strip_latta_apparatus.main()
    text = PAGES.read_text()

    # Reader structure: the first h1 is the collected-volume title; each work
    # begins at a later h1. The repeated Third Explanation head is furniture.
    text = "# LEIBNIZ: THE MONADOLOGY AND OTHER PHILOSOPHICAL WRITINGS\n\n" + text
    full_third = (
        "THIRD EXPLANATION—EXTRACT FROM A LETTER OF M. D. L. REGARDING HIS "
        "PHILOSOPHICAL HYPOTHESIS AND THE CURIOUS PROBLEM, PROPOUNDED TO THE "
        "MATHEMATICIANS BY ONE OF HIS FRIENDS, WITH AN EXPLANATION REGARDING "
        "SOME DISPUTED POINTS IN PRECEDING JOURNALS BETWEEN THE AUTHOR OF THE "
        "PRINCIPLES OF PHYSICS AND THE AUTHOR OF THE OBJECTIONS. 1696."
    )
    text = replace_once(text, full_third, "# " + full_third)
    text = replace_once(text, "\n\n### THIRD EXPLANATION\n", "\n")
    text = replace_once(text, "# INTRODUCTION.", "## INTRODUCTION")
    text = replace_once(text, "SEPTEMBER 12, 1695 . 1696.", "SEPTEMBER 12, 1695. 1696.")

    # The discarded notes' markers survive in three OCR spellings.
    text, latex_markers = re.subn(r"\$\^\{(?:13|14|15)\}\$", "", text)
    assert latex_markers == 3, latex_markers
    text = replace_once(text, "body ᵇ.", "body.")
    text = replace_once(text, "✓4.", "4.")
    text = replace_once(text, "12 . But,", "12. But,")
    text = replace_once(text, "desire |l'appétit|", "desire [l'appétit]")
    text = replace_once(text, "(Thcod. 350.)", "(Théod. 350.)")
    text = replace_once(text, "(Thcod. 401-403.)", "(Théod. 401-403.)")
    text = replace_once(
        text,
        "truths, those of reason\n\n---\n\ning and those of fact",
        "truths, those of reasoning and those of fact",
    )
    text = replace_once(text, "\n\n2\n\n---\n\nwhich, although", "\n\n---\n\nwhich, although")
    # Printed p. 295 changes from Leibniz's body to Latta's notes after the
    # colon; printed p. 296 resumes the same body sentence.
    text = replace_once(
        text,
        "supreme power:\n\n---\n\noutside of the commonwealth",
        "supreme power: outside of the commonwealth",
    )
    text, rejoined = sequential_rule_rejoin(text)
    assert rejoined == 123, rejoined

    # Unambiguous page-turn word wraps. These are asserted individually rather
    # than passed through the generic hyphen joiner because two other page
    # turns lost whole phrases and would otherwise become plausible nonsense.
    joins = {
        "out- side": "outside",
        "Accord- ingly": "Accordingly",
        "arti- ficial": "artificial",
        "im- possible": "impossible",
        "ex- traordinary": "extraordinary",
        "Some thing similar": "Something similar",
        "con- templation": "contemplation",
        "him- self": "himself",
        "immor- tality": "immortality",
        "con- sist": "consist",
        "some- thing": "something",
        "sub- stance": "substance",
    }
    for before, after in joins.items():
        text = replace_once(text, before, after)

    # Stage-4 readings made from the supplied scan.
    text = replace_once(
        text,
        "would be dis-" + RULE + "9. Indeed,",
        "would be discernible from another.\n\n9. Indeed,",
    )
    text = replace_once(
        text,
        "minimum out- receptivity or capacity",
        "minimum outlay. And the time, the place, or, in a word, the "
        "receptivity or capacity",
    )
    text = replace_once(
        text,
        "bitter things must be com- who has not tasted",
        "bitter things must be combined with them, so as to stimulate the "
        "taste. He who has not tasted",
    )
    text = replace_once(
        text,
        "the principle of the best 76. (Théod. 7, 149, 150.)",
        "the principle of the best. (Théod. 7, 149, 150.)",
    )
    text = replace_once(
        text,
        "falling back into fanatical finds a ground for all phenomena",
        "falling back into fanatical philosophy, such as the Mosaic "
        "philosophy of Fludd, which finds a ground for all phenomena",
    )

    # Mistral rendered eighteen superscript note calls as baseline numerals.
    # Each asserted phrase is unambiguous in context and the printed pages
    # show the numeral raised above the line; Latta's corresponding editorial
    # notes have already been removed.
    baseline_note_calls = {
        "memory 34.": "memory.",
        "affection 35 is": "affection is",
        "future 38;": "future;",
        "motion 39.": "motion.",
        "effect 40.": "effect.",
        "false 50;": "false;",
        "known by us 51.": "known by us.",
        "punishments appear 34.": "punishments appear.",
        "young boy Cyrus 35,": "young boy Cyrus,",
        "ordinary body 42 of animals": "ordinary body of animals",
        "attributed to Hippocrates 43)": "attributed to Hippocrates)",
        "according to Aristotle 44;": "according to Aristotle;",
        "may some day occur 74.": "may some day occur.",
        "these perceptions 75,": "these perceptions,",
        "[distingué] enough 76,": "[distingué] enough,",
        "last for ever 77,": "last for ever,",
        "his personality 78.": "his personality.",
        "perceptions explain 79 that": "perceptions explain that",
    }
    for before, after in baseline_note_calls.items():
        text = replace_once(text, before, after)

    # The range selector cut on an apparatus heading rather than on the last
    # authorial line. Restore the body text printed above Appendices H and I.
    text = replace_once(
        text,
        "This law, being as good and as general as the other, deserved as" + RULE
        + "# THIRD EXPLANATION",
        "This law, being as good and as general as the other, deserved as "
        "little to be broken, and this is so, according to my system, in which "
        "there is conservation of force and direction, and none of the natural "
        "laws of bodies are broken, notwithstanding the changes which take "
        "place in body in consequence of changes in the soul.\n\n"
        "# THIRD EXPLANATION",
    )
    text = replace_once(
        text,
        "Although many substances have" + RULE + "# NEW ESSAYS",
        "Although many substances have already attained a great perfection, "
        "yet on account of the infinite divisibility of the continuous, there "
        "always remain in the abyss of things slumbering parts which have yet "
        "to be awakened, to grow in size and worth, and, in a word, to advance "
        "to a more perfect state [ad meliorem cultum]. And hence no end of "
        "progress is ever reached.\n\n# NEW ESSAYS",
    )

    # Page rules that did not split a paragraph are furniture.
    remaining_rules = text.count(RULE)
    assert remaining_rules == 58, remaining_rules
    text = text.replace(RULE, "\n\n")

    # Eleven page turns split a continuous printed paragraph but begin after
    # syntactically complete text, so the generic classifier conservatively
    # leaves them alone. Exact end/start anchors make the joins reviewable.
    paragraph_joins = {
        "which has made\n\nthem fall again": "which has made them fall again",
        "another point of view;\n\nactive in so far": "another point of view; active in so far",
        "the dif-\n\nference between nature": "the difference between nature",
        "genuine 'pure love,'\n\nwhich takes pleasure": "genuine 'pure love,' which takes pleasure",
        "sufficiently under-\n\nstand the order": "sufficiently understand the order",
        "we see\n\nalso that it is": "we see also that it is",
        "assumptions or what\n\nwe take for granted": "assumptions or what we take for granted",
        "we always pass from\n\nsmall to great": "we always pass from small to great",
        "imperceptible [insensible]\n\nprogressions": "imperceptible [insensible] progressions",
        "destroy our philosophy.\n\nwhich seeks reasons": "destroy our philosophy, which seeks reasons",
        "established in the universe,\n\neverything is done": "established in the universe, everything is done",
    }
    text, spacing_repairs = re.subn(r"[ \t]+([,.;:!?])", r"\1", text)
    assert spacing_repairs == 236, spacing_repairs
    for before, after in paragraph_joins.items():
        text = replace_once(text, before, after)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    OUT.write_text(text)
    print(
        f"wrote {OUT}: {len(text)} chars; {rejoined} page-turn paragraphs rejoined, "
        f"{remaining_rules} structural page rules removed, "
        f"{spacing_repairs} punctuation spaces normalized"
    )


if __name__ == "__main__":
    main()
