#!/usr/bin/env python3
"""
One-time migration: backfill ocr_status (texts) and content_status (supplements,
module chapters/resources) from the hardcoded maps in site/src/lib/content-status.js.

Texts: only writes ocr_status for entries that appear in the TEXT_STATUS map
(scoped to Ancient Greece for v0.3). All other texts are left untouched —
hand-set 'not-applicable' on digital-native PDFs (modern papers) and 'pending'
on remaining scans as later eras come into scope.

Supplements: writes content_status for every supplement in the SUPPLEMENT_STATUS
map. Other supplements left untouched.

Modules: writes content_status on chapters and resources for every entry in the
MODULE_CHAPTER_STATUS map.

Idempotent: re-running overwrites status fields with the mapped value.
"""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
TEXTS_DIR = ROOT / "texts"
SUPPLEMENTS_DIR = ROOT / "supplements"
MODULES_DIR = SUPPLEMENTS_DIR / "modules"

TEXT_STATUS = {
    "homer-iliad": "complete",
    "homer-odyssey": "complete",
    "aeschylus-oresteia": "complete",
    "sophocles-oedipus-trilogy": "complete",
    "euripedes-bacchae": "complete",
    "aristophanes-clouds": "complete",
    "hippocrates-genuine-works": "complete",
    "plato-meno": "complete",
    "plato-symposium": "complete",
    "plato-phaedrus": "complete",
    "plato-theaetetus": "complete",
    "plato-timaeus": "pending",
    "aristotle-categories": "complete",
    "aristotle-nicomachean-ethics": "complete",
    "aristotle-politics": "complete",
    "aristotle-physics": "complete",
    "aristotle-metaphysics": "complete",
    "aristotle-de-anima": "needs-cleanup",
    "aristotle-parts-of-animals": "complete",
    "euclid-elements": "complete",
    "archimedes-equilibrium-of-planes": "complete",
    "archimedes-floating-bodies": "complete",
    "archimedes-heath-works": "complete",
    "archimedes-geometrical-solutions": "complete",
    "apollonius-conic-sections": "needs-cleanup",
    "ptolemy-almagest": "needs-cleanup",
    "dionysus-thrax-art-of-grammar": "complete",
    # Prometheus Bound was added after the hardcoded map was written
    "aeschylus-prometheus-bound": "complete",
}

SUPPLEMENT_STATUS = {
    "greek-math-companion": "complete",
    "archimedes-buoyancy-lab": "complete",
    "archimedes-levers-lab": "complete",
    "archimedes-quadrature-exercises": "complete",
    "archimedes-method-of-exhaustion-guide": "complete",
    "eratosthenes-measurement-lab": "complete",
    "parallax-lab": "stub",
    "ptolemy-observation-lab": "stub",
    "sun-observation-lab": "stub",
}

# Module chapter keys are "<module-dir>/<filename-stem>" → content_status
MODULE_CHAPTER_STATUS = {
    "1-ancient-greek/00-introduction": "complete",
    "1-ancient-greek/01-alphabet-and-reading-aloud": "complete",
    "1-ancient-greek/02-orienting-to-the-tools": "complete",
    "1-ancient-greek/03-the-case-system-and-the-article": "complete",
    "1-ancient-greek/04-noun-declensions-in-practice": "complete",
    "1-ancient-greek/05-verbs-tense-mood-and-the-participle": "complete",
    "1-ancient-greek/06-reading-attic-prose-and-verse": "complete",
    "1-ancient-greek/07-koine-transition": "complete",
}


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def backfill_texts():
    mapped = 0
    defaulted = 0
    repointed = 0
    for era_dir in sorted(TEXTS_DIR.iterdir()):
        if not era_dir.is_dir() or not era_dir.name[0].isdigit():
            continue
        for text_dir in sorted(era_dir.iterdir()):
            if not text_dir.is_dir():
                continue
            meta_path = text_dir / "metadata.json"
            if not meta_path.exists():
                continue
            text_id = text_dir.name
            meta = load_json(meta_path)
            if text_id in TEXT_STATUS:
                status = TEXT_STATUS[text_id]
                mapped += 1
            else:
                status = "pending"
                defaulted += 1
            meta["ocr_status"] = status

            # If the status indicates a markdown exists, point format/filename at it.
            if status in ("complete", "needs-cleanup"):
                md_files = sorted(text_dir.glob("*.md"))
                if md_files:
                    md_name = md_files[0].name
                    if meta.get("filename") != md_name or meta.get("format") != "markdown":
                        meta["filename"] = md_name
                        meta["format"] = "markdown"
                        repointed += 1

            write_json(meta_path, meta)
    print(f"texts: {mapped} from map, {defaulted} defaulted to pending, {repointed} repointed to markdown")


def backfill_supplements():
    mapped = 0
    defaulted = 0
    for era_dir in sorted(SUPPLEMENTS_DIR.iterdir()):
        if not era_dir.is_dir():
            continue
        if era_dir.name in {"modules", "references"}:
            continue
        for sup_dir in sorted(era_dir.iterdir()):
            if not sup_dir.is_dir():
                continue
            meta_path = sup_dir / "metadata.json"
            if not meta_path.exists():
                continue
            sup_id = sup_dir.name
            meta = load_json(meta_path)
            if sup_id in SUPPLEMENT_STATUS:
                meta["content_status"] = SUPPLEMENT_STATUS[sup_id]
                mapped += 1
            else:
                meta["content_status"] = "stub"
                defaulted += 1
            write_json(meta_path, meta)
    print(f"supplements: {mapped} from map, {defaulted} defaulted to stub")


def backfill_modules():
    updated = 0
    chapters_mapped = 0
    chapters_defaulted = 0
    resources_mapped = 0
    resources_defaulted = 0
    for mod_dir in sorted(MODULES_DIR.iterdir()):
        if not mod_dir.is_dir() or not mod_dir.name[0].isdigit():
            continue
        meta_path = mod_dir / "metadata.json"
        if not meta_path.exists():
            continue
        meta = load_json(meta_path)
        for ch in meta.get("chapters", []):
            stem = ch["filename"].rsplit(".", 1)[0]
            key = f"{mod_dir.name}/{stem}"
            if key in MODULE_CHAPTER_STATUS:
                ch["content_status"] = MODULE_CHAPTER_STATUS[key]
                chapters_mapped += 1
            else:
                ch["content_status"] = "stub"
                chapters_defaulted += 1
        for res in meta.get("resources", []):
            stem = res["filename"].rsplit(".", 1)[0]
            key = f"{mod_dir.name}/{stem}"
            if key in MODULE_CHAPTER_STATUS:
                res["content_status"] = MODULE_CHAPTER_STATUS[key]
                resources_mapped += 1
            else:
                res["content_status"] = "stub"
                resources_defaulted += 1
        write_json(meta_path, meta)
        updated += 1
    print(f"modules: {updated} module files updated")
    print(f"  chapters: {chapters_mapped} from map, {chapters_defaulted} defaulted to stub")
    print(f"  resources: {resources_mapped} from map, {resources_defaulted} defaulted to stub")


if __name__ == "__main__":
    backfill_texts()
    backfill_supplements()
    backfill_modules()
