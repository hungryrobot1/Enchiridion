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
3. **Colebrooke** (1817) — the editor. His notes are the **UNSIGNED** ones.
   **Drop these**, along with their reference marks, under the standing
   apparatus policy.

> **Correction, 2026-08-08.** This brief originally said the opposite — that
> `Ch.` marked Colebrooke's own notes and should be dropped. That was wrong, and
> a run caught it as a contradiction against the rule above before acting on it.
> Applied mechanically it would have deleted most of Pṛthūdaka's commentary,
> which is the thing this brief exists to protect.
>
> **`Ch.` abbreviates *Chaturvéda*** — Chaturvéda Pṛthūdaca Swámí, the
> commentator named on the section title page. The signed notes are his.
>
> Do not take the label on trust; the page carries the test. On printed p.278 a
> note signed `Ch.` discusses Skandasena and says "in this work, addition being
> the subject, sum is taught; and *the author* will teach its figure by a rule
> (§ 19)" — a commentator speaking about Brahmagupta. On the same page the note
> reading "It is not quite clear whether the examples are the author's or the
> commentator's … They are probably the commentator's; and consigned therefore
> to the notes" is **unsigned**: that is the editor's voice, and it is exactly
> the class to drop.
>
> **The rule is therefore: signed note → commentary, keep and mark. Unsigned
> note → Colebrooke, drop.** Chapter XVIII signs many passages `Com.`; treat
> that as commentary too. Where a note is signed with anything else, or the
> signature is illegible, leave it in place and list it for the reviewer rather
> than guessing.
>
> Note also what Colebrooke's unsigned note concedes: he is *not certain* the
> worked examples are the commentator's, only that they probably are, and he put
> them in the notes for that reason. So the attribution we ship is his best
> judgment and not a fact. Mark the commentary in a way that carries that
> uncertainty rather than asserting it.

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

> **Correction, 2026-08-08.** An answer to this run stipulated
> `Cuttácára`/`Cuttācāra` as that control. **The macron form does not occur in
> the text at all** — it was inferred from a sample rather than found, and
> stipulating it was the same error this brief warns about one section down. The
> run was right to refuse to proceed on a control it could not observe.
>
> Real same-skeleton pairs do occur and were found by the census itself:
> `sidd'hánta`/`sidd'hānta`, `bháscara`/`bhāscara`, `c'hárís`/`c'hāris`,
> `lilávati`/`līlāvatī`. **Use one of those as the document control.** A planted
> pair is still worth keeping, but it tests only the folding logic; it cannot
> show the census finds real disagreements in this document, which is the thing
> in doubt.

**Settled empirically, 2026-08-08:** visual inspection at 300 dpi across six
printed pages found **acute accents everywhere, and no macron anywhere in
print**, including at every location the OCR rendered with a macron. So the
macrons are an OCR modernisation artifact rather than a variant of the edition.
This is evidence from six pages, not a proof about 102 — see the answer in the
run record for how far it licenses repair.

## What the reviewer will need from you

`NOTES.md` opening with `## For the reviewer`, and in it: the commentary marking
you chose and how you applied it, the census output with its positive control,
every spelling you could not settle, and every place the printed page was too
poor to read. This text will be reviewed by someone who does not read Sanskrit,
so anything resting on the language must be checkable without it.
