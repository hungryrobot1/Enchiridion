#!/usr/bin/env bash
# Dispatch one proofreading batch to Codex, and record who did it.
#
#   ocr/4-proofread/dispatch-codex.sh <batch-dir> [model]
#
# Findings without provenance are half a record. This directory exists so a
# judgement made once stays legible later, and "the page shows Pisces" means
# something different coming from a strong model at high effort than from a
# cheap one — especially when we start comparing runs, or re-reading a stretch
# after revising the brief. So the model and effort are PINNED here rather than
# inherited from ~/.codex/config.toml, which can change under us, and they are
# written next to the findings.
#
# Notes on the flags, each of which was learned the hard way:
#
#   --sandbox workspace-write  The worker corrects edit/slice.md in place, so it
#                          needs write access to the BATCH — which is disposable
#                          and gitignored. It cannot reach the real text: the
#                          batch holds only a slice, and the real file is outside
#                          the sandbox root. Reference copies are protected by
#                          DETECTION rather than prevention — their hashes are
#                          recorded below and checked by verify-batch.py.
#   -o result.json         READ THIS FILE, never stdout. The streamed output
#                          includes intermediate drafts — our first run emitted a
#                          placeholder finding with empty fields before the real
#                          answer, and a stdout parser would have taken it.
#   --output-schema        Makes findings structurally valid rather than politely
#                          requested; a worker cannot return malformed records.
#   < /dev/null            codex exec reads stdin even when the prompt is an
#                          argument. Without this a backgrounded run hangs on
#                          "Reading additional input from stdin..." forever, and
#                          at fan-out scale every job hangs silently.
#   -c mcp_servers=...     The user's Codex can reach the Enchiridion MCP, i.e.
#                          the whole corpus. A proofreader needs the batch in
#                          front of it and nothing else.
#
# TWO RETURN SHAPES, selected by MODE, because which one is better is an open
# question and the only honest way to settle it is to run the same pages both
# ways and compare:
#
#   MODE=schema (default)  findings as schema-bound JSON + the edited slice.
#   MODE=prose             the edited slice + notes.md, a dialogic account. The
#                          diff already localises every change perfectly, so the
#                          schema's remaining contribution is the REASON — and
#                          prose carries a reason better than a field does. It
#                          also has room for the two things no schema elicited:
#                          an observation nobody asked for, and a QUESTION.
set -euo pipefail

BATCH="${1:?usage: dispatch-codex.sh <batch-dir> [model]}"
MODEL="${2:-gpt-5.6-sol}"
EFFORT="${EFFORT:-medium}"   # the pilot ran at medium and every finding
                             # verified correct; high is unproven spend.
                             # Override per-run: EFFORT=high dispatch-codex.sh ...
MODE="${MODE:-schema}"       # schema | prose

BATCH="$(cd "$BATCH" && pwd)"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCHEMA="$ROOT/findings-schema.json"

# Refresh the brief from source. prepare-batch.py copies it at creation time, so
# a batch prepared before a revision would run against the OLD brief and the
# revision would silently never reach the worker — which happened, and made one
# run's results uninterpretable. Copy at dispatch, when it is actually read.
TEXT_ID="$(python3 -c "import json,sys;print(json.load(open('$BATCH/MANIFEST.json'))['text_id'])")"
SRC_BRIEF="$ROOT/$TEXT_ID/brief.md"
[ -f "$SRC_BRIEF" ] && cp "$SRC_BRIEF" "$BATCH/BRIEF.md"
[ -f "$BATCH/BRIEF.md" ]    || { echo "no BRIEF.md in $BATCH"; exit 1; }
[ -f "$BATCH/markdown.md" ] || { echo "no markdown.md in $BATCH"; exit 1; }

# Portable array fill: macOS ships bash 3.2, which has no `mapfile`.
IMAGES=()
for f in "$BATCH"/pages/*.png; do
  [ -e "$f" ] && IMAGES+=("$f")
done
[ "${#IMAGES[@]}" -gt 0 ] || { echo "no page images in $BATCH/pages"; exit 1; }

read -r -d '' PROMPT_COMMON <<'EOF' || true
You are proofreading a scanned scholarly book against its OCR transcription.

Read BRIEF.md in this directory first — it explains the text, the known error
families, and what NOT to report. Then read markdown.md, which is the
transcription, prefixed with real line numbers from the source file. The page
images are attached.

Compare the pages against the markdown and report every disagreement, following
the brief. Work through the pages one at a time and do not stop early.
EOF

read -r -d '' PROMPT_SCHEMA <<'EOF' || true

Return findings TWO ways, and make them agree:

1. Correct edit/slice.md in place. Change only what the page disagrees with.
   Leave BRIEF.md and markdown.md untouched — markdown.md is reference only.
2. Return the JSON structure required by the output schema, one record per
   occurrence, including a record for every page (claim "clean" where you find
   nothing).

Every edit you make must have a matching finding explaining it, and every
finding claiming an error must appear as an edit. An edit with no finding is an
unexplained change and will be rejected.
EOF

read -r -d '' PROMPT_PROSE <<'EOF' || true

Return your work TWO ways.

1. Correct edit/slice.md in place. Change only what the page actually
   disagrees with. Leave BRIEF.md and markdown.md untouched — markdown.md is
   reference only. We diff this file against the original, so the diff already
   records exactly WHERE every change is. You do not need to tell us that.

2. Write notes.md: an account, in prose, of what you did and what you saw.

What notes.md is for. The diff says where; it cannot say why, and the why is
what lets one decision settle a whole family of errors later instead of being
re-argued page by page. So write to a colleague who will read the diff beside
your notes. Cover, in whatever order the work suggests:

  * The reasoning behind your corrections. Group them however they actually
    group — by family, by page, by shared argument. Do not enumerate one
    paragraph per changed character. Where a correction rests on something
    checkable — a glyph's shape, a footnote that glosses it, an arithmetic
    identity — say so and show it, because we can verify those independently.
  * How sure you are, and where you are not. A correction you would defend and
    a correction you guessed at must be distinguishable. If you cannot tell
    which of two readings the page shows, say that instead of choosing.
  * Anything you noticed that the brief does not describe. This is the most
    valuable thing you can send back. The brief's families were found by
    pattern-matching over the whole text, which is structurally blind to an
    error that occurs once. You are reading actual pages, so you can see those.
  * Anything the brief gets wrong, or leaves ambiguous enough that you had to
    guess what we wanted.
  * QUESTIONS. If something on these pages cannot be settled by looking harder
    — a convention we never explained, a passage where two readings are both
    defensible, a case where the brief's rule and the page disagree — ask.
    Write the question plainly and leave the text alone. An asked question is
    worth more to us than a confident guess, and previous runs asked none at
    all, which we do not believe reflects how clear these pages are.

Every change in the diff should be traceable to something in notes.md. A change
we cannot find an argument for gets reverted.
EOF

case "$MODE" in
  schema) PROMPT="$PROMPT_COMMON$PROMPT_SCHEMA"
          CODEX_OUT=(--output-schema "$SCHEMA" -o result.json) ;;
  prose)  PROMPT="$PROMPT_COMMON$PROMPT_PROSE"
          CODEX_OUT=(-o summary.md) ;;
  *)      echo "MODE must be schema or prose (got '$MODE')"; exit 1 ;;
esac

# Clear the previous run's outputs first. Otherwise a re-run in progress looks
# exactly like a finished one — provenance.json is written last, so its presence
# reads as completion even when it is a leftover.
rm -f "$BATCH/result.json" "$BATCH/provenance.json" "$BATCH/run.log" \
      "$BATCH/notes.md" "$BATCH/summary.md"

# Recorded before the run: the reference copy must come back untouched.
REF_SHA="$(git hash-object "$BATCH/markdown.md")"

echo "dispatching ${#IMAGES[@]} pages from $(basename "$BATCH")  [$MODEL, effort=$EFFORT, mode=$MODE]"
START=$(date -u +%Y-%m-%dT%H:%M:%SZ)

( cd "$BATCH" && codex exec \
    --sandbox workspace-write \
    --skip-git-repo-check \
    -m "$MODEL" \
    -c model_reasoning_effort="\"$EFFORT\"" \
    -c mcp_servers='{}' \
    -i "${IMAGES[@]}" \
    "${CODEX_OUT[@]}" \
    "$PROMPT" < /dev/null ) > "$BATCH/run.log" 2>&1

END=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TOKENS=$(grep -oE '^[0-9,]+$' "$BATCH/run.log" | tail -1 || true)

cat > "$BATCH/provenance.json" <<EOF
{
  "batch": "$(basename "$BATCH")",
  "model": "$MODEL",
  "reasoning_effort": "$EFFORT",
  "mode": "$MODE",
  "codex_cli": "$(codex --version)",
  "pages": ${#IMAGES[@]},
  "started": "$START",
  "finished": "$END",
  "tokens_reported": "${TOKENS:-unknown}",
  "brief_sha": "$(git hash-object "$BATCH/BRIEF.md")",
  "schema_sha": "$([ "$MODE" = schema ] && git hash-object "$SCHEMA" || echo n/a)",
  "reference_sha_after": "$(git hash-object "$BATCH/markdown.md")",
  "reference_sha_before": "$REF_SHA"
}
EOF

if [ "$MODE" = schema ]; then
  echo "  result.json      $(python3 -c "import json;print(len(json.load(open('$BATCH/result.json'))['findings']))" 2>/dev/null || echo '??') findings"
else
  echo "  notes.md         $(wc -w < "$BATCH/notes.md" 2>/dev/null || echo '??') words"
fi
echo "  provenance.json  $MODEL / $EFFORT / $MODE"
echo "  run.log          full transcript"
if [ "$REF_SHA" != "$(git hash-object "$BATCH/markdown.md")" ]; then
  echo "  !! markdown.md was MODIFIED during the run; it is reference only"
fi
echo
echo "next:  ocr/4-proofread/verify-batch.py $BATCH"
