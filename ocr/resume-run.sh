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

RUN_DIR="${1:?usage: ocr/resume-run.sh <run-dir> \"answer\" | --answer-file FILE}"
shift
if [ "${1:-}" = "--answer-file" ]; then
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
  find "$SRC_DIR" -maxdepth 1 -type f ! -name '*.md' -exec cp -n {} "$WORK/source/" \; 2>/dev/null || true
  after=$(ls -1 "$WORK/source" 2>/dev/null | wc -l | tr -d ' ')
  [ "$after" -gt "$before" ] && echo "  source/ gained $((after - before)) file(s) since dispatch"
fi

# Clear the OLD escalation from the workspace before resuming, so that anything
# found there afterwards is necessarily a new one. Doing this after the run
# instead deleted a freshly written second escalation, and then tested for it.
rm -f "$WORK/ESCALATION.md"

printf '%s\n' "$ANSWER" > "$WORK/ANSWER.md"
cp "$WORK/ANSWER.md" "$RUN/ANSWER.md"

PROMPT="Your escalation has been answered.

$ANSWER

The answer is also in ANSWER.md in your workspace, and source/ has been re-synced
in case it now holds a file you asked for. Carry on from where you stopped, under
the same instructions in TASK.md. If the answer raises a further question you
should not decide, write a new ESCALATION.md and finish again."

echo "resuming $(basename "$RUN")  [$MODEL, effort=$EFFORT, session ${SESSION:0:8}…]"
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

python3 - "$PROV" "$START" "$END" "$RC" <<'PY'
import json, sys
prov_path, start, end, rc = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
d = json.load(open(prov_path))
d.setdefault("resumes", []).append({"started": start, "finished": end, "exit_code": rc})
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
if [ $RC -eq 0 ]; then
  mkdir -p "$RUN/escalations"
  N=$(printf "%02d" $(( $(ls "$RUN/escalations"/*-escalation.md 2>/dev/null | wc -l) + 1 )))
  [ -f "$RUN/ESCALATION.md" ] && mv "$RUN/ESCALATION.md" "$RUN/escalations/$N-escalation.md"
  [ -f "$RUN/ANSWER.md" ] && mv "$RUN/ANSWER.md" "$RUN/escalations/$N-answer.md"
  echo "  archived exchange $N → escalations/"
else
  echo "  resume FAILED (exit $RC) — escalation left open" >&2
fi
[ -f "$WORK/NOTES.md" ] && cp "$WORK/NOTES.md" "$RUN/"
find "$WORK" -maxdepth 1 -name '*.md' ! -name 'TASK.md' ! -name 'NOTES.md' \
     ! -name 'ANSWER.md' -exec cp {} "$RUN/" \; 2>/dev/null || true
find "$WORK" -name '*.py' -not -path "$WORK/source/*" \
     -exec cp {} "$RUN/" \; 2>/dev/null || true
[ -f "$WORK/ESCALATION.md" ] && cp "$WORK/ESCALATION.md" "$RUN/" && \
  echo "  ESCALATED AGAIN — see $RUN/ESCALATION.md"

echo "  exit $RC → ${RUN#$ROOT/}/"
ls -1 "$RUN" | sed 's/^/    /'
