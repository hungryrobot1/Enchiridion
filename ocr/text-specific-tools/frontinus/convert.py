#!/usr/bin/env python3
"""Convert Frontinus, The Aqueducts of Rome (Bennett, Loeb 1925) to markdown.

Source: Bill Thayer's LacusCurtius transcription of the Loeb (Charles E.
Bennett) translation, as two HTML files (book_1.htm = paragraphs 1-63,
book_2.htm = 64-130; De Aquis is one work of 130 numbered sections split
into two books at 64). The text is faithful; what surrounds it is Thayer's
web apparatus.

Apparatus-stripping policy — the text itself only:
  DROP  the site nav / frontmatter, the boxed reader prompts, the page-
        number markers (p331 ...), the parallel-translation links ('R 2003'
        -> Rodgers 2003), the Latin-original flag images, footnote/endnote
        reference marks, Thayer's commentary boxes (the <table>s, e.g. the
        'aqua' notes), and everything from '<hr class="endnotes">' on (the
        Loeb Editor's Notes and Thayer's Notes).
  KEEP  Frontinus's text, the paragraph numbers (his native citation unit,
        kept as inline bold marks per the Loeb), the section headings
        (Preface; the Book divisions become the '# ' headings), the inline
        Latin technical terms (quinariae &c., set italic as in the Loeb),
        the fractions, and the lacuna asterisks.

--apply writes the merged markdown into the text dir; otherwise a review
copy goes to the scratchpad.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import lxml.html

BASE = Path("/Users/zacharygrunenberg/Projects/Enchiridion/texts/"
            "2-rome-late-antiquity/frontinus-aqueducts-of-rome")
FILES = [(BASE / "book_1.htm", "BOOK I"), (BASE / "book_2.htm", "BOOK II")]
OUT_MD = BASE / "frontinus-aqueducts-of-rome.md"
SCRATCH = Path("/private/tmp/claude-501/-Users-zacharygrunenberg-Projects-"
               "Enchiridion/afeb733e-335c-49f1-8e55-2cc8004cbfed/scratchpad/"
               "frontinus-review.md")
TITLE = "THE AQUEDUCTS OF ROME"

report: list[str] = []


def clean_ws(s: str) -> str:
    # drop the zero-width / word-joiner chars left where footnote-reference
    # superscripts were removed, and normalize nbsp + whitespace
    s = re.sub(r"[​‌‍⁠﻿­]", "", s)
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def prepare(root):
    """Strip apparatus nodes in place and normalize inline Latin/fractions."""
    drops = {"table": 0, "img": 0, "link": 0, "pagenum": 0, "box": 0}
    for el in root.xpath("//table"):
        el.drop_tree(); drops["table"] += 1
    for el in root.xpath("//img | //script | //style | //hr"):
        el.drop_tree(); drops["img"] += 1
    for el in root.xpath('//div[contains(@class,"boxlinksprompt")] '
                         '| //div[contains(@class,"contents")]'):
        el.drop_tree(); drops["box"] += 1
    for el in root.xpath('//a[contains(@class,"parallel")] '
                         '| //a[contains(@class,"ref")] '
                         '| //a[contains(@class,"note")]'):
        el.drop_tree(); drops["link"] += 1
    for el in root.xpath('//span[contains(@class,"pagenum")]'):
        el.drop_tree(); drops["pagenum"] += 1
    # fractions: <span class="fraction"><span top>5</><span bottom>12</></> -> 5/12
    for fr in root.xpath('//span[contains(@class,"fraction")]'):
        top = fr.xpath('.//span[contains(@class,"top")]')
        bot = fr.xpath('.//span[contains(@class,"bottom")]')
        tail = fr.tail
        for c in list(fr):
            fr.remove(c)
        fr.text = (f"{clean_ws(top[0].text_content())}/"
                   f"{clean_ws(bot[0].text_content())}") if top and bot else ""
        fr.tail = tail
    # inline Latin technical terms -> italic (as set in the Loeb)
    for la in root.xpath('//span[@lang="la"]'):
        t = clean_ws(la.text_content())
        tail = la.tail
        for c in list(la):
            la.remove(c)
        la.text = f"*{t}*" if t else ""
        la.tail = tail
    report.append(f"stripped: {drops}")


def convert(path, book_label, want_title):
    raw = path.read_text(encoding="utf-8", errors="replace")
    raw = raw.split('<hr class="endnotes">')[0]   # drop notes sections
    root = lxml.html.fromstring(raw)
    prepare(root)

    out: list[str] = []
    if want_title:
        out.append(f"# {TITLE}")
    out.append(f"# {book_label}")

    n_para = n_quote = 0
    started = False                                    # skip nav/frontmatter
    for el in root.iter("h1", "h2", "p"):
        if el.tag == "h1":
            started = True                            # title -> body follows
            continue                                  # work title added above
        if not started:
            continue
        if el.tag == "h2":
            # the only section headings are '[Preface]' and the 'Book I/II'
            # labels; both are dropped — the Book divisions are the '# '
            # headings, and the preface (paragraphs 1-2) reads continuously
            # with the rest of Book I (no lone sub-collapsible). User, 2026-07-22.
            continue
        # a body paragraph carries a chapter (= paragraph) number anchor
        ch = el.xpath('.//a[contains(@class,"chapter")]')
        num = clean_ws(ch[0].text_content()) if ch else ""
        for a in ch:
            a.drop_tree()
        text = clean_ws(el.text_content())
        if not text and not num:
            continue
        # tidy: space before punctuation, spaced-out italics/fraction edges
        text = re.sub(r"\s+([,.;:?!])", r"\1", text)
        line = f"**{num}** {text}" if num else text
        # paragraphs Frontinus quotes verbatim (senate resolutions, edicts,
        # the lex Quinctia) sit in <div class="prose"> -> block quote
        if el.xpath('ancestor::div[contains(@class,"prose")]'):
            line = "> " + line
            n_quote += 1
        out.append(line)
        if num:
            n_para += 1
    report.append(f"{book_label}: {n_para} paragraphs, {n_quote} quoted")
    return "\n\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    parts = [convert(p, label, i == 0) for i, (p, label) in enumerate(FILES)]
    text = "\n\n".join(parts)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    print("\n".join(report))
    h1 = len(re.findall(r"^# ", text, re.M))
    h2 = len(re.findall(r"^## ", text, re.M))
    paras = len(re.findall(r"^\*\*\d+\*\*", text, re.M))
    print(f"\noutput: {len(text)} chars, {h1} h1, {h2} h2, {paras} paragraphs")

    SCRATCH.write_text(text)
    print(f"review copy: {SCRATCH}")
    if args.apply:
        OUT_MD.write_text(text)
        print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    main()
