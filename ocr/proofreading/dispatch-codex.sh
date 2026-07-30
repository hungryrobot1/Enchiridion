#!/usr/bin/env bash
# Dispatch one proofreading batch to Codex, and record who did it.
#
#   ocr/proofreading/dispatch-codex.sh <batch-dir> [model]
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
set -euo pipefail

BATCH="${1:?usage: dispatch-codex.sh <batch-dir> [model]}"
MODEL="${2:-gpt-5.6-sol}"
EFFORT="${EFFORT:-medium}"   # the pilot ran at medium and every finding
                             # verified correct; high is unproven spend.
                             # Override per-run: EFFORT=high dispatch-codex.sh ...

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

read -r -d '' PROMPT <<'EOF' || true
You are proofreading a scanned scholarly book against its OCR transcription.

Read BRIEF.md in this directory first — it explains the text, the known error
families, and what NOT to report. Then read markdown.md, which is the
transcription, prefixed with real line numbers from the source file. The page
images are attached.

Compare the pages against the markdown and report every disagreement, following
the brief. Work through the pages one at a time and do not stop early.

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

# Clear the previous run's outputs first. Otherwise a re-run in progress looks
# exactly like a finished one — provenance.json is written last, so its presence
# reads as completion even when it is a leftover.
rm -f "$BATCH/result.json" "$BATCH/provenance.json" "$BATCH/run.log"

# Recorded before the run: the reference copy must come back untouched.
REF_SHA="$(git hash-object "$BATCH/markdown.md")"

echo "dispatching ${#IMAGES[@]} pages from $(basename "$BATCH")  [$MODEL, effort=$EFFORT]"
START=$(date -u +%Y-%m-%dT%H:%M:%SZ)

( cd "$BATCH" && codex exec \
    --sandbox workspace-write \
    --skip-git-repo-check \
    -m "$MODEL" \
    -c model_reasoning_effort="\"$EFFORT\"" \
    -c mcp_servers='{}' \
    -i "${IMAGES[@]}" \
    --output-schema "$SCHEMA" \
    -o result.json \
    "$PROMPT" < /dev/null ) > "$BATCH/run.log" 2>&1

END=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TOKENS=$(grep -oE '^[0-9,]+$' "$BATCH/run.log" | tail -1 || true)

cat > "$BATCH/provenance.json" <<EOF
{
  "batch": "$(basename "$BATCH")",
  "model": "$MODEL",
  "reasoning_effort": "$EFFORT",
  "codex_cli": "$(codex --version)",
  "pages": ${#IMAGES[@]},
  "started": "$START",
  "finished": "$END",
  "tokens_reported": "${TOKENS:-unknown}",
  "brief_sha": "$(git hash-object "$BATCH/BRIEF.md")",
  "schema_sha": "$(git hash-object "$SCHEMA")",
  "reference_sha_after": "$(git hash-object "$BATCH/markdown.md")",
  "reference_sha_before": "$REF_SHA"
}
EOF

echo "  result.json      $(python3 -c "import json;print(len(json.load(open('$BATCH/result.json'))['findings']))" 2>/dev/null || echo '??') findings"
echo "  provenance.json  $MODEL / $EFFORT"
echo "  run.log          full transcript"
if [ "$REF_SHA" != "$(git hash-object "$BATCH/markdown.md")" ]; then
  echo "  !! markdown.md was MODIFIED during the run; it is reference only"
fi
echo
echo "next:  ocr/proofreading/verify-batch.py $BATCH"
