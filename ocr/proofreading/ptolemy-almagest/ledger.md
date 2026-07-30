# Adjudication ledger — Ptolemy's *Almagest*

Decisions about what a printed glyph is, with the evidence for each. One row per
decision, not per occurrence: the point of the whole exercise is that settling a
glyph once settles every instance of it.

**A decision here does NOT license a global find-and-replace.** The corruption is
many-to-many — one printed glyph failed into several tokens, and at least two
tokens (`Ψ`, `Ξ`) stand in for *several different signs*. Toomer's own zodiacal
legend proves it: there, `Ψ` appears for Aries, Taurus, Gemini, Cancer, Leo,
Capricornus, Aquarius and Pisces, and `Ξ` for both Libra and Sagittarius. So a
token is evidence, not a key. Repairs are applied per occurrence, with asserted
match counts, by `ocr/text-specific-tools/ptolemy/fix-ocr-artifacts.py`.

## Zodiac signs

| Printed glyph | Sign | Seen in markdown as | Basis | Status |
|---|---|---|---|---|
| ♓ | Pisces | `\aleph` (p0182, line 4163) | Confirmed **three ways**: the glyph is two arcs joined by a bar; the sun's mean longitude at the Nabonassar epoch is a known ♓ 0;45° from III.7; and Toomer's own footnote 60 on that page reads "Literally '45 minutes of the *first* degree of Pisces'". | confirmed |
| ♊ | Gemini | `\square` (p0182, "count the result from … rearwards") | Page read: the printed glyph is the Gemini II-form. Note this does **not** license replacing `\square` generally — it has 5 occurrences and only this one is read. | confirmed (1 of 5) |
| ♊ | Gemini | `\pm` (p0181, line 4161, `\pm 5;30°`) | Page read, batch 1. | confirmed (this occurrence) |
| ♐ | Sagittarius | `\pm` (p0181, line 4161, `\pm 5½°`) | Page read, batch 1. **Same token as the row above, different sign, on the same line.** | confirmed (this occurrence) |
| ♐ | Sagittarius | *nothing at all* (p0179, line 4139) | Page read, batch 1. The print shows "Sagittarius 5½°"; the markdown has only `$5\frac{1}{2}^{\circ}$`. **The glyph left no trace.** | confirmed |
| ♓ | Pisces | `☋`, `☑` | Same value (`0;45°`) in the same epoch context as the confirmed `\aleph` occurrence. Not independently page-read. | probable |
| — | *unresolved* | `\simeq`(17), `\pm`(16), `☐`(13), `Ψ`(9), `Ø`(6), `\mathfrak{m}\mathfrak{g}`(6), `\square`(5), `\pi_1`(5), `∝`(4), `\varnothing`(4), `πₖ`(4), `ṡ`(4), `⇄`(4), `π₀`(3), `\Phi`(3), `\pi_2`(3), + ~40 tokens at 1–2 uses | — | open |

### Equivalence classes (same position, different corruption)

Two occurrences stating the same longitude close together are the same sign,
whichever sign that is. One page read settles a whole class.

| Class | Value | Tokens | Status |
|---|---|---|---|
| A | 29;30° | `♀` == `θ` | unread |
| B | 22;30° | `\Pi` == `\pi` | unread |
| C | 20;45° | `\pi_1` == `\pi_2` | unread |

Known equivocal, excluded from any bulk treatment: `Ψ` (8 signs in the legend),
`Ξ` (2 signs in the legend), and **`\pm` — PROVEN equivocal by page read**, standing
for Gemini and Sagittarius on the same line of p0181. That one is the warning
worth remembering: the slot-ratio inventory scored `\pm` as sign-like with 16
occurrences at a 0.84 ratio, which is exactly the profile that would have
tempted a bulk replacement. Sixteen occurrences would have been corrupted.

## Signs that left no trace — the invisible class

`♐` on p0179 line 4139 is the type case: the print shows a sign and the markdown
has a bare longitude. **No token-based method can find these**, because every
probe we have keys on a wrong symbol being present. They are discoverable only by
reading pages, which is the standing argument for this whole directory, and it
means every count of this family is a lower bound for a second, worse reason than
filtered singletons.

Practical consequence for repair: a fix script cannot anchor on a wrong token
here. It has to insert at a quoted position, so these findings must carry enough
surrounding text to locate them unambiguously.

## Taurus became the numeral 8 — the sign that hides as legitimate content

**Adjudicated 2026-07-30. `8` standing immediately before a longitude is Taurus,
23 occurrences.** Not applied yet; recorded here because the identification is
settled and the repair should go with the rest of the zodiac.

This one matters out of proportion to its size, because it is the first member
of a class every method we own is blind to. The census finds tokens that look
wrong. A digit does not look wrong in a book of numbers, and these read as
ordinary sequences — `mean position of the moon in longitude: 8 4;25°`,
`[Epoch] Position of Apogee: 8 16;10°`. Nothing is malformed, nothing renders
badly, and no filter on strange symbols will ever return them. **So the
248-occurrence zodiac count is a lower bound for a third reason: signs that
became ordinary characters were never in the counted population at all.**

Confirmed four independent ways, which is why it is settled rather than likely:

| Evidence | What it shows |
|---|---|
| Arithmetic | `[8 19;38° − φ 27;15° =] 22;23°` balances exactly on Taurus 19;38 − Aries 27;15. Gemini gives 52;23, Cancer 82;23 — nothing else is near. |
| Geometry | The Venus apogee `8 25°` and perigee `πₖ 25°` must be 180° apart. Taurus 25 → Scorpius 25 is exactly 180°. Eight occurrences ride on this. |
| The page | p0486 prints `♉ 25°` where the markdown reads `8 25°`. |
| Toomer's own prose | "[to Auriga and **Taurus**] when it passed by it. Thus its position … was 8 23½°." |

A fifth check confirms it is a *sign* rather than a numeral without identifying
which: `[8 22;31° − 8 0;19° =] 22;12°` is only a sentence if `8` is a sign on
both sides.

**Method worth reusing: a stated difference between two longitudes is an
equation, and it solves for the signs.** Signs span 30° from Aries 0°, so an
unknown token contributes a multiple of 30 and only one value fits. That
identifies glyphs without reading the page, and it works precisely where glyph
shape fails.

### Still open in this class

- **`9` occupies a sign slot** at least once ("the longitude of the mean sun was
  9 29½°") and is NOT identified. The surrounding elongation does not close on
  any sign cleanly, so a neighbouring value is probably misread too.
- **Suspected, unconfirmed:** Libra `♎` as `=` or `≈`; Aries `♈` as `Y`/`ϒ`;
  Capricorn `♑` as `13`. Needs pages.
- **New unidentified tokens** seen in sign slots: `≲`, `πr`, `\pi_{\mathrm{r}}`,
  `m_{\mathrm{L}}`, `\triangle`, `Φ`.
- **Signs are sometimes SPELLED OUT and correct.** Where Toomer quotes an earlier
  observer: "the sun was sighted in Leo 8½° … the apparent position of the moon
  was Taurus 12½°". Do not convert those to glyphs.
- **A fraction error found in passing, in that same Hipparchus quotation.** Leo
  8;30 to Taurus 12;30 is 86;00, but the text states the distance as 86;15. One
  of the three numbers is misread — `Leo 8¾` or `Taurus 12¼` would both close
  it. Needs the page.

## The first double run — pages 473–478 and 486–490, 2026-07-30

Four runs, two per page-set, same model and effort, compared by
`ocr/proofreading/compare-runs.py`. The zodiac was chosen for this because it is
the one family with no structural licence: a wrong sign leaves no arithmetic
residue unless the text happens to state a difference, so disagreement between
runs is the only detector available.

**The result argues against the reason we did it.** Of 22 readings found by both
runs, 21 agreed exactly and the single conflict was a MISS, not a misread — one
run failed to report a sign the other read correctly, and no case arose where
two confident runs read the same glyph as two different signs. On the earlier
A/B pages the runs *did* confidently disagree, so this is not a settled question;
but on this evidence double-running buys **recall insurance rather than misread
detection**, and recall insurance is worth much less, because a missed sign
survives to the next pass while a wrong one is written into the text.

The conflict is adjudicated in the text's favour: at `Virgo [i.e.
$\mathfrak{m}\mathfrak{g} 1°-2°$]` Toomer names the sign in his own prose, so the
run that read Virgo is right and the run that omitted it simply did not look.

**A caution the corroboration table does not express.** Agreement is on a
token-class within a page, and several of these tokens are equivocal. Both runs
agreeing that `\mathfrak{m}\mathfrak{g}` means Scorpius on p0488 does not license
the Virgo occurrence on the same page. Corroboration is necessary here, not
sufficient, and repairs remain per-occurrence.

### Identifications corroborated by both runs

| Token | Sign | Notes |
|---|---|---|
| `\simeq` | ♎ Libra | Both page-sets independently, plus arithmetic in each: Scorpius 20;50 − Libra 6;00 = 44;50, and Scorpius 20;55 − Libra 17;3 = 33;52. |
| `\pi_1`, `\pi_2` | ♏ Scorpius | **Predicted before the run.** Two stated subtractions solved to exactly +1.0000 sign-indices between `\pi_1` and `\simeq`; the pages then read them as Scorpius and Libra, which are adjacent. Arithmetic and eyes agreeing from opposite directions. |
| `\approx` | ♒ Aquarius | ♒ is two wavy lines and so is `≈`. **Do not bulk-replace**: `\approx` is also used legitimately for "approximately", 102 occurrences against a handful of signs. |
| `\varphi` | ♈ Aries | |
| `\Psi` | ♈ Aries | Already known equivocal — 8 signs in the legend. |
| `\square`, `□` | ♊ Gemini | Confirms the ledger's earlier 1-of-5 page read. |
| `\triangle` | ♎ Libra | Was an unidentified slot token. |
| `\aleph` | ♉ Taurus | **Conflicts with the earlier Pisces reading**, which was itself confirmed three ways. Both are right: `\aleph` is equivocal. |
| `\pi` | ♍ Virgo / ♏ Scorpius | Equivocal across pages. |
| `\pm` | ♐ Sagittarius | Consistent with the earlier page read; still equivocal overall. |
| `m,` | ♏ Scorpius | |
| `8`, `8 \cdot`, `8\frac{1}{2}` | ♉ Taurus | Replicated independently in both page-sets. In `8\frac{1}{2}` the fraction is spurious — the glyph's tail was read as a ½. |

Also corroborated: two signs that **left no trace at all** (Capricorn and Taurus,
both recovered from the print alone), which is the invisible class above showing
up exactly where it was predicted to.

### Cheap models on the same pages — terra and luna at low effort

Both light models were run over p0473–0478 against the strong pair's consensus of
11 readings, scored by `score-against.py`.

| Run | Recall | Contradictions | Elapsed |
|---|---|---|---|
| `gpt-5.6-terra`, effort low | 9/11 (82%) | **0** | 283s |
| `gpt-5.6-luna`, effort low | 9/11 (82%) | **4** | 233s |

**Identical recall; the entire difference is in contradictions.** This is the
result that justifies refusing to blend the two numbers into one score — a single
percentage would have made these models look equivalent, when one is usable and
the other is not. Luna's contradictions are the expensive kind: `\aleph` read as
Leo where the consensus says Taurus, `\Psi` as Pisces against Aries, `\simeq` and
`\triangle` as Aries against Libra — all at high confidence, all plausible, none
detectable downstream.

Terra's two misses are both from the **disguised class** — Taurus printed as the
numeral 8. That is a coherent failure rather than noise: the cheap model does
well at "this glyph looks wrong" and badly at "this ordinary-looking thing is
wrong," which is exactly the class we already knew every token-based method is
blind to. It suggests a division of labour rather than a straight substitution.

**A measurement bug worth keeping.** The first scoring included the reported page
in the finding key, and returned luna at 45% recall with 2 contradictions. Luna
had attributed a page of findings to its neighbour, so every one of them counted
as both a miss and a spurious extra. The true figures are 82% and 4 — the page
key had *flattered luna on contradictions*, the number that matters, while
punishing it on recall, the number that does not. `score-against.py` now excludes
the page by default. Note also that the page misattribution is itself a defect:
findings have to be locatable to be applied.

### An unplanned dividend

Roughly half of every run's findings were parts-vs-degrees, in precisely the
places the repair script deliberately declined to touch — where the governing
word sits in an earlier sentence. The pages confirm those are parts. The choice
to under-reach is now paid off rather than merely defended.

## Other families

| Family | Decision | Status |
|---|---|---|
| Raised unit letters | `^{\rho}` → `^{\mathrm{p}}` (12), `^{\delta}` → `^{\mathrm{d}}` (2). Text evidences its own correction: correct spellings number 427 and 16. | applied `6efd1e6` |
| Table of Chords, lost halves | 90 arc labels restored by recomputing from the chord value against Crd(θ)=120·sin(θ/2). 270 entries checked, 180 already correct, 0 unexplained. | applied `6efd1e6` |
| `^{h}` (44) vs `^{\mathrm{h}}` (2) | Left alone. Same unit, opposite convention from `p`; little is lost by ignoring synonym spread at this level. | declined |
| `2^{\varphi}` inside Toomer's own units key | Unresolvable without the page. | open |

## Rendering decision

Signs normalize to `U+2648`–`U+2653` **plus `U+FE0E`** (Variation Selector-15),
which requests text presentation. Without it these codepoints default to colour
emoji on most platforms. `U+FE0E` is embedded in the markdown rather than handled
in CSS because the corpus has several consumers — the reader, the MCP server, and
GitHub's raw view — and only the selector travels with the content.

This is also why `♀`/`♂` already render correctly in this text and needed no
intervention: they are text-presentation by default.
