#!/usr/bin/env python3
"""Generate INVENTORY.md — a flat, human- and AI-readable list of every
text, supplement, module, and reference currently in the repo.

Run from anywhere:
    python3 utilities/inventory.py

Output: INVENTORY.md at project root.
"""

from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "INVENTORY.md"

TEXTS_DIR = ROOT / "texts"
SUPPLEMENTS_DIR = ROOT / "supplements"
MODULES_DIR = SUPPLEMENTS_DIR / "modules"
REFERENCES_DIR = SUPPLEMENTS_DIR / "references"

SECTION_TITLES = {
    "1-ancient-greece": "Ancient Greece",
    "2-rome-late-antiquity": "Rome and Late Antiquity",
    "3-islamic-golden-age-medieval-europe": "Islamic Golden Age and Medieval Europe",
    "4-renaissance-scientific-revolution": "Renaissance and Scientific Revolution",
    "5-newtonian-enlightenment": "Newtonian Enlightenment",
    "6-nineteenth-century": "Nineteenth Century",
    "7-modern-era-i": "Modern Era I",
    "8-modern-era-ii": "Modern Era II",
}


def list_subdirs(path):
    if not path.is_dir():
        return []
    return sorted(d.name for d in path.iterdir() if d.is_dir() and not d.name.startswith("."))


def list_chapter_files(module_dir):
    """Module chapters are top-level .md files prefixed with a two-digit number."""
    if not module_dir.is_dir():
        return []
    return sorted(
        f.stem for f in module_dir.iterdir()
        if f.is_file() and f.suffix == ".md" and f.stem[:2].isdigit()
    )


def render_section(title, items):
    if not items:
        return f"### {title}\n\n_(none)_\n"
    lines = [f"### {title}", ""]
    lines.extend(f"- {item}" for item in items)
    lines.append("")
    return "\n".join(lines)


def main():
    out = []
    out.append("# Enchiridion Inventory")
    out.append("")
    out.append(f"_Generated {date.today().isoformat()} by `utilities/inventory.py`. "
               "Each entry is a directory name (which doubles as the item id)._")
    out.append("")

    # Texts
    out.append("## Texts")
    out.append("")
    for section_id in sorted(SECTION_TITLES.keys()):
        section_path = TEXTS_DIR / section_id
        items = list_subdirs(section_path)
        out.append(render_section(SECTION_TITLES[section_id], items))

    # Supplements (era-bound)
    out.append("## Supplements")
    out.append("")
    for section_id in sorted(SECTION_TITLES.keys()):
        section_path = SUPPLEMENTS_DIR / section_id
        items = list_subdirs(section_path)
        out.append(render_section(SECTION_TITLES[section_id], items))

    # Modules
    out.append("## Modules")
    out.append("")
    for module_id in list_subdirs(MODULES_DIR):
        module_path = MODULES_DIR / module_id
        chapters = list_chapter_files(module_path)
        out.append(f"### {module_id}")
        out.append("")
        if chapters:
            out.extend(f"- {ch}" for ch in chapters)
        else:
            out.append("_(no chapters)_")
        out.append("")

    # References
    out.append("## References")
    out.append("")
    for group_id in list_subdirs(REFERENCES_DIR):
        group_path = REFERENCES_DIR / group_id
        items = list_subdirs(group_path)
        out.append(render_section(group_id, items))

    OUTPUT.write_text("\n".join(out).rstrip() + "\n")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
