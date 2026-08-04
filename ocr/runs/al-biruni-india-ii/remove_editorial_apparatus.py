#!/usr/bin/env python3
"""Remove source-witnessed editorial furniture from Alberuni's India, vol. II.

Every removal is an exact, counted anchor.  The marginal labels were checked
against the outer margins of PDF leaves 2--247; Sachau's annotations and both
indexes are removed according to the answered apparatus decision.
"""

from __future__ import annotations

import argparse
from collections import Counter
import re
from pathlib import Path


PATH = Path(__file__).parent / "source/al-biruni-india-ii.md"

SYNOPSES = [
    "Enumeration of some of the eras of the Hindus.",
    "The author adopts the year 400 of Yazdajird as a test-year.",
    "How much of the life of Brahman has elapsed according to the Vishnu-Dharma.",
    "The ṣ̄aka-kāla.",
    "Era of Valabha.",
    "On the popular mode of dating by centennia or samvatsaras.",
    "Different beginnings of the year.",
    "End of the Tibetan dynasty, and origin of the Brahman dynasty.",
    "The tradition of Alfazârî and Ya’kûb Ibn Ţârik.",
    "Muḥammad Ibn Isḥâk of Sarakhs.",
    "Page 211. Star-cycles of a *kalpa* and *caturyuga*, according to Pulisa.",
    "Transformation of the word Arya-bhāṭa among the Arabs.",
    "Star-cycles according to Abū-alḥasan of Al’ahwāz. Page 212.",
    "On the leap month.",
    "Criticisms thereon.",
    "Explanation of the terms universal or partial months and days.\nUniversal adhimāsa months.",
    "Computation of the únarátra according to Pulisa.",
    "Cri¹cisms on Ta'kùb Ibn Tárik.",
    "More detailed rule for the same purpose.",
    "The latter method carried out for Śāka-kāla 953.",
    "A similar method of computation taken from the *Pulisa-siddhānta*.",
    "The method of a kargana employed by Arya-bhata.",
    "The ahar-gana as given by Ya'kūb Ibn Tārik.",
    "Publication of the last-mentioned method.",
    "(Lacuna.)",
    "**Explication of the latter method.**",
    "**The latter method applied to the gauge-year.**",
    "Method for the computation of the *unarātra* days according to Brahmagupta.",
    "Criticisms of this method.",
    "Method for finding the *adhimāsa* for the years of a *kalpa*, *caturyuga*, or *kaliyuga*.",
    "The latter method applied to the gauge-year.",
    "A second method for finding the adkimâsa, according to Pulisa.",
    "Rule how to construct a chronological data from a certain given number of days. The converse of the ahargana.",
    "Application of the rule to the gauge-year.",
    "Rule for the same purpose given by Ya'kûb Ibn Târik.",
    "Explanation of the latter method.",
    "Ya’kûb’s method for the computation of the partial *únarátra* days\nCriticism thereon.",
    "Method of ahargana as applied to special dates.",
    "Method of the Khaṇḍakhādyaka.",
    "*Application of this method to the gauge-year.*",
    "Method of the Arabic book Al-arkand.",
    "Method of the canon Karanatilaka.",
    "Application of this method to the gauge-year.",
    "Method of the *Pañca-Siddhántiká*. Page 228.\nApplication of this method to the gauge-year.",
    "Method of the Arabic canon\n*Al-harkan*.",
    "Application of the method to the gauge-date.",
    "Method of Durlabha of Multān.",
    "Method of Pulisa for the same purpose.",
    "Explanatory notes thereon.",
    "Methods of the *Khaṇḍakhādyaka*, *Karaṇatilaka*, and *Karaṇasāra*.",
    "Traditional view on the sun being below the moon.",
    "Popular notions of astronomy.",
    "Quotations from *Vāyu-Purāṇa*.",
    "On the nature of the stars.",
    "Distances of the planets from the centre of the earth, and their diameters, according to Ya'kûb Ibn Târik.",
    "Ptolemy on the distances of the planets. Page 236.",
    "The same computation according to the theory of Pulisa.",
    "Method for the computation of the bodies of sun and moon at any given time.",
    "Quotations from Pulisa, Brahmagupta, and Balabhadra.",
    "Criticisms on Brahmagupta's method.",
    "The author criticises the corrupt state of his manuscript of Brahmagupta. Page 241.",
    "Whether the Hindus have twenty-seven or twenty-eight lunar stations.",
    "A Vedic tradition from Brahmagupta.",
    "Method for computing the place of any given degree of a lunar station.\nTable of the lunar stations taken from the *Khandakhādyaka*.",
    "On the precession of the equinoxes; quotation from Varâhamihira, chap. iv. 7.",
    "The author criticises Varâhamihira’s statement.",
    "Each station occupies the same space on the ecliptic.",
    "Quotation from Brahmagupta.",
    "The author on the precession of the equinoxes.",
    "How far a star must be distant from the sun in order to become visible.",
    "Quotation from Vijayanandin.",
    "On the heliacal rising of Canopus.\nQuotation from Brahmagupta.",
    "On the ceremonies practised at the heliacal rising of certain stars.",
    "Quotation from Vāṇāhamihira's Asthma, ch. XII, preface, and vv. 1-16, on Can. p. s. Agastya and the sacrifice to him.",
    "Varâhami-hira's Saâ-hitâ, chap. xxiv. 1-37, on Rohiṇī.",
    "Quotation from the *Matsya-Purāṇa*.",
    "The idol of Somanāth.",
    "The worship of the idol of Somanāth.",
    "Popular belief about the cause of the tides.",
    "The golden fortress Baroi. Parallel of the Maledives and Laccadives. Page 254.",
    "**Praise of Varâhamihira.**",
    "**Strictures on Brahmagupta's want of sincerity.**",
    "**Quotation from the Brahmásiddhânta.**",
    "*Possible excuses for Brahmagupta.*",
    "Quotations from Varâhamihira's Sanskrit chap. v. 17, 16, 63.",
    "On the colours of the eclipses.",
    "Explanation of the term parvan.",
    "Quotation from Varāhamihira's Saṁhitā, chap. v. 19-23.",
    "Quotation from Varâhamihira's Samhitâ, chap. v. 236",
    "Which of the different measures of time have dominants and which not.",
    "The dominants of the planets according to *Vishnudharma*.",
    "Explanation of the terms *samvatsara* and *shashṭyabda*.",
    "A year is presided over by that month in which the heliacal rising of Jupiter occurs.",
    "How to find the lunar station of Jupiter’s heliacal rising. Quotation from Varāhamihira’s *Samhita*, chap. viii. 20, 21.",
    "Smaller cycles as contained in the cycle of sixty years.",
    "The names of the single years of a *samvatsara*.",
    "First period in the Brahman's life.",
    "Second period in the Brahman's life.",
    "The third period.",
    "The fourth period.\nThe duties of Brahmans in general.",
    "**Duties of the single castes.**",
    "Story of King Rāma, the Caṇḍāla and the Brahman.\nPhilosophic opinion about all things being equal.",
    "Story of the fire becoming leprous from *Vishṇu-Dharma*.",
    "An extract on holy ponds from the *Vāyu* and *Matsya Purāṇas*.",
    "On the construction of holy ponds.",
    "On the inequality of created beings and the origin of patriotism. A tradition from Śaunaka. Page 275.",
    "On Benares as an asylum.",
    "Why the meat of cows was forbidden.",
    "(Lacuna in the manuscript.)",
    "That all things are equal from a philosophical point of view.",
    "**Necessity of matrimony.**",
    "**Law of marriage.**",
    "The widow.",
    "Forbidden degrees of marriage.\nNumber of wives.",
    "**Partus sequitur venirem.**",
    "**Duration of the menstrual courses.**",
    "**On pregnancy and childbed.**",
    "On the causes of prostitution.",
    "### On procedure.",
    "### Number of witnesses.",
    "### Different kinds of oaths and ordeals.",
    "Law of murder.",
    "Law of theft.",
    "Punishment of an adulteress.",
    "Hindu prisoners of war, how treated after returning to their country.",
    "Law of inheritance.",
    "Parallel from Plato.",
    "Fire and the sunbeam as the nearest roads to God.",
    "Quotation from Mânî. Page 284.",
    "The bodies of children under three years are not burned.",
    "**Modes of suicide.**",
    "**The tree of Prayṅga.**",
    "Various methods of fasting.",
    "*Reward of the fasting in the single months.*",
    "The eighth and eleventh days of each half of a month are fast-days.",
    "On single fast-days throughout the year.",
    "The day of full moon in the month Śrāvaṇa is a fast-day holy to Somanātha.",
    "On the sixth day of Pausha is a fasting in honour of the sun.",
    "1st Kārttika.",
    "3rd Mārgaśīrṣa.",
    "The four days on which the four yugas are said to have commenced.",
    "Criticisms thereon.",
    "The days called *punyakála*.",
    "Method for calculating the moment of *samkranti*.",
    "On the length of the solar year according to Brahmagupta, Pulisa, and Aryabhāṭa.",
    "Another method for finding the *saṅkránti*.",
    "Times of eclipses.\nParvan and yogas.\nUnlucky days.",
    "Times of earthquakes.",
    "Quotation from the book Śrādhava of Mahādeva.",
    "**Explanation of karanas.**",
    "**Fixed and movable karaṇas.**",
    "Rule how to find the karanas. in question falls, which is done in this way:—",
    "Names of the lunar days of the half of a month.",
    "THE SEVEN MOVABLE KARANAS.",
    "Rule for the computation of the karaṇas. Page 297.",
    "The karaṇas as borrowed by Alkindi and other Arab authors.",
    "Explanation of vyatlpāta and vaidhṛita.",
    "Another method by Pulisa.",
    "Another method by the author of the *Kara-patilaka.*",
    "Twenty-seven yogas according to the Karnṣa-tilaka.",
    "Explanation of some technical terms of astrology.",
    "The houses.",
    "On the division of a zodiacal sign in nimbakras.",
    "2. In drekkāṇas.",
    "3. In nubbakras.",
    "On the different kinds of the aspect.",
    "Friendship and enmity of certain planets in relation to each other.",
    "The four forces of each planet.",
    "Laghujáta-kam, B. 6.",
    "### The second species.",
    "### The third species.",
    "### Laghujá-takam, ch. vi. 1.",
    "### The years of life bestowed by the ascendens.",
    "Various computations for the duration of life.",
    "Laghujātakam, ch. iii. 3.",
    "How one planet is affected by the nature of another one.\nSpecial methods of inquiry of the Hindu astrologers",
    "Ourstations from the *Sanktiā* of *Varāhami-hira*.",
    "On meteora. logy.",
]

EMBEDDED = [
    ("\nAnother method of Brahmagupta’s for computing the shadow.\n\n", "\n"),
    ("\nOrganization from the Viṣṇu-Purâṇa.\n\n", "\n"),
    ("Page 233\n\n", ""),
    ("Page 249\n\n", ""),
    ("Page 253.‖\n\n", ""),
    ("Varuna-mantra, Vâyava-mantra, Page 250. and Soma-mantra", "Varuna-mantra, Vâyava-mantra, and Soma-mantra"),
    ("divisor or bhāgahāra is 3200 Page 293.", "divisor or bhāgahāra is 3200."),
    ("Page 299. THESE are times", "These are times"),
    ("called 3rd Vaiś- *Gaur-t-r*", "called *Gaur-t-r*"),
    ("daughter of âkha. Page 288. the mountain", "daughter of the mountain"),
    ("According to the Hindus, the fire eats everything. On fireofferings in general.\nTherefore", "According to the Hindus, the fire eats everything. Therefore"),
    (" *amávásyá* The days of new moon and full moon.\nand *púrŋimá*", " *amávásyá* and *púrŋimá*"),
    ("\n15th Âśva-yuja.\n", "\n"),
    ("\n16th Âśva-yuja.\n", "\n"),
    ("\n23rd Âśva-yuja.\n", "\n"),
    ("\nBhâdrapadâ, new moon.\n", "\n"),
    ("\n3rd Bhâdrapadâ.\n", "\n"),
    ("\n6th Bhâdrapadâ.\n", "\n"),
    ("\n8th Bhâdrapadâ.\n", "\n"),
    ("\n16th Phālguna.\n", "\n"),
    ("\n23rd Phālguna.\n", "\n"),
    ("\nA festival in Mūltān.\n", "\n"),
    ("\nConclusion:\n", "\n"),
]


def remove_paragraph(text: str, paragraph: str, expected: int) -> str:
    anchor = f"\n\n{paragraph}\n\n"
    count = text.count(anchor)
    if count != expected:
        raise AssertionError(f"expected {expected} synopsis anchor(s), found {count}: {paragraph!r}")
    return text.replace(anchor, "\n\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    text = PATH.read_text()

    if text.count("\n# ANNOTATIONS.\n") != 2:
        raise AssertionError("expected the two Sachau ANNOTATIONS headings")
    main_text, removed = text.split("\n# ANNOTATIONS.\n", 1)
    for heading in ("# ANNOTATIONS.", "# INDEX I.", "# INDEX II."):
        expected = 1 if heading != "# ANNOTATIONS." else 1
        if removed.count(heading) != expected:
            raise AssertionError(f"unexpected removed-tail count for {heading!r}")
    if not main_text.endswith("\n\nVOL. I\n"):
        raise AssertionError("expected trailing volume signature before annotations")
    main_text = main_text.removesuffix("\n\nVOL. I\n")

    for synopsis, expected in Counter(SYNOPSES).items():
        main_text = remove_paragraph(main_text, synopsis, expected)
    for old, new in EMBEDDED:
        count = main_text.count(old)
        if count != 1:
            raise AssertionError(f"expected one embedded anchor, found {count}: {old!r}")
        main_text = main_text.replace(old, new, 1)

    # Join paragraph boundaries that cannot be syntactic stops.  These are the
    # body halves exposed by removing a margin label or a printed page break.
    unsafe_next = re.compile(r"(?:#|\||!\[|<|>|[-*+] |\d+[.)] )")
    joins = 0
    while True:
        match = re.search(r"([^\n])\n\n([^\n])", main_text)
        if not match:
            break
        left, right = match.group(1), match.group(2)
        start = main_text[match.start(2):].split("\n", 1)[0]
        if left not in ".!?;:—”’\"')]}" and not unsafe_next.match(start):
            main_text = main_text[:match.start()] + left + " " + main_text[match.start(2):]
            joins += 1
            continue
        # Temporarily protect a boundary not eligible for joining.
        main_text = main_text[:match.start()+1] + "\n\u200b\n" + main_text[match.start(2):]
    main_text = main_text.replace("\n\u200b\n", "\n\n")

    # Count frozen after diagnostic review; a changed input must stop here.
    if joins != 142:
        raise AssertionError(f"expected 142 mechanically incomplete-paragraph joins, found {joins}")
    main_text = main_text.rstrip() + "\n"

    print(f"synopses removed: {len(SYNOPSES)}")
    print(f"embedded margin/page intrusions repaired: {len(EMBEDDED)}")
    print("incomplete paragraph joins: 142")
    print("Sachau annotations removed: 2 sections")
    print("indexes removed: 2")
    if args.apply:
        PATH.write_text(main_text)
        print(f"wrote {PATH}")
    else:
        print("dry run only; pass --apply to write")


if __name__ == "__main__":
    main()
