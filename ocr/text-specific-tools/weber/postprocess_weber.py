#!/usr/bin/env python3
"""Turn the 272-page Mistral OCR response into a structured review draft.

Every transformation is either page furniture/layout debris or a reading that
the document establishes internally, except for the explicitly documented
printed-page-237 source-defect repair.  That repair uses John Howe's public-
domain text only where surviving letters in the scan confirm the reading and
leaves the unsupported parenthetical marked as illegible.  The script refuses
if the raw extraction or any expected match count changes.
"""

from __future__ import annotations

import re
import importlib.util
from pathlib import Path


RAW = Path("raw.md")
OUT = Path("weber-protestant-ethic-and-spirit-of-capitalism.md")
PAGE_BREAK = "\n\n---\n\n"
RAW_CHARS = 579_767
RAW_PAGES = 272

TITLE = "THE PROTESTANT ETHIC AND THE SPIRIT OF CAPITALISM"

NOTES_91_TO_93 = """91. The Lutheran emphasis on penitent grief is foreign to the spirit of ascetic Calvinism, not in theory, but definitely in practice. For it is of no ethical value to the Calvinist; it does not help the damned, while for those certain of their election, their own sin, so far as they admit it to themselves, is a symptom of backwardness in development. Instead of repenting of it they hate it and attempt to overcome it by activity for the glory of God. Compare the explanation of Howe (Cromwell's chaplain 1656-58) in *Of Men's Enmity against God and of Reconciliation between God and Man* (*Works of English Puritan Divines*, p. 237): "The carnal mind is enmity against God. It is the mind, therefore, not as speculative merely, but as practical and active that must be renewed", and "reconciliation . . . must begin in (1) a deep conviction . . . of your former enmity. . . . I have been alienated from God. . . . (2) ([illegible]) clear and lively apprehension of the monstrous iniquity and wickedness thereof." The hatred here is that of sin, not of the sinner. But as early as the famous letter of the Duchess Renata d'Este (Leonore's mother) to Calvin, in which she speaks of the hatred which she would feel toward her father and husband if she became convinced they belonged to the damned, is shown the transfer to the person. At the same time it is an example of what was said above [pp. 104-6] of how the individual became loosed from the ties resting on his natural feelings, for which the doctrine of predestination was responsible.

92. "None but those who give evidence of being regenerate or holy persons ought to be received or counted fit members of visible Churches. Where this is wanting, the very essence of a Church is lost", as the principle is put by Owen, the Independent-Calvinistic Vice-Chancellor of Oxford under Cromwell (*Inv. into the Origin of Ev. Ch.*). Further, see the following essay (not translated here.—TRANSLATOR).

93. See following essay."""

# Running heads.  Mistral sometimes emits them as headings, sometimes italic,
# and sometimes glues the first body words to the same line.
RUNNING_HEADS = (
    "The Protestant Ethic and the Spirit of Capitalism",
    "The Protestant Ethic and the Spirit of Capitancy",
    "Author's Introduction",
    "Introduction",
    "Religious Affiliation and Social Stratification",
    "The Spirit of Capitalism",
    "Luther's Conception of the Calling",
    "The Religious Foundations of Worldly Asceticism",
    "Asceticism and the Spirit of Capitalism",
    "Notes",
)
HEAD_ALT = "|".join(re.escape(x) for x in sorted(RUNNING_HEADS, key=len, reverse=True))
HEAD_RE = re.compile(rf"^(?:#{{1,3}}\s+)?\*?(?:{HEAD_ALT})\*?(?=\s|$)\s*")

STRUCTURAL_LINES = {
    "# AUTHOR'S INTRODUCTION",
    "# PART I",
    "# THE PROBLEM",
    "# CHAPTER I",
    "# RELIGIOUS AFFILIATION AND SOCIAL STRATIFICATION¹",
    "# CHAPTER II",
    "## THE SPIRIT OF CAPITALISM",
    "# CHAPTER III",
    "## CHAPTER II",
    "# LUTHER'S CONCEPTION OF THE CALLING",
    "# TASK OF THE INVESTIGATION",
    "# PART II",
    "# THE PRACTICAL ETHICS OF THE ASCETIC BRANCHES OF PROTESTANTISM",
    "## THE RELIGIOUS FOUNDATIONS OF WORLDLY ASCETICISM",
    "## ASCETICISM AND THE SPIRIT OF CAPITALISM",
    "# NOTES",
    "# INTRODUCTION",
}

INSERT = {
    1: f"# {TITLE}\n\n# AUTHOR'S INTRODUCTION",
    21: "# PART I\n\nTHE PROBLEM",
    23: "## CHAPTER I\n\n### RELIGIOUS AFFILIATION AND SOCIAL STRATIFICATION",
    35: "## CHAPTER II\n\n### THE SPIRIT OF CAPITALISM",
    67: "## CHAPTER III\n\n### LUTHER'S CONCEPTION OF THE CALLING\n\n#### TASK OF THE INVESTIGATION",
    81: "# PART II\n\nTHE PRACTICAL ETHICS OF THE ASCETIC BRANCHES OF PROTESTANTISM",
    83: "## CHAPTER IV\n\n### THE RELIGIOUS FOUNDATIONS OF WORLDLY ASCETICISM",
    143: "## CHAPTER V\n\n### ASCETICISM AND THE SPIRIT OF CAPITALISM",
    173: "# NOTES\n\n## INTRODUCTION",
}


def replace_exact(text: str, old: str, new: str, expected: int, label: str) -> str:
    actual = text.count(old)
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected} matches, found {actual}")
    return text.replace(old, new)


def strip_furniture(page: str, page_number: int) -> tuple[str, int]:
    removed = 0
    out = []
    for line in page.splitlines():
        # From prepared page 173 onward these are the printed divisions of the
        # consolidated authorial notes, not running heads.
        is_notes_chapter = page_number >= 173 and re.fullmatch(
            r"#{1,2} CHAPTER (?:I|II|III|IV|V)", line.strip()
        )
        if line.strip() in STRUCTURAL_LINES and not is_notes_chapter:
            removed += 1
            continue
        match = HEAD_RE.match(line.strip())
        if match:
            remainder = line.strip()[match.end():]
            # A starred running head can swallow the continuation's closing
            # emphasis marker (raw page 16).  The printed prose is not italic.
            if remainder.endswith(".*") and line.strip().startswith("*"):
                remainder = remainder[:-1]
            removed += 1
            if remainder:
                out.append(remainder)
            continue
        out.append(line)
    return "\n".join(out).strip(), removed


def join_page_boundary(left: str, right: str) -> tuple[str, bool]:
    """Join a sentence split by a physical leaf, never a structural boundary."""
    if not left or not right or right.startswith("#"):
        return left + ("\n\n" if left and right else "") + right, False
    lparts = left.rsplit("\n\n", 1)
    rparts = right.split("\n\n", 1)
    tail, head = lparts[-1].rstrip(), rparts[0].lstrip()
    if not tail or not head or tail[-1] in '.!?:;"”’)]':
        return left + "\n\n" + right, False
    sep = "" if tail.endswith("-") else " "
    if tail.endswith("-"):
        tail = tail[:-1]
    joined = tail + sep + head
    before = (lparts[0] + "\n\n") if len(lparts) == 2 else ""
    after = ("\n\n" + rparts[1]) if len(rparts) == 2 else ""
    return before + joined + after, True


def main() -> None:
    raw = RAW.read_text(encoding="utf-8")
    if len(raw) != RAW_CHARS:
        raise AssertionError(f"expected {RAW_CHARS} raw characters, found {len(raw)}")
    pages = raw.split(PAGE_BREAK)
    if len(pages) != RAW_PAGES:
        raise AssertionError(f"expected {RAW_PAGES} pages, found {len(pages)}")

    # The scan leaf is otherwise blank; these are a reader's pencil words, not
    # Weber's text.  The exact OCR page is asserted before removal.
    if pages[81].strip() != "51 Read\nwhen I\nreturn":
        raise AssertionError("prepared page 82 marginalia anchor changed")
    pages[81] = ""

    furniture = 0
    cleaned = []
    for number, page in enumerate(pages, 1):
        page, count = strip_furniture(page, number)
        furniture += count
        if number in INSERT:
            page = INSERT[number] + (("\n\n" + page) if page else "")
        cleaned.append(page)

    if furniture != 224:
        raise AssertionError(f"expected 224 running/structural heads, found {furniture}")

    text = ""
    boundary_joins = 0
    for page in cleaned:
        if not text:
            text = page
            continue
        text, joined = join_page_boundary(text, page)
        boundary_joins += int(joined)
    if boundary_joins != 220:
        raise AssertionError(f"expected 220 page-boundary joins, found {boundary_joins}")

    # The page header was inserted into Franklin's sentence and reversed two
    # fragments.  Both fragments and their unique order are present internally.
    text = replace_exact(
        text,
        '"It shows, besides, that you are mindful of what you how to be a capitalist.\n\nowe;',
        'how to be a capitalist.\n\n"It shows, besides, that you are mindful of what you owe;',
        1,
        "Franklin page-order repair",
    )
    text = replace_exact(text, "\n\n5-d\n\n", "\n\n", 1, "library-margin mark")

    # Impossible English with a single repair, licensed by the stage-3 rule.
    # In each case the damaged scan edge or blemish caused Mistral to substitute
    # a short non-word; no edition-specific variant is being normalized.
    text = replace_exact(
        text,
        "economic function is usually involves some previous ownership of citizens",
        "economic function usually involves some previous ownership of capital",
        1,
        "function/capital sentence",
    )
    text = replace_exact(text, "indulgent s the sinner", "indulgent to the sinner", 1, "to the sinner")
    text = replace_exact(text, "6-day, is now", "to-day, is now", 1, "to-day page turn")
    text = replace_exact(text, "mvn the first place", "In the first place", 1, "In the first place")

    # Mistral omitted notes 91–93 on printed p. 237 where a damaged horizontal
    # band crosses note 91. Notes 92–93 and the undamaged parts of 91 are read
    # directly from that page. Within the quotation, John Howe's public-domain
    # text supplies only readings confirmed by surviving scan fragments; Weber's
    # printed spaced ellipses remain and one unsupported parenthetical is marked.
    notes_anchor = (
        '90. The idea of the birthright, so important in history, thus received an important '
        'confirmation in England. "The firstborn which are written in heaven. . . . As the '
        'firstborn is not to be defeated in his inheritance, and the enrolled names are never '
        'to be obliterated, so certainly they shall inherit eternal life" (Thomas Adams, '
        '*Works of the Puritan Divines*, p. xiv).\n\n94. *Cat. Genev.*'
    )
    text = replace_exact(
        text,
        notes_anchor,
        notes_anchor.replace("\n\n94.", f"\n\n{NOTES_91_TO_93}\n\n94."),
        1,
        "printed-page-237 notes 91–93 restoration",
    )

    # Mistral used LaTeX superscripts for ordinary note markers.  They are
    # navigation-free authorial markers, not mathematical expressions.
    text, supers = re.subn(r"\$\^\{(\d+)\}\$", r"<sup>\1</sup>", text)
    if supers != 92:
        raise AssertionError(f"expected 92 LaTeX note markers, found {supers}")

    # Literal currency is prose. Escaping prevents the math linter from reading
    # the two dollar signs as an unmatched formula delimiter.
    text = replace_exact(text, "$75,000", "&#36;75,000", 1, "currency 75,000")
    text = replace_exact(text, "$8,000", "&#36;8,000", 1, "currency 8,000")

    # Canonicalize subsection headings that occur within, rather than at the
    # top of, their printed pages.
    text = replace_exact(text, "### A. CALVINISM", "#### A. CALVINISM", 1, "Calvinism heading")
    text = replace_exact(text, "### B. PIETISM", "#### B. PIETISM", 1, "Pietism heading")
    text = replace_exact(text, "# C. METHODISM", "#### C. METHODISM", 1, "Methodism heading")
    text = replace_exact(text, "## D. THE BAPTIST SECTS", "#### D. THE BAPTIST SECTS", 1, "Baptist heading")
    text, notes_i = re.subn(r"(?m)^# CHAPTER I$", "## CHAPTER I", text)
    text, notes_iii = re.subn(r"(?m)^# CHAPTER III$", "## CHAPTER III", text)
    if (notes_i, notes_iii) != (1, 1):
        raise AssertionError(
            f"expected one notes heading each for chapters I/III, found "
            f"{notes_i}/{notes_iii}"
        )

    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    # Reuse the repository's standard, corpus-aware wrap-hyphen joiner.  Do not
    # duplicate its compound-vs-wrap decision here.
    joiner_path = Path(__file__).resolve().parents[3] / "3-postprocess" / "join-line-wrap-hyphens.py"
    spec = importlib.util.spec_from_file_location("enchiridion_join_hyphens", joiner_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load standard joiner: {joiner_path}")
    joiner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(joiner)
    text, dropped, kept, _ = joiner.join(text)
    if (dropped, kept) != (26, 1):
        raise AssertionError(f"expected 26 dropped and 1 kept wrap hyphens, found {dropped}/{kept}")

    # Parsons's interventions are explicitly signed throughout the retained
    # apparatus: 22 use the full label and p. 237 uses the shortened form.
    translator_notes = len(re.findall(r"—TRANSLATOR(?:'|’)S NOTE", text, flags=re.IGNORECASE))
    translator_short = len(re.findall(r"—TRANSLATOR\)", text, flags=re.IGNORECASE))
    if (translator_notes, translator_short) != (22, 1):
        raise AssertionError(
            "expected 22 full and 1 shortened translator signatures, found "
            f"{translator_notes}/{translator_short}"
        )
    if text.count("[illegible]") != 1:
        raise AssertionError("expected exactly one marked source-defect lacuna")

    OUT.write_text(text, encoding="utf-8")
    print(
        f"wrote {OUT}: pages={len(pages)}, furniture={furniture}, "
        f"boundary_joins={boundary_joins}, note_markers={supers}, "
        f"wrap_hyphens={dropped}, compound_hyphens={kept}"
    )


if __name__ == "__main__":
    main()
