#!/usr/bin/env python3
"""Remove Sachau's contents pages and printed marginal synopses.

Volume II established the editorial decision: the translator's navigational
synopses are apparatus and come out. Volume I's Mistral output usually places
them at page end, but sometimes puts them first or between body paragraphs.
Accordingly this script does not infer from position or numbering. Candidates
are matched page-locally to independent Tesseract OCR of the physical outer
margin, then frozen by exact candidate count and SHA-256 digest.

The explicit rejection set is equally important: these are short body passages
whose words bled into the narrow margin OCR. Each was reviewed in page context.
Any changed candidate inventory aborts before editing.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path


RAW = Path("source/source.md")
PATH = Path("source/al-biruni-india-i.md")
CANDIDATES = Path("tmp/margin-candidates.tsv")
FIRST_LEAF = 57
EXPECTED_ALL = 413
EXPECTED_STRUCTURAL = 18
EXPECTED_SELECTED = 344
SELECTED_SHA256 = "7f362238fe51991d557892b656946a7a2847bf2b5cdf738437ac42c67d256e6f"

# Exact page-local body anchors which share vocabulary with a printed synopsis
# or intrude into the narrow OCR strip. They are evidence against deletion.
REJECTED_BODY: set[tuple[int, str]] = {
    (59, "IN THE NAME OF GOD, THE COMPASSIONATE, THE MERCIFUL."),
    (100, "The whole of these elements are twenty-five, viz. :—"),
    (102, "On the other hand, the lowest cause, as proceeding"),
    (103, "Further, the Hindus speak in different ways of the agent, as we have already mentioned. So the Vishnu Purāṇa says: \"Matter is the origin of the world. Its action in the world rises from an innate disposition, as a tree sows its own seed by an innate disposition, not"),
    (117, "\"The hunter, and the maker of snares and traps, come to Vahnijñāla."),
    (127, "Now we return and continue our quotation from the book Gîtâ."),
    (136, "It is evident from this that the first part of the path of liberation is instrumental to the second one."),
    (136, "The author of the book *Gītā* distributes the duties of worship among the *body*, the *voice*, and the *heart*."),
    (156, "The first class were the knights and princes."),
    (156, "The second class the monks, the fire-priests, and the lawyers."),
    (156, "The fourth class the husbandmen and artisans."),
    (158, "Such is the condition of the four castes. Arjuna"),
    (161, "In the first chapter of the Book of Laws of Plato, the Athenian stranger says: \"Who do you think was the"),
    (196, "The feet arising out of combinations of laghu and guru are the following:—"),
    (210, "Contents of the twenty-four chapters of the Brahma-siddhānta—"),
    (220, "The balances with which the Hindus weigh things are χαριστίωνες, of which the weights are immovable, whilst the scales move on certain marks and lines."),
    (223, "The elements of the calculations of the Hindus on the circumference of the circle rest on the assumption"),
    (223, "The distance between the ends of the index-finger and of the thumb is called *karabha*, and is reckoned as equal to two-thirds of a span."),
    (231, "The following are the names of the eighteen orders of numbers :—"),
    (239, "| Tower (rukh). | Horse. | Elephant. | King. | | | Pawn. | Tower. | | --- | --- | --- | --- | --- | --- | --- | --- | | Pawn. | Pawn. | Pawn. | Pawn. | | | Pawn. | Horse. | | | | | | | | Pawn. | Elephant. | | | | | | | | Pawn. | King. | | King. | Pawn. | | | | | | | | Elephant. | Pawn. | | | | | | | | Horse. | Pawn. | | | Pawn. | Pawn. | Pawn. | Pawn. | | Tower. | Pawn. | | | King. | Elephant. | Horse. | Tower. |"),
    (264, "This is the frontier of India from the north."),
    (264, "In the western frontier mountains of India there live various tribes of the Afghans, and extend up to the neighbourhood of the Sindh Valley."),
    (269, "The names of the week-days are the best known names of the planets connected with the word bāra, which follows after the planet's name, as in Persian the word shambih follows after the number of the week-day (dāshambih, sihshambih, &c.). So they say—"),
    (269, "Muslim astronomers call the planets the lords of the days, and, in counting the hours of the day, they begin with the dominus of the day, and then count the planets in the order from above to below. For instance, the sun is the dominus of the first day, and at the same time the"),
    (271, "The following table exhibits the commonest names of the seven planets :—"),
    (274, "The names of the months are related to those of the lunar stations. As two or three stations belong to each month, the name of the month is derived from one of them. We have in the following table written these particular stations with red ink (in this translation with an asterisk), in order to point out their relationship with the names of the months."),
    (275, "The image of the seventh sign he declares to be fire. It is called Tulā = balance."),
    (287, "The king Bali; and of the Daitya Mucukunda. In this world there are many houses for the Rākshasa, and Vishṇu resides there, and Śesha, the master of the serpents."),
    (287, "Plato says: “God spoke to the seven planets: You are the gods of the gods, and I am the father of the actions; I am he who made you so that no dissolution"),
    (292, "The commentator of the book of Patañjali, wishing to determine the dimension of the world, begins from below and says: \"The dimension of the darkness is one koṭi and 85 laksha yojana, i.e. 18,000,000 yojana."),
    (300, "On the words of Āryabhaṭa as quoted by Balabhadra we make the following remarks."),
    (314, "We exhibit the names of the rivers in the following table:—"),
    (316, "The river Irâva is joined by the river Kaj, which rises in Nagarkot in the mountains of Bhâtul. Thereupon follows as the fifth the river Shatladar (Satlej)."),
    (330, "followed in the calculation of the mountain Meru (in chap. xxiii.), we divide the square of T A, i.e. 50,625, by"),
    (330, "the earth. B is the standing-point of the observer; his stature is B C. Further, we draw the line C A, so that it touches the earth."),
    (332, "calculation, but it is never and nowhere true for the degrees of the earth."),
    (354, "To the 1st or central varga, the region Pāñcāla."),
    (363, "The following is the plan of the labyrinthine fortress:—"),
    (368, "The number which they use as divisor (4800) is the number of the yojanas of the circumference of the earth, for the difference between the spheres of the meridians of the two places stands in the same relation to the whole circumference of the earth as the mean motion of the planet (sun) from one place to the other to its whole daily rotation round the earth."),
    (371, "This method of calculation is found in the astronomical handbooks of the Hindus in conformity with the account of Alfazārī, save in one particular. The here-mentioned portio is the root of the difference between the squares of the sines of the two latitudes, not the sum of the squares of the sines of the two latitudes."),
    (376, "notion of time, which is a necessary postulate of the existing world."),
    (383, "The beginning of the day is the sun's rising above the horizon, the beginning of the night his disappearing below it. The Hindus consider the day as the first, the"),
    (409, "Saura-māna, i.e. the solar measure."),
    (409, "Sāvana-māna, i.e. the measure depending upon the rising (civil measure)."),
    (409, "Candra-māna, i.e. the lunar measure."),
    (409, "Nakshatra-māna, i.e. the lunar-station measure (sidereal measure)."),
    (409, "The civil day, based on the sāvana-māna, is here used as the unit of a day, for the purpose of measuring thereby the other kinds of days."),
    (410, "The saura-māna is used in the computation of the years which compose the kalpa and the four yugas in the caturyugas, of the years of the nativities, of the equinoxes and solstices, of the sixth parts of the year or the seasons, and of the difference between day and night in the nychthemeron. All these things are computed in solar years, months, and days."),
    (426, "According to Aryabhaṭa and Pulisa, the kalpa and caturyuga begin with midnight which follows after the day the beginning of which is the beginning of the kalpa, according to Brahmagupta."),
    (429, "\"The sum of the kṛita and tretā is 3,024,000 years, and the sum of the kṛita, tretā, and dvāpara is 3,888,000 years.\""),
    (441, "The following occurs in the third book of the Laws of Plato:—"),
    (448, "The author of the canon Karāṇasāra gives the following rule for the computation of the motion of the Great Bear, and of the place which, at any given time, it occupies:—"),
    (458, "The following table contains the names of Vāsudeva in the months:—"),
}


def is_structural(paragraph: str) -> bool:
    return paragraph.startswith(("#", "|")) or (
        any(char.isalpha() for char in paragraph)
        and paragraph.upper() == paragraph
    )


def ensure_candidates() -> None:
    if not Path("tmp/margin-census.tsv").exists():
        subprocess.run([sys.executable, "census_margins.py"], check=True)
    subprocess.run([sys.executable, "identify_margin_synopses.py"], check=True)


def candidate_inventory() -> list[tuple[int, str]]:
    ensure_candidates()
    all_candidates: list[tuple[int, str]] = []
    for line in CANDIDATES.read_text(encoding="utf-8").splitlines()[1:]:
        fields = line.split("\t", 4)
        if len(fields) != 5:
            raise AssertionError(f"malformed candidate row: {line!r}")
        all_candidates.append((int(fields[0]), fields[4]))
    if len(all_candidates) != EXPECTED_ALL:
        raise AssertionError(f"expected {EXPECTED_ALL} candidates, found {len(all_candidates)}")
    missing_rejects = REJECTED_BODY - set(all_candidates)
    if missing_rejects:
        raise AssertionError(f"rejected body anchors missing: {sorted(missing_rejects)!r}")
    structural = [pair for pair in all_candidates if is_structural(pair[1])]
    if len(structural) != EXPECTED_STRUCTURAL:
        raise AssertionError(
            f"expected {EXPECTED_STRUCTURAL} structural candidates, found {len(structural)}"
        )
    selected = [
        pair for pair in all_candidates
        if pair not in REJECTED_BODY and not is_structural(pair[1])
    ]
    if len(selected) != EXPECTED_SELECTED:
        raise AssertionError(f"expected {EXPECTED_SELECTED} synopses, found {len(selected)}")
    blob = "\n".join(f"{leaf}\t{text}" for leaf, text in selected).encode()
    digest = hashlib.sha256(blob).hexdigest()
    if digest != SELECTED_SHA256:
        raise AssertionError(f"synopsis inventory digest changed: {digest}")
    return selected


def flat(paragraph: str) -> str:
    return re.sub(r"\s+", " ", paragraph).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    selected = candidate_inventory()
    pages = PATH.read_text(encoding="utf-8").split("\n\n---\n\n")
    if len(pages) != 408:
        raise AssertionError(f"expected 408 OCR pages, found {len(pages)}")

    by_leaf: dict[int, set[str]] = {}
    for leaf, paragraph in selected:
        by_leaf.setdefault(leaf, set()).add(paragraph)

    removed = 0
    for page_index, page in enumerate(pages):
        leaf = FIRST_LEAF + page_index
        targets = by_leaf.get(leaf, set())
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", page) if p.strip()]
        normalized = [flat(p) for p in paragraphs]
        for target in targets:
            count = normalized.count(target)
            if count != 1:
                raise AssertionError(
                    f"leaf {leaf}: expected one exact synopsis, found {count}: {target!r}"
                )
        pages[page_index] = "\n\n".join(
            p for p, normalized_p in zip(paragraphs, normalized)
            if normalized_p not in targets
        )
        removed += len(targets)
    if removed != EXPECTED_SELECTED:
        raise AssertionError(f"expected to remove {EXPECTED_SELECTED}, removed {removed}")

    # Original PDF leaves 65--72 are Sachau's compiled contents pages. The
    # authorial preface ends on 64 and Chapter I begins on printed p.17 at 73.
    if "# TABLE OF CONTENTS." not in pages[8]:
        raise AssertionError("expected TABLE OF CONTENTS on original leaf 65")
    if not pages[16].startswith("# CHAPTER I."):
        raise AssertionError("expected Chapter I on original leaf 73")
    del pages[8:16]

    output = "\n\n---\n\n".join(pages).strip() + "\n"
    print(f"removed marginal synopses: {removed}")
    print("removed Sachau contents pages: 8 (original PDF leaves 65--72)")
    print(f"bytes: {PATH.stat().st_size} -> {len(output.encode())}")
    if args.apply:
        PATH.write_text(output, encoding="utf-8")
        print(f"wrote {PATH}")
    else:
        print("dry run; pass --apply to write")


if __name__ == "__main__":
    main()
