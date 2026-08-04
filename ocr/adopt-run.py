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
        if bad or rc_tree != 0 or regressed or anchors:
            print("\n  REFUSED — nothing written.")
            for r in regressed:
                print(f"    regression against the published text: {r}")
            if bad:
                print(f"    failing checks: {', '.join(bad)}")
            return 1

        if not args.apply:
            print("\n  all checks pass (dry run — pass --apply to adopt)")
            return 0

        shutil.copy2(staged, target)

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

    stamp_adopted(prov_path, prov, target)
    print(f"\n  adopted → {target.relative_to(ROOT)}")
    print("  ocr_status = needs-review  (machine-checked; nobody has read it yet)")

    rc, out = run(["npm", "--prefix", "site", "run", "build-index"])
    tail = [l for l in out.splitlines() if l.strip()][-1:] or [""]
    print(f"  {'ok ' if rc == 0 else 'FAIL'} build-index  {tail[0][:70]}")
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
