#!/usr/bin/env python3
"""recon-epub.py — what does this EPUB already contain that we would otherwise redo?

Run this on any text whose folder holds an `.epub`, BEFORE routing it. The stage
0 question is not only "does a better source exist" but "is there more inside the
source we already have" — the same question Dedekind answered by arriving with a
`.tex` beside its PDF.

The answer is often yes, and specifically about notation. A transcriber who
renders formulas to images usually keeps the LaTeX they rendered FROM, and every
producer keeps it somewhere different:

    Project Gutenberg   <img data-tex="\\dfrac{h}{2 \\pi}" src="..._101.svg">
    Wikisource          <img class="mwe-math-fallback-image-inline"
                             alt="{\\displaystyle S_{1}}" src="...">

And one that LOOKS like the others and is not:

    PG (MathSpeak)      <img class="f1frml" title="left-parenthesis x comma y
                             comma z right-parenthesis" src="...">

The third stores the formula's SPOKEN form — a description made for the formula,
not the string it was set from. It is reported separately and never counted as
recoverable, because turning it back into notation is translation, and ambiguous
as soon as an expression nests.

Check for the CONVENTION, not for one attribute. Looking only for `data-tex`
reported "no recoverable notation, route to OCR" for Einstein's *Foundation of
the General Theory of Relativity* — 571 formulas whose LaTeX was sitting in the
alt text of a Wikisource export. A probe that finds nothing has proved nothing
until it has been shown to find a case known to exist; when a new source shape
turns up, add it here rather than trusting the zero.

The default route for an EPUB is `1-prepare/convert-epub-to-pdf.sh`, because
Mistral's OCR API is PDF-only. That is right for a prose book and wrong for this
one: it renders the LaTeX to pixels so that OCR can read the pixels back as
LaTeX, at the ~95-97% accuracy the math track lives with. The attribute is the
string the pixels were made from.

What this does NOT establish. `data-tex` and an OCR read of its own SVG are two
renderings of one act of copying — they establish fidelity, never correctness,
and agreement between them is worth nothing (see dispatch-text.sh). The claim is
narrower and it is about error sources, not truth: whatever PG's transcriber got
wrong is in both routes, and OCR adds a second error source on top of it. Neither
route is a printed witness, so stage 4 still wants the page.

Reports, per source:
  - notation encoding: which convention, or images carrying none
  - formula count, how many carry recoverable LaTeX, how many only speech
  - images that are NOT notation (real illustrations, which any text-only
    conversion silently drops — this is how Bohr's formulas vanished)
  - spine/document count and heading tiers, for partition planning
  - PG START/END markers

Usage:
    python3 ocr/0-recon/recon-epub.py SOURCE.epub
    python3 ocr/0-recon/recon-epub.py --corpus          # sweep texts/
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

IMG_RE = re.compile(r"<img\b[^>]*>", re.I)
TEX_RE = re.compile(r'data-tex="([^"]*)"')
ALT_RE = re.compile(r'alt="([^"]*)"')
CLASS_RE = re.compile(r'class="([^"]*)"')
TITLE_RE = re.compile(r'title="([^"]*)"')
SRC_RE = re.compile(r'src="([^"]*)"')
HEIGHT_RE = re.compile(r"height:\s*([\d.]+)ex")
# MediaWiki wraps its fallback alt text; the braces are the wrapper, not TeX.
DISPLAYSTYLE_RE = re.compile(r"^\{\\displaystyle\s*(.*)\}$", re.S)


MATHML_RE = re.compile(r"<math\b", re.I)
HEAD_RE = re.compile(r"<h([1-6])\b[^>]*>(.*?)</h\1>", re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")
PG_RE = re.compile(r"\*\*\* ?(START|END) OF THE PROJECT GUTENBERG", re.I)

# A formula set on its own line rather than inline. Height is the signal present
# in every PG file; an inline symbol runs 1-2ex, a fraction stack more. Only a
# hint for planning — the extractor must decide properly.
DISPLAY_EX = 3.0


def extract_tex(tag: str) -> tuple[str, str, bool] | None:
    """(latex, convention, is_display) for a formula image, or None if it is a
    real illustration. Conventions are producer-specific; see the module docstring."""
    tex = TEX_RE.search(tag)
    if tex:
        h = HEIGHT_RE.search(tag)
        return unescape(tex.group(1)), "data-tex", bool(h and float(h.group(1)) > DISPLAY_EX)

    css = (CLASS_RE.search(tag).group(1) if CLASS_RE.search(tag) else "")

    # A THIRD shape, and not a source string: some PG transcriptions store the
    # spoken form in `title` — "left-parenthesis x comma y comma z
    # right-parenthesis" for (x, y, z). That is MathSpeak, produced FOR the
    # formula rather than the formula it was set from. Turning it back into
    # notation is translation, not recovery, and it is ambiguous as soon as an
    # expression nests. Counted separately so nobody mistakes it for LaTeX.
    if "frml" in css:
        title = TITLE_RE.search(tag)
        if title and title.group(1).strip():
            return unescape(title.group(1)), "mathspeak-title", False

    if "mwe-math" in css:
        alt = ALT_RE.search(tag)
        if not alt:
            return None
        body = unescape(alt.group(1)).strip()
        m = DISPLAYSTYLE_RE.match(body)
        if m:
            body = m.group(1).strip()
        # MediaWiki states it outright, which beats guessing from height.
        return body, "mediawiki-alt", "fallback-image-display" in css or "-display" in css

    return None


def unescape(s: str) -> str:
    return (s.replace("&amp;", "&").replace("&lt;", "<")
             .replace("&gt;", ">").replace("&quot;", '"'))



class Survey:
    def __init__(self, path: Path):
        self.path = path
        self.docs = 0
        self.images = 0
        self.with_tex = 0
        self.mathml = 0
        self.illustrations: Counter = Counter()
        self.conventions: Counter = Counter()
        self.verbalized = 0
        self.display = 0
        self.headings: Counter = Counter()
        self.pg_markers = 0
        self.samples: list[str] = []

    def run(self) -> "Survey":
        with zipfile.ZipFile(self.path) as z:
            names = [n for n in z.namelist()
                     if n.lower().endswith((".html", ".xhtml", ".htm"))]
            for name in sorted(names):
                self.docs += 1
                s = z.read(name).decode("utf-8", "ignore")
                self.mathml += len(MATHML_RE.findall(s))
                self.pg_markers += len(PG_RE.findall(s))
                for level, raw in HEAD_RE.findall(s):
                    text = TAG_RE.sub("", raw).strip()
                    if text:
                        self.headings[int(level)] += 1
                for tag in IMG_RE.findall(s):
                    self.images += 1
                    found = extract_tex(tag)
                    if found:
                        latex, convention, display = found
                        self.conventions[convention] += 1
                        if convention == "mathspeak-title":
                            self.verbalized += 1
                        else:
                            self.with_tex += 1
                        if display:
                            self.display += 1
                        if len(self.samples) < 6:
                            self.samples.append(latex)
                    else:
                        src = SRC_RE.search(tag)
                        self.illustrations[Path(src.group(1)).suffix.lower()
                                           if src else "?"] += 1
        return self

    @property
    def notation(self) -> bool:
        return self.with_tex > 0 or self.mathml > 0


def report(s: Survey) -> None:
    print(f"\n=== {s.path.name}")
    print(f"documents in spine: {s.docs}")
    if s.headings:
        tiers = ", ".join(f"h{k}×{v}" for k, v in sorted(s.headings.items()))
        print(f"heading tiers:      {tiers}")
    print(f"Gutenberg markers:  {s.pg_markers}")
    print(f"images:             {s.images}")
    print(f"  carrying LaTeX:   {s.with_tex}"
          f"{f' ({s.display} display, {s.with_tex - s.display} inline)' if s.with_tex else ''}")
    if s.conventions:
        print("  convention:       "
              + ", ".join(f"{k}×{v}" for k, v in s.conventions.most_common()))
    if s.verbalized:
        print(f"  verbalized only:  {s.verbalized}  (MathSpeak in title=, NOT LaTeX)")
    print(f"  MathML elements:  {s.mathml}")
    illos = sum(s.illustrations.values())
    if illos:
        kinds = ", ".join(f"{k or '(none)'}×{v}" for k, v in s.illustrations.most_common())
        print(f"  illustrations:    {illos}  [{kinds}]")

    if s.samples:
        print("\nsample notation:")
        for t in s.samples:
            print(f"    {t}")

    print()
    if s.with_tex:
        pct = 100.0 * s.with_tex / s.images if s.images else 0
        print(f"*** NOTATION IS ALREADY LATEX: {s.with_tex} formulas, {pct:.0f}% of images.")
        print("*** Do NOT route this through convert-epub-to-pdf.sh and OCR. That")
        print("*** renders these strings to pixels so OCR can read them back as")
        print("*** strings, and OCR's error rate is added on top of the")
        print("*** transcriber's, which is in both routes either way.")
        print("*** Route: extract from the source, reading the convention above.")
        if "mediawiki-alt" in s.conventions:
            print("*** MediaWiki names display vs inline in the class attribute —")
            print("*** use it; it is the producer's own statement, not a guess.")
        if "data-tex" in s.conventions:
            print("*** For data-tex the display/inline split above is a HEIGHT")
            print("*** HEURISTIC. Decide it from the typesetting, not from that.")
        print("*** Still not a printed witness: it is a transcription either way,")
        print("*** so stage 4 wants the page. Agreement between the stored LaTeX")
        print("*** and an OCR of the image it produced proves nothing.")
    elif s.mathml:
        print(f"*** NOTATION IS MATHML: {s.mathml} elements, convertible without OCR.")
        print("*** Route: extract from the source; MathML → LaTeX is mechanical.")
    elif s.verbalized:
        print(f"*** NOTATION IS MARKED UP BUT NOT RECOVERABLE: {s.verbalized} formulas")
        print("*** carry only their SPOKEN form in a title attribute. That is a")
        print("*** description produced for the formula, not the string it was set")
        print("*** from, and it is ambiguous as soon as an expression nests.")
        print("*** Route: convert-epub-to-pdf.sh, then OCR — as usual.")
        print("*** Worth keeping anyway: the spoken forms are a cheap way to FLAG")
        print("*** disagreements with the OCR output for a human to look at. They")
        print("*** cannot settle one, since both descend from the same transcription.")
    elif s.images:
        print("*** Images carry NO recoverable notation.")
        print("*** If any of them are formulas, they are pictures of formulas and")
        print("*** only OCR can read them — which is what the PDF route is for.")
        print("*** Route: convert-epub-to-pdf.sh, then OCR.")
        print("*** Whichever route: a text-only conversion DROPS these images")
        print("*** silently. Losing an illustration is visible; losing a formula")
        print("*** leaves fluent prose with holes in it.")
    else:
        print("*** No images at all: prose. Extract from the source directly;")
        print("*** the PDF round trip buys nothing and costs an OCR pass.")


def corpus_sweep(root: Path) -> int:
    hits: list[Survey] = []
    spoken: list[Survey] = []
    plain = 0
    for epub in sorted(root.glob("texts/*/*/*.epub")):
        try:
            s = Survey(epub).run()
        except Exception as exc:  # a malformed archive should not stop the sweep
            print(f"  !! {epub.parent.name}: {exc}", file=sys.stderr)
            continue
        if s.notation:
            hits.append(s)
        elif s.verbalized:
            spoken.append(s)
        else:
            plain += 1

    print(f"EPUBs surveyed: {len(hits) + len(spoken) + plain}")
    print(f"  carrying recoverable notation: {len(hits)}")
    print(f"  notation as speech only:       {len(spoken)}")
    print(f"  prose or illustrations only:   {plain}\n")
    if hits:
        total = sum(s.with_tex + s.mathml for s in hits)
        print(f"{total:,} formulas are already LaTeX in the corpus:\n")
        for s in sorted(hits, key=lambda x: -(x.with_tex + x.mathml)):
            print(f"  {s.with_tex + s.mathml:7,}  {s.path.parent.name}")
        print("\nEach of these is currently routed EPUB → PDF → OCR by default.")
    if spoken:
        print("\nNotation present but only as MathSpeak — these still need OCR:")
        for s in sorted(spoken, key=lambda x: -x.verbalized):
            print(f"  {s.verbalized:7,}  {s.path.parent.name}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("epub", type=Path, nargs="?")
    ap.add_argument("--corpus", action="store_true",
                    help="sweep every .epub under texts/ instead of one file")
    args = ap.parse_args()

    if args.corpus:
        return corpus_sweep(Path(__file__).resolve().parents[2])
    if not args.epub:
        ap.error("give an EPUB path, or --corpus")
    report(Survey(args.epub).run())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
