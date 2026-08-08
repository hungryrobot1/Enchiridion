#!/usr/bin/env python3
"""What every dispatch run is doing, and which ones are waiting on us.

  ocr/runs-status.py              the runs still open
  ocr/runs-status.py --all        every run ever dispatched
  ocr/runs-status.py --html FILE  same data as a standalone page
  ocr/runs-status.py --escalations only the runs blocked on an answer

## Why this exists

Delegation and escalation are the two halves of the loop: `dispatch-text.sh`
sends work out, and this says what came back. Without it a blocked run is
indistinguishable from a slow one, and the only way to tell is to go reading
logs — which means blocked runs sit unnoticed for exactly as long as nobody
happens to look.

## How state is derived

From files on disk, never from a database that could disagree with them:

  run.log growing and newer than provenance RUNNING
  ESCALATION.md present                     BLOCKED  (waiting on us)

An answered escalation is renamed ESCALATION-answered.md and keeps its ANSWER.md
beside it, so the exchange survives as the record while the run stops reporting
blocked. Only a live ESCALATION.md means somebody is waiting.
  provenance.json present, exit 0           DONE
  provenance.json present, exit non-zero    FAILED

"Growing" means modified in the last few minutes. A run whose log has gone quiet
without provenance is reported STALLED rather than RUNNING, because a machine
that slept mid-run looks exactly like a worker that is thinking, and the
difference matters when deciding whether to wait.

A growing log beats every other signal, and that ordering is the whole point.
Provenance, escalations and adoption records are all written when a run STOPS,
so after a re-dispatch they describe the attempt before this one. The comparison
is which file is newer: a log younger than the provenance beside it means an
attempt is under way that nothing on disk yet describes.

## Closed runs are hidden

By default this prints only what is still open, because a dashboard that also
prints months of finished work stops being read. A run is closed when it has
been adopted -- `adopt-run.py` stamps the provenance -- or when a `CLOSED.md` in
the run directory says why it was set aside without adoption. Nothing is
deleted: the run directories are the record, and `--all` shows every one.

`CLOSED.md` is freeform and its content is never parsed, only its first line is
shown. Writing one is how a superseded or abandoned run stops asking for
attention; deleting it reopens the run.

## Resuming

A blocked run is resumed with its session id, which the dispatcher records in
provenance.json for this purpose:

    codex exec resume <session-id> "your answer"

The worker restarts with its context intact, so an escalation costs a reply
rather than a re-run.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_manifest import output_candidates  # noqa: E402

# Seconds of log silence before RUNNING becomes STALLED. 300 was too eager:
# codex logs in bursts and goes quiet for longer than five minutes while
# working, so a live Einstein run was reported STALLED twice while its
# process was demonstrably alive. Runs so far have taken 13-44 minutes, so
# a quarter of an hour of silence is the first point worth remarking on.
QUIET_AFTER = 900


TERMINAL = ("ADOPTED", "CLOSED")


def first_line(path: Path) -> str:
    for line in path.read_text(errors="replace").splitlines():
        if line.strip() and not line.startswith("#"):
            return line.strip()[:60]
    return ""


def state_of(run: Path) -> tuple[str, str]:
    """Returns (state, detail). Derived from files, never asserted."""
    prov = run / "provenance.json"
    esc = run / "ESCALATION.md"
    log = run / "run.log"
    closed = run / "CLOSED.md"

    # Closed states come first, and CLOSED before ADOPTED: a run set aside by
    # hand is set aside whatever else its files say, including an escalation
    # nobody intends to answer.
    if closed.exists():
        return "CLOSED", first_line(closed) or "see CLOSED.md"

    # A live log OUTRANKS every record of a previous attempt, because every one
    # of those records is written when a run ENDS. Re-dispatching a text leaves
    # the old provenance, escalation and adoption in place until the new attempt
    # finishes, so the dashboard confidently described four actively running
    # texts by what had happened to them days earlier: two showed FAILED with an
    # exit code from an attempt that had already been superseded.
    #
    # The discriminator is which file is newer. dispatch-text.sh and
    # resume-run.sh both append to run.log throughout and write provenance.json
    # only at the end, so a log younger than the provenance beside it means a
    # further attempt is under way that no record yet describes.
    #
    # Being wrong here is worse than being coarse. A dashboard that reports a
    # working run as FAILED invites someone to re-dispatch it on top of itself,
    # and the state it was reporting was, by construction, one attempt stale.
    if log.exists():
        quiet = time.time() - log.stat().st_mtime
        newer = not prov.exists() or log.stat().st_mtime > prov.stat().st_mtime
        if newer and quiet < QUIET_AFTER:
            return "RUNNING", f"log active {int(quiet)}s ago"
        if newer and prov.exists():
            return "STALLED", f"log quiet {int(quiet // 60)}m, newer than provenance"

    if prov.exists():
        try:
            adopted = json.loads(prov.read_text()).get("adopted")
        except json.JSONDecodeError:
            adopted = None
        if adopted:
            return "ADOPTED", f"→ {adopted.get('target', '')}"

    if esc.exists():
        return "BLOCKED", first_line(esc) or "see ESCALATION.md"

    if prov.exists():
        try:
            d = json.loads(prov.read_text())
        except json.JSONDecodeError:
            return "DONE", "provenance unreadable"
        # The LAST attempt decides the state. A failed resume after a successful
        # first run was reported DONE, which hid a broken resume completely.
        resumes = d.get("resumes") or []
        last = resumes[-1] if resumes else d
        rc = last.get("exit_code", 0)
        where = " on resume" if resumes else ""
        if rc != 0:
            return "FAILED", f"exit {rc}{where}"
        # Exit 0 is necessary and not sufficient: codex handles SIGTERM and
        # exits 0, so a run cut off by a sleeping laptop looked exactly like a
        # finished one. `completed` records whether the log ended normally.
        # Runs predating the field are assumed complete rather than retroactively
        # doubted.
        if not last.get("completed", True):
            return "INCOMPLETE", f"cut off mid-work{where}; resumable"
        return "DONE", ""

    if log.exists():
        quiet = time.time() - log.stat().st_mtime
        if quiet < QUIET_AFTER:
            return "RUNNING", f"log active {int(quiet)}s ago"
        return "STALLED", f"log quiet {int(quiet // 60)}m"

    return "EMPTY", "no log, no provenance"


def minutes(prov: dict) -> float | None:
    try:
        t0 = datetime.fromisoformat(prov["started"].replace("Z", "+00:00"))
        t1 = datetime.fromisoformat(prov["finished"].replace("Z", "+00:00"))
        return (t1 - t0).total_seconds() / 60
    except (KeyError, ValueError):
        return None


def collect(root: Path) -> list[dict]:
    rows = []
    runs = root / "ocr" / "runs"
    if not runs.is_dir():
        return rows
    for run in sorted(p for p in runs.iterdir() if p.is_dir()):
        prov = {}
        if (run / "provenance.json").exists():
            try:
                prov = json.loads((run / "provenance.json").read_text())
            except json.JSONDecodeError:
                pass
        state, detail = state_of(run)
        outs = output_candidates(run)
        rows.append({
            "name": run.name,
            "state": state,
            "detail": detail,
            "minutes": minutes(prov),
            "output_kb": max((f.stat().st_size for f in outs), default=0) / 1024,
            "notes_kb": (run / "NOTES.md").stat().st_size / 1024
                        if (run / "NOTES.md").exists() else 0,
            "tools": len(list(run.glob("*.py"))),
            "session_id": prov.get("session_id", ""),
            "model": prov.get("model", ""),
            "path": str(run.relative_to(root)),
        })
    return rows


def print_table(rows: list[dict], only_blocked: bool, show_all: bool) -> None:
    hidden = 0
    if only_blocked:
        rows = [r for r in rows if r["state"] == "BLOCKED"]
    elif not show_all:
        keep = [r for r in rows if r["state"] not in TERMINAL]
        hidden = len(rows) - len(keep)
        rows = keep
    if not rows:
        if only_blocked:
            print("  nothing blocked")
        elif hidden:
            print(f"  nothing open — {hidden} closed run(s) hidden (--all to see them)")
        else:
            print("  no runs")
        return
    print(f"  {'run':44} {'state':8} {'min':>5} {'out KB':>7} {'notes':>6} {'tools':>5}")
    print("  " + "-" * 80)
    for r in rows:
        m = f"{r['minutes']:.0f}" if r["minutes"] is not None else "-"
        print(f"  {r['name'][:44]:44} {r['state']:8} {m:>5} "
              f"{r['output_kb']:7.0f} {r['notes_kb']:6.1f} {r['tools']:5}")
        if r["detail"]:
            print(f"      {r['detail']}")
    if hidden:
        print(f"\n  {hidden} closed run(s) hidden — --all to see them")
    blocked = [r for r in rows if r["state"] == "BLOCKED"]
    for r in blocked:
        print(f"\n  BLOCKED — {r['path']}/ESCALATION.md")
        if r["session_id"] and r["session_id"] != "unknown":
            print(f"    resume:  codex exec resume {r['session_id']} \"<your answer>\"")
        else:
            print("    resume:  session id not recorded; see run.log for 'session id:'")


def write_html(rows: list[dict], path: Path) -> None:
    colour = {"DONE": "#2f6f3e", "BLOCKED": "#9a5b00", "RUNNING": "#26506e",
              "FAILED": "#8c2f2f", "STALLED": "#6b5b2f", "EMPTY": "#666",
              "ADOPTED": "#777", "CLOSED": "#777", "INCOMPLETE": "#8c5a2f"}
    # The page is the archive view and keeps everything, but open work sorts to
    # the top and closed work greys out, so the two halves stay distinguishable
    # without a second file.
    cells = []
    for r in sorted(rows, key=lambda r: (r["state"] in TERMINAL, r["name"])):
        m = f"{r['minutes']:.0f}" if r["minutes"] is not None else "—"
        cells.append(
            f"<tr><td><code>{html.escape(r['name'])}</code>"
            f"{'<div class=d>' + html.escape(r['detail']) + '</div>' if r['detail'] else ''}</td>"
            f"<td><b style='color:{colour.get(r['state'], '#333')}'>{r['state']}</b></td>"
            f"<td class=n>{m}</td><td class=n>{r['output_kb']:.0f}</td>"
            f"<td class=n>{r['notes_kb']:.1f}</td><td class=n>{r['tools']}</td></tr>")
    path.write_text(f"""<!doctype html><meta charset=utf-8>
<title>Enchiridion — dispatch runs</title>
<style>
 body{{font:15px/1.5 Georgia,serif;margin:2.5rem auto;max-width:60rem;padding:0 1rem}}
 table{{border-collapse:collapse;width:100%}}
 th,td{{text-align:left;padding:.5rem .6rem;border-bottom:1px solid #ddd;vertical-align:top}}
 th{{font:600 12px/1.4 ui-monospace,monospace;text-transform:uppercase;letter-spacing:.06em;color:#555}}
 .n{{text-align:right;font:13px ui-monospace,monospace}}
 .d{{font:12px ui-monospace,monospace;color:#777;margin-top:.2rem}}
 code{{font:13px ui-monospace,monospace}}
 p{{color:#666;font-size:13px}}
 @media(prefers-color-scheme:dark){{body{{background:#14140f;color:#e8e4d9}}
   th,td{{border-color:#333}} .d,p,th{{color:#999}}}}
</style>
<h1>Dispatch runs</h1>
<table><tr><th>run<th>state<th>min<th>out KB<th>notes<th>tools</tr>
{''.join(cells)}</table>
<p>Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} by <code>ocr/runs-status.py</code>.
State is derived from files on disk, not stored. Open runs first, then adopted
and closed ones; the terminal shows only the open half.</p>""", encoding="utf-8")
    print(f"  wrote {path}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", metavar="FILE")
    ap.add_argument("--escalations", action="store_true",
                    help="only runs blocked on an answer")
    ap.add_argument("--all", action="store_true",
                    help="include adopted and closed runs")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    rows = collect(root)
    print_table(rows, args.escalations, args.all)
    if args.html:
        write_html(rows, Path(args.html))
    return 1 if any(r["state"] == "BLOCKED" for r in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
