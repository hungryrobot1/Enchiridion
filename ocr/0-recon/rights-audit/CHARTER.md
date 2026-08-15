# Rights audit — the method, identical for every section

You are auditing one slice of the Enchiridion corpus to establish **what we may
lawfully publish**, text by text. Another agent has each of the other slices and
is following this same charter. The slices are consolidated at the end, so the
value of your work depends on it being comparable to theirs.

Enchiridion publishes from the **United States** (GitHub Pages), so **US law
governs**. It is free, non-commercial, open source, MIT licensed.

## The one rule that matters most

**THE FILE SETTLES IT.** Open the actual source PDF or EPUB and read its title
page and copyright page. Do not reason from `metadata.json`, from the directory
name, from the Internet Archive identifier, or from what you know about the
work. Every serious error this project has made in this area came from a
plausible story about an edition instead of looking at it.

Three real examples, all from this corpus:

- 1.14 million words of Aristotle were nearly withheld on the assumption that a
  big modern-looking Aristotle file must be the 1984 Revised Oxford Translation.
  Its first page says *"translated under the editorship of W. D. Ross"* — the
  1928 Oxford translation, public domain.
- Buchanan's *Poetry and Mathematics* has an archive identifier suffixed
  `0000unse`, which normally means a later borrowed copy. Its copyright page
  says `COPYRIGHT, 1929 … FIRST PRINTING, JULY, 1929`.
- Weber's copyright page says *"This book is copyright under the Berne
  Convention. No portion of it may be reproduced by any process without written
  permission."* It is nonetheless public domain in the US, because the term ran
  out. **Read the date first, the notice second** — a printed reservation of
  rights is evidence about the publisher's wishes, never about the term.

To read a PDF's front matter:

```sh
ocr/.venv/bin/python3 -c "
import pymupdf; d=pymupdf.open('PATH')
for i in range(min(14, d.page_count)):
    t=d[i].get_text().strip()
    if t: print(f'--- p{i+1} ---'); print(t[:700])
"
```

EPUBs are zip archives; unzip and read the first XHTML files, or look for
`content.opf` metadata. If a text directory has **no source file at all**, say
so — that is a finding, not a blocker.

## The rules you are applying

A text is publishable if **one** of these is true and **you have seen it**:

1. Published in the US **before 1931**. (The boundary moves each January; today
   it is 1931, so a 1930 publication is clear and a 1931 one is not.)
2. It carries an **explicit licence** permitting redistribution — Creative
   Commons, a public-domain dedication, a government or IGO release.
3. We hold **written permission**. (We do not, for anything, yet.)

Some things that are **not** any of those, and have misled people before:

- *"It's on the Internet Archive."* Archive provenance carries **no information
  about rights in either direction.** IA lost *Hachette v. Internet Archive*
  (2d Cir. 2024) on controlled digital lending, which is a weaker use than ours.
- *"It's on arXiv."* The default arXiv licence grants **arXiv** the right to
  distribute and says nothing about us. Only an explicit CC-BY or CC0 counts.
- *"Everyone mirrors it"* / *"professors hand it out"* / *"no one has complained."*
- *"The author died long ago."* US terms for published works run from
  **publication**, not death. Life+70 is the UK/EU rule and is not ours.

**For a translation, the translation is the thing we publish, so the
TRANSLATION's date and translator govern — not the original work's.** A 1st-century
work in a 1975 translation is encumbered.

## The fork that decides what we do about it

This is the most valuable thing your line will record.

- **If the WORK is public domain and only the TRANSLATION is encumbered**, the
  choice was never "have this text or not" — it is "have *this* translation or
  not." Enchiridion can commission or produce its own freely licensed
  translation. Say `translation needed`, and where you can, name a
  public-domain source it could be translated *from* (an old edition in the
  original language, a pre-1931 translation into any language).
- **If the WORK ITSELF is in copyright**, no translation solves it. Only
  permission, expiry, or removal. Say `copyrighted`.

That distinction is the whole point of the audit. Get it right even when you
must leave the rest uncertain.

## What to write

Create the file named in your task, and nothing else. **Do not modify
`metadata.json`, the corpus, or any other file** — several agents are running at
once and the corpus is not yours to edit. Record metadata errors as findings.

Format, exactly. **No tables** — they are hard to read. One text per line:

```
Author, Title, decision — a few words of circumstance
```

Begin the decision with one of these words so the slices can be merged:

- `public domain` — clear, publishable, nothing to do
- `translation needed` — work is free, this translation is not
- `copyrighted` — the work itself is in copyright
- `undetermined` — say in a few words exactly what would settle it
- `no source` — the directory has no source file to judge

Real examples of the register wanted:

```
Arendt, Eichmann in Jerusalem, copyrighted — Viking 1963, in print, no translation involved
Homer, Iliad, public domain — Butler 1898, verified on the title page
Ptolemy, Almagest, translation needed — Toomer 1984 Princeton; translate from Halma's French, 1813
Kubrick and Clarke, 2001: A Space Odyssey, copyrighted — studio-held, no authorised published text
Chadwick, The Existence of a Neutron, undetermined — 1932 Royal Society; check whether the 1932 volume was renewed
```

Keep each line to one line. Where a whole group shares a situation, still give
each text its own line — the merged file is a worklist, and a reader must be
able to act on any single row without reading the ones around it.

**Sort your lines by decision word**, all the `copyrighted` together and so on,
so the file can be skimmed for the decisions that need making.

At the top of your file put three or four sentences: how many texts you
audited, how many you opened the source file for, and anything that surprised
you. At the bottom, under `## Metadata corrections`, list any `metadata.json`
whose `translator`, `year_written` or `year_translated` disagrees with the file
— author, field, what it says, what the file says. Do not fix them.

## Honesty

`undetermined` is a real answer and a useful one. A confident wrong verdict is
much worse than an honest gap, because someone will act on it. If you cannot
open a source, cannot find a date, or cannot tell which of two editions you are
holding, say that in the line. Do not guess to make the file look complete.
