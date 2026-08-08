# Brief — Brahmagupta, *Brahmasphuṭasiddhānta* chs. XII and XVIII (Colebrooke 1817)

Decisions already taken about this text. They were settled deliberately; do not
reopen them on your own judgment. Where this brief and your judgment disagree,
follow the brief and record the disagreement in `NOTES.md` — that record is
wanted. Escalate only if following it proves impossible, or if it is silent on
something it plainly ought to cover.

## The volume is three works, and you want one of them

Colebrooke's *Algebra, with Arithmetic and Mensuration, from the Sanscrit of
Brahmegupta and Bháscara* (London, 1817) prints three separate works back to
back. **The PDF is 478 pages; the printed page numbering starts 96 pages in.**

**`PDF page = printed page + 96`** — verified against six sample pages, including
both ends of the range below.

| work | author | printed | PDF |
|---|---|---|---|
| *Līlāvatī* | Bhāskara II | 1–128 | 97–224 |
| *Vīja-gaṇita* | Bhāskara II | 129–276 | 225–372 |
| **chs. XII + XVIII** | **Brahmagupta** | **277–378** | **373–474** |

**Your deliverable is the Brahmagupta only: printed 277–378, PDF 373–474, 102
pages.** The two Bhāskara works are wanted eventually and will be dispatched as
their own texts with their own directories. Do not process them here — a run
that tries all 378 pages risks the part we actually need. If you have capacity
left over, say so in `NOTES.md` rather than spending it northward.

Everything before printed page 277 that is *about* Brahmagupta — Colebrooke's
dissertation and his notes on the Indian algebraists — is editorial apparatus and
is out of scope under the corpus policy.

## This is a full OCR

The PDF carries a text layer and it is unusable: roughly 1,931 characters per
page against a ~16-character mean line, with words shredded across lines. It also
**silently drops every diacritic** — it renders *praśna* as `prasna` and page 276
as `876`. Do not use it as a witness for anything, least of all spelling. It is
worth reading once to see how badly it fails, and then setting aside.

## Pṛthūdaka's commentary stays, and must stay marked

The section title page (PDF 373) reads:

> GAṆITĀDHYĀYA, ON ARITHMETIC; THE TWELFTH CHAPTER OF THE
> BRAHME-SPHUTA-SIDD'HANTA, BY BRAHMEGUPTA; **WITH SELECTIONS FROM THE COMMENTARY
> ENTITLED VĀSANĀ-BHĀSHYA, BY CHATURVEDA-PRIT'HUDACA-SWAMI.**

So there are **three voices** on these pages, and the run must keep them apart:

1. **Brahmagupta** (c. 628) — the numbered verses. The text.
2. **Pṛthūdaka** (c. 864) — the *Vāsanā-Bhāshya*, printed as selections woven
   through the chapter. **Keep this.** He is a primary source in his own right,
   not editorial matter, and the edition announces him on its title page. He also
   supplies the worked examples without which Brahmagupta's bare rules are close
   to unreadable.
3. **Colebrooke** (1817) — the editor. His footnotes are **signed `Ch.`**, which
   makes them mechanically separable. **Drop these**, along with their reference
   marks, under the standing apparatus policy.

The danger is voice 2 being read as voice 1: Pṛthūdaka is two centuries later
than Brahmagupta, and unmarked interleaving would let a reader attribute ninth-
century mathematics to a seventh-century author. **Every passage of commentary
must be distinguishable in the markdown from the verse it comments on.** How to
mark it is yours to propose — blockquote, a labelled sub-heading, whatever the
printed page's own typography supports. Say what you chose, show a sample, and
say how you told the two apart on the page. If the printing does *not* reliably
distinguish them somewhere, that is the escalation.

Colebrooke also prints bracketed interpolations of his own inside the
translation (`[direct and inverse,]`). Those are translator's interpolations, not
notes: **keep them, brackets and all**, as with the rest of the corpus.

## Diacritics: preserve, census, and repair almost nothing

Colebrooke transliterates in full — *Cuṭṭaca*, *praśna*, *vyavahāra* — and OCR
will confuse ṭ/t, ś/s, ā/a, ḍ/d, ṅ/n. **Transcribe the marks as printed. Do not
normalize to IAST or to anything else**, and do not strip them. Colebrooke's
scheme is his own, it is inconsistent with modern practice, and the inconsistency
is evidence rather than error.

The question to ask is not *does this render* but **where does this document
disagree with itself**. Build a diacritic census as a text-specific tool:

- strip the marks from every transliterated term to get a skeleton
  (`cuttaca`, `prasna`),
- bucket the occurrences by skeleton,
- report every bucket holding more than one spelling, with counts and locations.

A bucket that disagrees is a candidate, not a verdict. Judge within a section. A
variant that is self-consistent across many occurrences is weaker evidence of
error than a lone one. **Never repair a variant you have not seen printed** —
that is a stage-4 rule and it binds here, because the text layer cannot witness
diacritics at all, so the *only* witness is the page image. Where you cannot
settle a spelling, leave it as transcribed and list it for the reviewer.

**The census must be shown to work before its output is believed.** Give it a
positive control: a term you have confirmed by eye is spelled two ways in the
scan, and check the census finds it. A census returning few disagreements is not
good news until it has been shown capable of finding one.

## What the reviewer will need from you

`NOTES.md` opening with `## For the reviewer`, and in it: the commentary marking
you chose and how you applied it, the census output with its positive control,
every spelling you could not settle, and every place the printed page was too
poor to read. This text will be reviewed by someone who does not read Sanskrit,
so anything resting on the language must be checkable without it.
