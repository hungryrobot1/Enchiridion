# Withheld texts

Eight texts are present in this working tree and deliberately absent from the
repository. This is the census of them, why each is out, and what would bring it
back.

**The default is to honour copyright.** Where a text is encumbered we do not
publish it, and we do not lean on anyone else's fair-use posture to do so.

## Why "we got it from the Internet Archive" is not a reason

Most of these files came from archive.org, and that fact carries **no
information about rights in either direction.** It is worth writing down why,
because the intuition that it helps is a natural one.

- **IA lost.** *Hachette v. Internet Archive* (2d Cir. 2024) held that controlled
  digital lending was not fair use, on all four factors, against a non-profit
  with an expressly educational mission. That is the nearest precedent to what
  we would be doing, and it runs against us.
- **The shelter would not transfer even if it existed.** Fair use is judged per
  use. IA's lending had an owned copy behind each loan, one-to-one ratios, loan
  periods and DRM. We would publish the whole text, openly and permanently, to
  anyone. On amount and market effect — the two factors IA lost on — our use is
  strictly weaker than the use that already lost.
- **For community uploads there is no fair-use claim to inherit at all.** IA
  hosts those under DMCA safe harbour, which protects a host from what its users
  upload. It says nothing about someone who downloads and republishes, and
  §512(c) is unlikely to reach us in any case, since we publish our own curated
  corpus rather than storing material at the direction of users.
- **No takedown request is not permission.** It is evidence of not having been
  noticed — and a curated curriculum site with a domain, a mission and search
  visibility is far easier to find and attribute than one file in a large
  archive.

*Engineering judgment, not legal advice.*

## The nine

### Public-domain work, encumbered translation (6)

The work is centuries out of copyright in every case. Only the English rendering
is owned — which means the question was never "have this text or not", but "have
*this translation* or not". **Our own translation is the durable fix**, and a
public-domain source exists to translate from for most of them.

| text | translation withheld | in print | translate from |
|---|---|---|---|
| Ptolemy, *Almagest* | G.J. Toomer, 1984 (Princeton) | yes | Halma's French, 1813–16 |
| Fibonacci, *Liber Abaci* | Laurence Sigler, 2003 (Springer) | yes, ~$100, only complete English | Boncompagni's Latin, 1857 |
| Hildegard, *Book of the Rewards of Life* | Bruce Hozeski, 1994 (Oxford) | yes | Migne, *Patrologia Latina* |
| Alhazen, *Optics* I–III | A.I. Sabra, 1989 (Warburg) | — | Risner's Latin, 1572 |
| Averroes, *Incoherence of the Incoherence* | Simon Van Den Bergh, 1954 | out of print | public-domain Arabic |
| al-Farabi, *Philosophy of Plato and Aristotle* | Muhsin Mahdi, 1962 | out of print | Arabic; verify an edition exists |

**Each candidate source must be verified before it is relied on.** The table
records where to look, not what has been confirmed.

A translation we make ourselves is honest work even when it is rough: it can be
published freely, corrected over time, and improved by anyone who reads the
language better than we do. What it must never do is claim more than it has
earned — see `ocr/3-postprocess/STAGE.md` on status, and never mark such a text
`complete` on our own say-so.

### The work itself is in copyright (2)

No translation is involved; these are the papers themselves. **Permission is the
only route**, and asking is a real option that costs nothing to try.

| text | holder to ask |
|---|---|
| Turing, *On Computable Numbers* (1936) | London Mathematical Society |
| Watson & Crick, *Molecular Structure of Nucleic Acids* (1953) | Springer Nature |

This is the shape of the whole of section 8, where **56 of 57 pending texts were
published after 1930.** Rights, not sourcing, will decide what the modern era's
curriculum can be — and much of it cannot be solved by translating, because
there is nothing to translate.

### Cleared, and worth recording as a near miss

**`aristotle-collective-works` is NOT withheld.** It was flagged only because its
translator read "Various" with no year, and it was briefly withheld on a guess
that 1.14 million words of Aristotle from an archive download would be the
Revised Oxford Translation (Barnes, 1984, Princeton).

**The guess was wrong, and the file says so on its first page:** *"The Works of
Aristotle, translated under the editorship of W. D. Ross"*, with the individual
translators named — Edghill, Jenkinson, Mure, Pickard-Cambridge. "Barnes"
appears nowhere in it. That is the Oxford Translation of 1928, and it is public
domain. The attribution is now recorded in `metadata.json`, with a `rights`
field, so the question is asked once.

The lesson is the one the pipeline keeps teaching: **the file settles it, and a
missing metadata field is a gap in our record rather than evidence about the
work.** A plausible story about provenance is not provenance. The Organon texts
already in the corpus were extracted from this same file and independently
attributed to those same 1928 translators — which was the evidence sitting in
plain view the whole time.

## What "withheld" means mechanically

- The directory stays on disk, with its sources, transcription, images and
  review notes. Nothing is deleted.
- The directory is listed in `.gitignore` and untracked, so it is not in the
  published repository.
- `metadata.json` is renamed to `metadata.withheld.json`, which keeps
  `build-index` from indexing it.
- `build-index` also asks git which text directories are tracked and skips the
  rest — the reader fetches markdown raw from the repo, so an untracked text
  would otherwise be an entry whose every link 404s.
- Entries are removed from `syllabi/grand-tour.json` and, where present, from
  `site/src/lib/sample-works.js`.
- **Supplement → text pointers are left in place.** `resolveItem` returns null
  for an id it cannot resolve, so the grand tour degrades quietly, and the
  pointer records the pairing for when the text returns.

To restore one, reverse those five steps; the `.gitignore` section lists them.

## Open: the history

**These files were committed and pushed before this decision, so they remain in
the git history**, reachable by commit SHA even though they are absent from the
current tree. Removing them means rewriting history — `git filter-repo` or
equivalent — and a force push that invalidates every existing clone and SHA.

**Deferred deliberately** until this census is complete, which it now is. That
conversation should decide it once, for all nine at once, rather than piecemeal.
