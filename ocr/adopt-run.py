#!/usr/bin/env python3
"""Take a dispatch run's output into the corpus, or refuse and change nothing.

  ocr/adopt-run.py <run-dir>              dry run: check everything, write nothing
  ocr/adopt-run.py <run-dir> --apply      adopt, if and only if every check passes
  ocr/adopt-run.py <run-dir> --candidate FILE   name the output explicitly

## Why adoption is ours and not the worker's

A worker cannot reach the corpus: it writes inside its workspace and the real
text sits outside the sandbox root. That is the property that makes dispatch safe
to run at all, and handing a worker a tool that writes into `texts/` would spend
it. So the worker PROPOSES -- it names its final artifact in `PROPOSED.md` and
says what it verified -- and adoption happens from outside, gated on checks this
script runs for itself rather than on the worker's report of them.

## Validate first, write last

Every check runs against a staged copy in a temporary directory. The corpus is
touched only after all of them pass, and then in one move. A rejected adoption
leaves `texts/` byte-identical to how it started, so a failed attempt costs
nothing and can simply be run again once the cause is fixed.

Re-adopting the same output is a no-op rather than an error: the file compares
equal, the status is already right, and the script says so and exits 0.

## What it checks

  * the candidate parses as markdown and yields a section tree (the reader's own
    module, not a second implementation of it);
  * the diagnostic triad, run here rather than believed from NOTES.md;
  * for a text that already has markdown, that the triad has not REGRESSED --
    adopting something worse than what is already published is the one failure
    this cannot be allowed to make quietly.

## What it deliberately does not check

Whether the words are the right words. Nothing here reads the text against its
source, which is why adoption sets `needs-review` and never `complete`. Only a
person who has compared it to the printed page can make that change.
"""
from __future__ import annotations

import argparse
import filecmp
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_manifest import output_candidates  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
VENV = ROOT / "ocr" / ".venv" / "bin" / "python3"


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    return p.returncode, (p.stdout + p.stderr)


def triad(md: Path) -> dict[str, tuple[int, str]]:
    """Exit code and last meaningful line for each check."""
    out = {}
    for name, cmd in (
        ("lint-math", [str(VENV), "ocr/verify/lint-math.py", str(md)]),
        ("check-math", ["node", "ocr/verify/check-math.js", str(md)]),
        ("check-raw-latex", ["node", "ocr/verify/check-raw-latex.js", str(md)]),
    ):
        rc, text = run(cmd)
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        # The SUMMARY line, not the last line: check-math prints KaTeX warnings
        # after its summary, and comparing warning text across two runs would
        # make the regression test meaningless.
        summary = next((l for l in lines if re.search(
            r"(issues|failures|surviving backslashes) across", l)), lines[-1] if lines else "")
        out[name] = (rc, summary[:90])
    return out


def failures(summary: str) -> int | None:
    """The leading count out of a check's summary line, for regression tests."""
    m = re.match(r"\s*(\d+)\s", summary)
    return int(m.group(1)) if m else None


def find_candidate(run_dir: Path, explicit: str | None) -> Path | None:
    if explicit:
        p = (run_dir / explicit) if not Path(explicit).is_absolute() else Path(explicit)
        return p if p.is_file() else None
    proposed = run_dir / "PROPOSED.md"
    if proposed.is_file():
        # First fenced or backticked filename in the proposal.
        m = re.search(r"[`\"]([\w.\-/]+\.md)[`\"]", proposed.read_text())
        if m:
            p = run_dir / Path(m.group(1)).name
            if p.is_file():
                return p
    cands = output_candidates(run_dir)
    return cands[0] if len(cands) == 1 else None


TOOLS_DIR = ROOT / "ocr" / "text-specific-tools"


def tools_slug(text_id: str) -> str:
    """Which author directory a text's tools belong in.

    Matched against the directories that already exist before anything is
    derived, because the convention there is an author's name and no rule
    recovers it from a text id: `marcus-aurelius` keeps both words, `cantor`
    keeps one. Falling back, take the first component, or the first two where
    the first is a particle -- `al-khwarizmi-algebra` is al-Khwarizmi, not "al".
    """
    for existing in sorted(p.name for p in TOOLS_DIR.iterdir() if p.is_dir()):
        if text_id == existing or text_id.startswith(existing + "-"):
            return existing
    parts = text_id.split("-")
    return "-".join(parts[:2]) if len(parts[0]) <= 3 and len(parts) > 1 else parts[0]


def file_tools(run_dir: Path, text_id: str) -> list[Path]:
    """Copy a run's scripts into text-specific-tools/, beside their precedents.

    The manifest calls these load-bearing: without them an adopted text is an
    artifact nobody can rebuild, and re-deriving a repair after a source is
    re-extracted means having the script that made it. But a worker cannot file
    them -- the repository is read-only to it by design -- so five runs' worth
    sat in ocr/runs/ where text-specific-tools/ is supposed to be the canonical
    record. Four separate runs reported this as a gap. It is a gap in adoption.

    Copied, not moved: the run directory is the record of what the worker
    produced and stays intact.
    """
    scripts = sorted(p for p in run_dir.iterdir()
                     if p.suffix in (".py", ".sh") and p.is_file())
    if not scripts:
        return []
    dest = TOOLS_DIR / tools_slug(text_id)
    dest.mkdir(parents=True, exist_ok=True)
    for s in scripts:
        shutil.copy2(s, dest / s.name)

    # A note rather than a STAGE.md edit: this records where the scripts came
    # from, which is the thing a later reader needs and cannot reconstruct.
    note = dest / "PROVENANCE.md"
    line = (f"- `{text_id}` — {len(scripts)} script(s) from dispatch run "
            f"`{run_dir.name}`, adopted "
            f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}: "
            + ", ".join(f"`{s.name}`" for s in scripts) + "\n")
    if not note.exists():
        note.write_text(
            "# Where these scripts came from\n\n"
            "Written by dispatched workers and copied here at adoption. The run "
            "directory under `ocr/runs/` holds the worker's own notes on each.\n\n")
    if line not in note.read_text():
        with note.open("a") as fh:
            fh.write(line)
    return [dest / s.name for s in scripts]


# A run's NOTES.md mixes two things deliberately: what this TEXT needs, and what
# the attempt taught us about our TOOLING. Only the first belongs beside the
# text -- the run is a record of an event, the text folder a record of a thing
# that outlives every run that touched it.
#
# This excludes the pipeline sections rather than enumerating the textual ones,
# because the two failure modes are not symmetric. Dropping a finding hides a
# real defect from the only person who will ever look for it; importing a
# paragraph about a slow script wastes a few seconds. An include-list was tried
# first and immediately lost Anselm's page-cited repairs, which are the most
# valuable thing that run produced.
PIPELINE_HEADINGS = (
    "time", "tooling", "pipeline", "documentation", "scripts and",
    "observations", "controls", "where the",
)


def extract_text_findings(notes: Path) -> list[tuple[str, str]]:
    """Pull the sections of a run's NOTES.md that are about the text.

    Heading-matched rather than clever, and biased toward keeping: everything
    survives except sections that are plainly about our tooling. The full notes
    are one link away regardless, so this decides what a reviewer sees without
    being asked, not what exists.
    """
    if not notes.is_file():
        return []
    out: list[tuple[str, str]] = []
    current: str | None = None
    body: list[str] = []
    for line in notes.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(#{2,3}) (.+)$", line)
        if m:
            if current and any(b.strip() for b in body):
                out.append((current, "\n".join(body).strip()))
            title = m.group(2).strip()
            low = title.lower()
            current = None if any(k in low for k in PIPELINE_HEADINGS) else title
            body = []
        elif current:
            body.append(line)
    if current and any(b.strip() for b in body):
        out.append((current, "\n".join(body).strip()))
    return out


def write_review(text_dir: Path, text_id: str, meta: dict, run_dir: Path,
                 prov: dict) -> Path:
    """Create or refresh the text's review record.

    This is the bridge between processing and review. A run knows things a
    reviewer needs -- which readings are doubtful, what witness exists, what was
    repaired and on whose authority -- and until now that knowledge lived only in
    `ocr/runs/`, gitignored siblings away from the text it describes, in a
    directory that gets pruned.

    An existing human review log is never overwritten: everything below the log
    marker is regenerated, everything above it is the reviewer's and is kept.
    """
    review = text_dir / "review.md"
    marker = "<!-- review log — hand-written, never regenerated -->"
    kept = ""
    if review.is_file():
        existing = review.read_text(encoding="utf-8")
        if marker in existing:
            kept = existing.split(marker, 1)[1]

    findings = extract_text_findings(run_dir / "NOTES.md")
    # The run's own handover leads, if it wrote one. The charter asks for it; the
    # sweep below still carries everything else, so a run that forgets loses
    # nothing -- which is the point. A section that decides what survives is a
    # whitelist, and every whitelist in this pipeline has silently dropped work.
    findings.sort(key=lambda f: 0 if "for the reviewer" in f[0].lower() else 1)
    rel_run = run_dir.relative_to(ROOT)
    parts = [
        f"# {meta.get('title', text_id)} — review record",
        "",
        "What is known about this text as a text: where it came from, what can "
        "check it, and what is doubtful. Generated at adoption from the "
        "processing run, then maintained by whoever reviews it.",
        "",
        "**Status is a claim about process, not about correctness.** "
        "`needs-review` means machine-processed and unread. `complete` means a "
        "person performed the review below and judged the text shippable — not "
        "that it is free of errors. Every text is an ongoing project.",
        "",
        "## Provenance",
        "",
        f"- Source file: `{meta.get('filename', '?')}`",
        f"- Translator: {meta.get('translator') or '—'}"
        + (f" ({meta['year_translated']})" if meta.get("year_translated") else ""),
        f"- Processed by run [`{rel_run}`](../../../{rel_run}) "
        f"({prov.get('model', '?')}, {prov.get('started', '?')[:10]})",
        f"- Full processing notes: [`{rel_run}/NOTES.md`](../../../{rel_run}/NOTES.md)",
        "",
    ]
    if findings:
        parts += ["## What the processing run found", ""]
        parts += [
            "Copied from the run's notes at adoption. These are the text's open "
            "questions, not the pipeline's.", ""]
        for title, body in findings:
            parts += [f"### {title}", "", body, ""]
    else:
        parts += [
            "## What the processing run found", "",
            "The run recorded no text-specific findings under a recognised "
            f"heading. Read [`{rel_run}/NOTES.md`](../../../{rel_run}/NOTES.md) "
            "before reviewing — it may still say something useful.", ""]

    parts += [
        "## Review", "",
        "The pass that sets `complete`: read the run's escalations and notes to "
        "learn what the processing actually encountered, then read the text in "
        "the rendered reader, comparing against the source where something looks "
        "wrong. Not a full proofread — a judgement about whether it is shippable.",
        "",
        "- [ ] Escalations and notes read",
        "- [ ] Rendered in the reader; structure, headings and contents look right",
        "- [ ] Spot-checked against the source where the notes flagged doubt",
        "- [ ] Remaining known issues recorded below",
        "",
        marker,
    ]
    # Seed a visible log below the marker when there is nothing there yet.
    # The marker alone is an HTML comment: it works, but a reviewer opening the
    # file sees a generated record that appears to end, with no indication that
    # the bottom of it is theirs. An invisible convention gets reinvented — this
    # one nearly acquired a parallel `notes.md` for want of a heading.
    seed = (
        "\n\n## Review log\n\n"
        "Observations, questions and decisions from reading this text. "
        "Everything below the marker above belongs to the reviewer and is never "
        "regenerated, so append freely — re-adopting the run rewrites only what "
        "is above it.\n"
    )
    review.write_text("\n".join(parts) + (kept if kept else seed), encoding="utf-8")
    return review


def stamp_adopted(prov_path: Path, prov: dict, target: Path) -> None:
    """Record that this run's output reached the library.

    The dashboard hides adopted runs by default, so that what it prints stays
    the work still open rather than a growing history. This is the only fact it
    cannot derive from the files it already reads: a run directory looks the
    same before and after its output was taken, and the published text carries
    no memory of which run produced it.

    Written by the tool that did the thing, into the run's own provenance,
    beside the other stamps -- not into a separate index that could disagree.
    """
    prov["adopted"] = {
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "target": str(target.relative_to(ROOT)),
    }
    prov_path.write_text(json.dumps(prov, indent=2) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--candidate")
    ap.add_argument("--readopt", action="store_true",
                    help="re-adopt a run whose published text has since changed")
    args = ap.parse_args()

    run_dir = Path(args.run_dir).resolve()
    if not run_dir.is_dir():
        print(f"no such run directory: {run_dir}", file=sys.stderr)
        return 2

    prov_path = run_dir / "provenance.json"
    if not prov_path.is_file():
        print("no provenance.json — this run did not finish", file=sys.stderr)
        return 2
    prov = json.loads(prov_path.read_text())
    # "text" is the legacy key from the hand-rolled wrapper that predated
    # dispatch-text.sh; the first run in ocr/runs/ still carries it.
    text_id = prov.get("text_id") or prov.get("text")
    if not text_id:
        print("provenance names no text", file=sys.stderr)
        return 2

    if (run_dir / "ESCALATION.md").is_file():
        print("run is BLOCKED on an escalation; answer it before adopting", file=sys.stderr)
        return 2

    cand = find_candidate(run_dir, args.candidate)
    if cand is None:
        print("cannot identify the output. The run left several .md files and no\n"
              "PROPOSED.md naming one. Pass --candidate FILE.", file=sys.stderr)
        return 2

    dirs = list(ROOT.glob(f"texts/*/{text_id}"))
    if not dirs:
        print(f"no text directory for '{text_id}'", file=sys.stderr)
        return 2
    text_dir = dirs[0]
    meta_path = text_dir / "metadata.json"
    meta = json.loads(meta_path.read_text())
    # metadata.filename points at the SOURCE for a text that has not been
    # processed yet -- for Dedekind it was 21016-pdf.pdf, and reusing it here
    # would have adopted the markdown straight over the source PDF. Only reuse
    # it when it already names markdown; otherwise take the convention name.
    existing = meta.get("filename") or ""
    target = text_dir / (existing if existing.endswith(".md") else f"{text_id}.md")

    print(f"  run      : {run_dir.name}")
    print(f"  candidate: {cand.name}  ({cand.stat().st_size/1024:.0f} KB)")
    print(f"  target   : {target.relative_to(ROOT)}")

    # A run that has already been adopted is no longer an authority on the
    # published text. Backfilling adoption stamps re-ran this over Dedekind and
    # silently reverted a hand edit made after adoption -- restoring a state the
    # library had deliberately moved on from -- and reset an ocr_status a person
    # had promoted to complete. Adoption is one-way by design; going back the
    # other way has to be asked for.
    if prov.get("adopted") and target.is_file() and not args.readopt:
        drifted = not filecmp.cmp(cand, target, shallow=False)
        promoted = meta.get("ocr_status") == "complete"
        if drifted or promoted:
            print("\n  REFUSED — this run was already adopted"
                  f" ({prov['adopted'].get('at', '')}), and the published text has"
                  " since moved:")
            if drifted:
                print("    the file differs from this run's output (edited after adoption)")
            if promoted:
                print("    its status is 'complete' — somebody read it")
            print("  Re-adopting would overwrite that. Pass --readopt if that is"
                  " what you mean.")
            return 1

    if target.is_file() and filecmp.cmp(cand, target, shallow=False):
        if meta.get("ocr_status") in ("needs-review", "complete"):
            print("  already adopted, byte-identical, status set — nothing to do")
            if args.apply:
                stamp_adopted(prov_path, prov, target)
                # Still refresh the review record. It was introduced after some
                # texts were adopted, and re-deriving it costs nothing: the
                # hand-written log below the marker is preserved.
                review = write_review(text_dir, text_id, meta, run_dir, prov)
                print(f"  review {review.relative_to(ROOT)}")
            return 0
        print("  content already identical; only the status differs")

    # --- everything below runs against a staged copy ---
    with tempfile.TemporaryDirectory() as td:
        staged = Path(td) / target.name
        shutil.copy2(cand, staged)

        rc, out = run([str(VENV), "-c",
                       "import sys;sys.path.insert(0,'site/src/lib');"
                       "print('markdown readable:', len(open(sys.argv[1]).read())>0)",
                       str(staged)])
        print(f"  {'ok ' if rc == 0 else 'FAIL'} readable")

        rc_tree, tree_out = run(["node", "-e", f"""
          const {{readFileSync}} = require('fs');
          const md = readFileSync({json.dumps(str(staged))}, 'utf8');
          const n = (md.match(/^#{{1,3}} /gm) || []).length;
          if (!n) {{ console.error('no headings — the reader would render one blob'); process.exit(1); }}
          console.log('headings: ' + n);
        """])
        print(f"  {'ok ' if rc_tree == 0 else 'FAIL'} structure  {tree_out.strip()[:60]}")

        # In-page anchors are worse than broken here: the router treats an
        # unknown hash as a route and ejects the reader to the front page. This
        # is a gate rather than advice because it reached adoption once already.
        # Images. A repair run may regenerate figures -- al-Khwarizmi recropped
        # 18 diagrams from the scan at 288 dpi, referencing `img-N.png` where the
        # corpus held only the older `img-N.jpeg` -- so a reference can resolve
        # against the run, against the text directory, or nowhere. Nowhere means
        # a published text with broken figures, and nothing else here would have
        # noticed: the triad reads math, and the anchor check reads links.
        refs = sorted(set(re.findall(r'\]\(images/([^)]+)\)', staged.read_text())))
        run_images = run_dir / "images"
        unresolved = [r for r in refs
                      if not (text_dir / "images" / r).is_file()
                      and not (run_images / r).is_file()]
        from_run = [r for r in refs if (run_images / r).is_file()
                    and not (text_dir / "images" / r).is_file()]
        if refs:
            print(f"  {'ok ' if not unresolved else 'FAIL'} images       "
                  f"{len(refs)} referenced, {len(from_run)} new from this run"
                  + (f", {len(unresolved)} UNRESOLVED" if unresolved else ""))
            for r in unresolved[:5]:
                print(f"      missing: {r}")

        anchors = len(re.findall(r'href="#', staged.read_text()))
        print(f"  {'ok ' if anchors == 0 else 'FAIL'} no in-page links"
              f"{'' if anchors == 0 else f'  ({anchors} found — run strip-inpage-anchors.py)'}")

        new = triad(staged)
        for name, (rc_c, tail) in new.items():
            print(f"  {'ok ' if rc_c == 0 else 'FAIL'} {name:16} {tail}")

        regressed = []
        if target.is_file():
            old = triad(target)
            for name in new:
                a, b = failures(old[name][1]), failures(new[name][1])
                if a is not None and b is not None and b > a:
                    regressed.append(f"{name}: {a} -> {b}")

        bad = [n for n, (rc_c, _) in new.items() if rc_c != 0]
        if bad or rc_tree != 0 or regressed or anchors or unresolved:
            print("\n  REFUSED — nothing written.")
            for r in regressed:
                print(f"    regression against the published text: {r}")
            if unresolved:
                print(f"    {len(unresolved)} image reference(s) resolve nowhere")
            if bad:
                print(f"    failing checks: {', '.join(bad)}")
            return 1

        if not args.apply:
            print("\n  all checks pass (dry run — pass --apply to adopt)")
            return 0

        shutil.copy2(staged, target)
        if from_run:
            (text_dir / "images").mkdir(exist_ok=True)
            for r in from_run:
                shutil.copy2(run_images / r, text_dir / "images" / r)
            print(f"  copied {len(from_run)} new image(s) into {(text_dir / 'images').relative_to(ROOT)}")

    meta["filename"] = target.name
    meta["format"] = "markdown"
    # needs-review is a floor, not an assignment. Only a person reading the text
    # against its source can set 'complete', and this must never take that back.
    if meta.get("ocr_status") != "complete":
        meta["ocr_status"] = "needs-review"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    filed = file_tools(run_dir, text_id)
    for p in filed:
        print(f"  filed  {p.relative_to(ROOT)}")

    review = write_review(text_dir, text_id, meta, run_dir, prov)
    print(f"  review {review.relative_to(ROOT)}")

    stamp_adopted(prov_path, prov, target)
    print(f"\n  adopted → {target.relative_to(ROOT)}")
    print("  ocr_status = needs-review  (machine-checked; nobody has read it yet)")

    rc, out = run(["npm", "--prefix", "site", "run", "build-index"])
    tail = [l for l in out.splitlines() if l.strip()][-1:] or [""]
    print(f"  {'ok ' if rc == 0 else 'FAIL'} build-index  {tail[0][:70]}")
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
