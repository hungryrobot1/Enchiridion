# Translating for Enchiridion

This document governs the translations Enchiridion makes itself. It is short on purpose. Translating is work that a capable reader of the language already knows how to do; what this page adds is the posture the program takes toward the author and the reader, and the few mechanics that let a translation be checked, corrected, and read beside its original. The evidence for every rule here is in the notes of the translations that taught it, beginning with `translation/runs/leibniz-binary-arithmetic/NOTES.md`.

## What an Enchiridion translation is

A free, open English rendering of a work whose original is public domain, released with the repository under its licence, read beside the original in an interlinear, and honest about what it is: a baseline that anyone who reads the language better than we do can correct. It is never presented as authoritative, and it is never marked complete on our own say-so.

The original is not an appendix to it. The original goes through the text pipeline first, as a full citizen, and the translation is made from that settled transcription. The transcription is the witness for every choice the translation makes, and the thing the reader is invited to check it against.

## The posture

**Cognate first.** Wherever reasonable, render a word by its English cognate or by the same word. It is the least invasive choice, morphologically faithful, and neutral about interpretation: the reader inherits the author's word, not our paraphrase of it. In an interlinear, same-shaped words are the anchors a reader without the language uses to see which sentence answers which.

The carve-out is the false friend. A cognate whose English sense has drifted from the author's is the most invasive choice while looking like the least. Depart from the cognate when you must, record every departure with its reason, and notice if the list grows long — that is the policy being evaded.

**Plain in syntax, never in concept.** Untangle the sentence; never simplify the argument. Where the original is ambiguous, keep the ambiguity rather than resolving it for the reader. Keep the author's technical terms and gloss them once rather than swapping in an easier word. Keep the author's sentence order wherever English tolerates it. The sentence should be passable; the thought should be exactly as hard as the author left it.

**The witness keeps the author's errors; the translation corrects them and says so.** A misprint in the source stays in the transcription. The translation prints the corrected reading with a footnote naming what the source prints and, where there is one, the internal proof — a sum that does not add, a label the arithmetic contradicts. Where a reading is doubtful rather than wrong, translate what is printed and footnote the likelier sense.

**No notes beyond those.** The program does not pre-digest. A translation carries the footnotes the misprints and the one-time glosses require, and nothing explanatory.

## The mechanics

**The ledger.** Each translation keeps a `decisions.md`: the recurring and contested terms, the rendering chosen for each, and the reason. It is written before drafting, from the text, and it grows at adjudication. The ledger outranks impulse, not argument: a translator who disagrees keeps the ledger's rendering in the text and makes the case in the notes, so that a good argument changes the ledger for every later pass and a silent departure changes nothing. Ledgers carry forward; the next text by the same author starts from the last one.

**Two passes, independently.** Every translation is made at least twice, by translators who have not seen each other's work, each given only the original and the ledger. Where the passes agree we have a baseline; where they diverge a human looks. That divergence is the only signal we have that a sentence is genuinely hard, and it is worth exactly as much as the independence that produced it.

**Segments.** The transcription is cut into aligned units with stable IDs, and every pass mirrors them. That is what makes the interlinear assemblable, the passes comparable, and completeness checkable: a missing ID is a missing sentence.

**Tables, figures and calculations are copied, not translated.** Byte for byte from the witness, with prose labels rendered and numbers untouched. The one licence is the ledger's own: a misprint inside a table that its arithmetic proves wrong is corrected and footnoted.

**The boundary with the transcription.** Verifying the transcription, or the source behind it, is the text pipeline's concern, not the translator's. But a translator is a fresh reader of the original and will notice what the transcribers could not. So: translate what is printed, record the concern with its segment ID, and hand it back across the line. That is valuable precisely because it is not acted on here.

**Status.** `translation_status` is `baseline` when two passes have been adjudicated and machine-checked; `reviewed` only when a human who reads the language has read it against the source. The machine checks completeness, numeric fidelity and arithmetic. They test well-formedness and never meaning, and the tool says so.

## Where the rest lives

The dispatch, the checker, and the assembler are in `translation/`, and each carries its own explanation. The lessons that produced this page — what a machine witness can lose without saying so, why layout can carry meaning, why original-language text belongs in files rather than in conversation — are in the run notes, where they were learned. Read those before writing more here.
