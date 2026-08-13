# Brief — The Protestant Ethic and the Spirit of Capitalism (Weber, tr. Parsons)

What was observed about **this copy**, and how. A starting point, not a ground
truth: where the file disagrees, **the file wins** — say so in `NOTES.md`. Where
this brief and a `STAGE.md` disagree, **follow the stage**; that is a defect
here. If you have a strong reason to go against something written below, take
it — and record the reason.

Derived 2026-08-13 on the host by opening the PDF, before dispatch.

## Rights: settled, and the copyright page will tell you otherwise

`metadata.json` carries a `rights` field, and recon will print it. Read it
before you read the copyright page, because **the copyright page says the
opposite**: *"This book is copyright under the Berne Convention. No portion of
it may be reproduced by any process without written permission."*

That notice was accurate when printed and the term has since expired — first
published 1930, ninety-five years, public domain in the US from 1 January 2026.
Our copy is the **third impression, 1950**, and an impression is not a new
edition, so no new copyright arises from it.

Nothing here needs re-deciding. It is flagged only so the notice does not stop
the run.

## What the copy is

318 PDF pages, an Internet Archive scan. Observed by reading the title page and
the contents:

- **Title page**: Scribner's (New York) and Allen & Unwin (London), translated
  by Talcott Parsons, with a foreword by R. H. Tawney.
- **Contents** (PDF p. 11) lists, in order: Translator's Preface · Foreword ·
  Author's Introduction · Part I chapters I–III · Part II chapters IV–V.
- **Notes** run from roughly PDF p. 225 to p. 307 — around eighty pages of
  endnotes, the single largest structure in the book after the text.
- **Index** follows, to about p. 317.

## Scope: this is a fragment, and Parsons says so

The Translator's Preface (PDF p. 13) records that the essay first appeared in
the *Archiv für Sozialwissenschaft und Sozialpolitik* in 1904–5 and was
reprinted in 1920 as the first study in the unfinished *Gesammelte Aufsätze zur
Religionssoziologie*. Parsons calls what he has given English readers *"only a
fragment"* of that series.

That is the shape of the work, not damage. **Do not go looking for the rest of
the series**, and do not read its absence as a defect. Saying so in `NOTES.md`
lets the entry be qualified at adoption.

## The notes are the hard part

The apparatus rules are in `ocr/3-postprocess/STAGE.md` and they govern. The
reason this text is worth a brief is that its eighty-page note apparatus is
**mixed**, and the two kinds fall on opposite sides of the rule:

- **Weber's own notes are authorial** and stay. They are not marginal — they
  carry a large part of the argument, and cutting them would cut the book.
- **Parsons's notes are a translator's editorial additions.** The rule sends
  those out, alongside his Preface.

Whether the printed page actually distinguishes them, and how, is **not
something this brief knows** — it was not checked. Establish it from the file
before acting, and if the distinction turns out not to be reliably marked, that
is worth an escalation rather than a guess.

The `Author's Introduction` is Weber's own 1920 *Vorbemerkung* and is part of
the work. **Tawney's Foreword is not Weber**, and the Index is not either.

## The embedded text layer is bad OCR

Observed by extracting text with PyMuPDF: `first pubHshed`, `Archil für`,
`w4iich`, `Fatist`. The PDF has a text layer and it is an old scanner's
guesswork, not born-digital text. Recon should see this for itself; it is noted
so that the presence of *some* extractable text is not mistaken for a
source-native route.

Expect German throughout the notes — book titles, journal names, quoted phrases
— with umlauts, and occasional Greek and Hebrew transliteration.
