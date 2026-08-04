#!/usr/bin/env python3
"""Set volume/chapter hierarchy for the reader's lazy sectioning contract."""

from pathlib import Path


PATH = Path(__file__).parent / "source/al-biruni-india-ii.md"
MULTILINE_TITLES = [
    "ON THE CALCULATION OF “AHARGAṆA” IN GENERAL,\nTHAT IS, THE RESOLUTION OF YEARS AND MONTHS\nINTO DAYS, AND, VICE VERSÀ, THE COMPOSITION OF\nYEARS AND MONTHS OUT OF DAYS.",
    "ON THE AHARGANA, OR THE RESOLUTION OF YEARS INTO MONTHS, ACCORDING TO SPECIAL RULES WHICH ARE ADOPTED IN THE CALENDARS FOR CERTAIN DATES OR MOMENTS OF TIME.",
    "ON THE HELIACAL RISINGS OF THE STARS, AND ON THE CEREMONIES AND RITES WHICH THE HINDUS PRACTISE AT SUCH A MOMENT.",
    "ON THAT WHICH ESPECIALLY CONCERNS THE BRAHMANS, AND WHAT THEY ARE OBLIGED TO DO DURING THEIR WHOLE LIFE.",
    "ON THE RITES AND CUSTOMS WHICH THE OTHER CASTES, BESIDES THE BRAHMANS, PRACTISE DURING THEIR LIFETIME.",
    "ON DAYS WHICH ARE HELD IN SPECIAL VENERATION,\nON LUCKY AND UNLUCKY TIMES, AND ON SUCH\nTIMES AS ARE PARTICULARLY FAVOURABLE FOR\nACQUIRING IN THEM BLISS IN HEAVEN.",
    "ON THE INTRODUCTORY PRINCIPLES OF HINDU ASTROLOGY, WITH A SHORT DESCRIPTION OF THEIR METHODS OF ASTROLOGICAL CALCULATIONS.",
]


text = PATH.read_text()
if text.count("\n## CHAPTER ") != 32:
    raise AssertionError("expected 32 h2 chapter markers")
if text.count("\n### ") != 26:
    raise AssertionError("expected 26 existing h3 chapter/subsection titles")
text = text.replace("\n## CHAPTER ", "\n# CHAPTER ")
text = text.replace("\n### ", "\n## ")

for title in MULTILINE_TITLES:
    anchor = f"\n\n{title}\n\n"
    if text.count(anchor) != 1:
        raise AssertionError(f"expected one unheaded chapter-title anchor: {title!r}")
    collapsed = " ".join(title.splitlines())
    text = text.replace(anchor, f"\n\n## {collapsed}\n\n", 1)

PATH.write_text(text)
print("promoted 32 chapter markers to h1")
print("promoted 26 existing titles/subtitles to h2")
print("promoted 7 multiline chapter titles to h2")
