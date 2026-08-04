#!/usr/bin/env python3
"""Remove Volume I marginal synopses missed by the first OCR census.

The broad census deliberately required at least two lexical matches against a
separate Tesseract pass.  That conservative threshold missed short labels and
labels whose six-point type OCRed poorly.  Every entry below was subsequently
checked in the photographed outer margin of the named original PDF leaf.  The
page key matters: several words also occur legitimately in the body.

Run after ``remove_editorial_apparatus.py`` and before page separators are
discarded.  No document-wide substitution is performed.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


PATH = Path("source/al-biruni-india-i.md")

# (original PDF leaf, exact OCR paragraph with whitespace flattened)
SYNOPSES = [
    (83, "Quotation from Patañjali."),
    (90, "Galenus."),
    (92, "Galenus."),
    (96, "Purusha."),
    (96, "Avyakta."),
    (97, "Ahaṅkāra."),
    (97, "Mahābhūta"),
    (97, "Annotation from Vāyu Purāṇa."),
    # Mistral joined the adjacent printed page-reference label to this synopsis.
    (98, "Pañca mátáras. Page 21."),
    (100, "Karmendri-yāṇi."),
    (111, "Patañjali."),
    (113, "Sûfî doctrine."),
    (115, "The three lokas."),
    (118, "Ṣūfī parallel."),
    (125, "Sūfī parallel."),
    (137, "From Sāṃkhya."),
    (138, "From Patañjali."),
    (139, "Ṣūfī parallels."),
    (143, "Sūfī parallels."),
    (151, "Greek parallels. Stories about Zeus."),
    (163, "Different matrimonial systems."),
    (164, "Birth of Vyāsa."),
    (167, "Origin of idol-worship in the nature of man."),
    (184, "On the Rig- veda."),
    (188, "Mahā- bhārata."),
    (195, "Definition of mātrā."),
    (198, "On the pēdas."),
    (199, "On the metre Aryá."),
    (200, "Metrum Khafif."),
    (208, "On the Siddhāntas."),
    (215, "On Pañca-tantra."),
    (245, "Nāgārjuna, the author of a book on Rasāyana."),
    (247, "Story about the piece of silver in the door of the Government-house in Dhâra."),
    (251, "Hunting practices."),
    (258, "From Māhūra to Dhār."),
    (259, "From Dhâr to Tâna."),
    (267, "On the rainfall in India."),
    (270, "On ὄραι καίρικαί and ὄραι- ἰσημεριναί."),
    (305, "Buddhistic views."),
    (307, "1. Jambū-Dvīpa."),
    (308, "2. Śāka-Dvīpa."),
    (310, "3. Kuśa-Dvīpa."),
    (310, "4. Krauñca-Dvīpa."),
    (310, "5. Śālmala-Dvīpa."),
    (311, "6. Gomeda-Dvīpa."),
    (311, "7. Pushkara-Dvīpa."),
    (318, "Vishnu-Purāṇa."),
    (323, "Quotation from the Brahmasiddhānta of Brahmagupta."),
    (351, "Quotation from Vāyu-Purāṇa."),
    (369, "The equation vyastatrairdśika."),
    (379, "Brahman's waking and sleeping."),
    (381, "Abū-Ma'shar uses Indian theories."),
    (383, "Definition of day and night."),
    (383, "Manushyâ- horâtra."),
    (387, "Day of Brahman."),
    (389, "Parārdhakalpa."),
    (390, "Ghaṭī."),
    (390, "Cashaka."),
    (390, "Prāṇa."),
    (392, "Kāshṭhā, kalā."),
    (394, "Muhūrta."),
    (396, "Story of Śiśupāla."),
    (398, "Dominants of the muhūrtas."),
    (405, "Various kinds of months."),
    (435, "Pedigree of Hippocrates."),
    (437, "Saying of Mānī."),
    (439, "Quotation from Aratus."),
    (453, "Quotation from Vishṇu-Purāṇa."),
]


def flat(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def leaf_for_page(index: int) -> int:
    # Sachau's eight contents leaves 65--72 have already been removed.
    return 57 + index if index < 8 else 65 + index


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    pages = PATH.read_text(encoding="utf-8").split("\n\n---\n\n")
    if len(pages) != 400:
        raise AssertionError(f"expected 400 retained scan pages, found {len(pages)}")
    by_leaf: dict[int, set[str]] = {}
    for leaf, paragraph in SYNOPSES:
        by_leaf.setdefault(leaf, set()).add(paragraph)

    removed = 0
    for index, page in enumerate(pages):
        leaf = leaf_for_page(index)
        targets = by_leaf.get(leaf, set())
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", page) if p.strip()]
        normalized = [flat(p) for p in paragraphs]
        for target in targets:
            count = normalized.count(target)
            if count != 1:
                raise AssertionError(
                    f"leaf {leaf}: expected one synopsis, found {count}: {target!r}"
                )
        pages[index] = "\n\n".join(
            paragraph
            for paragraph, normalized_paragraph in zip(paragraphs, normalized)
            if normalized_paragraph not in targets
        )
        removed += len(targets)

    # On leaf 99 Mistral appended the one-word margin label to the body line.
    leaf99 = 99 - 65
    old = "XX. Next follows the will, which directs the senses Mansa."
    # The scan continues the same sentence on the next leaf: "senses in the
    # exercise ...".  The full stop belonged to the removed label, not body.
    new = "XX. Next follows the will, which directs the senses"
    if pages[leaf99].count(old) != 1:
        raise AssertionError("leaf 99: expected one embedded Mansa synopsis")
    pages[leaf99] = pages[leaf99].replace(old, new, 1)

    # Leaf 315 prints the synopsis "Sindh river." in the outer margin between
    # the typesetter-wrapped halves of Kāyabish. Mistral put all three pieces
    # on one line, so repair the full witnessed anchor rather than the phrase.
    leaf315 = 315 - 65
    old = "In the mountains bordering on the kingdom of Kāya- Sindh river.\nbish, i.e. Kābul"
    new = "In the mountains bordering on the kingdom of Kāyabish, i.e. Kābul"
    if pages[leaf315].count(old) != 1:
        raise AssertionError("leaf 315: expected one embedded Sindh river synopsis")
    pages[leaf315] = pages[leaf315].replace(old, new, 1)

    if removed != len(SYNOPSES):
        raise AssertionError(f"expected {len(SYNOPSES)} removals, made {removed}")
    output = "\n\n---\n\n".join(pages).strip() + "\n"
    print(f"page-local residual synopses removed: {removed}")
    print("embedded synopses repaired: 2 (original PDF leaves 99 and 315)")
    if args.apply:
        PATH.write_text(output, encoding="utf-8")
        print(f"wrote {PATH}")
    else:
        print("dry run; pass --apply to write")


if __name__ == "__main__":
    main()
