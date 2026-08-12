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

RECONCILIATION IS NOT AUDIT, AND THE DIFFERENCE COST A RUN. Everything here
except the sequence check compares two lists THIS PIPELINE PRODUCED, so it can
only find loss that hit one side and not the other. Galileo's OCR dropped four
diagrams and eight captions before either side existed; markdown and disk agreed
at 131 = 131 and this tool said clean. The printed numbering is the one witness
the pipeline did not write, and it is checked FIRST because it is also free.

VALIDATED AGAINST THE CASE THAT DEFEATED THE PREVIOUS VERSION. Run on Galileo's
raw pre-repair OCR (138 refs, 138 files, no reconciliation finding at all), the
sequence check reports gaps at 3, 10, 44, 48, 55, 60, 86, 100, 111, 113 and 125
-- the three diagrams and all eight captions the run found by hand. Fig. 50 is
correctly absent from that list: its caption survived inside `more-Fig. 50 over`,
so the number WAS in the prose and the defect was a different one. That check is
a one-off validation against a live text, not a control; live controls expire
when the text is fixed, so the permanent controls in self_test() are synthetic.

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
# Editions invent their own word for this: Hooke's Micrographia numbers plates
# `Schem. I`, and a text whose label is not below is a text whose sequence goes
# unchecked in silence. Hence --label, and hence the RESULT block saying out
# loud when no sequence was found.
DEFAULT_LABELS = ("fig(?:ure)?", "plate")


def build_fig_ref(labels: tuple[str, ...] = DEFAULT_LABELS) -> re.Pattern:
    alt = "|".join(labels)
    return re.compile(rf"\b({alt})\.?\s*([0-9]{{1,3}}|[IVXLC]{{1,6}})\b", re.I)


FIG_REF = build_fig_ref()

# Below this many distinct numbers, a "sequence" is coincidence rather than a
# numbering scheme, and its gaps mean nothing.
SEQ_MIN = 3

# A printed numbering is DENSE: it runs 1, 2, 3 with few holes. Ordinary prose
# using the same word is sparse -- De Re Metallica is a book about metal plates,
# and three stray uses spanning `plate I` to `plate C` produced 97 "gaps" that
# cost a run real time. Below this fill ratio it is not a numbering scheme and
# no gap is reported.
SEQ_DENSITY = 0.5

# `Fig. 3` is nearly always a citation. `figure 3` is often prose -- in Euler's
# Elements of Algebra "figure" means DIGIT, and a dense, clean sequence 2-9 was
# still not about diagrams. We cannot tell those apart mechanically, and this
# tool does not guess elsewhere (it will not call an ornament an ornament), so
# it does not guess here: it reports which surface form was seen and says that a
# spelled-out-only sequence is weak evidence.
ABBREVIATED = ("fig.", "figs.", "pl.")

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


# Micrographia's thumbnails are every one of them squeezed into a fixed 110x170
# box, so their aspect ratios drift from the plates they shrink: 17 of 38 failed
# the 6% prefilter, and at a 13x downscale the 32x32 comparison rejected more.
# Content detection found 8 of 38.
#
# Loosening the pixel thresholds would bring back Huygens' 47 phantom pairs, so
# this adds a SECOND, INDEPENDENT witness instead -- the publisher's own naming.
# `scheme-01.png` beside `scheme-01t.png` is a claim someone else made, and it
# survives a downscale that defeats the pixels. Same principle as the printed
# sequence: prefer the witness the pipeline did not write.
THUMB_SUFFIXES = ("t", "-t", "_t", "-thumb", "_thumb", "thumb",
                  "-small", "_small", "-sm", "_sm")


def find_name_pairs(facts: list[dict]) -> list[tuple[dict, dict]]:
    """Thumbnail/original pairs asserted by FILENAME rather than by pixels."""
    by_stem = {f["path"].stem: f for f in facts}
    pairs = []
    for stem, small in by_stem.items():
        for suf in THUMB_SUFFIXES:
            if not stem.endswith(suf) or len(stem) <= len(suf):
                continue
            large = by_stem.get(stem[:-len(suf)])
            # Only a claim if the named thumbnail really is the smaller file.
            if large and small["area"] and large["area"] > small["area"]:
                pairs.append((small, large))
                break
    return pairs


_ROMAN = [(100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
          (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def _to_roman(n: int) -> str:
    out = []
    for v, s in _ROMAN:
        while n >= v:
            out.append(s)
            n -= v
    return "".join(out)


def _from_roman(s: str) -> int | None:
    """Strict: only canonical numerals parse. Round-tripping is the whole test.

    The regex is deliberately loose so it can catch `Plate iv`, which means it
    also catches `Fig. ill`. Requiring int -> roman -> the same string back
    rejects ILL, IIII and XXXX without a table of exceptions.
    """
    val = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
    s = s.upper()
    total = prev = 0
    for ch in reversed(s):
        if ch not in val:
            return None
        v = val[ch]
        total += -v if v < prev else v
        prev = max(prev, v)
    return total if total and _to_roman(total) == s else None


def figure_sequence(text: str, pat: re.Pattern | None = None) -> list[dict]:
    """The printed numbering, as a sequence, with its GAPS.

    THIS IS THE ONLY WITNESS HERE THAT THE PIPELINE DID NOT WRITE. Every other
    check in this file compares two lists we produced -- markdown references
    against files on disk -- so it can only ever find loss that hit one side and
    not the other. A figure dropped by OCR is missing from BOTH, the two sides
    agree perfectly, and the audit reports clean. That is not a bug in the
    comparison; it is what reconciliation means.

    The printed numbers are different in kind: the printer wrote `Fig. 57`, not
    us, and the number survives the loss of the figure it names because it is
    spread over the whole book. Galileo's run found four absent diagrams and
    eight absent captions by reconstructing this sequence BY HAND, after an
    audit that had already told it 131 references matched 131 files.

    A gap is a FINDING FOR A PERSON, never a failure: an edition may skip a
    number, and a figure may be printed without being named in the prose.

    WHAT IT MUST NOT DO IS INVENT GAPS. Shipped without the density floor, this
    reported 97 of them on De Re Metallica -- a book about metal plates, where
    three ordinary uses of the word spanned `plate I` to `plate C`. That cost a
    run real time and is worse than reporting nothing.
    """
    pat = pat or FIG_REF
    groups: dict[tuple[str, str], Counter] = defaultdict(Counter)
    forms: dict[tuple[str, str], Counter] = defaultdict(Counter)
    for m in pat.finditer(text):
        word, token = m.group(1).lower(), m.group(2)
        kind = word.rstrip(".") or "figure"
        surface = m.group(0)[:len(m.group(1)) + 1].lower()
        key_sys = "arabic" if token.isdigit() else "roman"
        n = int(token) if token.isdigit() else _from_roman(token)
        if n is None:
            continue
        groups[(kind, key_sys)][n] += 1
        forms[(kind, key_sys)][surface] += 1

    out = []
    for (kind, system), counts in sorted(groups.items()):
        if len(counts) < SEQ_MIN:
            continue
        lo, hi = min(counts), max(counts)
        fmt = _to_roman if system == "roman" else str
        span = hi - lo + 1
        density = len(counts) / span
        f = forms[(kind, system)]
        abbreviated = sum(v for k, v in f.items() if k in ABBREVIATED)
        out.append({
            "kind": kind, "system": system, "lo": lo, "hi": hi,
            "distinct": len(counts), "density": density,
            # A sparse scatter is prose reusing the word, not a numbering.
            "is_numbering": density >= SEQ_DENSITY,
            # Spelled out throughout is weak evidence that these are citations.
            "abbreviated": abbreviated,
            "forms": dict(f),
            "missing": ([n for n in range(lo, hi + 1) if n not in counts]
                        if density >= SEQ_DENSITY else []),
            "fmt": fmt,
        })
    return sorted(out, key=lambda s: -s["distinct"])


def audit(md: Path | None, images: Path | None, source: Path | None,
          pat: re.Pattern | None = None) -> dict:
    text = md.read_text(encoding="utf-8", errors="replace") if md else ""

    # The comparison is by BASENAME, both sides. Gilbert's run could not tell
    # which basis was in play, so it is stated here and checked below: if two
    # references differ only by directory, the basename basis is silently
    # merging them and every count after this is wrong.
    ref_paths = MD_IMG.findall(text) + HTML_IMG.findall(text)
    ref_counts = Counter(Path(r).name for r in ref_paths)
    by_base: dict[str, set[str]] = defaultdict(set)
    for r in ref_paths:
        by_base[Path(r).name].add(r)
    collisions = sorted(b for b, paths in by_base.items() if len(paths) > 1)

    images = images or (md.parent / "images" if md else None)
    have_images = bool(images and images.is_dir())
    on_disk = sorted(p for p in images.iterdir()
                     if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif",
                                             ".svg", ".webp")) if have_images else []
    facts = [image_facts(p) for p in on_disk if p.suffix.lower() != ".svg"]
    names = {p.name for p in on_disk}

    by_sha = defaultdict(list)
    for f in facts:
        by_sha[f["sha"]].append(f)

    in_source = None
    if source and source.suffix.lower() in (".epub", ".zip"):
        with zipfile.ZipFile(source) as z:
            in_source = {Path(n).name for n in z.namelist()
                         if Path(n).suffix.lower() in (".png", ".jpg", ".jpeg", ".gif")}

    pat = pat or FIG_REF
    sequences = figure_sequence(text, pat)

    # What this run was actually able to check. "No findings" is a claim about
    # the witnesses you had, and the verdict has to say which those were.
    witnesses = {
        "markdown refs vs files on disk": bool(md) and have_images,
        "printed figure sequence": bool(sequences),
        "filename thumbnail convention": bool(find_name_pairs(facts)),
        "source artifact": in_source is not None,
    }

    return {
        "referenced": ref_counts,
        "collisions": collisions,
        "on_disk": names,
        "have_images": have_images,
        "have_md": bool(md),
        "facts": facts,
        "dangling": sorted(set(ref_counts) - names) if have_images else [],
        "orphans": sorted(names - set(ref_counts)) if md else [],
        "duplicates": [v for v in by_sha.values() if len(v) > 1],
        "pairs": find_pairs(facts),
        "name_pairs": find_name_pairs(facts),
        "fig_refs": {m.group(2).upper() for m in pat.finditer(text)},
        "sequences": sequences,
        "in_source": in_source,
        "witnesses": witnesses,
    }


def report_sequence(a: dict) -> int:
    """Runs FIRST and costs nothing. Galileo's run named the ordering directly:
    'Had that cheap sequence check happened first, the missing captions and
    source-page crops would have been found together rather than in successive
    passes.'"""
    gaps = 0
    if not a["sequences"]:
        print("\n  printed sequence      none found — no numbering scheme with "
              f"{SEQ_MIN}+ distinct")
        print("                        numbers. The strongest witness available "
              "here is")
        print("                        absent; see the RESULT block.")
        return 0

    for s in a["sequences"]:
        f = s["fmt"]
        span = f"{s['kind'].title()} {f(s['lo'])}–{f(s['hi'])}"
        print(f"\n  printed sequence      {span} ({s['system']}), "
              f"{s['distinct']} distinct, density {s['density']:.2f}")

        if not s["is_numbering"]:
            print("                        NOT A NUMBERING SCHEME — too sparse to be")
            print("                        one. These are almost certainly ordinary")
            print("                        prose uses of the word. No gaps reported;")
            print("                        reporting them here once produced 97.")
            continue

        if not s["abbreviated"]:
            forms = ", ".join(sorted(s["forms"]))
            print(f"                        spelled out throughout ({forms}) — WEAK")
            print("                        evidence that these are figure citations.")
            print("                        In Euler 'figure' means DIGIT. Confirm the")
            print("                        word means a diagram here before acting.")

        if not s["missing"]:
            print("                        continuous, no gap")
            continue
        gaps += len(s["missing"])
        shown = ", ".join(f(n) for n in s["missing"][:20])
        print(f"  ⚠ GAPS IN THE SEQUENCE  {len(s['missing'])}: {shown}"
              f"{'…' if len(s['missing']) > 20 else ''}")
        print("      The prose numbers these but never names them. THIS IS THE")
        print("      ONE CHECK HERE THAT CAN SEE A FIGURE LOST FROM BOTH THE")
        print("      MARKDOWN AND THE DISK — the case reconciliation is blind to.")
        print("      A gap is not automatically a defect: an edition may skip a")
        print("      number, and a figure may be printed without being named.")
        print("      Go to the printed pages either side and look.")
    return gaps


def report(a: dict, show_all: bool) -> int:
    gaps = report_sequence(a)
    print()
    print(f"  images on disk        {len(a['on_disk']) if a['have_images'] else '— (no images dir)'}")
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

    named = [p for p in a["name_pairs"]
             if {p[0]["path"], p[1]["path"]} not in
             [{q[0]["path"], q[1]["path"]} for q in a["pairs"]]]
    if named:
        print(f"\n  ⚠ THUMBNAIL PAIRS BY FILENAME  {len(named)} more")
        for small, large in named[:8]:
            print(f"      {small['path'].name} ({small['w']}×{small['h']})"
                  f"  ↔  {large['path'].name} ({large['w']}×{large['h']})")
        print("      The names claim these are the same image at two sizes, and")
        print("      the content check did NOT catch them — a fixed-box thumbnail")
        print("      changes the aspect ratio and loses the detail the pixel")
        print("      comparison needs. Two witnesses disagreeing is information.")

    if a["collisions"]:
        print(f"\n  ⚠ BASENAME COLLISIONS     {len(a['collisions'])}")
        for n in a["collisions"][:8]:
            print(f"      {n}")
        print("      Both sides of this audit are compared by BASENAME. These")
        print("      names appear at more than one path, so they are being")
        print("      merged and every count above understates the true number.")

    if a["fig_refs"] and a["have_images"]:
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

    problems = (len(a["dangling"]) + len(a["duplicates"]) + len(a["pairs"])
                + len(named) + len(a["collisions"]) + gaps)

    # THE VERDICT DECLARES ITS OWN REACH. Galileo's run trusted a clean result
    # that was clean about the wrong thing: 131 references matched 131 files
    # while four diagrams were absent from both. "No findings" is a claim about
    # the witnesses you had, so the witnesses are named either way.
    had = [w for w, ok in a["witnesses"].items() if ok]
    lacked = [w for w, ok in a["witnesses"].items() if not ok]
    print()
    print(f"  RESULT: {problems} finding(s) that need a person." if problems
          else "  RESULT: no defect found — against the witnesses listed below.")
    for w in had:
        print(f"    checked      {w}")
    for w in lacked:
        print(f"    NOT checked  {w}")
    print(f"\n  reach: {len(had)} of {len(a['witnesses'])} witnesses.")
    if not a["witnesses"]["printed figure sequence"]:
        print("    Without a printed sequence, every check here compares two lists")
        print("    THIS PIPELINE PRODUCED. A figure lost before extraction is")
        print("    missing from both, they agree, and nothing above can see it.")
    if not a["witnesses"]["source artifact"]:
        print("    Without --source, an image that never survived extraction is")
        print("    invisible.")
    print("  Always invisible: whether a figure is a diagram or an ornament, and")
    print("  whether a correct-looking figure is the RIGHT one for its place.")
    print("  Nothing here has been changed; this tool only reports.")
    return 1 if problems else 0


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

    # THE CONTROL THIS REVISION EXISTS FOR. Galileo's audit reported 131
    # references against 131 files and was right; four diagrams were absent
    # from BOTH sides and it could not see them. So: a text whose markdown and
    # disk agree perfectly, with a hole in the printed numbering.
    seq_imgs = tmp / "seq-images"
    seq_imgs.mkdir(exist_ok=True)
    for n in (1, 2, 3, 5, 6):                      # Fig. 4 was lost at OCR
        Image.new("RGB", (300, 200), (n * 7, 40, 40)).save(seq_imgs / f"f{n}.png")
    seq_md = tmp / "seq.md"
    seq_md.write_text("".join(f"As Fig. {n} shows. ![](seq-images/f{n}.png)\n\n"
                              for n in (1, 2, 3, 5, 6)))
    s = audit(seq_md, seq_imgs, None)
    seq = s["sequences"][0] if s["sequences"] else None
    checks += [
        ("SYMMETRIC LOSS: refs and disk agree perfectly (the Galileo case)",
         not s["dangling"] and not s["orphans"]),
        ("...and the printed sequence still finds the missing figure",
         seq is not None and seq["missing"] == [4]),
        ("the sequence witness is reported as checked",
         s["witnesses"]["printed figure sequence"] is True),
        ("an absent --source is reported as NOT checked",
         s["witnesses"]["source artifact"] is False),
        ("NEGATIVE: a continuous sequence reports no gap",
         not figure_sequence("Fig. 1 a. Fig. 2 b. Fig. 3 c. Fig. 4 d.")[0]["missing"]),
        ("NEGATIVE: too few numbers is not treated as a sequence",
         figure_sequence("Fig. 1 and Fig. 9 only.") == []),
        ("roman numbering is read as a sequence",
         any(x["system"] == "roman" for x in
             figure_sequence("Plate I. Plate II. Plate IV."))),
        ("...and its gap is found",
         [x for x in figure_sequence("Plate I. Plate II. Plate IV.")
          if x["system"] == "roman"][0]["missing"] == [3]),
        ("NEGATIVE: 'Fig. ill' is not parsed as a roman numeral",
         _from_roman("ILL") is None and _from_roman("IIII") is None),
        ("figures and plates are counted as separate sequences",
         len(figure_sequence("Fig. 1 Fig. 2 Fig. 3 Plate 7 Plate 8 Plate 9")) == 2),
    ]

    # An edition's own word for a figure. Micrographia numbers plates `Schem. I`
    # and would otherwise be audited against a sequence of nothing, silently.
    schem = "Schem. I. Schem. II. Schem. IV. Schem. V."
    checks += [
        ("NEGATIVE: an unknown label finds no sequence at all",
         figure_sequence(schem) == []),
        ("--label finds it, and its gap",
         figure_sequence(schem, build_fig_ref(DEFAULT_LABELS + ("schem",)))[0]
         ["missing"] == [3]),
    ]

    # THE TWO WAYS THIS INVENTED WORK IN ITS FIRST WAVE. Both cost a run time,
    # and both are false POSITIVES -- worse than silence, because a person has
    # to disprove each one.
    metallurgy = ("A plate I of copper. Another plate L. A third plate C. "
                  "Beat the plate thin.")            # De Re Metallica: 97 gaps
    algebra = ("the figure 2 and the figure 3, then figure 4, figure 5, "
               "figure 6, figure 7, figure 8, figure 9")   # Euler: digits
    seq_m = figure_sequence(metallurgy)
    seq_a = figure_sequence(algebra)
    checks += [
        ("SPARSE: prose reusing the word is not a numbering scheme",
         all(not x["is_numbering"] for x in seq_m)),
        ("...and it reports no gaps at all (this once produced 97)",
         all(not x["missing"] for x in seq_m)),
        ("DENSE BUT SPELLED OUT: reported, and marked weak evidence",
         bool(seq_a) and seq_a[0]["is_numbering"] and seq_a[0]["abbreviated"] == 0),
        ("an abbreviated `Fig.` sequence is NOT marked weak",
         figure_sequence("Fig. 1 a. Fig. 2 b. Fig. 3 c.")[0]["abbreviated"] > 0),
    ]

    # THE HOOKE CASE: a fixed-box thumbnail whose aspect ratio does NOT match
    # its original, so the pixel comparison cannot see it. 110x170 from 826x1225
    # is Micrographia's actual shape. Content found 8 of 38; the names find all.
    np_imgs = tmp / "np-images"
    np_imgs.mkdir(exist_ok=True)
    Image.new("RGB", (826, 1225), (30, 60, 90)).save(np_imgs / "scheme-01.png")
    Image.new("RGB", (110, 170), (30, 60, 90)).save(np_imgs / "scheme-01t.png")
    Image.new("RGB", (400, 400), (1, 2, 3)).save(np_imgs / "unrelated.png")
    nf = [image_facts(p) for p in sorted(np_imgs.iterdir())]
    named = find_name_pairs(nf)
    checks += [
        ("a fixed-box thumbnail is found by FILENAME when pixels cannot",
         len(named) == 1
         and {named[0][0]["path"].name, named[0][1]["path"].name}
         == {"scheme-01t.png", "scheme-01.png"}),
        ("NEGATIVE: an unrelated file is not paired by name",
         all("unrelated.png" not in {s["path"].name, l["path"].name}
             for s, l in named)),
    ]

    # A basename collision must be visible, since both sides compare on it.
    coll_md = tmp / "coll.md"
    coll_md.write_text("![](a/fig1.png) and ![](b/fig1.png)\n")
    checks.append(("a basename collision is reported",
                   audit(coll_md, imgs, None)["collisions"] == ["fig1.png"]))
    bad = 0
    for name, ok in checks:
        bad += not ok
        print(f"  {'pass' if ok else 'FAIL'}  {name}")
    if bad:
        print(f"\n  {bad} CONTROL(S) FAILED — this audit cannot be trusted.")
        return 2
    print("\n  controls pass: it finds the defects it exists for, it finds a "
          "figure lost\n  symmetrically from markdown AND disk, and it does not "
          "invent a pair, a\n  duplicate or a gap where there is none")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("markdown", type=Path, nargs="?")
    ap.add_argument("--images", type=Path, help="default: sibling images/")
    ap.add_argument("--source", type=Path,
                    help="the .epub or .zip, to find images that never made it out")
    ap.add_argument("--all", action="store_true", help="list every image")
    ap.add_argument("--label", action="append", metavar="WORD",
                    help="the edition's word for a numbered figure, if it is "
                         "not fig/figure/plate — e.g. --label schem for "
                         "Micrographia. Repeatable.")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            return self_test(Path(d) / "audit")
    # Gilbert's run wanted to look into an EPUB before there was any markdown.
    # Either input alone is a usable audit; only BOTH missing is an error, and
    # whichever is absent is then named as an unchecked witness in the RESULT.
    if args.markdown is None and args.source is None and args.images is None:
        ap.error("give a markdown file, or --source, or --images "
                 "(or --self-test)")

    pat = build_fig_ref(DEFAULT_LABELS + tuple(re.escape(w) for w in args.label)) \
        if args.label else FIG_REF

    print(f"  text                  {args.markdown.name if args.markdown else '— (none given)'}")
    return report(audit(args.markdown, args.images, args.source, pat), args.all)


if __name__ == "__main__":
    sys.exit(main())
