#!/usr/bin/env python3
"""extract-lexicon.py — extract the Greek–English Lexicon from Fitzpatrick's Elements.

The lexicon pages (540-544 of Elements.pdf) set their Greek in dvipdfm
Type 3 fonts with junk glyph names AND a bogus 5-entry ToUnicode, so
normal text extraction yields raw CB-font byte codes ("¢gago n" for
ἤγαγον). The Type 3 byte layout is identical to the embedded CFF
`grmn1000` font used elsewhere in the book, whose encoding array names
every glyph semantically (uni1F24, alphatonos, sigma1, ...). So:

  1. parse grmn1000's CFF encoding -> code-to-glyphname -> Unicode
  2. walk the lexicon pages with get_texttrace() (Type 3 glyph ids ARE
     the byte codes — no dependence on PyMuPDF's char guessing)
  3. decode Type 3 spans through the table; pass Charter (Latin) spans
     through; insert spaces at >0.15 em positional gaps (TeX emits none)
  4. reassemble two-column hanging-indent entries: a line starting at
     the column margin opens an entry, indented lines continue it

Codes absent from the grmn1000 subset are filled by the CB layout's
iota-subscript symmetry (code+4 = same vowel+ypogegrammeni, +0x70 in
Unicode for the eta block) — every fill is listed at the end of the run;
any code that still can't be mapped is reported loudly as ⟦NNN⟧.

Usage:
    python3 ocr/text-specific-tools/euclid/extract-lexicon.py \\
        texts/1-ancient-greece/euclid-elements/source/Elements.pdf \\
        texts/1-ancient-greece/euclid-elements/source/lexicon.md
"""

from __future__ import annotations

import argparse
import io
import sys
from collections import Counter
from pathlib import Path

import pymupdf
from fontTools.cffLib import CFFFontSet

PAGES = range(540, 545)  # 1-based; p539 is the section title page
COLUMN_SPLIT_X = 312.0   # mid-gutter: col1 extends to ~308, col2 starts ~315
ENTRY_X_TOL = 3.0        # line at column margin ± this = new entry
SPACE_GAP_EM = 0.15
LINE_Y_TOL = 2.0

AGL = {
    'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'epsilon': 'ε',
    'zeta': 'ζ', 'eta': 'η', 'theta': 'θ', 'iota': 'ι', 'kappa': 'κ',
    'lambda': 'λ', 'mu': 'μ', 'nu': 'ν', 'xi': 'ξ', 'omicron': 'ο',
    'pi': 'π', 'rho': 'ρ', 'sigma': 'σ', 'sigma1': 'ς', 'tau': 'τ',
    'upsilon': 'υ', 'phi': 'φ', 'chi': 'χ', 'psi': 'ψ', 'omega': 'ω',
    'Alpha': 'Α', 'Beta': 'Β', 'Gamma': 'Γ', 'Epsilon': 'Ε', 'Zeta': 'Ζ',
    'Eta': 'Η', 'Theta': 'Θ', 'Iota': 'Ι', 'Kappa': 'Κ', 'Lambda': 'Λ',
    'Mu': 'Μ', 'Nu': 'Ν', 'Xi': 'Ξ', 'Omicron': 'Ο', 'Pi': 'Π',
    'Rho': 'Ρ', 'Sigma': 'Σ', 'Tau': 'Τ', 'Upsilon': 'Υ', 'Phi': 'Φ',
    'Chi': 'Χ', 'Psi': 'Ψ',
    'alphatonos': 'ά', 'epsilontonos': 'έ', 'etatonos': 'ή',
    'iotatonos': 'ί', 'omicrontonos': 'ό', 'upsilontonos': 'ύ',
    'omegatonos': 'ώ', 'upsilondieresis': 'ϋ', 'iotadieresis': 'ϊ',
    'tonos': '΄', 'anoteleia': '·', 'comma': ',', 'period': '.',
    'hyphen': '-', 'bracketleft': '[', 'bracketright': ']',
    'semicolon': ';', 'space': ' ',
    'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
    'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
}


def build_cb_table(doc: pymupdf.Document) -> dict[int, str]:
    """code -> unicode char, from the embedded grmn1000 CFF encoding."""
    xref = None
    for pno in range(doc.page_count):
        for f in doc[pno].get_fonts():
            if 'grmn' in f[3]:
                xref = f[0]
                break
        if xref:
            break
    if xref is None:
        raise RuntimeError("no grmn1000 font found in document")
    _, _, _, buf = doc.extract_font(xref)
    cff = CFFFontSet()
    cff.decompile(io.BytesIO(bytes(buf)), None)
    font = cff[cff.fontNames[0]]
    table: dict[int, str] = {}
    for code, name in enumerate(font.Encoding):
        if name == '.notdef':
            continue
        if name.startswith('uni'):
            table[code] = chr(int(name[3:], 16))
        elif name in AGL:
            table[code] = AGL[name]
    # Iota-subscript symmetry fill: in the CB layout each accented-vowel
    # block repeats 4 slots later with ypogegrammeni; the eta block's
    # Unicode points sit 0x70 below their plain forms (1F2x -> 1F9x).
    fills = []
    for code in range(128, 256):
        if code in table or (code - 4) not in table:
            continue
        base = ord(table[code - 4])
        if 0x1F20 <= base <= 0x1F27:           # eta with breathing/accent
            table[code] = chr(base + 0x70)     # + ypogegrammeni
            fills.append((code, table[code]))
    if fills:
        print("symmetry-filled codes:", ', '.join(f"{c}→{u}" for c, u in fills))
    # ASCII-identity punctuation the grmn subset lacks but the Type 3
    # sets use (47 = '/' in "ἐλάσσων/ἐλάττων").
    table.setdefault(47, '/')
    return table


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    doc = pymupdf.open(args.pdf)
    cb = build_cb_table(doc)
    unmapped: Counter = Counter()

    def decode_char(span_font: str, ch: tuple) -> str:
        uni, gid = ch[0], ch[1]
        if 'Type3' in span_font:
            if gid in cb:
                return cb[gid]
            unmapped[gid] += 1
            return f'⟦{gid}⟧'
        return chr(uni)

    entries: list[str] = []
    for pno in PAGES:
        page = doc[pno - 1]
        # collect positioned chars: (col, y, x, char, size, x_end)
        chars = []
        for span in page.get_texttrace():
            fname = span['font']
            if 'grmn' in fname:
                continue  # page numbers
            size = span.get('size', 10.0) or 10.0
            for ch in span['chars']:
                x, y = ch[2]
                x_end = ch[3][2]
                c = decode_char(fname, ch)
                chars.append((0 if x < COLUMN_SPLIT_X else 1, y, x, c, size, x_end))

        for col in (0, 1):
            col_chars = sorted((c for c in chars if c[0] == col),
                               key=lambda t: (round(t[1] / LINE_Y_TOL), t[2]))
            # group into lines
            lines: list[list[tuple]] = []
            last_y = None
            for t in col_chars:
                if last_y is None or abs(t[1] - last_y) > LINE_Y_TOL:
                    lines.append([])
                lines[-1].append(t)
                last_y = t[1]
            margin = min((ln[0][2] for ln in lines if ln), default=0.0)

            def append_continuation(text: str) -> None:
                # Line-wrap hyphen: 'in-' + 'transitive' joins tight with
                # the hyphen dropped. A spaced hyphen (' -') is content
                # ('conj' + '- conjunction', 'ἀδύνατος -ον') — keep it
                # and join with a space.
                prev = entries[-1]
                if prev.endswith('-') and not prev.endswith(' -'):
                    entries[-1] = prev[:-1] + text
                else:
                    entries[-1] = prev + ' ' + text

            seen_greek = False
            for ln in lines:
                text = ''
                prev_end = None
                for _, _, x, c, size, x_end in ln:
                    if prev_end is not None and x - prev_end > SPACE_GAP_EM * size:
                        text += ' '
                    text += c
                    prev_end = x_end
                text = text.strip()
                if not text or 'LEXICON' in text.upper() or 'ΣΤΟΙΧΕΙΩΝ' in text:
                    continue  # running header
                has_greek = any(0x370 <= ord(c) <= 0x1FFF for c in text)
                # The ABBREVIATIONS preamble (first page, column 1, above
                # the first Greek entry) is one flush-margin paragraph —
                # margin position alone would split it line-per-entry.
                in_preamble = (pno == PAGES[0] and col == 0 and not seen_greek
                               and not has_greek)
                seen_greek = seen_greek or has_greek
                starts_entry = abs(ln[0][2] - margin) <= ENTRY_X_TOL
                if in_preamble and entries:
                    append_continuation(text)
                    continue
                if starts_entry or not entries:
                    entries.append(text)
                else:
                    append_continuation(text)

    out = ["# Greek–English Lexicon", ""]
    for e in entries:
        out.append(e)
        out.append("")
    args.output.write_text("\n".join(out), encoding="utf-8")
    print(f"{len(entries)} entries -> {args.output}")
    if unmapped:
        print(f"UNMAPPED codes ({sum(unmapped.values())} occurrences) — fix before use:")
        for code, n in unmapped.most_common():
            print(f"  {code}: ×{n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
