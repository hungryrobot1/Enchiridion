#!/usr/bin/env python3
"""audit-figures.py — reconcile a text's images against its prose. Report only.

    ocr/.venv/bin/python3 ocr/figures/audit-figures.py TEXT.md [--images DIR]
                                                       [--source FILE] [--all]
    ocr/.venv/bin/python3 ocr/figures/audit-figures.py --self-test

WHY THIS EXISTS. Three runs in one wave, on three different source shapes, each
had to build its own version of this and each said so:

  - Huygens: the brief's "65 PNGs, all illustrations" collapsed one unreferenced
    cover, 53 argument diagrams and 11 typographic assets into a single number.
    Resolving that needed parallel counts from the ZIP, the XHTML, the extractor
    output and the final Markdown, because nothing reconciles them.
  - Lobachevsky: "the shipped diagram audit tools require a scaffold and
    manifest that this ordinary OCR output does not produce." The images were
    all present and the available tool could not consume them.
  - Napier: had to write a table-geometry and figure-coverage verifier, having
    expected a general one analogous to the promoted duplicate-leaf tool.

`audit-diagram-coverage.py` is the existing tool and it is not this one: it
needs a proposition scaffold, a manifest and the PDF, and it reads label-cluster
artifacts specific to Euclid. It answers "which proposition still needs repair".
This answers "do the images and the prose agree with each other", for any text,
from what a run actually produces.

WHAT IT WILL NOT DO IS CLASSIFY. A diagram and a picture of an equation are the
same fact to every tool in this repository, and an ornament and a small figure
differ only by intent. So this prints size, reference count and pairing evidence
and leaves the judgment where it belongs. A tool that guessed here would be
believed, and Huygens is the case that shows what that costs: recon routed it to
OCR precisely because something decided that images without notation must be
mathematics.

Report only. It never moves, renames or deletes a file.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image

# Markdown and inline HTML both appear in adopted texts.
MD_IMG = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")
HTML_IMG = re.compile(r"<img[^>]*?\bsrc\s*=\s*[\"']([^\"']+)", re.I)
# "Fig. 2", "Figure 12", "PLATE IV" — the prose's own claim that a figure exists.
FIG_REF = re.compile(r"\b(?:fig(?:ure)?\.?|plate)\s*([0-9]{1,3}|[IVXLC]{1,6})\b", re.I)

ORNAMENT_PX = 100 * 100      # below this area, almost certainly not an argument
THUMB_RATIO = 0.5            # a thumbnail is at most half its original's width
ASPECT_TOL = 0.06


def image_facts(path: Path) -> dict:
    try:
        with Image.open(path) as im:
            w, h = im.size
    except Exception:
        w = h = 0
    data = path.read_bytes()
    return {"path": path, "w": w, "h": h, "area": w * h,
            "bytes": len(data), "sha": hashlib.sha256(data).hexdigest()}


def _thumbprint(path: Path, size=(32, 32)) -> list[int] | None:
    """A tiny greyscale rendering, for comparing two images by what they SHOW."""
    try:
        with Image.open(path) as im:
            return list(im.convert("L").resize(size, Image.BILINEAR).tobytes())
    except Exception:
        return None


def find_pairs(facts: list[dict], max_diff: int = 12) -> list[tuple[dict, dict]]:
    """Thumbnail/original pairs: one image is a downscale of another.

    Last wave a "52 illustrations" count concealed 26 thumbnail/original pairs,
    which is a doubled figure count and a reader shown the wrong image half the
    time.

    The first version of this used aspect ratio and relative size alone, and on
    Huygens' 62 geometric diagrams it reported 47 pairs -- which is nonsense,
    and the useful kind: in a set of figures drawn to a house style, matching
    proportions are the norm rather than evidence. Shape coincidence cannot
    carry this.

    So aspect and size are only a cheap PREFILTER now, and the decision is made
    on content: downscale both to 32x32 greyscale and compare. Two renderings of
    the same drawing agree closely; two different diagrams of the same
    proportions do not.
    """
    pairs = []
    usable = [f for f in facts if f["w"] and f["h"]]
    prints: dict[Path, list[int] | None] = {}
    for i, a in enumerate(usable):
        for b in usable[i + 1:]:
            ar_a, ar_b = a["w"] / a["h"], b["w"] / b["h"]
            if abs(ar_a - ar_b) / max(ar_a, ar_b) > ASPECT_TOL:
                continue
            small, large = sorted((a, b), key=lambda f: f["area"])
            if small["w"] > large["w"] * THUMB_RATIO or not small["area"]:
                continue
            for f in (small, large):
                if f["path"] not in prints:
                    prints[f["path"]] = _thumbprint(f["path"])
            ps, pl = prints[small["path"]], prints[large["path"]]
            if ps is None or pl is None:
                continue
            diff = sum(abs(x - y) for x, y in zip(ps, pl)) / len(ps)
            if diff <= max_diff:
                pairs.append((small, large))
    return pairs


def audit(md: Path, images: Path | None, source: Path | None) -> dict:
    text = md.read_text(encoding="utf-8", errors="replace")
    refs = [Path(r).name for r in MD_IMG.findall(text) + HTML_IMG.findall(text)]
    ref_counts = Counter(refs)

    images = images or (md.parent / "images")
    on_disk = sorted(p for p in images.iterdir()
                     if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif",
                                             ".svg", ".webp")) if images.is_dir() else []
    facts = [image_facts(p) for p in on_disk if p.suffix.lower() != ".svg"]
    names = {p.name for p in on_disk}

    by_sha = defaultdict(list)
    for f in facts:
        by_sha[f["sha"]].append(f)

    fig_refs = {m.group(1).upper() for m in FIG_REF.finditer(text)}

    in_source = None
    if source and source.suffix.lower() in (".epub", ".zip"):
        with zipfile.ZipFile(source) as z:
            in_source = {Path(n).name for n in z.namelist()
                         if Path(n).suffix.lower() in (".png", ".jpg", ".jpeg", ".gif")}

    return {
        "referenced": ref_counts,
        "on_disk": names,
        "facts": facts,
        "dangling": sorted(set(ref_counts) - names),
        "orphans": sorted(names - set(ref_counts)),
        "duplicates": [v for v in by_sha.values() if len(v) > 1],
        "pairs": find_pairs(facts),
        "fig_refs": fig_refs,
        "in_source": in_source,
    }


def report(a: dict, show_all: bool) -> int:
    print(f"  images on disk        {len(a['on_disk'])}")
    print(f"  referenced in prose   {len(a['referenced'])} distinct, "
          f"{sum(a['referenced'].values())} reference(s)")

    if a["in_source"] is not None:
        lost = sorted(a["in_source"] - a["on_disk"])
        print(f"  present in the source {len(a['in_source'])}"
              + (f"   ⚠ {len(lost)} did not survive extraction" if lost else "  (all extracted)"))
        for n in lost[:8]:
            print(f"      not extracted: {n}")

    tiny = [f for f in a["facts"] if 0 < f["area"] < ORNAMENT_PX]
    big = [f for f in a["facts"] if f["area"] >= ORNAMENT_PX]
    print(f"\n  by size               {len(big)} at or above 100×100, "
          f"{len(tiny)} below")
    print("                        SIZE IS EVIDENCE, NOT A CLASS. Small usually")
    print("                        means rule, ornament or drop-cap; it can also")
    print("                        mean a small diagram. You decide.")

    if a["dangling"]:
        print(f"\n  ⚠ REFERENCED BUT ABSENT   {len(a['dangling'])}")
        for n in a["dangling"][:12]:
            print(f"      {n}")
        print("      The prose points at these and the reader will get a broken")
        print("      image. This is the one finding here that is unambiguous.")

    if a["orphans"]:
        print(f"\n  ⚠ PRESENT BUT UNREFERENCED  {len(a['orphans'])}")
        for n in a["orphans"][:12]:
            print(f"      {n}")
        print("      Usually a cover or an ornament the extractor kept. If any is")
        print("      an argument diagram, the prose lost its figure.")

    if a["duplicates"]:
        print(f"\n  ⚠ BYTE-IDENTICAL GROUPS   {len(a['duplicates'])}")
        for g in a["duplicates"][:6]:
            print(f"      {' = '.join(f['path'].name for f in g)}")

    if a["pairs"]:
        print(f"\n  ⚠ THUMBNAIL/ORIGINAL CANDIDATES  {len(a['pairs'])}")
        for small, large in a["pairs"][:8]:
            print(f"      {small['path'].name} ({small['w']}×{small['h']})"
                  f"  ↔  {large['path'].name} ({large['w']}×{large['h']})")
        print("      Same aspect ratio, one materially smaller. A count that")
        print("      includes both is double what the reader should see.")

    if a["fig_refs"]:
        print(f"\n  figure references in the prose: {len(a['fig_refs'])} distinct "
              f"({', '.join(sorted(a['fig_refs'])[:10])}{'…' if len(a['fig_refs']) > 10 else ''})")
        print(f"  images at or above 100×100:     {len(big)}")
        if len(a["fig_refs"]) != len(big):
            print("      These differ. That is INFORMATION, not a failure — a plate")
            print("      may be unnumbered, one figure may be referenced twice, and")
            print("      an ornament may sit above the size line. Report the pair.")

    if show_all:
        print("\n  every image:")
        for f in sorted(a["facts"], key=lambda f: -f["area"]):
            print(f"      {f['path'].name:<38} {f['w']:>5}×{f['h']:<5} "
                  f"{f['bytes']//1024:>5} KB  ×{a['referenced'].get(f['path'].name, 0)}")

    problems = len(a["dangling"]) + len(a["duplicates"]) + len(a["pairs"])
    print()
    if problems:
        print(f"  RESULT: {problems} finding(s) that need a person. Nothing here has")
        print("  been changed; this tool only reports.")
        return 1
    print("  RESULT: no unambiguous defect. Note what that does NOT mean: it")
    print("  cannot tell a diagram from an ornament, or a correct figure from a")
    print("  wrong one placed where a correct one belongs — and any count")
    print("  difference printed above is still yours to explain.")
    return 0


# Synthetic and permanent. A control that depends on a text staying broken
# expires the moment the text is fixed -- check-source-identity.py's live
# control broke exactly that way, twice.
def self_test(tmp: Path) -> int:
    tmp.mkdir(parents=True, exist_ok=True)
    imgs = tmp / "images"
    imgs.mkdir(exist_ok=True)

    def png(name, w, h, colour):
        Image.new("RGB", (w, h), colour).save(imgs / name)

    png("fig1.png", 400, 300, (10, 10, 10))
    png("fig1-thumb.png", 100, 75, (10, 10, 10))   # same aspect, quarter width
    png("fig2.png", 400, 300, (200, 30, 30))        # same aspect as fig1, same size
    png("copy-a.png", 220, 140, (7, 9, 11))
    png("copy-b.png", 220, 140, (7, 9, 11))         # byte-identical to copy-a
    png("ornament.png", 40, 12, (99, 99, 99))
    png("orphan.png", 300, 300, (1, 2, 3))
    # The case that made the first version useless: a SMALL image of the same
    # proportions as a large one, showing something else. On Huygens' 62
    # diagrams, shape coincidence alone produced 47 phantom pairs.
    png("small-but-different.png", 100, 75, (250, 250, 250))

    md = tmp / "t.md"
    md.write_text(
        "See ![](images/fig1.png) and Fig. 2 at ![](images/fig2.png).\n\n"
        "![](images/copy-a.png) ![](images/copy-b.png) ![](images/ornament.png)\n\n"
        "![](images/fig1-thumb.png) ![](images/small-but-different.png)\n\n"
        "And ![](images/gone.png) which was never extracted.\n")

    a = audit(md, imgs, None)
    checks = [
        ("a referenced-but-absent image is found",
         a["dangling"] == ["gone.png"]),
        ("an unreferenced image on disk is found",
         a["orphans"] == ["orphan.png"]),
        ("byte-identical duplicates are found",
         any({f["path"].name for f in g} == {"copy-a.png", "copy-b.png"}
             for g in a["duplicates"])),
        ("a thumbnail/original pair is found",
         any({s["path"].name, l["path"].name} == {"fig1-thumb.png", "fig1.png"}
             for s, l in a["pairs"])),
        ("NEGATIVE: two same-size images of equal aspect are NOT a pair",
         not any({s["path"].name, l["path"].name} == {"fig1.png", "fig2.png"}
                 for s, l in a["pairs"])),
        ("NEGATIVE: a smaller image of the same SHAPE showing something else "
         "is not a thumbnail",
         not any("small-but-different.png" in {s["path"].name, l["path"].name}
                 for s, l in a["pairs"])),
        ("NEGATIVE: distinct images are not called duplicates",
         all(len(g) == 2 for g in a["duplicates"])),
        ("a prose figure reference is detected",
         "2" in a["fig_refs"]),
    ]
    bad = 0
    for name, ok in checks:
        bad += not ok
        print(f"  {'pass' if ok else 'FAIL'}  {name}")
    if bad:
        print(f"\n  {bad} CONTROL(S) FAILED — this audit cannot be trusted.")
        return 2
    print("\n  controls pass: it finds the four defects it exists for, and does "
          "not invent a pair or a duplicate where there is none")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("markdown", type=Path, nargs="?")
    ap.add_argument("--images", type=Path, help="default: sibling images/")
    ap.add_argument("--source", type=Path,
                    help="the .epub or .zip, to find images that never made it out")
    ap.add_argument("--all", action="store_true", help="list every image")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            return self_test(Path(d) / "audit")
    if args.markdown is None:
        ap.error("a markdown file is required unless --self-test")

    print(f"  text                  {args.markdown.name}")
    return report(audit(args.markdown, args.images, args.source), args.all)


if __name__ == "__main__":
    sys.exit(main())
