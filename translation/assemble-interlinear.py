#!/usr/bin/env python3
"""Pair a witness and a translation into the reader's interlinear markup.

  translation/assemble-interlinear.py <run-dir> <translation.md> <lang> > out.md

For each segment ID in the witness, emits the original in `<div class="lang-LANG">`
followed immediately by the English in `<div class="lang-en">` -- the shape the
reader already pairs into interlinear rows for Euclid's Greek. Segment order is
the witness's. Footnotes collected after the last pair. Anything in the witness
with no English counterpart is an error, not a silent gap.
"""
import re, sys
from pathlib import Path

SEG = re.compile(r"<!--\s*seg:([A-Za-z0-9_\-]+)")

def blocks(text: str) -> dict[str, str]:
    body = text.split("\n---\n")[0] if "\n---\n" in text else text
    out = {}
    for s in SEG.findall(body):
        m = re.search(r"<!--\s*seg:" + re.escape(s) + r"\b.*?-->", body, re.S)
        rest = body[m.end():]
        n = re.search(r"<!--\s*seg:", rest)
        b = re.sub(r"<!--.*?-->", "", rest[: n.start()] if n else rest, flags=re.S)
        # The last segment runs to end of file, which in a witness means its
        # trailing ledger sections. A heading after the text is the text's end.
        b = re.split(r"\n#{1,3} ", b, maxsplit=1)[0] if s != "title" else b
        out[s] = b.strip("\n")
    return out

def strip_heading(s: str) -> str:
    s = re.sub(r"^#+\s*", "", s.strip()).rstrip(".")
    # an editor's item number ("XXI.") is apparatus, not title
    return re.sub(r"^[IVXLC]+\.\s+", "", s)

def footnotes(text: str) -> str:
    return text.split("\n---\n", 1)[1].strip("\n") if "\n---\n" in text else ""

def main(run: Path, trans: Path, lang: str) -> int:
    witness = next(run.glob("transcription-pass-*.md"))
    w, t = blocks(witness.read_text()), blocks(trans.read_text())
    missing = [s for s in w if s not in t]
    if missing:
        print(f"translation lacks segments: {missing}", file=sys.stderr)
        return 1
    out = []
    for s in w:
        a, b = w[s], t[s]
        if s == "title":
            # Headings live OUTSIDE the pairs, as Euclid's do: the reader sections
            # on headings and anchors both columns to them. The English title is
            # the document heading; the full titles then face each other as the
            # first pair, so the reader sees the original's wording too.
            a, b = strip_heading(a), strip_heading(b)
            out.append(f"# {b}\n")
            a, b = f"*{a}*", f"*{b}*"
        out.append(f'<div class="lang-{lang}">\n\n{a}\n\n</div>\n<div class="lang-en">\n\n{b}\n\n</div>\n')
    fn = footnotes(trans.read_text())
    if fn:
        out.append("\n" + fn + "\n")
    sys.stdout.write("\n".join(out))
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__); sys.exit(2)
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]))
