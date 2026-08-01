#!/usr/bin/env bash
# Dispatch one text through the pipeline, and keep the record.
#
#   ocr/dispatch-text.sh <text-id> [model]
#
# This is BOOKKEEPING ONLY. It assembles a workspace, pins provenance, and files
# what comes back under ocr/runs/<text-id>/. It says nothing about how to process
# a text — that is ocr/README.md and the STAGE.md files, which the worker reads
# for itself. Nothing here is per-genre or per-text, because after one run we do
# not know what varies, and guessing is how you get an interface you have to
# unlearn.
#
# It exists because the first run was assembled by hand and the record came out
# wrong twice: artifacts landed in a scratch directory the user could not read,
# and provenance was written by a wrapper that died when the machine slept.
# Comparing runs requires the record to be uniform; hand-assembly puts variation
# in the one place we cannot afford it.
#
# The worker writes only inside workspace/, which sits below the run directory
# and is gitignored. The corpus is readable but outside the sandbox root, so it
# cannot be modified. What matters is copied up to the run directory at the end.

set -euo pipefail

TEXT_ID="${1:?usage: ocr/dispatch-text.sh <text-id> [model]}"
MODEL="${2:-gpt-5.6-sol}"
EFFORT="${EFFORT:-medium}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="$(ls -d "$ROOT"/texts/*/"$TEXT_ID" 2>/dev/null | head -1 || true)"
[ -n "$SRC_DIR" ] || { echo "no text directory for '$TEXT_ID'" >&2; exit 1; }

RUN="$ROOT/ocr/runs/$TEXT_ID"
WORK="$RUN/workspace"
rm -rf "$WORK"; mkdir -p "$WORK/source"

# Sources only. Never the corpus markdown: a worker handed the current .md would
# be reviewing our previous answer instead of reading the source.
find "$SRC_DIR" -maxdepth 1 -type f \
     \( -name '*.pdf' -o -name '*.epub' -o -name '*.txt' -o -name '*.htm*' \
        -o -name 'metadata.json' \) -exec cp {} "$WORK/source/" \;

TITLE=$(python3 -c "import json;m=json.load(open('$SRC_DIR/metadata.json'));print(m.get('title',''))")
AUTHOR=$(python3 -c "import json;m=json.load(open('$SRC_DIR/metadata.json'));print(m.get('author',''))")

cat > "$WORK/TASK.md" <<EOF
# Task

Take one text as far through the Enchiridion pipeline as it will honestly go.

**The text:** $AUTHOR, *$TITLE* (\`$TEXT_ID\`). Its sources are in \`source/\`,
along with the metadata the library currently holds for it.

**Where to start:** \`$ROOT/ocr/README.md\`, then \`$ROOT/ocr/DISPATCH.md\`.
Each stage directory has a \`STAGE.md\` saying what it consumes, what it
produces, what test says it succeeded, and — the useful part — what that test
does not check. There is no brief specific to this text. If those documents
leave you guessing, that is a fact about them worth reporting.

**Where you may write:** this workspace. The repository is readable, and its
tools, precedents in \`ocr/text-specific-tools/\`, and documentation are yours to
use. Use \`$ROOT/ocr/.venv/bin/python3\` where PyMuPDF is needed.

**What the checks are for.** The diagnostic triad asks whether a renderer can
handle the notation — so it is informative exactly to the degree the text
contains notation, and says nothing about whether the words are the right words.
Most checks here answer a narrower question than their name suggests. Reading
what a check actually asks is worth more than running it.

**What we want besides the text.** Keep \`NOTES.md\`. The processing is the
smaller half of this; the larger half is what the attempt teaches about the
pipeline. Worth recording: where the documentation was wrong, missing, or
contradicted what you found; what you decided and on what evidence; what you
could not settle and why; anything true beyond this one text.

A stage left undone with a clear account of what blocked it is a good outcome.
So is a decision made on stated evidence. What is not useful is a silent guess,
because nothing downstream can catch one.
EOF

mkdir -p "$RUN"
START=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "dispatching $TEXT_ID  [$MODEL, effort=$EFFORT]"

set +e
( cd "$WORK" && codex exec \
    --sandbox workspace-write \
    --skip-git-repo-check \
    -m "$MODEL" \
    -c model_reasoning_effort="\"$EFFORT\"" \
    -c mcp_servers='{}' \
    "$(cat TASK.md)" < /dev/null ) > "$RUN/run.log" 2>&1
RC=$?
set -e
END=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Provenance is written HERE, not by whatever called this, so a caller that dies
# does not take the record with it.
cat > "$RUN/provenance.json" <<EOF
{
  "text_id": "$TEXT_ID",
  "model": "$MODEL",
  "reasoning_effort": "$EFFORT",
  "codex_cli": "$(codex --version 2>/dev/null || echo unknown)",
  "repo_head": "$(git -C "$ROOT" rev-parse --short HEAD)",
  "started": "$START",
  "finished": "$END",
  "exit_code": $RC
}
EOF

# Lift the record out of the disposable workspace.
cp "$WORK/TASK.md" "$RUN/" 2>/dev/null || true
[ -f "$WORK/NOTES.md" ] && cp "$WORK/NOTES.md" "$RUN/" || echo "  NO NOTES.md — the run reported nothing about itself" >&2
find "$WORK" -maxdepth 1 -name '*.md' ! -name 'TASK.md' ! -name 'NOTES.md' \
     -exec cp {} "$RUN/" \; 2>/dev/null || true
find "$WORK/ocr" -name '*.py' -exec cp {} "$RUN/" \; 2>/dev/null || true

echo "  exit $RC → ocr/runs/$TEXT_ID/"
ls -1 "$RUN" | sed 's/^/    /'
