#!/usr/bin/env python3
"""What every dispatch run is doing, and which ones are waiting on us.

  ocr/runs-status.py              table on stdout
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

  provenance.json absent, run.log growing   RUNNING
  ESCALATION.md present                     BLOCKED  (waiting on us)
  provenance.json present, exit 0           DONE
  provenance.json present, exit non-zero    FAILED

"Growing" means modified in the last few minutes. A run whose log has gone quiet
without provenance is reported STALLED rather than RUNNING, because a machine
that slept mid-run looks exactly like a worker that is thinking, and the
difference matters when deciding whether to wait.

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
import time
from datetime import datetime
from pathlib import Path

QUIET_AFTER = 300  # seconds without a log write before RUNNING becomes STALLED


def state_of(run: Path) -> tuple[str, str]:
    """Returns (state, detail). Derived from files, never asserted."""
    prov = run / "provenance.json"
    esc = run / "ESCALATION.md"
    log = run / "run.log"

    if esc.exists():
        first = ""
        for line in esc.read_text(errors="replace").splitlines():
            if line.strip() and not line.startswith("#"):
                first = line.strip()[:60]
                break
        return "BLOCKED", first or "see ESCALATION.md"

    if prov.exists():
        try:
            rc = json.loads(prov.read_text()).get("exit_code", 0)
        except json.JSONDecodeError:
            return "DONE", "provenance unreadable"
        return ("DONE", "") if rc == 0 else ("FAILED", f"exit {rc}")

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
        outs = [f for f in run.glob("*.md")
                if f.name not in ("NOTES.md", "TASK.md", "ESCALATION.md")]
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


def print_table(rows: list[dict], only_blocked: bool) -> None:
    if only_blocked:
        rows = [r for r in rows if r["state"] == "BLOCKED"]
    if not rows:
        print("  no runs" if not only_blocked else "  nothing blocked")
        return
    print(f"  {'run':44} {'state':8} {'min':>5} {'out KB':>7} {'notes':>6} {'tools':>5}")
    print("  " + "-" * 80)
    for r in rows:
        m = f"{r['minutes']:.0f}" if r["minutes"] is not None else "-"
        print(f"  {r['name'][:44]:44} {r['state']:8} {m:>5} "
              f"{r['output_kb']:7.0f} {r['notes_kb']:6.1f} {r['tools']:5}")
        if r["detail"]:
            print(f"      {r['detail']}")
    blocked = [r for r in rows if r["state"] == "BLOCKED"]
    for r in blocked:
        print(f"\n  BLOCKED — {r['path']}/ESCALATION.md")
        if r["session_id"] and r["session_id"] != "unknown":
            print(f"    resume:  codex exec resume {r['session_id']} \"<your answer>\"")
        else:
            print("    resume:  session id not recorded; see run.log for 'session id:'")


def write_html(rows: list[dict], path: Path) -> None:
    colour = {"DONE": "#2f6f3e", "BLOCKED": "#9a5b00", "RUNNING": "#26506e",
              "FAILED": "#8c2f2f", "STALLED": "#6b5b2f", "EMPTY": "#666"}
    cells = []
    for r in rows:
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
State is derived from files on disk, not stored.</p>""", encoding="utf-8")
    print(f"  wrote {path}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", metavar="FILE")
    ap.add_argument("--escalations", action="store_true",
                    help="only runs blocked on an answer")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    rows = collect(root)
    print_table(rows, args.escalations)
    if args.html:
        write_html(rows, Path(args.html))
    return 1 if any(r["state"] == "BLOCKED" for r in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
