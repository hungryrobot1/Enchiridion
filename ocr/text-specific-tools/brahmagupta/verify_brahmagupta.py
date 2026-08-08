#!/usr/bin/env python3
"""Non-editing final acceptance checks for the Brahmagupta proposal."""

from pathlib import Path
import re


TEXT = Path("brahmagupta-brahmasphutasiddhanta.md")


def main() -> int:
    text = TEXT.read_text(encoding="utf-8")
    assert text.startswith("# BRAHME-SPHUTA-SIDD'HÁNTA, CHAPTERS XII AND XVIII\n")
    assert text.rstrip().endswith("FINIS.")
    assert text.count("\n# CHAPTER XII.\n") == 1
    assert text.count("\n# CHAPTER XVIII.\n") == 1
    assert text.count("*Pṛthūdaka commentary:*") == 126
    assert text.count("*Signed note retained for review:*") == 4
    assert "It is not quite clear whether the examples" not in text
    assert "SPHUÚA" not in text
    assert not any(mark in text for mark in "āīōēĀĪŌŪĒ")
    assert text.count("ū") == 126  # only the modern editorial label Pṛthūdaka
    assert "\n\n---\n\n" not in text
    assert "#### " not in text
    assert "```" not in text
    refs = re.findall(r"!\[[^]]*\]\((images/[^)]+)\)", text)
    assert len(refs) == 33
    assert len(set(refs)) == 33
    missing = [ref for ref in refs if not Path(ref).is_file()]
    assert not missing, missing
    assert not Path("toc.json").exists()
    print(
        "final acceptance: 3 h1 title/chapter boundaries; 126 certain commentary and 4 neutral signed-note groups; "
        "33 unique figure references present; no page rules, macrons, h4s, fences, or toc.json"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
