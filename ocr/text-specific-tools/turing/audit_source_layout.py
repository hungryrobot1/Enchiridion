#!/usr/bin/env python3
"""Assert the page-by-page table/figure counterpart audit for Turing 1936.

The visual adjudication was performed against all 36 rendered scan pages.  No
page contains an illustration, diagram, graph, photograph, or other genuinely
pictorial object.  Printed pp.233--241, 243--246, and 258 contain columnar or
array-like tables; the map below records a page-specific markdown counterpart
for every one.  Some dense skeleton tables were linearized as display math or
plain rows rather than Markdown pipe tables.  This audit establishes presence,
not correctness of any symbol or column alignment.

Usage:
    python3 audit_source_layout.py SOURCE.pdf RAW.md FINAL.md
"""

from __future__ import annotations

import sys
from pathlib import Path

import pymupdf


# PDF page -> (printed page, description, required OCR-page anchors)
TABLE_PAGES: dict[int, tuple[int, str, tuple[str, ...]]] = {
    4: (233, "first four-row computing-machine table", ("*Configuration*", "|  $b$ | None | $P0, R$ | $c$")),
    5: (234, "simplified table and five-configuration example", ("|  b | None | P0 | b", "|  q | Any (0 or 1) | R, R | q")),
    6: (235, "successive complete-configurations table and form (C)", ("|  : | ə | ə | 0", "\\tag{C}")),
    7: (236, "first skeleton table for f(C,B,a)", ("m-config. Symbol Behaviour Final m-config.", "f₁(ℭ, 𝔐, a)")),
    8: (237, "further skeleton-table examples", ("Further examples.", "\\mathfrak{pc}_1")),
    9: (238, "copy/replace/compare skeleton-table rows", ("\\mathfrak{c}\\mathfrak{c}_1", "\\mathfrak{c}\\mathfrak{p}_2")),
    10: (239, "find-last/copy/erase skeleton-table rows", ("\\mathfrak{q}_1", "\\mathfrak{p}\\mathfrak{e}_2")),
    11: (240, "three standard-form instruction rows", ("*m-config.*", "$q_i$ | $S_j$ | $PS_k, L$")),
    12: (241, "renamed four-row machine-I table", ("|  $q_1$ | $S_0$ | $PS_1, R$", "|  $q_4$ | $S_0$ | $PS_0, R$")),
    14: (243, "opening universal-machine e(anf) table", ("|  e(anf)", "e_1(\\text{anf})")),
    15: (244, "subsidiary skeleton table and opening U table", ("Subsidiary skeleton table.", "\\text{con}_2")),
    16: (245, "continuation of the universal-machine table", ("sim f'(sim₁, sim₁, z)", "mf₁")),
    17: (246, "final universal-machine instruction rows", ("|  inst |", "inst_{1}(N)")),
    29: (258, "modified-machine replacement and added rows", ("u_1", "\\operatorname{re}(u_3, u_3, k, h)")),
}


def main() -> int:
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    pdf_path, raw_path, final_path = map(Path, sys.argv[1:])
    doc = pymupdf.open(pdf_path)
    if doc.page_count != 36:
        raise AssertionError(f"expected 36 printed leaves, found {doc.page_count}")

    raw = raw_path.read_text(encoding="utf-8")
    pages = raw.split("\n\n---\n\n")
    if len(pages) != 36:
        raise AssertionError(f"expected 36 OCR page segments, found {len(pages)}")
    if "![" in raw:
        raise AssertionError("unexpected image reference in zero-image OCR result")

    for pdf_page in range(1, 37):
        printed = pdf_page + 229
        if pdf_page in TABLE_PAGES:
            expected_printed, description, anchors = TABLE_PAGES[pdf_page]
            if expected_printed != printed:
                raise AssertionError("table ledger printed-page mapping drifted")
            for anchor in anchors:
                if anchor not in pages[pdf_page - 1]:
                    raise AssertionError(
                        f"PDF {pdf_page}/printed {printed} lacks counterpart anchor {anchor!r}"
                    )
            print(
                f"PDF {pdf_page:02d} / printed {printed}: TABLE counterpart present — "
                f"{description}"
            )
        else:
            print(
                f"PDF {pdf_page:02d} / printed {printed}: no table and no pictorial object "
                "on visual page walk"
            )

    final = final_path.read_text(encoding="utf-8")
    restored = (
        "If we regard a symbol as literally printed on a square",
        "If $\\mathfrak{M}$ computes $\\gamma$",
        "A function $a_n$ may be defined in many other ways",
        "Although it is not possible to find a general process for determining whether a given number is satisfactory",
        "† *Loc. cit.*",
    )
    for anchor in restored:
        if final.count(anchor) != 1:
            raise AssertionError(f"restored-footnote anchor count is not one: {anchor!r}")

    print(
        "RESULT: all 14 printed table-bearing pages have textual counterparts; "
        "all 36 pages were visually walked; no genuinely pictorial object exists "
        "to extract; five scan-visible omitted footnotes are present in final markdown"
    )
    print(
        "LIMIT: this is a coverage audit only. It does not establish correctness "
        "of table entries, formulae, Fraktur letters, or subscripts."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
