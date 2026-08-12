#!/usr/bin/env python3
"""extract-epub.py — markdown from an EPUB, with its notation recovered.

For the texts `0-recon/recon-epub.py` flags as carrying recoverable LaTeX. The
default EPUB route renders those strings to pixels so that OCR can read them
back as strings; this reads them directly.

    python3 ocr/2-extract/extract-epub.py SOURCE.epub OUT.md
    python3 ocr/2-extract/extract-epub.py SOURCE.epub OUT.md --report

What it does:

  - reads documents in SPINE order from the OPF, not by filename. Sorted
    filenames put chapter 10 before chapter 2 in most Gutenberg builds.
  - recovers each formula from its producer's convention (see ../epub_notation.py)
    and writes it as `$...$` or `$$...$$`.
  - keeps real illustrations, copying them into `images/` beside the output and
    rewriting the reference. A text-only conversion drops them silently, which
    is how a formula becomes a hole in a fluent sentence.
  - trims Project Gutenberg's front and back matter at the START/END markers,
    per the apparatus policy. `--keep-boilerplate` leaves it in.

What it does NOT do, deliberately:

  - decide the final heading structure. It emits the levels the EPUB used;
    naming a text's real divisions is stage 4 work.
  - strip editorial apparatus beyond the PG markers. Introductions, notes on the
    text and indices are a judgment per text — stage 3.
  - establish correctness. This is the transcriber's text either way: it is not
    a printed witness, and recovering LaTeX only avoids ADDING OCR's error rate
    on top of the transcriber's. Stage 4 still wants the page.

`--report` prints a diagnostic pass over the recovered notation: how the split
between display and inline was decided, and every formula that looks damaged.
Read it before trusting a run — the anomalies are where this route's own error
patterns show up, and they are different from OCR's.
"""

from __future__ import annotations

import argparse
import posixpath
import re
import shutil
import sys
import zipfile
from collections import Counter
from pathlib import Path

from lxml import etree, html as lxml_html

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from epub_notation import read_notation  # noqa: E402

PG_START_RE = re.compile(r"\*\*\* ?START OF THE PROJECT GUTENBERG.*?\*\*\*", re.I | re.S)
PG_END_RE = re.compile(r"\*\*\* ?END OF THE PROJECT GUTENBERG.*?\*\*\*", re.I | re.S)

BLOCK = {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "li",
         "tr", "pre", "hr", "table", "figure", "figcaption"}
INLINE_EM = {"em", "i", "cite"}
INLINE_STRONG = {"strong", "b"}
SKIP = {"script", "style", "head", "title"}


def spine_documents(z: zipfile.ZipFile) -> list[str]:
    """Content documents in reading order, from the OPF's spine."""
    try:
        container = etree.fromstring(z.read("META-INF/container.xml"))
        ns = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
        opf_path = container.find(".//c:rootfile", ns).get("full-path")
        opf = etree.fromstring(z.read(opf_path))
        ns2 = {"o": "http://www.idpf.org/2007/opf"}
        manifest = {i.get("id"): i.get("href")
                    for i in opf.findall(".//o:manifest/o:item", ns2)}
        base = posixpath.dirname(opf_path)
        docs = []
        for ref in opf.findall(".//o:spine/o:itemref", ns2):
            href = manifest.get(ref.get("idref"))
            if not href:
                continue
            full = posixpath.normpath(posixpath.join(base, href)) if base else href
            if full.lower().endswith((".html", ".xhtml", ".htm")):
                docs.append(full)
        if docs:
            return docs
    except Exception as exc:  # malformed OPF: fall back, but say so
        print(f"  ! could not read spine ({exc}); falling back to sorted names",
              file=sys.stderr)
    return sorted(n for n in z.namelist()
                  if n.lower().endswith((".html", ".xhtml", ".htm")))


def _wrap(inner: str, mark: str) -> str:
    """Wrap in an emphasis marker, KEEPING the whitespace at its edges.

    Markdown will not render `* text *`, so the marker has to sit tight against
    the words -- but the earlier version got there with `inner.strip()`, which
    DELETED that whitespace instead of moving it. `<i>Micrographia </i>is` came
    out as `*Micrographia*is`.

    Nothing downstream could see it. The extractor's own report is about
    notation and said "no anomalies"; the triad tests math well-formedness; and
    the result still reads as fluent prose with two words fused. Hooke's run
    found it by eye and had to repair it per-text, and it plausibly explains
    part of the standing corpus finding of paragraphs ending mid-word.

    So: strip for the marker, and put the whitespace back outside it.

    It is deliberately put back VERBATIM rather than collapsed to one space.
    `a <i> spaced </i>word` really does carry two spaces, HTML and Markdown both
    collapse them on render, and a general whitespace-collapsing pass here would
    eat the two-space hardbreaks that verse depends on. Faithful and slightly
    redundant beats tidy and lossy.
    """
    core = inner.strip()
    lead = inner[:len(inner) - len(inner.lstrip())]
    trail = inner[len(inner.rstrip()):]
    return f"{lead}{mark}{core}{mark}{trail}"


class Extractor:
    def __init__(self, out_dir: Path, keep_images: bool = True):
        self.out_dir = out_dir
        self.keep_images = keep_images
        self.conventions: Counter = Counter()
        self.display = 0
        self.inline = 0
        self.illustrations: list[str] = []
        self.formulas: list[str] = []
        self.unrecoverable = 0
        # Set while rendering a table cell: a row is one line, so a
        # displayed formula inside it must not carry blank lines.
        self.in_cell = False

    # -- inline ---------------------------------------------------------------

    def inline_text(self, el) -> str:
        parts = []
        if el.tag == "img":
            parts.append(self.image(el))
        elif el.tag == "br":
            parts.append("  \n")
        else:
            if el.text:
                parts.append(el.text)
        for child in el:
            if child.tag in SKIP:
                continue
            inner = self.inline_text(child)
            if child.tag in INLINE_EM and inner.strip():
                inner = _wrap(inner, "*")
            elif child.tag in INLINE_STRONG and inner.strip():
                inner = _wrap(inner, "**")
            elif child.tag == "sup" and inner.strip():
                inner = _wrap(inner, "^")
            elif child.tag == "sub" and inner.strip():
                inner = _wrap(inner, "~")
            parts.append(inner)
            if child.tail:
                parts.append(child.tail)
        return "".join(parts)

    def sole_formula(self, el):
        """The one recoverable formula in this block, if it holds nothing else.

        Equation numbers are ignored when deciding "nothing else": a displayed
        equation labelled (5) is still a displayed equation. They are rare
        enough in these sources to keep the rule simple — anything longer than
        a short parenthetical counts as prose and the block stays inline.
        """
        imgs = el.findall(".//img")
        if len(imgs) != 1:
            return None
        found = read_notation(etree.tostring(imgs[0], encoding="unicode"))
        if not found or not found.recoverable:
            return None
        text = "".join(el.itertext()).strip()
        if text and not re.fullmatch(r"[\(\[]?\s*[\d\w.]{1,6}\s*[\)\]]?", text):
            return None
        return found

    def image(self, el) -> str:
        raw = etree.tostring(el, encoding="unicode")
        found = read_notation(raw)
        if found:
            self.conventions[found.convention] += 1
            if not found.recoverable:
                # Present but not a source string. Leaving a marker rather than
                # the speech: silently writing prose where a formula stood is
                # the failure this whole route exists to avoid.
                self.unrecoverable += 1
                return "<!-- FORMULA NOT RECOVERABLE: spoken form only -->"
            self.formulas.append(found.latex)
            if found.display:
                self.display += 1
                # Inside a table cell, INLINE delimiters — not display ones.
                #
                # A row is one line, so blank lines around `$$` tear it in half.
                # But dropping just the blank lines is not enough: the reader's
                # display pattern spans newlines (it stops only at a blank
                # line), and consecutive rows have none, so one row's `$$` can
                # pair with the NEXT row's and every pairing after that shifts
                # by one. Six of Newton's tables read as raw LaTeX that way.
                # `$...$` forbids newlines outright, so a cell cannot leak into
                # its neighbour. Nothing is lost: a cell cannot render a
                # displayed block regardless.
                if self.in_cell:
                    return f"${found.latex}$"
                return f"\n\n$${found.latex}$$\n\n"
            self.inline += 1
            return f"${found.latex}$"

        src = el.get("src")
        if not src:
            return ""
        name = posixpath.basename(src)
        self.illustrations.append(name)
        alt = (el.get("alt") or "").strip()
        return f"![{alt}](images/{name})"

    # -- blocks ---------------------------------------------------------------

    def walk(self, el, out: list[str], depth: int = 0) -> None:
        tag = el.tag if isinstance(el.tag, str) else ""
        if tag in SKIP:
            return

        # A formula image is often a DIRECT child of a div rather than sitting
        # inside a paragraph. Without this branch it reaches the container case
        # below, which finds no text and no children and emits nothing: 110 of
        # Einstein's 571 formulas disappeared exactly this way, leaving prose
        # that still read cleanly. Handle inline-level elements as content.
        if tag == "img":
            emitted = self.image(el).strip()
            if emitted:
                out.append(emitted)
            return

        if re.fullmatch(r"h[1-6]", tag or ""):
            text = self.inline_text(el).strip()
            if text:
                out.append("#" * int(tag[1]) + " " + re.sub(r"\s+", " ", text))
            return
        if tag == "hr":
            out.append("---")
            return
        if tag in ("p", "figcaption", "dd"):
            # A formula standing alone in its own block was set as a displayed
            # equation, whatever the producer's class attribute claims. This is
            # the only signal available for a Wikisource export, which labels
            # every formula inline.
            sole = self.sole_formula(el)
            if sole is not None:
                self.formulas.append(sole.latex)
                self.conventions[sole.convention] += 1
                self.display += 1
                out.append(f"$${sole.latex}$$")
                return
            text = self.inline_text(el).strip()
            if text:
                out.append(re.sub(r"[ \t]+", " ", text))
            return
        if tag == "blockquote":
            inner: list[str] = []
            for child in el:
                self.walk(child, inner, depth + 1)
            body = "\n\n".join(inner).strip()
            if body:
                out.append("\n".join("> " + ln for ln in body.split("\n")))
            return
        if tag in ("ul", "ol"):
            marker = (lambda i: f"{i}.") if tag == "ol" else (lambda i: "-")
            for i, li in enumerate([c for c in el if c.tag == "li"], 1):
                text = self.inline_text(li).strip()
                if text:
                    out.append(f"{marker(i)} {re.sub(r'\\s+', ' ', text)}")
            return
        if tag == "table":
            self.in_cell = True
            for tr in el.iter("tr"):
                cells = [re.sub(r"\s+", " ", self.inline_text(c).strip())
                         for c in tr if c.tag in ("td", "th")]
                if cells:
                    out.append("| " + " | ".join(cells) + " |")
            self.in_cell = False
            return

        # A container: descend, but keep any loose text it holds directly.
        if el.text and el.text.strip():
            out.append(el.text.strip())
        for child in el:
            self.walk(child, out, depth + 1)
            if child.tail and child.tail.strip():
                out.append(child.tail.strip())

    # -- driver ---------------------------------------------------------------

    def run(self, src: Path, keep_boilerplate: bool) -> str:
        blocks: list[str] = []
        with zipfile.ZipFile(src) as z:
            names = spine_documents(z)
            for name in names:
                try:
                    raw = z.read(name)
                except KeyError:
                    continue
                doc = lxml_html.fromstring(raw)
                body = doc.find("body")
                self.walk(body if body is not None else doc, blocks)

            if self.keep_images and self.illustrations:
                self.copy_images(z, src)

        text = "\n\n".join(b for b in blocks if b.strip())
        text = re.sub(r"\n{3,}", "\n\n", text)
        if not keep_boilerplate:
            text = self.trim_pg(text)
        return text.strip() + "\n"

    def copy_images(self, z: zipfile.ZipFile, src: Path) -> None:
        dest = self.out_dir / "images"
        dest.mkdir(parents=True, exist_ok=True)
        wanted = set(self.illustrations)
        for entry in z.namelist():
            base = posixpath.basename(entry)
            if base in wanted:
                with z.open(entry) as fh, open(dest / base, "wb") as out:
                    shutil.copyfileobj(fh, out)

    @staticmethod
    def trim_pg(text: str) -> str:
        start = PG_START_RE.search(text)
        if start:
            text = text[start.end():]
        end = PG_END_RE.search(text)
        if end:
            text = text[:end.start()]
        return text


def unescaped_count(s: str, ch: str) -> int:
    """Occurrences of `ch` not escaped by a backslash.

    Counted by parity: `\\{` is escaped, `\\\\{` is a line break followed by a
    group open. Getting this wrong reported ten of Einstein's `cases`
    environments as damaged.
    """
    n = 0
    for i, c in enumerate(s):
        if c != ch:
            continue
        backslashes = 0
        j = i - 1
        while j >= 0 and s[j] == "\\":
            backslashes += 1
            j -= 1
        if backslashes % 2 == 0:
            n += 1
    return n


def report(ex: Extractor) -> None:
    print("\n--- notation ---", file=sys.stderr)
    for k, v in ex.conventions.most_common():
        print(f"  {k}: {v}", file=sys.stderr)
    print(f"  display: {ex.display}   inline: {ex.inline}", file=sys.stderr)
    if ex.unrecoverable:
        print(f"  NOT RECOVERABLE (marked in the text): {ex.unrecoverable}",
              file=sys.stderr)
    print(f"  illustrations: {len(set(ex.illustrations))}", file=sys.stderr)

    # Where this route's own error patterns live. They are not OCR's: OCR
    # misreads a glyph, this inherits whatever the transcriber typed.
    anomalies: Counter = Counter()
    examples: dict[str, str] = {}

    def flag(kind: str, tex: str) -> None:
        anomalies[kind] += 1
        examples.setdefault(kind, tex)

    # Every one of these checks was wrong before it was right, and each way is
    # worth keeping in mind, because all three fired confidently on valid
    # notation:
    #
    #   `>` is ordinary mathematics, not stray HTML.
    #   `\}` is an escaped delimiter, not an unclosed group — `\left. ... \right\}`
    #        reads as unbalanced if you count naively.
    #   `\\\\{` is TWO line breaks followed by a group, not an escaped brace. A
    #        brace is escaped only after an ODD number of backslashes, and
    #        stripping `\{` blindly undercounts the opens.
    #
    # A check that cries wolf on valid notation is worse than no check: it
    # trains you to skim the report, which is where the real defect will be.
    for tex in ex.formulas:
        if not tex.strip():
            flag("empty", tex)
        if unescaped_count(tex, "{") != unescaped_count(tex, "}"):
            flag("unbalanced braces", tex)
        if re.search(r"(?<!\\)\$", tex):
            flag("unescaped dollar (would break the delimiters)", tex)
        elif "\\$" in tex:
            flag("escaped dollar — verify against the page", tex)
        if re.search(r"</|<[a-zA-Z]+[\s/>]", tex):
            flag("contains an HTML tag", tex)
        if "\\displaystyle" in tex:
            flag("displaystyle wrapper left in", tex)
        if re.search(r"[Ѐ-ӿͰ-Ͽ]", tex):
            flag("non-Latin script inside math", tex)
        if "�" in tex:
            flag("replacement character (encoding loss)", tex)
        # Valid LaTeX that KaTeX does not implement. The reader's answer is a
        # corpus-wide macro (site/src/readers/md-reader.js, KATEX_MACROS, which
        # already carries \arc and \Crd) — not a rewrite of the text.
        for macro in ("\\DeclareMathOperator", "\\newcommand", "\\def",
                      "\\mathchoice", "\\raisebox"):
            if macro in tex:
                flag(f"{macro} — valid TeX, unsupported by KaTeX", tex)

    print("\n--- anomalies ---", file=sys.stderr)
    if not anomalies:
        print("  none found across "
              f"{len(ex.formulas)} formulas", file=sys.stderr)
        print("  (a clean sweep is not proof: these checks catch damage that is"
              " visible\n   in the string, not a formula faithfully carrying a"
              " transcriber's error)", file=sys.stderr)
    for kind, n in anomalies.most_common():
        print(f"  {n:5}  {kind}", file=sys.stderr)
        print(f"         e.g. {examples[kind][:110]}", file=sys.stderr)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("epub", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--report", action="store_true",
                    help="diagnostics on the recovered notation, to stderr")
    ap.add_argument("--keep-boilerplate", action="store_true",
                    help="do not trim at the Project Gutenberg markers")
    ap.add_argument("--no-images", action="store_true",
                    help="do not copy illustrations into images/")
    args = ap.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    ex = Extractor(args.out.parent, keep_images=not args.no_images)
    text = ex.run(args.epub, args.keep_boilerplate)
    args.out.write_text(text, encoding="utf-8")

    words = len(text.split())
    print(f"{args.out}: {words:,} words, {len(ex.formulas):,} formulas recovered",
          file=sys.stderr)
    if args.report:
        report(ex)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
