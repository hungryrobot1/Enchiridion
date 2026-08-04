#!/usr/bin/env python3
"""Replace the missed p. 15 table approximation and renumber diagram refs.

This is a narrowly asserted follow-up to ``repair_al_khwarizmi.py``.  The main
repair script now performs the same transformation when run from the supplied
raw markdown; this file records the one-time change made to the already-repaired
workspace copy after visual figure QA found the omission.
"""
from pathlib import Path
import re


TEXT = Path(__file__).resolve().parent / "source/al-khwarizmi-algebra.md"
TABLE = "| D | G |\n| --- | --- |\n| C | A |\n| B | K |\n| T | H |"


def main() -> int:
    raw = TEXT.read_text()
    if raw.count(TABLE) != 1:
        raise SystemExit(f"REFUSED: expected one p. 15 table, found {raw.count(TABLE)}")
    refs = re.findall(r"images/img-(\d+)\.png", raw)
    if refs != [str(i) for i in range(17)]:
        raise SystemExit(f"REFUSED: expected ordered refs 0..16, found {refs}")

    def shift(match: re.Match[str]) -> str:
        return f"images/img-{int(match.group(1)) + 1}.png"

    repaired = re.sub(r"images/img-(\d+)\.png", shift, raw)
    repaired = repaired.replace(
        TABLE, "![Figure on printed page 15](images/img-0.png)"
    )
    if len(re.findall(r"images/img-\d+\.png", repaired)) != 18:
        raise SystemExit("REFUSED: expected 18 final image references")
    TEXT.write_text(repaired)
    print(f"written: {TEXT} (18 figure references)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
