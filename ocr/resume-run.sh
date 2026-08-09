#!/usr/bin/env bash
# Answer a blocked run and let it carry on.
#
#   ocr/resume-run.sh <run-dir> "your answer"
#   ocr/resume-run.sh <run-dir> --answer-file FILE
#
# A worker that hits a question it should not decide writes ESCALATION.md and
# finishes, rather than holding a process open waiting for us. This restarts it
# with `codex exec resume`, so it comes back with its context intact and an
# answer, and an escalation costs a reply rather than a re-run.
#
# Bookkeeping only, like dispatch-text.sh. It carries no opinion about the
# answer; it just makes sure the answer reaches the worker and the exchange
# survives in the record.
#
# Before resuming it re-syncs the workspace's source/ from the text directory,
# because the commonest answer to an escalation is a file the worker did not
# have -- Dedekind and Einstein both stopped for a missing TeX source. An answer
# that says "the TeX is there now" is useless if the workspace was assembled
# before it existed.
#
# Answered exchanges are archived, never deleted, as numbered pairs under
# escalations/: 01-escalation.md beside 01-answer.md. Only a LIVE ESCALATION.md
# at the top level means blocked, so the dashboard clears once answered while the
# exchange survives. That record is the learning signal this loop exists for.

set -euo pipefail

RUN_DIR="${1:?usage: ocr/resume-run.sh <run-dir> \"answer\" | --answer-file FILE | --interrupted}"
shift
# --interrupted restarts a run that was cut off rather than one that asked a
# question. A sleeping laptop leaves codex parked on a half-open socket; the
# process must be killed, and what it needs afterwards is not an answer. Sending
# it "your escalation has been answered" would be a lie about its own history,
# and the exchange must NOT be archived as an escalation, because none occurred.
INTERRUPTED=false
if [ "${1:-}" = "--interrupted" ]; then
  INTERRUPTED=true
  ANSWER=""
elif [ "${1:-}" = "--answer-file" ]; then
  ANSWER="$(cat "${2:?--answer-file needs a path}")"
else
  ANSWER="${1:?an answer is required}"
fi

RUN="$(cd "$RUN_DIR" && pwd)"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="$RUN/workspace"
[ -d "$WORK" ] || { echo "no workspace in $RUN — nothing to resume" >&2; exit 1; }

PROV="$RUN/provenance.json"
[ -f "$PROV" ] || { echo "no provenance.json — cannot find the session" >&2; exit 1; }
SESSION="$(python3 -c "import json;print(json.load(open('$PROV')).get('session_id',''))")"
[ -n "$SESSION" ] && [ "$SESSION" != "unknown" ] || {
  echo "no session id recorded; this run cannot be resumed" >&2; exit 1; }
MODEL="$(python3 -c "import json;print(json.load(open('$PROV')).get('model','gpt-5.6-sol'))")"
EFFORT="$(python3 -c "import json;print(json.load(open('$PROV')).get('reasoning_effort','medium'))")"
TEXT_ID="$(python3 -c "import json;d=json.load(open('$PROV'));print(d.get('text_id') or d.get('text',''))")"

# Re-sync sources: the answer is often a file that did not exist at dispatch.
SRC_DIR="$(ls -d "$ROOT"/texts/*/"$TEXT_ID" 2>/dev/null | head -1 || true)"
if [ -n "$SRC_DIR" ]; then
  before=$(ls -1 "$WORK/source" 2>/dev/null | wc -l | tr -d ' ')
  # Honour the run's own repair flag, or the re-sync would quietly re-impose the
  # extraction-job exclusion on a repair job and withhold the very file it is
  # about. cp -n throughout: source/ is the pristine copy and the worker's
  # working files live elsewhere, but never overwrite what is already there.
  REPAIR_RUN="$(python3 -c "import json;print(json.load(open('$PROV')).get('repair',False))")"
  if [ "$REPAIR_RUN" = "True" ]; then
    find "$SRC_DIR" -maxdepth 1 -type f -exec cp -n {} "$WORK/source/" \; 2>/dev/null || true
  else
    find "$SRC_DIR" -maxdepth 1 -type f ! -name '*.md' -exec cp -n {} "$WORK/source/" \; 2>/dev/null || true
  fi
  # See dispatch-text.sh: `-type f` never carried the text's images/ across, so
  # every image reference in a repair job's markdown resolved to nothing.
  # Every subdirectory, not just one named `images/` -- see dispatch-text.sh:
  # a saved web page keeps its assets in `<page>_files/`, and naming `images/`
  # is a whitelist that silently drops any other layout.
  find "$SRC_DIR" -mindepth 1 -maxdepth 1 -type d \
    -exec cp -Rn {} "$WORK/source/" \; 2>/dev/null || true
  after=$(ls -1 "$WORK/source" 2>/dev/null | wc -l | tr -d ' ')
  [ "$after" -gt "$before" ] && echo "  source/ gained $((after - before)) file(s) since dispatch"
fi

# Clear the OLD escalation from the workspace before resuming, so that anything
# found there afterwards is necessarily a new one. Doing this after the run
# instead deleted a freshly written second escalation, and then tested for it.
rm -f "$WORK/ESCALATION.md"

if [ "$INTERRUPTED" = true ]; then
  PROMPT="Your run was cut off part-way through. Nothing was wrong with the work:
the machine this was running on went to sleep, the connection died, and the
process had to be killed. You did not fail and you did not ask a question.

Everything you had written to the workspace is still there. Take a moment to
read back what you had done -- your own notes and files are the record, since
your last few actions may not have completed -- and carry on from where you
stopped, under the same instructions in TASK.md.

If anything you were part-way through was left in an inconsistent state, say so
in NOTES.md rather than assuming it completed."
else
  printf '%s\n' "$ANSWER" > "$WORK/ANSWER.md"
  cp "$WORK/ANSWER.md" "$RUN/ANSWER.md"

  PROMPT="Your escalation has been answered.

$ANSWER

The answer is also in ANSWER.md in your workspace, and source/ has been re-synced
in case it now holds a file you asked for. Carry on from where you stopped, under
the same instructions in TASK.md. If the answer raises a further question you
should not decide, write a new ESCALATION.md and finish again."
fi

echo "resuming $(basename "$RUN")  [$MODEL, effort=$EFFORT, session ${SESSION:0:8}…]"
[ "$INTERRUPTED" = true ] && echo "  (restart after interruption — no escalation to archive)"
MARKERS_BEFORE=$(grep -ac "tokens used" "$RUN/run.log" || true)
START=$(date -u +%Y-%m-%dT%H:%M:%SZ)
set +e
# `codex exec resume` does NOT accept --sandbox at all -- that flag belongs to
# `codex exec` alone -- so the sandbox goes through -c sandbox_mode instead.
# Options also come before the session id here. Getting either wrong produces an
# instant exit 2 that, until the dashboard was taught to read the last attempt,
# looked exactly like a completed run.
( cd "$WORK" && codex exec resume \
    -c sandbox_mode='"workspace-write"' \
    --skip-git-repo-check \
    -m "$MODEL" \
    -c model_reasoning_effort="\"$EFFORT\"" \
    -c mcp_servers='{}' \
    "$SESSION" "$PROMPT" < /dev/null ) >> "$RUN/run.log" 2>&1
RC=$?
set -e
END=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# See dispatch-text.sh: exit 0 does not mean the turn ended, because codex exits
# 0 on SIGTERM. Each resume appends its own "tokens used" marker, so the count
# rising across this attempt is what says it ran to a natural stop.
MARKERS_AFTER=$(grep -ac "tokens used" "$RUN/run.log" || true)
COMPLETED=false
[ "${MARKERS_AFTER:-0}" -gt "${MARKERS_BEFORE:-0}" ] && COMPLETED=true

python3 - "$PROV" "$START" "$END" "$RC" "$COMPLETED" "$INTERRUPTED" <<'PY'
import json, sys
prov_path, start, end, rc = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
completed, interrupted = sys.argv[5] == "true", sys.argv[6] == "true"
d = json.load(open(prov_path))
d.setdefault("resumes", []).append({
    "started": start, "finished": end, "exit_code": rc,
    "completed": completed, "reason": "interrupted" if interrupted else "escalation",
})
json.dump(d, open(prov_path, "w"), indent=2)
PY

# Archive the exchange as a numbered pair. Only retire it if the resume actually
# ran: a failed resume leaves the question genuinely unanswered, and clearing the
# dashboard while nobody is working on it is worse than leaving it noisy.
#
# One file per run could not survive what actually happened. A single ANSWER.md
# was overwritten by a test reply; a single ESCALATION-answered.md would have
# been overwritten the moment Descartes escalated a second time -- the archival
# mechanism destroying the record it existed to keep. Numbering pairs them and
# keeps the order they occurred in, and `ocr/runs/*/escalations/` then reads as
# one corpus of everything workers could not decide.
if [ "$INTERRUPTED" = true ]; then
  :   # nothing was asked, so there is nothing to archive
elif [ $RC -eq 0 ]; then
  mkdir -p "$RUN/escalations"
  N=$(printf "%02d" $(( $(ls "$RUN/escalations"/*-escalation.md 2>/dev/null | wc -l) + 1 )))
  [ -f "$RUN/ESCALATION.md" ] && mv "$RUN/ESCALATION.md" "$RUN/escalations/$N-escalation.md"
  [ -f "$RUN/ANSWER.md" ] && mv "$RUN/ANSWER.md" "$RUN/escalations/$N-answer.md"
  echo "  archived exchange $N → escalations/"
else
  echo "  resume FAILED (exit $RC) — escalation left open" >&2
fi
[ -f "$WORK/NOTES.md" ] && cp "$WORK/NOTES.md" "$RUN/"
# Everything the worker left, not an extension list -- see dispatch-text.sh.
find "$WORK" -maxdepth 1 -type f ! -name 'TASK.md' ! -name 'ANSWER.md' \
     -exec cp {} "$RUN/" \; 2>/dev/null || true
find "$WORK" \( -name '*.py' -o -name '*.sh' \) -not -path "$WORK/source/*" \
     -exec cp {} "$RUN/" \; 2>/dev/null || true
[ -d "$WORK/controls" ] && cp -R "$WORK/controls" "$RUN/" 2>/dev/null || true
# Images the run produced or corrected.
[ -d "$WORK/images" ] && cp -R "$WORK/images" "$RUN/" 2>/dev/null || true
# The same rescue dispatch-text.sh performs, and for the same reason: markdown
# left in source/ is work, and losing work to a filing rule is the failure this
# pipeline keeps repeating. This copy was missing here while dispatch-text.sh had
# it, so a run that finished via a RESUME could strand its output -- which is now
# most runs. al-Biruni wrote its 667 KB proposed text to source/ and named it in
# PROPOSED.md; the run directory got the proposal and not the text, and the next
# dispatch of that text would have deleted it.
if [ -d "$WORK/source" ]; then
  for f in "$WORK/source"/*.md; do
    [ -e "$f" ] || continue
    orig="$SRC_DIR/$(basename "$f")"
    if [ ! -f "$orig" ] || ! cmp -s "$f" "$orig"; then
      cp "$f" "$RUN/" && echo "  rescued $(basename "$f") from source/" >&2
    fi
  done
  # Images too, and for the same reason. `ocr.py` writes images/ beside the
  # markdown it produces, so an OCR run resynced into source/ leaves them there.
  # The adopt gate refuses a text whose image references resolve nowhere, which
  # is correct -- but the images existed and were simply never lifted.
  if [ -d "$WORK/source/images" ]; then
    mkdir -p "$RUN/images"
    cp -Rn "$WORK/source/images"/* "$RUN/images/" 2>/dev/null || true
  fi
fi
[ -f "$WORK/ESCALATION.md" ] && cp "$WORK/ESCALATION.md" "$RUN/" && \
  echo "  ESCALATED AGAIN — see $RUN/ESCALATION.md"

echo "  exit $RC → ${RUN#$ROOT/}/"
ls -1 "$RUN" | sed 's/^/    /'
