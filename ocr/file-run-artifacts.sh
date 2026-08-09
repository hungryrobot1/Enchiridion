#!/usr/bin/env bash
# Lift what a worker left in workspace/ up into the run directory.
#
#   ocr/file-run-artifacts.sh <run-dir> [--answer-file FILE]
#
# The worker writes only inside workspace/, which is gitignored. Everything that
# matters -- the notes, the proposal, the tools it built, the images it produced
# or corrected -- has to be copied up, or the run's record is a directory with a
# stale escalation in it and nothing else.
#
# This lived inside resume-run.sh until 2026-08-09, when a resume was issued by
# calling `codex exec resume` directly. The worker finished the work correctly;
# the filing never happened, so the dashboard went on reporting BLOCKED on a
# question that had been answered and the artifacts sat in a gitignored
# directory. The copy-up is not part of resuming, it is part of *finishing*, so
# it belongs somewhere both paths can reach.
#
# Losing work to a filing rule is the failure this pipeline keeps repeating:
# dispatch copied only top-level files until saved-page assets went missing;
# resume lacked the source/ rescue until al-Biruni nearly stranded 667 KB. Same
# shape each time, which is the argument for one implementation.

set -euo pipefail

RUN="${1:?usage: ocr/file-run-artifacts.sh <run-dir> [--answer-file FILE]}"
RUN="$(cd "$RUN" && pwd)"
WORK="$RUN/workspace"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEXT_ID="$(basename "$RUN")"
SRC_DIR="$(ls -d "$ROOT"/texts/*/"$TEXT_ID" 2>/dev/null | head -1 || true)"

ANSWER_FILE=""
[ "${2:-}" = "--answer-file" ] && ANSWER_FILE="${3:?--answer-file needs a path}"

[ -d "$WORK" ] || { echo "no workspace under $RUN" >&2; exit 1; }

[ -f "$WORK/NOTES.md" ] && cp "$WORK/NOTES.md" "$RUN/"
# Everything the worker left, not an extension list -- see dispatch-text.sh.
find "$WORK" -maxdepth 1 -type f ! -name 'TASK.md' ! -name 'ANSWER.md' \
     -exec cp {} "$RUN/" \; 2>/dev/null || true
find "$WORK" \( -name '*.py' -o -name '*.sh' \) -not -path "$WORK/source/*" \
     -exec cp {} "$RUN/" \; 2>/dev/null || true
[ -d "$WORK/controls" ] && cp -R "$WORK/controls" "$RUN/" 2>/dev/null || true
[ -d "$WORK/images" ] && cp -R "$WORK/images" "$RUN/" 2>/dev/null || true

# Markdown left in source/ is work. See resume-run.sh's note on al-Biruni.
if [ -d "$WORK/source" ] && [ -n "$SRC_DIR" ]; then
  for f in "$WORK/source"/*.md; do
    [ -e "$f" ] || continue
    orig="$SRC_DIR/$(basename "$f")"
    if [ ! -f "$orig" ] || ! cmp -s "$f" "$orig"; then
      cp "$f" "$RUN/" && echo "  rescued $(basename "$f") from source/" >&2
    fi
  done
  if [ -d "$WORK/source/images" ]; then
    mkdir -p "$RUN/images"
    cp -Rn "$WORK/source/images"/* "$RUN/images/" 2>/dev/null || true
  fi
fi

# An escalation the worker deleted has been answered; archive the exchange so
# the reasoning survives, and stop the dashboard reporting a resolved question.
if [ ! -f "$WORK/ESCALATION.md" ] && [ -f "$RUN/ESCALATION.md" ]; then
  mkdir -p "$RUN/escalations"
  N=$(printf "%02d" $(( $(ls "$RUN/escalations"/*-escalation.md 2>/dev/null | wc -l) + 1 )))
  mv "$RUN/ESCALATION.md" "$RUN/escalations/$N-escalation.md"
  if [ -n "$ANSWER_FILE" ] && [ -f "$ANSWER_FILE" ]; then
    cp "$ANSWER_FILE" "$RUN/escalations/$N-answer.md"
  elif [ -f "$RUN/ANSWER.md" ]; then
    mv "$RUN/ANSWER.md" "$RUN/escalations/$N-answer.md"
  fi
  echo "  archived exchange $N → escalations/"
elif [ -f "$WORK/ESCALATION.md" ]; then
  cp "$WORK/ESCALATION.md" "$RUN/"
  echo "  ESCALATED AGAIN — see $RUN/ESCALATION.md"
fi

echo "  filed → ${RUN#$ROOT/}/"
