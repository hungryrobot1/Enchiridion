#!/usr/bin/env python3
"""Clean the Mistral OCR of Taylor's Proclus Vol II (1792) — shared machinery
for both works in the volume: the Euclid-commentary continuation (Books
III–IV) and the Elements of Theology.

The OCR output is page-separated (--- between pages), which lets every pass
work page-aware against the ORIGINAL scan's IA text layer as witness:

  - **f→s repair**: Mistral renders the long-ſ three ways — modernized s
    (most pages), literal ſ (rare), and silently as f ("fome would rather
    chufe"). The IA layer preserves ſ faithfully as U+017F, so per page:
    an OCR token containing f that is ABSENT from the witness page, whose
    f→s variant IS present, is repaired. Deterministic lookup, not a
    heuristic. Literal ſ is mapped to s directly.
  - **catchwords**: the 1792 printer repeats the next page's first word at
    each page foot; a short final line equal to the next page's opening
    word is dropped.
  - **running heads**: despaced-uppercase page-top lines (COMMENTARIES OF
    PROCLUS / ELEMENTS OF THEOLOGY, with or without page number), bare
    page numbers, VOL. II. lines, and single gathering letters.
  - **proposition headings**: normalized to one level and sequence-checked;
    a heading repeating the current proposition or breaking the sequence is
    a recto running head and is dropped.
  - **Taylor's footnotes**: '* '-opening paragraphs dropped (editorial
    apparatus). Their cross-page continuations can interleave; suspected
    continuations (lowercase-opening paragraph at a page start that the
    rejoin pass refuses) are REPORTED for hand review, not guessed at.
  - glued headings split ("…theorem.### PROPOSITION VII"), letter-spaced
    headings despaced, page-boundary paragraphs rejoined.

Usage:
    python3 clean-vol2-ocr.py --work euclid   SPLIT.pdf OUT.md CHUNK.md...
    python3 clean-vol2-ocr.py --work theology SPLIT.pdf OUT.md CHUNK.md...

For --work euclid the page map skips the scan's re-shot signature (split
pages 67–82, a duplicate of 51–66 verified by hash + fuzzy comparison).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pymupdf

MARKER_STAR = re.compile(r"^\*\s")
PAGENUM_RE = re.compile(r"^\d{1,3}\.?$")
SIG_RE = re.compile(r"^(VOL\. ?II\.?( [A-Za-z])?|[A-Z]|[A-Z] ?\d)$")
NUMERAL_ITEM_RE = re.compile(r"^#{0,4}\s*([IVX]+)\.$")
PROP_RE = re.compile(
    r"^#{0,4}\s*P\s*R\s*O\s*P\s*O\s*S\s*I?\s*T\s*I?\s*O\s*N\s+([IVXLC]+)",
    re.I)
HEAD_GLUE_RE = re.compile(r"(\S)(#{1,4} )")
ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def roman_to_int(s: str) -> int | None:
    s = s.upper()
    if not s or any(c not in ROMAN for c in s):
        return None
    t = 0
    for i, c in enumerate(s):
        v = ROMAN[c]
        t += -v if i + 1 < len(s) and ROMAN[s[i + 1]] > v else v
    return t


def despace(s: str) -> str:
    return re.sub(r"\s+", "", s)


def norm_word(w: str) -> str:
    return re.sub(r"[^a-zſ]+", "", w.lower())


def f_variants(tok: str) -> list[str]:
    """All variants of tok with subsets of 'f' replaced by 's' (≤6 f's)."""
    idxs = [i for i, c in enumerate(tok) if c == "f"]
    if not idxs or len(idxs) > 6:
        return []
    out = []
    for mask in range(1, 1 << len(idxs)):
        chars = list(tok)
        for b, i in enumerate(idxs):
            if mask >> b & 1:
                chars[i] = "s"
        out.append("".join(chars))
    return out


def witness_tokens(page) -> set[str]:
    t = page.get_text().lower().replace("ſ", "s")
    return set(re.findall(r"[a-z]+", t))


def is_running_head(bare: str, forms: set[str]) -> bool:
    """Fuzzy match: OCR mangles running heads ('PEROCLUS'); accept when the
    despaced letters are within edit distance 2 of a known form."""
    if bare in forms:
        return True
    for f in forms:
        if abs(len(bare) - len(f)) <= 2 and len(bare) > 10:
            import difflib
            if difflib.SequenceMatcher(None, bare, f).ratio() > 0.85:
                return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", choices=["euclid", "theology"], required=True)
    ap.add_argument("split_pdf")
    ap.add_argument("out_md")
    ap.add_argument("chunks", nargs="+")
    args = ap.parse_args()

    doc = pymupdf.open(args.split_pdf)
    if args.work == "euclid":
        pagemap = [p for p in range(227) if not (67 <= p <= 82)]
        head_forms = {"COMMENTARIESOFPROCLUS"}
        prop_level = "## "
    else:
        # The EoT scan carries four clusters of re-shot leaves (verified by
        # fuzzy near-offset comparison + page renders: 49–50 dup 47–48,
        # 61–62 dup 59–60, 95–96 dup 93–94, 109–112 dup 105–108). The later
        # copies are dropped; chunk inputs must be pre-deduped to match.
        EOT_DROPS = {49, 50, 61, 62, 95, 96, 109, 110, 111, 112}
        pagemap = [p for p in range(len(doc)) if p not in EOT_DROPS]
        head_forms = {"ELEMENTSOFTHEOLOGY", "THEELEMENTSOFTHEOLOGY"}
        prop_level = "### "

    pages: list[list[str]] = []
    for c in args.chunks:
        cur: list[str] = []
        for chunk_page in Path(c).read_text().split("\n---\n"):
            pages.append(chunk_page.split("\n"))
    assert len(pages) == len(pagemap), f"{len(pages)} pages vs map {len(pagemap)}"

    stats = {"fs_fixed": 0, "long_s": 0, "runheads": 0, "pagenums": 0,
             "sigs": 0, "catchwords": 0, "footnotes": 0, "prop_runheads": 0,
             "glue_splits": 0, "rejoins": 0}
    review: list[str] = []

    # ---- page-aware passes ----
    cleaned_pages: list[list[str]] = []
    for k, lines in enumerate(pages):
        wit = witness_tokens(doc[pagemap[k]])
        out: list[str] = []
        for ln in lines:
            s = ln.strip()
            if not s:
                out.append("")
                continue
            bare = despace(re.sub(r"[^A-Za-z]", "", s)).upper()
            if s.strip("# ") == "":
                continue                      # empty heading artifact
            if "PROPOSIT" not in bare and is_running_head(bare, head_forms):
                stats["runheads"] += 1
                continue
            if PAGENUM_RE.match(s):
                stats["pagenums"] += 1
                continue
            if SIG_RE.match(s) and not PROP_RE.match(s):
                stats["sigs"] += 1
                continue
            # long-s literal
            if "ſ" in s:
                stats["long_s"] += s.count("ſ")
                s = s.replace("ſ", "s")
            # f->s witness repair, word by word
            words = s.split(" ")
            for i, w in enumerate(words):
                nw = norm_word(w)
                if "f" not in nw or nw in wit:
                    continue
                for v in f_variants(nw):
                    if v in wit:
                        # case-preserving rebuild: walk the original word,
                        # flipping f->s wherever the matched variant says so
                        res = []
                        j = 0
                        for ch in w:
                            cl = ch.lower()
                            if cl.isalpha() or cl == "ſ":
                                tgt = v[j] if j < len(v) else cl
                                if cl == "f" and tgt == "s":
                                    res.append("S" if ch.isupper() else "s")
                                else:
                                    res.append(ch)
                                j += 1
                            else:
                                res.append(ch)
                        words[i] = "".join(res)
                        stats["fs_fixed"] += 1
                        break
            out.append(" ".join(words))
        cleaned_pages.append(out)

    # catchwords: short last line == next page's first word
    for k in range(len(cleaned_pages) - 1):
        cur = cleaned_pages[k]
        nxt = cleaned_pages[k + 1]
        last = next((i for i in range(len(cur) - 1, -1, -1) if cur[i].strip()),
                    None)
        first = next((l for l in nxt if l.strip()), "")
        if last is None or not first:
            continue
        lw = cur[last].strip().rstrip("-—,.;:").lower()
        fw = re.sub(r"[^a-zA-Z'’-]", "", first.split(" ")[0]).lower()
        if lw and len(lw) < 20 and " " not in cur[last].strip() and lw == fw:
            cur.pop(last)
            stats["catchwords"] += 1

    # ---- document-level ----
    text = "\n".join("\n".join(p) for p in cleaned_pages)
    text, n = HEAD_GLUE_RE.subn(r"\1\n\n\2", text)
    stats["glue_splits"] = n
    # heading hyphen-split across a page ("# PROPO-" / "SITION XLIX")
    text = re.sub(r"PROPO-\s*\n+#*\s*SITION", "PROPOSITION", text)

    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

    def int_to_roman(n: int) -> str:
        vals = [(100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"),
                (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
        out = ""
        for v, r in vals:
            while n >= v:
                out += r
                n -= v
        return out

    out_paras: list[str] = []
    prop_no = 0
    thm_no = 0
    prb_no = 0
    for p in paras:
        m = PROP_RE.match(p)
        if m:
            n_ = roman_to_int(despace(m.group(1)))
            first_line, _, rest = p.partition("\n")
            if n_ == prop_no:
                # recto running head repeats the current proposition:
                # drop the heading line, keep any body that followed it
                stats["prop_runheads"] += 1
                if rest.strip():
                    out_paras.append(rest.strip())
                continue
            # a new section: force the sequence, warn on numeral mismatch
            # (the prop numeral and its THEOREM/PROBLEM subtitle numeral are
            # independent sequences — each corrects the other's OCR wobble)
            prop_no += 1
            title = re.sub(r"\s+", " ",
                           re.sub(r"^#+\s*", "", first_line)).strip()
            title = re.sub(r"P\s*R\s*O\s*P\s*O\s*S\s*I?\s*T\s*I?\s*O\s*N",
                           "PROPOSITION", title)
            if n_ != prop_no:
                review.append(
                    f"prop numeral forced: OCR {m.group(1)!r} -> "
                    f"{int_to_roman(prop_no)}: {title[:60]!r}")
                title = re.sub(r"(PROPOSITION )[IVXLC]+",
                               rf"\g<1>{int_to_roman(prop_no)}", title)
            sm = re.search(r"(THEOREM|PROBLEM)\.?\s*([IVXLC]*)", title)
            if sm:
                kind, num = sm.group(1), roman_to_int(sm.group(2) or "")
                if kind == "THEOREM":
                    thm_no += 1
                    want = thm_no
                else:
                    prb_no += 1
                    want = prb_no
                # Taylor's Prop I subtitle is unnumbered "PROBLEM." — it
                # consumes number 1 but stays as typeset
                if num is not None and num != want:
                    review.append(
                        f"{kind} numeral forced: OCR {sm.group(2)!r} -> "
                        f"{int_to_roman(want)} (in {title[:50]!r})")
                    title = re.sub(rf"({kind})\s*[IVXLC]*",
                                   rf"\1 {int_to_roman(want)}", title)
            elif prop_no > 1 and args.work == "euclid":
                review.append(f"prop without THEOREM/PROBLEM subtitle: "
                              f"{title[:60]!r}")
            out_paras.append(prop_level + title)
            if rest.strip():
                out_paras.append(rest.strip())
            continue
        if MARKER_STAR.match(p):
            stats["footnotes"] += 1
            continue
        out_paras.append(p)

    # ---- euclid structural assembly: Book III / Book IV ----
    if args.work == "euclid":
        DECOR = {"COMMENTARIES", "OF", "PROCLUS", "BOOKIII",
                 "CONCERNINGPETITIONSANDAXIOMS"}
        assembled: list[str] = ["# Book III. Concerning Petitions and Axioms."]
        in_book3 = True
        for p in out_paras:
            bare = despace(re.sub(r"[^A-Za-z]", "", p)).upper()
            if bare in DECOR and len(p) < 60:
                continue
            if bare == "BOOKIV":
                assembled.append("# Book IV.")
                in_book3 = False
                continue
            if bare == "AXIOMS" and len(p) < 20:
                assembled.append("## AXIOMS.")
                continue
            if bare in ("PETITIONSORPOSTULATES",) and len(p) < 40:
                assembled.append("## PETITIONS or POSTULATES.")
                continue
            m = NUMERAL_ITEM_RE.match(p)
            if m and in_book3:
                # petition/axiom item numeral -> h4 (renders inline under
                # the h2 label since no h3 exists between them)
                assembled.append(f"#### {m.group(1)}.")
                continue
            assembled.append(p)
        out_paras = assembled

    # ---- theology structural assembly ----
    if args.work == "theology":
        DECOR = {"ELEMENTS", "OF", "THEOLOGY", "THE"}
        COR_RE = re.compile(r"^#{0,4}\s*C\s*O\s*R\s*O\s*L\s*L\s*A\s*R\s*Y",
                            re.I)
        assembled = ["# THE ELEMENTS OF THEOLOGY",
                     "*Translated by Thomas Taylor*"]
        for p in out_paras:
            bare = despace(re.sub(r"[^A-Za-z]", "", p)).upper()
            first = p.split("\n")[0]
            if bare in DECOR and len(p) < 25:
                continue
            if COR_RE.match(first):
                rest = p.partition("\n")[2].strip()
                assembled.append("#### COROLLARY.")
                if rest:
                    assembled.append(rest)
                continue
            if first.startswith("#") and "PROPOSITION" not in first.upper():
                # Taylor's thematic topic head -> h2 group
                title = re.sub(r"\s+", " ",
                               re.sub(r"^#+\s*", "", first)).strip()
                assembled.append("## " + title)
                rest = p.partition("\n")[2].strip()
                if rest:
                    assembled.append(rest)
                continue
            assembled.append(p)
        out_paras = assembled

    # page-boundary paragraph rejoin (+ footnote-continuation reporting).
    # An image-ref paragraph (inline diagram) may interrupt a sentence; the
    # text is rejoined across it and the image kept in place before the
    # merged paragraph.
    TERMINAL = tuple(".!?:;”’)")
    IMG_RE = re.compile(r"^!\[")
    i = 0
    while i < len(out_paras):
        p = out_paras[i]
        if not p.startswith("#") and not IMG_RE.match(p):
            j = i + 1
            while j < len(out_paras) and IMG_RE.match(out_paras[j]):
                j += 1
            if (j < len(out_paras) and not p.endswith(TERMINAL)
                    and not out_paras[j].startswith("#")
                    and out_paras[j][:1].islower()):
                imgs = out_paras[i + 1:j]
                out_paras[i:j + 1] = imgs + [p + " " + out_paras[j]]
                stats["rejoins"] += 1
                continue
        i += 1
    for i, p in enumerate(out_paras):
        if p[:1].islower():
            review.append(f"lowercase-start para (footnote continuation?): "
                          f"{p[:70]!r}")

    Path(args.out_md).write_text("\n\n".join(out_paras) + "\n")
    print(f"pages: {len(pages)}   paragraphs: {len(out_paras)}   "
          f"propositions: {prop_no}")
    print("   ".join(f"{k}={v}" for k, v in stats.items()))
    print(f"output: {args.out_md}")
    print(f"review items: {len(review)}")
    for r in review[:40]:
        print("  ⚠ " + r)
    return 0


if __name__ == "__main__":
    main()
