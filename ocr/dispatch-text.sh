#!/usr/bin/env bash
# Dispatch one text through the pipeline, and keep the record.
#
#   ocr/dispatch-text.sh <text-id> [model]
#
# Two things live here and nothing else: the BOOKKEEPING (assemble a workspace,
# pin provenance, file what comes back under ocr/runs/<text-id>/) and the CHARTER
# sent to the worker. There was a separate ocr/DISPATCH.md holding the charter;
# it duplicated the prompt and the two would have drifted apart. One file, so the
# instructions and the thing that sends them are versioned together.
#
# What is NOT here is anything per-genre or per-text. How to process a text is
# ocr/README.md and the STAGE.md files, which the worker reads for itself.
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

# RUN_LABEL keeps a second run of the same text beside the first instead of on
# top of it. Re-running a text after changing its inputs is the whole method
# here, and two runs cannot be compared if the first is only recoverable from
# git history.
RUN="$ROOT/ocr/runs/${TEXT_ID}${RUN_LABEL:+-$RUN_LABEL}"
WORK="$RUN/workspace"
rm -rf "$WORK"; mkdir -p "$WORK/source"

# Everything the text directory holds. On an EXTRACTION job the corpus markdown
# is excluded: it is our previous answer rather than a source, and a worker
# handed it reviews us instead of reading the original.
#
# REPAIR=1 says the existing markdown IS the subject -- the text is already
# transcribed and the work is post-processing it. Then withholding it hands the
# worker everything except the file the run is for, which is how a whitelist
# withheld the Dedekind .tex from the run we fetched it for. This is the case
# the exclusion's comment anticipated, so it is a narrower rule and not a looser
# one: the caller says which job this is, rather than the script guessing from
# metadata that is itself unreliable.
#
# A blacklist rather than a whitelist, because the first version listed pdf,
# epub, txt, htm and metadata -- and would have silently withheld that .tex,
# the single most valuable file in that directory. A source type nobody
# anticipated should arrive, not vanish.
if [ "${REPAIR:-}" = "1" ]; then
  find "$SRC_DIR" -maxdepth 1 -type f -exec cp {} "$WORK/source/" \;
else
  find "$SRC_DIR" -maxdepth 1 -type f ! -name '*.md' -exec cp {} "$WORK/source/" \;
fi
# `-type f` copies no directories, so a text's images/ never arrived. The
# markdown references them, so a repair job saw every reference resolve to
# nothing: al-Biruni stopped and asked whether to reconstruct three figures that
# already existed, and al-Khwarizmi rebuilt eighteen from the scan rather than
# ask. Both responses were reasonable and both were caused by us.
[ -d "$SRC_DIR/images" ] && cp -R "$SRC_DIR/images" "$WORK/source/" || true

TITLE=$(python3 -c "import json;m=json.load(open('$SRC_DIR/metadata.json'));print(m.get('title',''))")
AUTHOR=$(python3 -c "import json;m=json.load(open('$SRC_DIR/metadata.json'));print(m.get('author',''))")

# One paragraph, only when the job starts from an existing transcription. It says
# where to start and what the markdown's standing is; everything else in the
# charter applies unchanged, which is the point of not having modes.
OPENING="Take one text as far through the Enchiridion pipeline as it will honestly go."
REPAIR_NOTE=""
if [ "${REPAIR:-}" = "1" ]; then
  OPENING="Take one text that is ALREADY TRANSCRIBED further through the Enchiridion pipeline."
  REPAIR_NOTE="
**This is a repair job, not an extraction.** \`source/\` contains the markdown
the library currently publishes for this text, alongside the original it was
made from and any images the text already has. That markdown is the subject of
the work: repair it rather than re-deriving it. The original is there so you can
check the markdown against it — it is the page witness, and where the two
disagree the page is right.

**Write your repaired markdown to the workspace root, not over \`source/\`.**
Keep \`source/\` as delivered, so the two can be compared and so the repair can
be re-run from a clean input. An earlier run read "improve it in place" as an
instruction to edit \`source/\` directly, and its finished work was not collected,
because \`source/\` is the input and is deliberately not gathered up afterwards.
If you produce new or corrected images, put them in an \`images/\` directory at
the workspace root too.

Which stage the work belongs to is yours to determine from the state of the
file. Say what you concluded and why."
fi

# The prompt IS the charter. There was a separate ocr/DISPATCH.md saying much of
# this; it overlapped with the prompt and the two would have drifted. One place,
# versioned with the script that sends it.
#
# Two heredocs on purpose: the first interpolates paths and titles, the second is
# quoted so prose containing $ and backticks needs no escaping. Escaping a long
# charter by hand is how a charter acquires silent typos.
cat > "$WORK/TASK.md" <<EOF
# Task

$OPENING

**The text:** $AUTHOR, *$TITLE* (\`$TEXT_ID\`). Its sources are in \`source/\`,
along with the metadata the library currently holds for it.
$REPAIR_NOTE

**The repository** is at \`$ROOT\`, readable but not writable by you. Start with
\`$ROOT/ocr/README.md\`. Use \`$ROOT/ocr/.venv/bin/python3\` where PyMuPDF is
needed — it imports as \`pymupdf\`, not \`fitz\`.

**Where you may write:** this workspace, and nowhere else.
EOF

cat >> "$WORK/TASK.md" <<'CHARTER'

## How the pipeline is arranged

A text moves through numbered stages: `0-recon`, `1-prepare`, `2-extract`,
`3-postprocess`, `4-proofread`. Unnumbered directories are called from anywhere —
`verify/` holds checks that never edit, `figures/` and `drama/` are tracks that
span several stages, `text-specific-tools/` holds per-text work and its
precedents are worth reading before you write your own.

Each stage carries a `STAGE.md` saying what it consumes, what it produces, what
test says it succeeded, and what that test does not check. The last field is the
useful one. There is no brief specific to your text; if these documents leave you
guessing, that is a fact about them worth reporting.

## What the checks are for

Most checks here answer a narrower question than their name suggests, and knowing
which question is worth more than running them.

The diagnostic triad asks whether a renderer can handle the notation. It is
informative exactly to the degree the text contains notation, and it says nothing
about whether the words are the right words. A text with no mathematics will pass
it while telling you nothing.

Two sources agreeing is weaker evidence than it looks. An epub and a PDF built
from one transcription, or a PDF generated from the TeX beside it, are two
renderings of a single act of copying: they establish fidelity, never
correctness. Where that is the situation, say so rather than letting agreement
stand in for a second witness.

And a probe that finds nothing has proved nothing until it has been shown to find
a case known to exist. Four separate false conclusions here came from believing a
zero. Ship a negative control, or a positive one — compare a page with itself
before trusting a duplicate scan that reports none.

## Working on the text

Never edit the text by hand. Repairs go through a script with asserted anchors
and counts, so that a wrong edit is reviewable rather than invisible, and so the
work can be re-derived when a source is re-extracted. Run the relevant acceptance
test after each change and report what it said.

## One printed mark, two spellings

Transcribing mathematics means deciding, glyph by glyph, what was printed. Those
decisions are made page by page and are not consistent with one another, so a
finished text usually contains places where one printed mark was resolved two
ways. At least one is wrong, and nothing here can see it: both spellings render,
so the triad passes.

The question is not "does this render" but **where does this document disagree
with itself**. Three shapes are worth hunting:

- **A rare spelling beside a common one of the same kind** — a relation used once
  where a synonym is used thirty times.
- **One notation spelled two ways** — `\alpha_{-1}` on one line and `a_{-1}` on
  another, for the same quantity. The strongest signal, and invisible to anything
  counting LaTeX commands, because `a` is not a command.
- **Anything inside math that is not mathematics** — a CJK or Cyrillic character,
  a `\text{}` wrapped round a single mark, a `\stackrel` inventing a structure the
  page does not have. This is what OCR emits when it cannot identify a glyph.

`ocr/verify/math-vocab-census.py` reports all three and decides none of them.

Two cautions, both learned by getting it wrong:

**Judge within a section, not across the document.** The same token can be right
in one part and wrong in another. Cantor writes `a_\nu` for the elements of an
aggregate in § 7, correctly, and the OCR wrote `a_\nu` for the ordinal in § 18,
wrongly. A document-wide fix corrupts § 7.

**A self-consistent variant is weaker evidence than a lone one.** Three
occurrences agreeing with each other may be a distinction the edition really
makes; one against thirty is likely a slip.

None of this is a verdict. Each is a question only the printed page answers, and
the answer is one of three: the edition genuinely distinguishes them — say why;
it is a misread — repair it by anchor and **cite the page you read**; or you
cannot tell — escalate. **Do not repair a variant you have not seen printed.**
The commoner spelling is not automatically right. What you know is that they
cannot both be.

**The repair rule above is a stage-4 rule.** It governs adjudicating a reading
against the printed page. Stage 3 repairs on evidence inside the document itself
and needs no page: `1 saw` has no subject, `moti/n` is not a word, and neither is
a doubtful reading of anything. The test is where the evidence lives and whether
exactly one repair is available — see `3-postprocess/STAGE.md`, which states it
in full. Do not defer a broken string to stage 4; do not resolve an ambiguous one
in stage 3.

## The library holds whole works

**Transcribe the entire work, always.** The library's promise is that a reader
can read any text cover to cover. What the syllabus recommends is often a small
fraction of a book — a few chapters, one of thirteen parts — and that has no
bearing on what gets transcribed. Never narrow a text to the part you think will
be assigned, and never stop early because a work is long.

This does not loosen the apparatus policy: editorial introductions, commentary,
bibliographies and indices still come out. The distinction is between *the work*
and *the edition's furniture around it*. A translator's commentary volume is
furniture even when it is half the file; Book XIII is the work even if nobody is
assigned it.

Where a work spans several physical volumes or several supplied files, it is
still one work. Say so, and transcribe all of it.

## When to stop and ask

Stopping is a good outcome, and three kinds of question are worth stopping for.

**A decision that is ours to make.** Apparatus is the standing example: editorial
introductions, notes-on-the-text and bibliographies come out, while authorial
footnotes and a translator's bracketed interpolations stay — and getting it
backwards deletes the author. Alternating verse and prose is another; a
whole-work verse declaration shatters prose that alternates with it. These fail
invisibly, which is why they are worth a question rather than a guess.

**Permission, which is not a judgment at all.** Network access, or anything that
touches an external service. Ask; do not decide.

**OCR is always run by hand, by us, outside this sandbox — which has no network.**
Do not invoke `ocr.py`; it cannot work here, and three runs in one batch each
spent a cycle discovering that. If OCR is the track, do all the preparation, then
escalate a HANDOFF rather than a request: the prepared file and the exact command,
the page ranges kept and dropped with an asserted count, which boundary leaves you
rendered and what they show, the duplicate-leaf scan with its control, and whether
you cropped — including an explicit "no crop, because…" when you did not. The
preparation is what makes the OCR clean, and it is entirely yours to do.

**The method's premise does not hold here.** If the approach the documents assume
turns out not to apply to your text — no independent witness where one was
presumed, a stage contract written for PDFs when a better source is not a PDF —
that is the most valuable thing you can tell us, because it corrects the
documents rather than the text.

To stop: write `ESCALATION.md` in this workspace saying what you need and what
turns on it, then finish. Your session is resumable, so you will be restarted
with an answer and your context intact. A blocked stage with a clear account
beats a finished text with a silent guess, because nothing downstream can catch
a guess.

## Two things about the reader you cannot infer from the source

In-page links do not work here. The router keys on the URL hash, so a footnote
link does not fail quietly — it sends the reader to the front page and loses
their place; and sections are built lazily, so the target is usually not present
anyway. Keep a superscript marker, which is the author's and tells a reader which
sentence carries the note, and drop the navigation around it.
`3-postprocess/strip-inpage-anchors.py` does exactly this.

The first `h1` in a file is treated as the document title, and lazy sectioning
begins at the second. So a collected volume needs its own title as the opening
`h1` — otherwise the whole of the first work stays eager and never collapses.

## What a run is expected to leave behind

Four things, and only these are load-bearing:

- **the markdown** — the transcription itself;
- **`PROPOSED.md`** — naming which file that is, when there is more than one;
- **`NOTES.md`** — what you did, found, and could not establish;
- **the scripts that produced it** — anywhere in the workspace; they are lifted
  from wherever you put them. Without them the text is an artifact nobody can
  rebuild.

Plus `ESCALATION.md` if you had to stop and ask.

Everything else in the workspace is disposable, and you should feel free to
treat it that way — intermediates, extractions, scratch files. In particular
**do not write a `toc.json`.** The site generates a text's contents from its own
headings at build time, and the headings themselves are settled at review. A run
that hand-authors one is producing something nobody consumes.

## Naming your result

If you produce a text you believe belongs in the library, write `PROPOSED.md`
naming the file in backticks and saying what you verified about it. Adoption is
not yours to perform — the corpus is outside your sandbox by design — but a run
that leaves several markdown files and no proposal cannot be adopted without
someone guessing which one you meant. One earlier run left a raw extraction and a
draft side by side, and neither was labelled.

A proposal is not a claim that the text is finished. Adoption sets its status to
`needs-review`: machine-checked, and not yet read against the source by a person.

## What to write down

Keep `NOTES.md`. The processing is the smaller half of this; what the attempt
teaches about the pipeline is the larger half. Worth recording: what you decided
and on what evidence, where the documentation was wrong or missing or
contradicted what you found, what you could not settle, and anything true beyond
this one text.

Note also where the time went — which steps were slow, and whether each was slow
because the work is genuinely intricate or because the tooling made it harder
than it needed to be. We cannot tell those apart from the outside.

Do not mark anything complete that you have not verified, and do not change
`ocr_status` to claim a completeness you could not establish.
CHARTER

mkdir -p "$RUN"

# DRY=1 assembles the workspace and stops. A malformed charter or a missing
# source is only visible once the workspace exists, and finding out by spending
# a run is the expensive way to learn it.
if [ "${DRY:-}" = "1" ]; then
  echo "DRY RUN — workspace assembled, nothing dispatched"
  echo "  $WORK"
  echo "  source/:"; ls -1 "$WORK/source" | sed 's/^/    /'
  echo "  TASK.md: $(wc -l < "$WORK/TASK.md" | tr -d ' ') lines"
  exit 0
fi

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
# The session id makes a run RESUMABLE: `codex exec resume <id> "<answer>"`
# restarts the worker with its context intact, which is how an escalation gets
# answered without holding a process open waiting for us.
SESSION_ID="$(grep -aoE 'session id: [0-9a-f-]{36}' "$RUN/run.log" | head -1 | awk '{print $3}' || true)"

# EXIT CODE IS NOT A COMPLETION SIGNAL. `codex exec` handles SIGTERM and exits
# 0, so three runs killed mid-work after the machine slept were all recorded
# exit 0 and displayed as DONE -- a killed run and a finished one were
# indistinguishable in the record.
#
# The log itself can tell them apart: codex prints a "tokens used" summary when
# a turn ends normally, and nothing of the sort when it is cut off. Checked
# against the five completed runs (all have it) and the three killed ones (none
# do) before being trusted, because a probe that returns zero has proved nothing
# until it has been shown to find a case known to exist.
COMPLETED=false
grep -aq "tokens used" "$RUN/run.log" && COMPLETED=true

cat > "$RUN/provenance.json" <<EOF
{
  "text_id": "$TEXT_ID",
  "repair": $([ "${REPAIR:-}" = "1" ] && echo true || echo false),
  "model": "$MODEL",
  "reasoning_effort": "$EFFORT",
  "codex_cli": "$(codex --version 2>/dev/null || echo unknown)",
  "repo_head": "$(git -C "$ROOT" rev-parse --short HEAD)",
  "session_id": "${SESSION_ID:-unknown}",
  "started": "$START",
  "finished": "$END",
  "exit_code": $RC,
  "completed": $COMPLETED
}
EOF

# Lift the record out of the disposable workspace.
cp "$WORK/TASK.md" "$RUN/" 2>/dev/null || true
[ -f "$WORK/NOTES.md" ] && cp "$WORK/NOTES.md" "$RUN/" || echo "  NO NOTES.md — the run reported nothing about itself" >&2
[ -f "$WORK/ESCALATION.md" ] && { cp "$WORK/ESCALATION.md" "$RUN/"; echo "  ESCALATED — see $RUN/ESCALATION.md"; } || true
# EVERY top-level file the worker left, not a list of extensions we thought of.
# The extension list was .md and .py, so Hamlet's toc.json -- a required
# deliverable, named in its own PROPOSED.md -- stayed in the gitignored
# workspace and would have been destroyed by the next dispatch. Cantor's
# run_repair.sh likewise. That is the same whitelist-defaults-to-exclusion
# failure as the source copier and the tool lifter before it, and the rule it
# keeps teaching is that the part of a system that keeps the record should fail
# loudly and keep too much.
find "$WORK" -maxdepth 1 -type f ! -name 'TASK.md' ! -name 'ANSWER.md' \
     -exec cp {} "$RUN/" \; 2>/dev/null || true
# Any tool the worker wrote, wherever it chose to put it. The first version
# looked only under $WORK/ocr and silently dropped both Dedekind tools:
# Rousseau used ocr/text-specific-tools/, Dedekind used text-specific-tools/,
# and nothing tells a worker which. Search the workspace, skip its sources.
find "$WORK" \( -name '*.py' -o -name '*.sh' \) -not -path "$WORK/source/*" \
     -exec cp {} "$RUN/" \; 2>/dev/null || true
# Controls are evidence: a worker that plants a known defect to prove a checker
# can see it has produced the only artifact that justifies trusting the checker.
[ -d "$WORK/controls" ] && cp -R "$WORK/controls" "$RUN/" 2>/dev/null || true
# Images the run produced or corrected.
[ -d "$WORK/images" ] && cp -R "$WORK/images" "$RUN/" 2>/dev/null || true
# Rescue: a repair job that edited source/ in place despite the charter. The
# input is pristine in the text directory, so anything here that differs from it
# is work, and losing work to a filing rule is the failure this pipeline keeps
# repeating.
if [ -d "$WORK/source" ]; then
  for f in "$WORK/source"/*.md; do
    [ -e "$f" ] || continue
    orig="$SRC_DIR/$(basename "$f")"
    if [ ! -f "$orig" ] || ! cmp -s "$f" "$orig"; then
      cp "$f" "$RUN/" && echo "  rescued $(basename "$f") — it was repaired inside source/" >&2
    fi
  done
fi

echo "  exit $RC → ${RUN#$ROOT/}/"
ls -1 "$RUN" | sed 's/^/    /'
