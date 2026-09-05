#!/usr/bin/env bash
# Dispatch one independent translation pass, and keep the record.
#
#   translation/dispatch-translation.sh <text-id> <pass-number> [model]
#
# Same shape as ocr/dispatch-text.sh and deliberately thinner: assemble a
# workspace, pin provenance, lift what comes back into translation/runs/<id>/.
# The charter is the second heredoc, versioned with the script that sends it.
#
# INDEPENDENCE IS THE CONTROL. The workspace holds the settled original and the
# decisions ledger and nothing else -- never an earlier pass, never the notes
# from one. Two passes that agree are a baseline; where they diverge, a human
# looks. That only means something if the second translator never saw the first.
#
# The run directory is NOT disposable: it already holds the transcription, the
# ledger and earlier passes. Only workspace/ is rebuilt.

set -euo pipefail

TEXT_ID="${1:?usage: translation/dispatch-translation.sh <text-id> <pass-number> [model]}"
PASS="${2:?pass number, e.g. 2}"
MODEL="${3:-gpt-5.6-sol}"
EFFORT="${EFFORT:-medium}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN="$ROOT/translation/runs/$TEXT_ID"
WORK="$RUN/workspace"
WITNESS="$(ls "$RUN"/transcription-pass-*.md 2>/dev/null | head -1 || true)"
[ -n "$WITNESS" ] || { echo "no settled transcription in $RUN" >&2; exit 1; }
[ -f "$RUN/decisions.md" ] || { echo "no decisions.md in $RUN" >&2; exit 1; }
OUT="translation-pass-$PASS.md"
[ ! -f "$RUN/$OUT" ] || { echo "$RUN/$OUT already exists; pick another pass number" >&2; exit 1; }

SRC_DIR="$(ls -d "$ROOT"/texts/*/"$TEXT_ID" 2>/dev/null | head -1 || true)"
TITLE=$(python3 -c "import json;print(json.load(open('$SRC_DIR/metadata.json')).get('title',''))" 2>/dev/null || echo "$TEXT_ID")
AUTHOR=$(python3 -c "import json;print(json.load(open('$SRC_DIR/metadata.json')).get('author',''))" 2>/dev/null || true)
LANG_FROM=$(python3 -c "import json;print(json.load(open('$SRC_DIR/metadata.json')).get('original_language','the original language'))" 2>/dev/null || echo "the original language")

rm -rf "$WORK"; mkdir -p "$WORK/source"
cp "$WITNESS" "$WORK/source/original.md"
cp "$RUN/decisions.md" "$WORK/decisions.md"

cat > "$WORK/TASK.md" <<EOF
# Task

Translate one text into English for Enchiridion, as pass $PASS of an
independent multi-pass translation.

**The text:** $AUTHOR, *$TITLE* (\`$TEXT_ID\`), from $LANG_FROM. The settled
transcription of the original is \`source/original.md\`. The term decisions
already taken are in \`decisions.md\`.

**Where you may write:** this workspace, and nowhere else. **Where you may
read:** this workspace only. The repository at \`$ROOT\` contains earlier
passes over this same text, and you must not open them — see below for why.
EOF

cat >> "$WORK/TASK.md" <<'EOF'

## Why you must not look at any other pass

Enchiridion translates each text at least twice, by translators who have not
seen each other's work. Where the passes agree we have a baseline; where they
diverge a human looks, and the divergence is the only signal we have that a
sentence is hard. That signal is worth exactly as much as your independence.
If you saw the other pass, agreement would mean nothing. So: the original and
the ledger are your whole world for this task. Say in `NOTES.md` that you
kept to it.

## What an Enchiridion translation is

Free, open, and honest about what it is: a baseline that anyone who reads the
language better than we do can correct. It is not presented as authoritative
and it is never marked complete on our own say-so. It is meant to be read
beside the original in an interlinear, sentence answering sentence.

**Cognate first.** Wherever reasonable, render a word by its English cognate
or by literally the same word. It is the least invasive choice, morphologically
faithful, and neutral about interpretation — the reader inherits the author's
word, not our paraphrase. In an interlinear, same-shaped words are visible
anchors between the facing texts. The carve-out is the false friend: a cognate
whose English sense has drifted is the *most* invasive choice while looking
like the least. Depart from the cognate when you must, and record every
departure with its reason under `## Departures` in `NOTES.md`. That list
should be short.

**Plain in syntax, never in concept.** Untangle the sentence; never simplify
the argument. Where the original is ambiguous, keep the ambiguity rather than
resolving it for the reader. Keep the author's technical terms and gloss them
once rather than swapping in an easier word. Keep the author's sentence order
wherever English tolerates it. The sentence should be passable; the thought
should be exactly as hard as the author left it.

**The ledger outranks impulse, not argument.** Follow `decisions.md`. If you
have a strong reason to depart from a recorded decision, do not quietly
depart: keep the ledger's rendering in the text and make your case in
`NOTES.md` under `## Ledger disagreements`, with the rationale. A good
argument changes the ledger for every later pass; a silent departure changes
nothing and hides the disagreement.

## The boundary with the transcription

The transcription is settled and is not yours to correct. If you come to
believe it is wrong — a word that cannot be what the author wrote, a table
that does not add up, a line that seems to have dropped — **translate what is
printed** and record the concern under `## Transcription concerns` in
`NOTES.md`, with the segment ID. That goes back across the boundary to the
people who own the transcription. You are a fresh reader of the original, and
you will notice things the transcribers could not; that is valuable precisely
because you do not act on it.

The ledger names the source's known misprints and how to handle each: correct
in the translation, footnote the correction, leave the witness alone.

## The mechanics

- `source/original.md` is segmented with HTML comments: `<!-- seg:ID ... -->`.
  **Mirror every segment ID in your output**, in order, as the same comment.
  Every source segment must have a target segment. That is how the
  interlinear is assembled and how completeness is checked; a missing ID is a
  missing sentence.
- **Tables, figures and worked calculations are not translated; they are
  copied.** Reproduce them byte for byte from the source. Do not re-type a
  number from memory. Where a caption or label inside them is prose,
  translate the label and leave the numbers untouched.
- Footnotes in the standard `[^n]` form, collected at the end. Use them for
  the ledger's misprint corrections and for the one-time glosses the ledger
  calls for. Do not add explanatory notes beyond those: the program does not
  pre-digest.
- Headings as the original has them, capitalized as the original capitalizes.

## What to leave behind

- **`translation-pass-N.md`** — N as given in the task title; the translation.
- **`NOTES.md`** — with the sections named above (`## Departures`,
  `## Ledger disagreements`, `## Transcription concerns`; say "none" where
  none), a line confirming you did not look outside the workspace, and close
  it with `## Where this was harder than it needed to be`: say plainly what was
  harder than it needed to be. Describe the problem, not the solution. "Nothing,
  really" is a complete answer; so is naming one thing.
- **`ESCALATION.md`** only if you cannot proceed — say what turns on the
  answer. A hard sentence is not an escalation; that is the work.
EOF

sed -i '' "s/translation-pass-N.md/$OUT/" "$WORK/TASK.md"

START=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "dispatching $TEXT_ID pass $PASS  [$MODEL, effort=$EFFORT]"
set +e
( cd "$WORK" && codex exec \
    --sandbox workspace-write \
    --skip-git-repo-check \
    -m "$MODEL" \
    -c model_reasoning_effort="\"$EFFORT\"" \
    -c mcp_servers='{}' \
    "$(cat TASK.md)" < /dev/null ) > "$RUN/run-pass-$PASS.log" 2>&1
RC=$?
set -e
END=$(date -u +%Y-%m-%dT%H:%M:%SZ)

SESSION_ID="$(grep -aoE 'session id: [0-9a-f-]{36}' "$RUN/run-pass-$PASS.log" | head -1 | awk '{print $3}' || true)"
COMPLETED=false
grep -aq "tokens used" "$RUN/run-pass-$PASS.log" && COMPLETED=true

cat > "$RUN/provenance-pass-$PASS.json" <<EOF
{
  "text_id": "$TEXT_ID",
  "pass": $PASS,
  "model": "$MODEL",
  "reasoning_effort": "$EFFORT",
  "codex_cli": "$(codex --version 2>/dev/null || echo unknown)",
  "repo_head": "$(git -C "$ROOT" rev-parse --short HEAD)",
  "witness": "$(basename "$WITNESS")",
  "session_id": "${SESSION_ID:-unknown}",
  "started": "$START",
  "finished": "$END",
  "exit_code": $RC,
  "completed": $COMPLETED
}
EOF

# Lift the record. Notes and escalations are per-pass, so they do not clobber.
cp "$WORK/TASK.md" "$RUN/TASK-pass-$PASS.md" 2>/dev/null || true
[ -f "$WORK/$OUT" ] && cp "$WORK/$OUT" "$RUN/" || echo "  NO $OUT — the pass produced no translation" >&2
[ -f "$WORK/NOTES.md" ] && cp "$WORK/NOTES.md" "$RUN/NOTES-pass-$PASS.md" || echo "  NO NOTES.md — the pass reported nothing about itself" >&2
[ -f "$WORK/ESCALATION.md" ] && { cp "$WORK/ESCALATION.md" "$RUN/ESCALATION.md"; echo "  ESCALATED — see $RUN/ESCALATION.md"; } || true

echo "  exit $RC → $RUN/"
ls "$RUN" | sed 's/^/    /'
