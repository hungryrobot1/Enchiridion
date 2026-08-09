#!/usr/bin/env python3
"""Apply readings verified against printed Nature pages 737–738.

Every replacement below has an exact anchor and asserted count.  These are
stage-4 repairs: each was adjudicated from the supplied scan, not inferred from
frequency or from the corrupted embedded OCR layer.
"""

from pathlib import Path


PATH = Path(__file__).resolve().parent / "watson-crick-molecular-structure-of-nucleic-acids.md"

# (printed page, before, after, reason)
REPAIRS = [
    (
        737,
        "The two ribbons symbolize the two phosphate-sugar chains",
        "The two ribbons symbolise the two phosphate-sugar chains",
        "British spelling is legible in the printed caption",
    ),
    (
        737,
        "The vertical line marks the fibre axis\n\n",
        "The vertical line marks the fibre axis.\n\n",
        "printed caption ends with a full stop",
    ),
    (
        737,
        "β-D-deoxy-ribofuranose residues with 3',5' linkages",
        "β-D-deoxyribofuranose residues with 3′,5′ linkages",
        "printed line-wrap hyphen removed; raised prime marks preserved",
    ),
    (
        737,
        "Each chain loosely resembles Furberg's model No. 1;",
        "Each chain loosely resembles Furberg's² model No. 1;",
        "printed superscript reference 2 was dropped by OCR",
    ),
    (
        737,
        "every 3.4 A. in the z-direction",
        "every 3·4 A. in the z-direction",
        "printed decimal mark is a centred dot",
    ),
    (
        737,
        "It has been found experimentally¹,⁴",
        "It has been found experimentally³,⁴",
        "printed citations are references 3 and 4",
    ),
    (
        737,
        "The previously published X-ray data¹,⁴",
        "The previously published X-ray data⁵,⁶",
        "printed citations are references 5 and 6",
    ),
    (
        738,
        "Proc. U.S. Nat. Acad. Sci., 33, 84 (1953)",
        "Proc. U.S. Nat. Acad. Sci., 39, 84 (1953)",
        "printed volume is 39",
    ),
    (
        738,
        "for references see Zamcahof, S.",
        "for references see Zamenhof, S.",
        "printed surname is Zamenhof",
    ),
    (
        738,
        "J. Gen. Physiol., 30, 201 (1952)",
        "J. Gen. Physiol., 36, 201 (1952)",
        "printed volume is 36",
    ),
    (
        738,
        "Symp. Soc. Exp. Biol. 1, Nucleic Acid",
        "Symp. Soc. Exp. Biol., 1, Nucleic Acid",
        "printed comma follows the abbreviated journal title",
    ),
]


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    for page, before, after, reason in REPAIRS:
        count = text.count(before)
        assert count == 1, (
            f"page {page}: expected one exact anchor, found {count}: {before!r}"
        )
        text = text.replace(before, after, 1)
        print(f"p. {page}: {before!r} -> {after!r} ({reason})")
    PATH.write_text(text, encoding="utf-8")
    print(f"applied {len(REPAIRS)} scan-verified repairs to {PATH.name}")


if __name__ == "__main__":
    main()
