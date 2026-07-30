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
