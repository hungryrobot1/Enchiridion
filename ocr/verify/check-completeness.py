#!/usr/bin/env python3
"""check-completeness.py — account for every word between an EPUB and our markdown.

    ocr/.venv/bin/python3 ocr/verify/check-completeness.py SOURCE.epub OUT.md \
        [--dropped-doc SUBSTRING]... [--dropped-text FILE]... [--self-test]

WHAT QUESTION THIS ANSWERS, AND WHICH IT DOES NOT.

It asks whether anything present in the source failed to arrive in the output
*without anyone saying so*. That is a question about OUR EXTRACTOR, and the
extractor is the thing that has actually been silently wrong:

  - 110 of Einstein's 571 formulas vanished into an unhandled branch, leaving
    prose that still read fluently;
  - Kant's seven `<pre>` blocks and Smith's ten lost the alignment that WAS
    their content;
  - 31 of Newton's tables reached the reader as pipe paragraphs;
  - and `extract-epub.py` still skips a spine document it cannot read, in
    silence, so a whole chapter can disappear and nothing anywhere says so.

It does NOT ask whether the text is correct. Locke's Sect. 2 reads "distinguish
these powers one from wealth, a father of a family", which has plainly lost
words — and it will pass every check here, faithfully, because the loss is in
the transcription we were given. Only the printed page catches that. This is a
CONSERVATION check, and conservation is not truth.

It compares against the SOURCE XHTML and deliberately not against the sibling
PDF. Runs kept building the PDF comparison; it is weaker. Calibre generated
that PDF from this same XHTML, so it adds a second extraction's error modes
while telling you nothing new about the transcription.

WHY DECLARED REMOVALS ARE THE WHOLE DESIGN.

A plain diff is useless here, because the output is SUPPOSED to differ: we
remove apparatus on purpose, and about a fifth of Newton's source is
Chittenden's. A tool that flagged all of that would be turned off by the second
text.

So the run declares what it removed, and this verifies the difference is
EXACTLY the declared removals and nothing else. That is what makes the check
non-tautological — and it has a second effect worth as much as the first. It
forces the boundary of the work to be stated explicitly, up front, in a form
something else can check. Three runs in one wave decided that boundary late and
expensively; a brief can assert it, but only this can hold a run to it.

Project Gutenberg's header and footer are declared for you: `extract-epub.py`
trims them deterministically at the START/END markers, so this trims the same
region from the source side rather than making every run restate it.
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

from lxml import etree, html as lxml_html

ROOT = Path(__file__).resolve().parents[2]

SKIP = {"script", "style", "head", "title"}
PG_START_RE = re.compile(r"\*\*\* ?START OF THE PROJECT GUTENBERG.*?\*\*\*", re.I | re.S)
PG_END_RE = re.compile(r"\*\*\* ?END OF THE PROJECT GUTENBERG.*?\*\*\*", re.I | re.S)

# A word is a run of letters/digits. Case and punctuation are noise for this
# question: we are asking whether the WORDS arrived, not whether a comma moved.
WORD_RE = re.compile(r"[^\W_]+", re.UNICODE)


def words(text: str) -> Counter:
    return Counter(w.casefold() for w in WORD_RE.findall(text))


# ---------------------------------------------------------------- the source

def spine_documents(z: zipfile.ZipFile) -> list[str]:
    """Content documents in reading order. Mirrors extract-epub.py."""
    try:
        container = etree.fromstring(z.read("META-INF/container.xml"))
        ns = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
        opf_path = container.find(".//c:rootfile", ns).get("full-path")
        opf = etree.fromstring(z.read(opf_path))
        ns2 = {"o": "http://www.idpf.org/2007/opf"}
        manifest = {i.get("id"): i.get("href")
                    for i in opf.findall(".//o:manifest/o:item", ns2)}
        import posixpath
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
    except Exception:
        pass
    return sorted(n for n in z.namelist()
                  if n.lower().endswith((".html", ".xhtml", ".htm")))


def document_text(raw: bytes) -> str:
    doc = lxml_html.fromstring(raw)
    for el in doc.iter():
        if isinstance(el.tag, str) and el.tag in SKIP:
            el.getparent().remove(el) if el.getparent() is not None else None
    body = doc.find("body")
    return (body if body is not None else doc).text_content()


def preformatted_blocks(raw: bytes) -> list[str]:
    """The blocks whose whitespace IS their content, as the extractor sees them."""
    doc = lxml_html.fromstring(raw)
    out = []
    for el in doc.iter():
        if not isinstance(el.tag, str):
            continue
        if el.tag == "pre" or (el.tag == "div"
                               and "pre" in (el.get("class") or "").split()):
            body = el.text_content().strip("\n").rstrip()
            if body.strip():
                out.append(body)
    return out


# ---------------------------------------------------------------- our output

MATH_RE = re.compile(r"\$\$.*?\$\$|(?<!\\)\$.*?(?<!\\)\$", re.S)


def strip_markdown(md: str) -> tuple[str, list[str]]:
    """Return (prose, math spans) with our own syntax removed from the prose.

    Order matters, and one step here is easy to get wrong in a way that
    invents thousands of findings. Emphasis markers must come out BEFORE
    tokenising, because they split words the source had joined: Newton's
    `N<i>p</i>` is the single token `np` in the source and prints as `N*p*`,
    which tokenises as `n` and `p`. Removing the markers rather than treating
    them as separators is what makes the two sides comparable — the first
    version of this check reported 4,323 phantom additions on that alone.
    """
    md = re.sub(r"<!--.*?-->", " ", md, flags=re.S)
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", md)      # images, alt text and all
    math = MATH_RE.findall(md)
    md = MATH_RE.sub(" ", md)
    md = re.sub(r"<[^>]+>", " ", md)                   # tags, attributes and all
    # Emphasis, superscript and subscript markers all JOIN. `^` matters as
    # much as `*` here and was missed first time round: the extractor writes
    # `<sup>2</sup>` as `AZ^2^`, where the source's own text says `AZ2`, and
    # treating the carets as boundaries left 25 phantom losses of `az2` alone
    # on the Principia. Math has already been lifted out above, so the caret
    # remaining at this point is always ours.
    md = re.sub(r"[*_`~^]", "", md)
    return md, math


def markdown_words(md: str) -> Counter:
    return words(strip_markdown(md)[0])


# ---------------------------------------------------------------- the check

class Result:
    def __init__(self):
        self.missing: Counter = Counter()
        self.added: Counter = Counter()
        self.silent_docs: list[str] = []
        self.lost_pre: list[str] = []
        self.rare_by_doc: Counter = Counter()
        self.promoted: Counter = Counter()
        self.retained = 0
        self.dropped = 0

    @property
    def ok(self) -> bool:
        return not (self.missing or self.silent_docs or self.lost_pre)


def check(epub: Path, out_md: Path, dropped_docs: list[str],
          dropped_text: list[str]) -> Result:
    r = Result()
    md = out_md.read_text(encoding="utf-8")
    prose, math_spans = strip_markdown(md)
    actual = words(prose)

    # What a formula could plausibly have absorbed from the prose, matched
    # PER SPAN and exactly. Testing membership in all the math concatenated
    # was far too loose: `of` and `the` turn up somewhere in 1,936 formulas,
    # so 119 perfectly ordinary English words were being excused as notation.
    # COUNTED, not merely collected. Newton's formulas carry real English
    # inside `\text{...}` — one of them reads `\text{because of the given
    # quantity}` — so membership alone let a single `of` inside one formula
    # excuse all 64 `of`s that had gone missing from removed prose. A bucket
    # that forgives by identity rather than by quantity is an amnesty.
    math_tokens: Counter = Counter()
    for span in math_spans:
        bare = re.sub(r"\\[a-zA-Z]+", " ", span)          # drop \mathrm, \dfrac …
        # A SET per span: one formula accounts for one occurrence of a token,
        # however many times it says it. Counting the compacted form and the
        # word tokens separately double-counted every short span. Erring low
        # here errs toward reporting, which is the right direction to err.
        seen = {w.casefold() for w in WORD_RE.findall(bare)}
        seen.add(re.sub(r"[^\w]", "", bare).casefold())
        # Per TERM, not just per word and per whole span. The source writes
        # Newton's squares as running text — `AZ2`, `BD2` — and the output
        # sets them as `\mathrm{AZ}^{2}`, which splits into `AZ` and `2` and
        # matches neither. Dropping only the grouping and superscript marks
        # rejoins each term, so `\mathrm{AZ}^2 = \mathrm{BD}^2` offers `az2`
        # and `bd2` rather than a single unusable `az2bd2`.
        terms = re.sub(r"[{}^_\\,\s]", "", bare)
        seen.update(w.casefold() for w in WORD_RE.findall(terms))
        math_tokens.update(seen)
    math_tokens.pop("", None)

    expected: Counter = Counter()
    per_doc: dict[str, Counter] = {}

    with zipfile.ZipFile(epub) as z:
        for name in spine_documents(z):
            if any(d in name for d in dropped_docs):
                r.dropped += 1
                continue
            try:
                raw = z.read(name)
            except KeyError:
                # The very failure mode this tool exists for; do not inherit it.
                r.silent_docs.append(f"{name} (unreadable in the archive)")
                continue
            r.retained += 1
            text = document_text(raw)
            # PG's own header/footer: the extractor trims them, so trim here
            # too rather than making every run declare the same two regions.
            s = PG_START_RE.search(text)
            if s:
                text = text[s.end():]
            e = PG_END_RE.search(text)
            if e:
                text = text[:e.start()]

            w = words(text)
            per_doc[name] = w
            expected += w

            if w and not (set(w) & set(actual)):
                r.silent_docs.append(f"{name} (contributed nothing to the output)")

            for block in preformatted_blocks(raw):
                lines = [ln for ln in block.split("\n") if ln.strip()]
                # An indented line proves the alignment survived; a block with
                # no indentation anywhere cannot testify either way, so skip it.
                indented = [ln for ln in lines if ln.startswith((" ", "\t"))]
                if indented and not any(ln in md for ln in indented):
                    r.lost_pre.append(f"{name}: {indented[0][:60]!r}")

    for passage in dropped_text:
        expected -= words(passage)

    r.missing = expected - actual
    r.added = actual - expected

    # NOTATION PROMOTED OUT OF PROSE.
    #
    # Older mathematics is often set as running text: Newton's Book II writes
    # `nn - aa - 2ao - oo` in ordinary type, and a run may legitimately render
    # that as real notation. The words then leave the prose for a math span,
    # and a check that strips math sees them as lost -- 2,467 of them on the
    # Principia, none of which was a loss.
    #
    # A missing token whose characters appear inside a math span in the output
    # is reported under its own heading rather than as damage. This is a
    # WEAKER claim than the rest of the tool makes and it is deliberately
    # separated: it says the characters are still somewhere, not that the
    # formula says what the sentence said.
    for tok, lost in list(r.missing.items()):
        excusable = min(lost, math_tokens.get(tok, 0)) if len(tok) > 1 else 0
        if excusable:
            r.promoted[tok] = excusable
            if excusable == lost:
                del r.missing[tok]
            else:
                r.missing[tok] = lost - excusable

    # Localisation. A token that occurs exactly once in the whole source names
    # its document unambiguously, so a missing one says WHERE the loss is —
    # far more use than a bag of counts saying only how much.
    rare = {t for t, n in expected.items() if n == 1}
    for name, w in per_doc.items():
        lost_here = (set(w) & rare) & set(r.missing)
        if lost_here:
            r.rare_by_doc[name] = len(lost_here)
    return r


def render(r: Result, epub: Path, out_md: Path) -> None:
    print(f"  source   {epub.name}: {r.retained} spine document(s) retained, "
          f"{r.dropped} declared as removed")
    print(f"  output   {out_md.name}")

    if r.silent_docs:
        print(f"\n  ✗ {len(r.silent_docs)} document(s) reached the reader as nothing:")
        for d in r.silent_docs:
            print(f"      {d}")

    if r.missing:
        total = sum(r.missing.values())
        print(f"\n  ✗ {total:,} word occurrence(s) in the source are NOT in the "
              f"output and were NOT declared removed")
        if r.rare_by_doc:
            print("    where (by words unique to one document):")
            for name, n in r.rare_by_doc.most_common(8):
                print(f"      {n:6}  {name}")
        print("    most common:")
        for w, n in r.missing.most_common(10):
            print(f"      {n:6}  {w}")

    if r.lost_pre:
        print(f"\n  ✗ {len(r.lost_pre)} preformatted block(s) lost their "
              f"alignment — the whitespace there IS the content:")
        for p in r.lost_pre[:6]:
            print(f"      {p}")

    if r.promoted:
        total = sum(r.promoted.values())
        print(f"\n  · {total:,} word occurrence(s) left the prose for a math span "
              f"— notation\n    the source set as running text. Not damage, and "
              f"not verified either:\n    the characters are still present; "
              f"whether the formula says what the\n    sentence said is not "
              f"tested here.")
        for w, n in r.promoted.most_common(6):
            print(f"      {n:6}  {w}")

    if r.added:
        total = sum(r.added.values())
        print(f"\n  ⚠ {total:,} word occurrence(s) in the output are not in the "
              f"source. Usually our own scaffolding; check it is not prose.")
        for w, n in r.added.most_common(8):
            print(f"      {n:6}  {w}")

    if r.ok:
        print("\n  ok — every word in the source is either in the output or "
              "declared removed.")

    # The reach, stated whatever the verdict. A clean result here has been
    # read as "the text is good" before, and it is not that claim.
    print("\n  what this does NOT establish: that the text is CORRECT. A word "
          "the\n  transcriber got wrong, or a phrase dropped before we ever saw "
          "the file,\n  is conserved perfectly by this check. Stage 4 still "
          "wants the printed page.")


# ---------------------------------------------------------------- controls

def _epub(tmp: Path, docs: dict[str, str]) -> Path:
    """A minimal but real EPUB, so the controls exercise the actual reader."""
    path = tmp / "control.epub"
    items = "".join(
        f'<item id="d{i}" href="{n}" media-type="application/xhtml+xml"/>'
        for i, n in enumerate(docs))
    refs = "".join(f'<itemref idref="d{i}"/>' for i in range(len(docs)))
    opf = ('<?xml version="1.0"?><package xmlns="http://www.idpf.org/2007/opf" '
           f'version="3.0"><manifest>{items}</manifest><spine>{refs}</spine></package>')
    container = ('<?xml version="1.0"?><container version="1.0" '
                 'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                 '<rootfiles><rootfile full-path="content.opf" '
                 'media-type="application/oebps-package+xml"/></rootfiles></container>')
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("META-INF/container.xml", container)
        z.writestr("content.opf", opf)
        for name, body in docs.items():
            z.writestr(name, f"<html><body>{body}</body></html>")
    return path


def selftest() -> int:
    import tempfile
    ok = True
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        src = _epub(tmp, {
            "a.xhtml": "<p>Alpha bravo charlie delta.</p>",
            "b.xhtml": "<p>Echo foxtrot golf hotel.</p>",
            "c.xhtml": "<p>Chittenden wrote this life of the author.</p>",
        })
        out = tmp / "out.md"

        def run(md, dropped_docs=(), dropped_text=(), label="", want=None):
            nonlocal ok
            out.write_text(md, encoding="utf-8")
            r = check(src, out, list(dropped_docs), list(dropped_text))
            passed = want(r)
            ok &= passed
            print(f"  {'PASS' if passed else 'FAIL'}  {label}")
            if not passed:
                print(f"        missing={dict(r.missing)} added={dict(r.added)} "
                      f"silent={r.silent_docs} pre={r.lost_pre}")

        run("Alpha bravo charlie delta.\n\nEcho foxtrot golf hotel.\n\n"
            "Chittenden wrote this life of the author.\n",
            label="a complete extraction is silent",
            want=lambda r: r.ok)

        # THE case this exists for: extract-epub.py's `except KeyError: continue`.
        run("Alpha bravo charlie delta.\n\nChittenden wrote this life of the author.\n",
            label="a whole document dropped in silence is caught",
            want=lambda r: len(r.silent_docs) == 1 and "b.xhtml" in r.silent_docs[0]
            and sum(r.missing.values()) == 4)

        run("Alpha bravo charlie delta.\n\nEcho foxtrot golf hotel.\n",
            dropped_docs=["c.xhtml"],
            label="the same drop, DECLARED, is silent",
            want=lambda r: r.ok and r.dropped == 1)

        # Undeclared partial loss inside a retained document -- the Einstein shape.
        run("Alpha bravo.\n\nEcho foxtrot golf hotel.\n\n"
            "Chittenden wrote this life of the author.\n",
            label="words lost mid-document are caught, and localised",
            want=lambda r: set(r.missing) == {"charlie", "delta"}
            and r.rare_by_doc.most_common(1)[0][0] == "a.xhtml")

        run("Alpha bravo charlie delta.\n\nEcho foxtrot golf hotel.\n\n"
            "Chittenden wrote this life of the author. Editorial gloss added here.\n",
            label="words we ADDED are reported separately from words we lost",
            want=lambda r: not r.missing and "gloss" in r.added)

        # A control that cannot fail is not a control: the declaration must not
        # be able to excuse a loss it does not name.
        run("Alpha bravo charlie delta.\n",
            dropped_docs=["c.xhtml"],
            label="declaring one removal does not excuse an undeclared second",
            want=lambda r: sum(r.missing.values()) == 4
            and any("b.xhtml" in s for s in r.silent_docs))

        # Emphasis markers must JOIN, not separate. Newton's `N<i>p</i>` is one
        # token in the source and `N*p*` in the output; treating `*` as a
        # boundary reported 4,323 phantom additions on the Principia alone.
        em_src = _epub(tmp, {"e.xhtml": "<p>Draw the line N<i>p</i>G to the point.</p>"})
        out.write_text("Draw the line N*p*G to the point.\n", encoding="utf-8")
        r = check(em_src, out, [], [])
        p = r.ok
        ok &= p
        print(f"  {'PASS' if p else 'FAIL'}  emphasis markers join words rather "
              f"than splitting them")

        # The same defect through the other marker, which is where it actually
        # bit: the source's running-text `AZ2` is set as `AZ<sup>2</sup>` and
        # printed `AZ^2^`.
        sup_src = _epub(tmp, {"s.xhtml": "<p>the area pDdm and AZ2 conjunctly.</p>"})
        out.write_text("the area pDdm and AZ^2^ conjunctly.\n", encoding="utf-8")
        r = check(sup_src, out, [], [])
        p = r.ok
        ok &= p
        print(f"  {'PASS' if p else 'FAIL'}  superscript markers join too "
              f"(`AZ^2^` is the source's `AZ2`)")

        # Notation the source set as running text may legitimately become math.
        math_src = _epub(tmp, {"m.xhtml": "<p>Then nn minus aa is the excess.</p>"})
        out.write_text("Then $nn$ minus $aa$ is the excess.\n", encoding="utf-8")
        r = check(math_src, out, [], [])
        p = not r.missing and set(r.promoted) == {"nn", "aa"}
        ok &= p
        print(f"  {'PASS' if p else 'FAIL'}  text notation promoted to math is "
              f"reported apart from damage")

        # And the bucket must not become an amnesty. A word genuinely lost is
        # still lost even if its letters happen to occur inside some formula.
        out.write_text("Then $nn$ minus $aa$ is the.\n", encoding="utf-8")
        r = check(math_src, out, [], [])
        p = "excess" in r.missing
        ok &= p
        print(f"  {'PASS' if p else 'FAIL'}  the math bucket does not excuse a "
              f"word that really went missing")

        # The amnesty in its subtler form, which is how it actually happened:
        # ONE occurrence inside a formula excusing MANY losses elsewhere.
        many = _epub(tmp, {"n.xhtml": "<p>because of one, of two, of three, of "
                                      "four, of five.</p>"})
        out.write_text("because $\\text{of}$ one, two, three, four, five.\n",
                       encoding="utf-8")
        r = check(many, out, [], [])
        p = r.missing.get("of") == 4 and r.promoted.get("of") == 1
        ok &= p
        print(f"  {'PASS' if p else 'FAIL'}  one word inside a formula excuses "
              f"ONE loss, not every loss of that word")

        # Preformatted alignment, which is content and not formatting.
        pre_src = _epub(tmp, {
            "p.xhtml": "<pre>     Grain.      Duties.\n Oats to 16s.    9d.\n</pre>"})
        out.write_text("<pre>\n     Grain.      Duties.\n Oats to 16s.    9d.\n</pre>\n",
                       encoding="utf-8")
        r = check(pre_src, out, [], [])
        p = not r.lost_pre and r.ok
        ok &= p
        print(f"  {'PASS' if p else 'FAIL'}  pre: preserved alignment passes")

        out.write_text("Grain. Duties. Oats to 16s. 9d.\n", encoding="utf-8")
        r = check(pre_src, out, [], [])
        p = len(r.lost_pre) == 1
        ok &= p
        print(f"  {'PASS' if p else 'FAIL'}  pre: flattened alignment is caught "
              f"even though every WORD survived")

    print("all controls pass" if ok else "CONTROLS FAILED")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    if "--self-test" in sys.argv:
        return selftest()
    ap.add_argument("epub", type=Path)
    ap.add_argument("markdown", type=Path)
    ap.add_argument("--dropped-doc", action="append", default=[], metavar="SUBSTRING",
                    help="a spine document removed on purpose; repeatable")
    ap.add_argument("--dropped-text", action="append", default=[], type=Path,
                    metavar="FILE", help="a file holding a passage removed on "
                                         "purpose; repeatable")
    args = ap.parse_args()

    passages = [p.read_text(encoding="utf-8") for p in args.dropped_text]
    r = check(args.epub, args.markdown, args.dropped_doc, passages)
    render(r, args.epub, args.markdown)
    return 0 if r.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
