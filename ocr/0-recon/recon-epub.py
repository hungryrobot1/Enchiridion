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

# The stage directories start with digits, so they are not importable as
# packages; ocr/ is added to the path instead. The notation conventions are
# shared with 2-extract/extract-epub.py rather than copied -- see that module.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from epub_notation import read_notation  # noqa: E402
from route import Facts, decide, render  # noqa: E402

IMG_RE = re.compile(r"<img\b[^>]*>", re.I)
SRC_RE = re.compile(r'src="([^"]*)"')
MATHML_RE = re.compile(r"<math\b", re.I)
HEAD_RE = re.compile(r"<h([1-6])\b[^>]*>(.*?)</h\1>", re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")
PG_RE = re.compile(r"\*\*\* ?(START|END) OF THE PROJECT GUTENBERG", re.I)

# A formula set on its own line rather than inline. Height is the signal present
# in every PG file; an inline symbol runs 1-2ex, a fraction stack more. Only a
# hint for planning — the extractor must decide properly.
DISPLAY_EX = 3.0


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
                    found = read_notation(tag)
                    if found:
                        self.conventions[found.convention] += 1
                        if found.recoverable:
                            self.with_tex += 1
                        else:
                            self.verbalized += 1
                        if found.display:
                            self.display += 1
                        if len(self.samples) < 6:
                            self.samples.append(found.latex)
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

    # The route is a computed verdict now rather than prose the reader
    # assembles. It used to be four branches of `***` lines here, and one of
    # them was wrong: any EPUB whose images carried no notation was sent to OCR,
    # on the reasoning that they might be pictures of formulas. Huygens'
    # Treatise on Light is 53 geometric diagrams and prose, and the run had to
    # read the surrounding argument and every image to establish that the
    # headline did not fit. `route.decide` returns UNDETERMINED there instead,
    # which is the true answer: nothing we compute tells a diagram from an
    # equation.
    print()
    print(render(decide(Facts(
        structured="epub",
        notation=(s.conventions.most_common(1)[0][0] if s.conventions
                  else ("mathml" if s.mathml else None)),
        notation_count=s.with_tex + s.mathml,
        unrecoverable_count=s.verbalized,
        plain_images=sum(s.illustrations.values()),
    ))))

    # These are about HOW to extract, not about which route, so they sit beside
    # the verdict rather than inside it.
    if "mediawiki-alt" in s.conventions:
        print("\n  note            MediaWiki names display vs inline in the class")
        print("                  attribute — use it. It is the producer's own")
        print("                  statement, not a guess.")
    if "data-tex" in s.conventions:
        print("\n  note            for data-tex the display/inline split above is a")
        print("                  HEIGHT HEURISTIC, and it is wrong often enough to")
        print("                  matter: Hilbert's run found 15 wrong display")
        print("                  decisions sitting behind a clean 248/248 count and")
        print("                  a green renderer. Decide display from the")
        print("                  typesetting context instead.")


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
