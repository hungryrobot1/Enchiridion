#!/usr/bin/env python3
"""Run the shipped EPUB completeness check with XHTML block boundaries visible.

Faraday's EPUB minifies table cells and definition-list entries with no
inter-element whitespace.  lxml's ``text_content()`` therefore presents e.g.
``<td>acid</td><td>0.16</td>`` as the invented source token ``acid0`` while the
extractor correctly emits separate Markdown cells.  The shipped checker reports
205 false losses on its own raw extraction.  This wrapper changes only source
tokenisation: block elements contribute a boundary space, then the authoritative
checker performs its normal accounting.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from lxml import html as lxml_html


BLOCK_ELEMENTS = {
    "address", "article", "aside", "blockquote", "br", "caption", "dd",
    "div", "dl", "dt", "figcaption", "figure", "footer", "h1", "h2",
    "h3", "h4", "h5", "h6", "header", "hr", "li", "main", "nav", "ol",
    "p", "pre", "section", "table", "tbody", "td", "tfoot", "th", "thead",
    "tr", "ul",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("epub", type=Path)
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--dropped-text", action="append", type=Path, default=[])
    parser.add_argument(
        "--checker",
        type=Path,
        default=Path(
            "/Users/zacharygrunenberg/Projects/Enchiridion/ocr/verify/"
            "check-completeness.py"
        ),
    )
    args = parser.parse_args()

    spec = importlib.util.spec_from_file_location("enchiridion_completeness", args.checker)
    assert spec and spec.loader
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)

    def boundary_aware_document_text(raw: bytes) -> str:
        doc = lxml_html.fromstring(raw)
        for element in list(doc.iter()):
            if isinstance(element.tag, str) and element.tag in checker.SKIP:
                parent = element.getparent()
                if parent is not None:
                    parent.remove(element)
        for element in doc.iter():
            if isinstance(element.tag, str) and element.tag in BLOCK_ELEMENTS:
                element.tail = " " + (element.tail or "")
        body = doc.find("body")
        return (body if body is not None else doc).text_content()

    checker.document_text = boundary_aware_document_text
    declared = [path.read_text(encoding="utf-8") for path in args.dropped_text]
    result = checker.check(args.epub, args.markdown, [], declared)
    checker.render(result, args.epub, args.markdown)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
