"""How each producer stores the LaTeX it rendered a formula image from.

Shared by `0-recon/recon-epub.py`, which counts these, and `2-extract/
extract-epub.py`, which recovers them. One implementation on purpose: the
`level + 1` assumption cost this project seven copies across three files before
anyone noticed the copies had drifted, and a notation convention is exactly the
kind of rule that grows a new case every few texts.

Three shapes are known. TWO are recoverable source strings; the third is not,
and the difference is the whole point:

    data-tex        Project Gutenberg. The LaTeX the SVG was rendered from.
                    <img data-tex="\\dfrac{h}{2 \\pi}" src="..._101.svg">

    mediawiki-alt   Wikisource. Same thing in the alt text, wrapped in
                    \\displaystyle braces that are the wrapper, not the formula.
                    <img class="mwe-math-fallback-image-inline"
                         alt="{\\displaystyle S_{1}}">

    mathspeak-title NOT a source string. Some PG transcriptions store the
                    formula's SPOKEN form — "left-parenthesis x comma y comma z
                    right-parenthesis" for (x, y, z). A description made for the
                    formula rather than the string it was set from. Turning it
                    back into notation is translation, and ambiguous as soon as
                    an expression nests, so callers must treat it as absent.

When a fourth turns up — and stage 0's own notes say to expect one — add it
here, and say in the docstring what it does and does not establish.
"""

from __future__ import annotations

import re
from typing import NamedTuple

TEX_RE = re.compile(r'data-tex="([^"]*)"')
ALT_RE = re.compile(r'alt="([^"]*)"')
CLASS_RE = re.compile(r'class="([^"]*)"')
TITLE_RE = re.compile(r'title="([^"]*)"')
HEIGHT_RE = re.compile(r"height:\s*([\d.]+)ex")
DISPLAYSTYLE_RE = re.compile(r"^\{\\displaystyle\s*(.*)\}$", re.S)

# Gutenberg gives no display/inline flag, so height is the available signal: an
# inline symbol runs 1-2ex, a stacked fraction more. A HEURISTIC — it will
# misfile a tall inline radical. MediaWiki says which it is, and is believed.
DISPLAY_EX = 3.0

RECOVERABLE = ("data-tex", "mediawiki-alt")


class Notation(NamedTuple):
    latex: str
    convention: str
    display: bool

    @property
    def recoverable(self) -> bool:
        return self.convention in RECOVERABLE


def unescape(s: str) -> str:
    return (s.replace("&amp;", "&").replace("&lt;", "<")
             .replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'"))


def read_notation(tag: str) -> Notation | None:
    """Notation carried by an <img> tag, or None if it is a real illustration.

    `tag` is the raw markup of the element. Callers must check `.recoverable`
    before writing the result into a text: a mathspeak-title hit means notation
    is present and is NOT available as LaTeX.
    """
    tex = TEX_RE.search(tag)
    if tex:
        body = unescape(tex.group(1)).strip()
        # Some PG transcriptions put the mode in the string itself. That beats
        # the height heuristic, and the wrapper must come off either way — left
        # in, `\displaystyle {...}` inside `$...$` is a rendering bug rather
        # than the formula.
        explicit_display = False
        if body.startswith("\\displaystyle"):
            explicit_display = True
            body = body[len("\\displaystyle"):].strip()
            if body.startswith("{") and body.endswith("}"):
                body = body[1:-1].strip()
        h = HEIGHT_RE.search(tag)
        return Notation(body, "data-tex",
                        explicit_display or bool(h and float(h.group(1)) > DISPLAY_EX))

    css = CLASS_RE.search(tag)
    css = css.group(1) if css else ""

    if "frml" in css:
        title = TITLE_RE.search(tag)
        if title and title.group(1).strip():
            return Notation(unescape(title.group(1)).strip(), "mathspeak-title", False)

    if "mwe-math" in css:
        alt = ALT_RE.search(tag)
        if not alt:
            return None
        body = unescape(alt.group(1)).strip()
        stripped = DISPLAYSTYLE_RE.match(body)
        if stripped:
            body = stripped.group(1).strip()
        # NOT to be trusted for display/inline. Einstein's *Foundation* marks
        # all 571 of its formulas `-inline`, numbered display equations
        # included, so this only ever says "inline" there. The extractor
        # decides from context instead: a formula alone in its block is display.
        return Notation(body, "mediawiki-alt", "-display" in css)

    return None
