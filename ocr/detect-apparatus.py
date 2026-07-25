#!/usr/bin/env python3
"""Detect leftover editorial/scholarly apparatus in a corpus text.

House policy: a text's markdown is the text itself only — editor/translator
commentary, scholarly footnotes, and modern historical notes are stripped.
Some texts (Heath's Diophantus especially) were extracted with the apparatus
still interleaved. This flags candidate apparatus paragraphs for review.

Heuristic (tuned for math texts, whose real content is mostly short lines):
  HIGH  — paragraph names a post-classical mathematician, cites a modern work,
          or carries a modern date / cross-reference marker. Nearly always
          apparatus; Diophantus cannot mention Fermat.
  REVIEW — long prose (>= --min-words) with no signal. Usually legitimate
          (a text's own definitions, long problem enunciations) — eyeball
          before cutting.

Usage:  python3 ocr/detect-apparatus.py <file.md> [--min-words 45] [--high-only]
"""
import re, sys, argparse

# Names/markers that can only be editorial in an ancient text. Deliberately NOT
# bare 4-digit numbers — a math text's arithmetic is full of them (1681 = 41²).
SIGNALS = re.compile(r"""\b(
    Fermat|Bachet|Xylander|Tannery|Nesselmann|Wertheim|Cossali|Vieta|Vi[eè]te|
    Euler|Lagrange|Gauss|Dirichlet|Kummer|Wieferich|Cauchy|Legendre|
    Diophantus\s+himself|the\s+fragment|
    Oeuvres|Bulletin|Encyclop[aä]|will\s+be\s+given\s+in\s+.*Supplement|
    in\s+the\s+Supplement|Bachet's\s+note|A\.?D\.?\s*1[0-9]{3}|
    Theon|Hiller|Heiberg|Hultsch|Nesselmann|D'Ooge|
    p\.\s*\d+,\s*\d+|\bff\.(?:\s|$)|,\s*ed\.
)\b""", re.VERBOSE)

def paragraphs(text):
    off, out = 0, []
    for chunk in re.split(r"(\n\s*\n)", text):
        if chunk.strip() and not re.fullmatch(r"\n\s*\n", chunk):
            line = text.count("\n", 0, off) + 1
            out.append((line, chunk.strip()))
        off += len(chunk)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--min-words", type=int, default=45)
    ap.add_argument("--high-only", action="store_true")
    a = ap.parse_args()
    text = open(a.file).read()
    high, review = [], []
    for line, p in paragraphs(text):
        if p.startswith("#"):
            continue
        words = len(p.split())
        if SIGNALS.search(p):
            high.append((line, words, p))
        elif words >= a.min_words:
            review.append((line, words, p))

    def show(label, items):
        print(f"\n===== {label} ({len(items)}) =====")
        for line, words, p in items:
            head = " ".join(p.split()[:18])
            print(f"  L{line:<5} {words:>4}w  {head}…")

    show("HIGH — apparatus (strip)", high)
    if not a.high_only:
        show("REVIEW — long prose, no signal", review)
    print(f"\nHIGH={len(high)}  REVIEW={len(review)}")

if __name__ == "__main__":
    main()
