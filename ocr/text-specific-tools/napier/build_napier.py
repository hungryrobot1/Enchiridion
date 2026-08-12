#!/usr/bin/env python3
"""Build reader-ready Napier Markdown from the 79-page raw OCR.

All transformations are count-asserted.  Repairs here use either internal
evidence (page-turn duplication, impossible English, signatures/catchwords) or
page evidence explicitly recorded in NOTES.md (drop capitals and one Briggs
table whose geometry the OCR collapsed).
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path


KEEP_IMAGES = {
    "img-6.jpeg": "Line divided at b into segments a-b and b-c",
    "img-7.jpeg": "Line marked at equal intervals from b to d",
    "img-8.jpeg": "Line TS marked with decreasing intervals",
    "img-9.jpeg": "Geometrical and arithmetical motion diagram",
    "img-10.jpeg": "Diagram of the limits of a logarithm",
    "img-11.jpeg": "Line b-c-d-e-f",
    "img-12.jpeg": "Line b-a-c-d-e-g-f",
    "img-13.jpeg": "Line V-T-c-d-e-S",
    "img-14.jpeg": "Semicircle construction for Proposition 55",
    "img-15.jpeg": "Semicircle construction for Proposition 56",
    "img-23.jpeg": "Spherical triangle A-B-C-D",
    "img-27.jpeg": "Semicircle demonstration in Briggs's notes",
}


def replace_exact(text: str, before: str, after: str, expected: int = 1) -> str:
    count = text.count(before)
    assert count == expected, (repr(before[:100]), count, expected)
    return text.replace(before, after)


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} RAW.md OUT.md")
    raw, out = map(Path, sys.argv[1:])
    text = raw.read_text(encoding="utf-8")

    assert len(text.split("\n\n---\n\n")) == 79
    assert text.count("\n\n---\n\n") == 78
    assert len(re.findall(r"^!\[img-\d+\.jpeg\]", text, re.M)) == 29
    assert len(re.findall(r"^\|(?:.*\|)\s*$", text, re.M)) == 220

    # Seventeen OCR-extracted ornaments and drop capitals are decoration, not
    # figures.  Keep the twelve diagrams on which the arguments depend.
    for number in [0, 1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26]:
        text = replace_exact(
            text, f"![img-{number}.jpeg](images/img-{number}.jpeg)\n\n", ""
        )
    text = replace_exact(text, "![img-28.jpeg](images/img-28.jpeg)", "")
    for filename, alt in KEEP_IMAGES.items():
        text = replace_exact(
            text,
            f"![{filename}](images/{filename})",
            f"![{alt}](images/{filename})",
        )

    # The printed divisions and attributions, consolidated from display lines.
    text = replace_exact(
        text,
        "# TO THE READER STUDIOUS OF\n\n# THE MATHEMATICS,\n\n# GREETING.",
        "# PREFACE BY ROBERT NAPIER",
    )
    text = replace_exact(text, "# TO THE READER.\n\n", "", 2)
    text = replace_exact(
        text,
        "# THE CONSTRUCTION OF\nTHE WONDERFUL CANON\n\nOF LOGARITHMS; ( HEREIN\n\n"
        "CALLED BY THE AUTHOR\n\nTHE ARTIFICIAL TABLE )\n\nand their relations to\n\n"
        "their natural\n\nnumbers.",
        "# THE CONSTRUCTION OF THE WONDERFUL CANON OF LOGARITHMS\n\n"
        "*(Herein called by the Author the Artificial Table), and their relations "
        "to their natural numbers.*",
    )
    text = replace_exact(text, "# CONSTRUCTION OF THE CANON.\n\n", "", 2)
    text = replace_exact(
        text,
        "# SOME REMARKS\n## BY THE LEARNED\n### HENRY BRIGGS\nOn the foregoing APPENDIX.",
        "# REMARKS ON THE APPENDIX BY HENRY BRIGGS",
    )
    text = replace_exact(text, "# REMARKS ON APPENDIX.\n\n", "", 2)
    text = replace_exact(
        text,
        "# SOME VERY REMARKABLE\n*PROPOSITIONS FOR THE*\nsolution of spherical triangles\n"
        "*with wonderful ease.*",
        "# SOME VERY REMARKABLE PROPOSITIONS FOR THE SOLUTION OF SPHERICAL "
        "TRIANGLES WITH WONDERFUL EASE",
    )
    text = replace_exact(
        text,
        "# SOME NOTES\n\n## BY THE LEARNED\n\n## HENRY BRIGGS\n\n"
        "## ON THE FOREGOING PROPOSITIONS.",
        "# NOTES ON THE FOREGOING PROPOSITIONS BY HENRY BRIGGS",
    )
    text = text.replace("# EXAMPLE.", "## EXAMPLE.")
    text = text.replace("### EXAMPLE.", "## EXAMPLE.")
    text = text.replace("### ANOTHER EXAMPLE.", "## ANOTHER EXAMPLE.")
    text = text.replace("# ANOTHER EXAMPLE.", "## ANOTHER EXAMPLE.")
    text = text.replace("# THIRD EXAMPLE.", "## THIRD EXAMPLE.")
    text = replace_exact(text, "# [B] If a first sine divide a third, )", "## [B] If a first sine divide a third")
    text = replace_exact(text, "### *Hence it follows that the logarithm )*", "## [C] Hence it follows that the logarithm")
    text = replace_exact(text, "\n\n[C]\n\n", "\n\n")

    # Drop-cap letters are visible in the retained scans.  These repairs also
    # restore words that are impossible in English without the initial glyph.
    for before, after, count in [
        ("EVERAL years ago", "SEVERAL years ago", 1),
        ("MONG the various", "AMONG the various", 1),
        ("WO numbers with", "TWO numbers with", 1),
        ("IVEN an arc", "GIVEN an arc", 1),
        ("L Et two sines", "LET two sines", 1),
        ("ADd together", "ADD together", 1),
        ("*IVEN three sides", "*GIVEN three sides", 1),
    ]:
        text = replace_exact(text, before, after, count)
    text = replace_exact(text, "I. LOGARITHMIC TABLE", "1. LOGARITHMIC TABLE")
    text = replace_exact(text, "LOGA-RITHMS", "LOGARITHMS")
    text = replace_exact(text, "8c", "&c.", 3)
    # Scan/editorial debris verified on the page: the faint pencilled `(2005)`
    # on PDF p.32 is not part of the typesetting, while the standalone
    # correction on PDF p.38 points into Macdonald's excluded translator notes.
    text = replace_exact(text, " (2005)", "")
    text = replace_exact(
        text, "\n\n[This should be 9995001.224804—see note.]", ""
    )
    text = replace_exact(text, " [BBOX]0.2000,0.5000,0.3000,0.6000[/BBOX]", "")
    text = replace_exact(text, " [BBOX]0.2000,0.6000,0.3000,0.6000[/BBOX]", "")

    # The first Briggs example was flattened together with a signature and
    # catchword.  PDF pp.79-80 show a three-column arrangement continued by
    # the common divisor and multiplication statement.
    text = replace_exact(
        text,
        "|  Let the given numbers be | $$\\begin{cases} 25118865 \\\\ 39810718 "
        "\\end{cases}$$ | Logarithms. 4 6  |\n| --- | --- | --- |\n|  G | 4 | Let  |"
        "\n\n---\n\nLet the common divisor be\n\nI\n\nThe first multiplied by "
        "itself 5 times\nThe second ,, ,, 3 ,, } makes 251188649\n1000000",
        "|  | Number | Logarithm |\n| --- | --- | --- |\n"
        "| Let the given numbers be | 25118865 | 4 |\n"
        "|  | 39810718 | 6 |\n\n"
        "Let the common divisor be 1.\n\n"
        "The first multiplied by itself 5 times, and the second 3 times, "
        "make 251188649/1000000.",
    )
    # Page-verified digit repairs: PDF p.80 prints the number 1 in these
    # arithmetic tables; OCR read the old-style digit as capital I.
    text = replace_exact(text, "|  I | (0) |  | 0  |", "|  1 | (0) |  | 0  |", 2)
    text = replace_exact(
        text,
        "|  Let the common divisor be |  | I  |",
        "|  Let the common divisor be |  | 1  |",
    )

    # Page furniture and catchwords.  Each longer anchor ensures an actual
    # body occurrence cannot be silently removed.
    furniture = [
        "\n\nA 4\n\n2. Of",
        "\n\nB 3 contains",
        "\n\nC 2 28. Whence",
        "\n\nD 2\n\nEXAMPLE.",
        "\n\nD 3 limit,",
        "\n\nE 3\n\n51. All",
        "\n\nF 4 APPENDIX.",
        "\n\nG 2\n\nA saving",
        "\n\nG 3\n\nBut,",
        "\n\nH 4\n\nSOME",
        "\n\nK\n\nAgain,",
        "\n\nK 2\n\nSOME",
        "\n\nK 4 Proportion.",
    ]
    for value in furniture:
        text = replace_exact(text, value, "")

    # Exact page-turn repairs.  The document itself supplies both halves or a
    # duplicated catchword, so these need no conjectural reading.
    repairs = [
        ("men\n\ntioned", "mentioned"),
        ("being\n\n---\n\nbeing left", "being left"),
        ("9999998. 0005021\n\n---\n\n0005021 is", "9999998.0005021 is"),
        ("the*\n\n---\n\nless of the other", "the less of the other"),
        ("and\n\n---\n\nand 43.1", "and 43.1"),
        ("carried on\n\n---\n\neasily", "carried on easily"),
        ("Thus\n\n---\n\nFirst table.", "Thus:\n\nFirst table."),
        ("proceed from\nradius\n\n---\n\nradius with", "proceed from radius with"),
        ("geometrically their\n\n---\n\ntheir logarithms", "geometrically their logarithms"),
        ("C 3 S,\n\n---\n\n3 S,", "3 S,"),
        ("distances T S, 1 S,\n\n---\n\n1 S, 2 S", "distances T S, 1 S, 2 S"),
        ("and T d\n\n---\n\nT d the less", "and T d the less"),
        ("proportionals of the First table. You may in this way\n\n---\n\nway,", "proportionals of the First table. You may in this way,"),
        ("For since by\n\nthese\n\n---\n\nthese definitions", "For since by these definitions"),
        ("making the differences\n\n---\n\nferences", "making the differences"),
        ("difference of the sines\n\n---\n\nsines. Then", "difference of the sines. Then"),
        ("of the given sine\n\n---\n\nsine and the table sine", "of the given sine and the table sine"),
        ("100.0005050 for the greater\n\n---\n\nlimit,", "100.0005050 for the greater limit,"),
        ("all the proportionals\n\n---\n\ntionals in", "all the proportionals in"),
        ("in the first column\n\n---\n\ncolumn of", "in the first column of"),
        ("you prefer to com-\n\nE\n\npute\n\n---\n\npute,", "you prefer to compute,"),
        ("third Radical table\n\n---\n\ntable serves", "third Radical table serves"),
        ("will, as regards the difference of the logarithms, correspond\n\nto\n\n---\n\nto the proportion", "will, as regards the difference of the logarithms, correspond to the proportion"),
        ("until you obtain a number within the limits of the Radical table. By 50\n\n---\n\nfind the logarithm", "until you obtain a number within the limits of the Radical table. By 50 find the logarithm"),
        ("then e i\n\nis\n\n---\n\nis the sine", "then e i is the sine"),
        ("whose logarithm\n\n---\n\nlogarithm is required", "whose logarithm is required"),
        ("under the last\n\n---\n\nthree columns", "under the last three columns"),
        ("From\n\n---\n\nFrom the Radical", "From the Radical"),
        ("which\ncorrespond\n\n---\n\ncorrespond to", "which correspond to"),
        ("G\n\nFor\n\n---\n\nFor as", "For as"),
        ("Also\n\n---\n\nAlso if", "Also if"),
        ("Therefore\n\n---\n\nTherefore take", "Therefore take"),
        ("Proposition; H 2 but\n\n---\n\nbut they", "Proposition; but they"),
        ("numbers of the\n\n---\n\n*the quotients", "numbers of *the quotients"),
        ("the num-*\n\n---\n\nber of quotients", "the number of quotients"),
        ("adhering to the\n\n---\n\nthe last quotient", "adhering to the last quotient"),
        ("4. *Given*\n\n---\n\n4. Given", "4. Given"),
        ("will be produced;\n\n---\n\nproduced; its arc", "will be produced; its arc"),
        ("10. Given\n\n---\n\n10. Given", "10. Given"),
        ("to be\n\nthree\n\n---\n\nthree times", "to be three times"),
        ("3. Given two arcs, to find a third, whose sine shall be equal to the difference of the sines of the given arcs.\n\nLet\n\n---\n\nLet the arcs", "3. Given two arcs, to find a third, whose sine shall be equal to the difference of the sines of the given arcs.\n\nLet the arcs"),
        ("The sum of the two arcs is 18° 40', the half sum 9° 20', and their logarithms 1139241 and 1819061 respectively. Also the difference of the two arcs is 17° 12', the half difference 8° 36', and their logarithms 1218382 and 1900221 respectively.\n\nNow\n\n---\n\nNow add", "The sum of the two arcs is 18° 40', the half sum 9° 20', and their logarithms 1139241 and 1819061 respectively. Also the difference of the two arcs is 17° 12', the half difference 8° 36', and their logarithms 1218382 and 1900221 respectively.\n\nNow add"),
        ("its logarithm\nI 4 14449;\n\n---\n\n14449;", "its logarithm 14449;"),
        ("divide by\n\n---\n\nby the half difference", "divide by the half difference"),
        ("required versed sine. To this logarithm\n\n---\n\nlogarithm add", "required versed sine. To this logarithm add"),
        ("their loga-\nK 3 rithms\n\n---\n\nrithms", "their logarithms"),
        ("Thus:—\n\nLet\n\n---\n\nLet there", "Thus:—\n\nLet there"),
        ("uniformly maintained, whether\n\n---\n\nwhether there", "uniformly maintained, whether there"),
    ]
    for before, after in repairs:
        text = replace_exact(text, before, after)

    # Page separators that remain now mark neither content nor navigation.
    remaining = text.count("\n\n---\n\n")
    assert remaining == 30, remaining
    text = text.replace("\n\n---\n\n", "\n\n")

    # Remove a few isolated signatures/catchwords whose adjoining page already
    # carries the complete reading.
    for before in ["\n\nF\n", "\n\nG\n", "\n\nH\n", "\n\nI\n"]:
        text = text.replace(before, "\n")

    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    assert text.startswith("# THE CONSTRUCTION OF THE WONDERFUL CANON")
    assert text.count("\n# ") == 6
    assert not re.search(r"^---$", text, re.M)
    assert len(re.findall(r"^!\[", text, re.M)) == 12
    assert len(re.findall(r"^\|(?:.*\|)\s*$", text, re.M)) == 221
    assert "NOTES BY THE TRANSLATOR" not in text

    out.write_text(text, encoding="utf-8")
    image_dir = out.parent / "images"
    image_dir.mkdir(exist_ok=True)
    source_images = raw.parent / "images"
    for filename in KEEP_IMAGES:
        shutil.copy2(source_images / filename, image_dir / filename)
    print(
        f"{out}: 79 OCR pages -> 6 top-level divisions; retained 26 tables "
        f"and {len(KEEP_IMAGES)} diagrams; removed 17 ornaments; repaired "
        f"46 asserted page-turn/furniture anchors"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
