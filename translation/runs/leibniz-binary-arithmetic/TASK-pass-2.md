# Task

Translate one text into English for Enchiridion, as pass 2 of an
independent multi-pass translation.

**The text:** Gottfried Wilhelm Leibniz, *Explanation of Binary Arithmetic* (`leibniz-binary-arithmetic`), from French. The settled
transcription of the original is `source/original.md`. The term decisions
already taken are in `decisions.md`.

**Where you may write:** this workspace, and nowhere else. **Where you may
read:** this workspace only. The repository at `/Users/zacharygrunenberg/Projects/Enchiridion` contains earlier
passes over this same text, and you must not open them — see below for why.

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

- **`translation-pass-2.md`** — N as given in the task title; the translation.
- **`NOTES.md`** — with the sections named above (`## Departures`,
  `## Ledger disagreements`, `## Transcription concerns`; say "none" where
  none), a line confirming you did not look outside the workspace, and close
  it with `## Where this was harder than it needed to be`: say plainly what was
  harder than it needed to be. Describe the problem, not the solution. "Nothing,
  really" is a complete answer; so is naming one thing.
- **`ESCALATION.md`** only if you cannot proceed — say what turns on the
  answer. A hard sentence is not an escalation; that is the work.
