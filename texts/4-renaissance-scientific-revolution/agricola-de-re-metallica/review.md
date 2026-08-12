# De Re Metallica — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `agricola-de-re-metallica.md`
- Translator: Herbert Clark Hoover, Lou Henry Hoover (1912)
- Processed by run [`ocr/runs/agricola-de-re-metallica`](../../../ocr/runs/agricola-de-re-metallica) (gpt-5.6-sol, 2026-08-12)
- Full processing notes: [`ocr/runs/agricola-de-re-metallica/NOTES.md`](../../../ocr/runs/agricola-de-re-metallica/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### For the reviewer

The proposed text uses all 291 full-resolution Gutenberg woodcuts supplied
after the initial escalation. The figures are integral to Agricola's
explanations; check several densely lettered machine figures first, then the 17
tables (especially the large needle/assay tables in Books VII and XI), the 25
Greek spans, and the reconstructed opening drop caps of the dedication and each
book. Visual spot-checks of dense originals `fig365.jpg`, `fig470.jpg`, and
`fig277.jpg` confirmed that their letter labels and printed captions are clear.

The only textual witness supplied is Project Gutenberg's structured HTML
transcription of the Hoover & Hoover 1912 translation. It can establish that
the derived Markdown is faithful to that transcription; it cannot establish
that Gutenberg or the Hoovers read the 1912 printed page correctly. No
independent scan or second transcription is present. I made no stage-4 reading
repairs and did not adjudicate any spelling against a printed page. The exact
visible stream comparison currently accounts for 189,669 word/number tokens.

The build retains Agricola's dedication and all twelve books. Following the
brief, it removes the Hoovers' translators' preface, introduction, all 13
work-range footnote regions (359 notes), and the exactly corresponding 359 body
calls. It also removes the non-work Fabricius laudation, appendices A-C,
indices, and Gutenberg transcriber's notes. No unattributed note remains: the
source marks this apparatus uniformly, and its contents repeatedly speak in the
Hoovers' editorial voice. Agricola's 291 woodcuts and their lettered captions
stay; 13 ornamental drop-cap images in the work are reconstructed as their
single textual letters.

There is no page-indexed list of doubtful repaired readings because none were
repaired and no printed-page witness was supplied. The bounded open question is
global: the full transcription still needs stage-4 comparison against the 1912
edition. Source page-number spans were edition furniture and were removed from
reader output, but remain in the HTML for a future alignment.

### Route and source identity

`recon-html.py --self-test` passed its positive and negative controls. Recon
found 328,801 source words, 303 unique local `src` assets, no missing `src`
assets, and no image-carried notation. Its initial verdict was UNDETERMINED.
Visual inspection of three distributed samples (`fig59thumb.jpg`,
`fig276thumb.jpg`, and `fig582thumb.jpg`) showed an instrument diagram and two
process woodcuts, not pictures of equations. This resolved the route to
source-native HTML extraction; OCR would add an error source while recovering
nothing unavailable in the markup.

`check-source-identity.py --self-test` proved it can flag a wrong work and wrong
translation and still accept a match. Its corpus check accepted this source as
Agricola's *De Re Metallica*. The file and metadata agree on the Hoover & Hoover
translation and the 1912 edition details visible in the captured front matter;
metadata was not changed, and `ocr_status` remains `pending`.

### The brief and the file

I followed the brief's apparatus ruling. Two factual descriptions in it do not
match the file:

- The claimed 585 visible `Fig.` references are actually 585 occurrences of
  `fig…jpg` basenames in markup: 291 thumbnail `src` values, 291 linked original
  `href` values, and three front/back-matter figure references. The visible
  prose contains zero literal `Fig.` labels. The generic sequence audit
  therefore has no true numbered-figure sequence to test.
- The 303/303 “all present locally” result covers resources loaded through
  `src`; it does not cover image anchors. The work has 291 remote original-image
  `href` targets and none was saved in the initial browser capture. That
  escalation was resolved by fetching and verifying the complete original set.

The full source image classification is 291 unique work woodcuts, 16 drop-cap
uses (13 in the work and three in removed furniture), and four centered title
page images in removed furniture: 311 `<img>` uses total over 303 unique local
assets. The work's 291 thumbnails and 291 supplied originals are each complete
and distinct; only the originals ship with the proposed Markdown.

### Build and verification

`build_agricola.py` is the count-guarded derivation. It asserts the two direct
HTML boundary positions, the 13/359/359 apparatus census, the Book I-XII
sequence, 17 retained work tables, 291 unique work images, and 13 reconstructed
drop caps. It preserves tables as minimal structural HTML because Markdown
cannot represent their spans; the retained tables contain 16 `colspan`
attributes. The proposed full-resolution build is 1,050,348 characters and ends
at `END OF BOOK XII.` It prefers a complete full-resolution set when one exists
and refuses a partial set.

`verify_agricola.py` independently reselects the work from the source and
compares its visible word/number stream with the Markdown. It passed at 189,669
tokens, verified title + dedication + Books I-XII, reconciled 291 references to
291 files, proved every shipped figure byte-identical to its supplied original,
checked the 17 tables and 16 spans, and confirmed that Hoover apparatus, edition
furniture, navigation attributes, replacement characters, and `toc.json` are
absent.

The controlled diagnostic triad proved all three checkers can reject their
planted defect, then reported no findings on the candidate. This work contains
no LaTeX math blocks, so the KaTeX arm scanned zero blocks and says nothing
about textual correctness. The raw-LaTeX consumer still ran the Markdown
renderer and found no surviving backslashes; the delimiter linter found no
issues. On the final run each tool explicitly reported one file scanned.

`audit-figures.py --self-test` passed all controls. On this text it reconciled
291 Markdown references to 291 local files with no dangling or orphaned finding.
Its density guard correctly rejected both apparent sequences—`Fig 40–591` and
`Plate I–C`—as sparse ordinary prose uses rather than numbering schemes, and
reported no defect. It cannot use HTML as its `--source` artifact, so recon plus
the text-specific verifier carry source coverage here.

`fetch_agricola_originals.py` was run externally after escalation and verified
291/291 JPEGs. Its asserted manifest contains 291 unique exact Gutenberg URLs
and output names, from `fig40.jpg` through `fig591.jpg`, limited to the work and
excluding all footnotes. The resumed build copied that complete set and removed
all generated thumbnail-mode files.

### Decisions made without escalation

The long dedication is authorial presentation and stays under the stage-3
front-matter rule. The Fabricius laudatory poem is someone else presenting
Agricola and is edition furniture, so it goes. Woodcut captions stay because
they identify the lettered components used by the surrounding argument.
Span-dependent tables stay as HTML rather than being flattened into visually
plausible but structurally false Markdown. Drop caps are ornaments rather than
figures, but their letters are part of the words, so the images go and the
letters return as text.

### Where this was harder than it needed to be

The documentation was thickest around routing: the README, recon contract, and
extract contract repeat enough surrounding rationale that locating the narrow
HTML consequence required reading all three, even though the eventual rule was
simple. The stage-2 contract explicitly says the rest of the source-native
track has no tool; that left a large, table-heavy Gutenberg HTML book requiring
a new per-text converter and fidelity verifier. I expected a general HTML-to-
reader extraction base analogous to the EPUB extractor, but none exists.

The ordering fought the run at asset completeness. Recon's clean 303/303 result
came first and sounded conclusive; only later inspection of image-bearing
anchors revealed that every one of the 291 full-resolution work images was
remote and absent. That fact would have changed the figure plan immediately.
The cheap generic figure audit happened after conversion and then consumed time
on 97 false plate gaps generated from ordinary prose rather than a printed
sequence.

The choices that could reasonably have gone another way were the heading level
of the dedication, retaining captions as part of the argument, and preserving
all complex tables as raw structural HTML rather than trying to simplify them.
The source and reader rules supported those choices, but no HTML-specific stage
contract settled them automatically.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->

## Review log

Observations, questions and decisions from reading this text. Everything below the marker above belongs to the reviewer and is never regenerated, so append freely — re-adopting the run rewrites only what is above it.
