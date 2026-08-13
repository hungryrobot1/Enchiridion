## For the reviewer

The proposed file is `du-bois-the-souls-of-black-folk.md`. The supplied witness
is a 260-page, born-digital PDF of Brent Hayes Edwards's 2007 Oxford World's
Classics edition. Its “Note on the Text” says the edition reproduces the first
edition published by A. C. McClurg on 18 April 1903. I did not independently
verify that editorial claim, and there is no second witness in `source/`.

The transcription keeps the complete 1903 work: title leaf, Du Bois's
dedication, Forethought, chapters I–XIV, and After-Thought. It removes the Oxford
introduction, Note on the Text, Select Bibliography, chronology, edition
contents leaf, explanatory notes, and three separately published pieces added
as appendices (“The Conservation of Races,” “The Talented Tenth,” and the
self-review/anniversary preface). Those appendices are Du Bois's writing but are
not part of *The Souls of Black Folk*. The authorial dedication stays; the
edition contents page goes under the pipeline's contents-page policy.

The prose is not OCR. It comes from the PDF's embedded text layer, with paragraph
starts, set-off verse, italics, line-wrap hyphenation, and page-turn continuation
recovered from glyph geometry. This strongly establishes fidelity to the PDF's
own encoding, not correctness against the 1903 printing: the PDF and its text
layer are two products of the same typesetting act, not independent witnesses.
No prose reading was changed on a visual hunch. Mechanical repairs were limited
to ligature expansion and line-wrap joins where the adjacent lowercase fragment
made one word; edition spellings and punctuation remain.

Oxford points from the body to its explanatory notes with 145 Baskerville
asterisk glyphs. Those navigation markers were removed with the editorial notes.
Two three-glyph asterisms on printed pages 14 and 32 are authorial structure and
remain as `* * *`. The build asserts all 151 source asterisks and accounts for
them as 145 removed pointers plus six retained asterism glyphs.

The PDF text layer entirely omits the printed music. Nineteen vector-drawing
regions were found and rasterized directly: chapter openings on printed pages
7, 15, 33, 45, 54, 63, 77, 93, 111, 128, 140, 145, 153, and 167, plus music
within chapter XIV on pages 170, 172, 173, 176, and 177. I reviewed a contact
sheet for crop completeness and order; all are legible and complete. I did not
verify the music note by note. Check these first, especially the final song split
across pages 176–177. The raster images preserve what this edition prints rather
than translating the notation into another system.

There is no bounded list of doubtful OCR readings because no OCR was used. The
bounded open question is the nineteen music images above: crop fidelity was
checked, musical correctness was not. The prose still needs ordinary cover-to-
cover review against the rendered PDF, with special attention to italics that
cross font-subset boundaries and hyphenated compounds at line ends.

## Source identity and route

`metadata.json` correctly names W. E. B. Du Bois, *The Souls of Black Folk*,
English, 1903. The actual file is the Edwards-edited 2007 Oxford edition named
on its title and copyright pages; the core work metadata is not contradicted.
Recon reported `ROUTE: pdf-native` because PDFsharp produced a usable born-
digital text layer. That is correct for the prose. Recon's single-image inventory
did not report the nineteen vector musical regions, so the route needed a
figure-track supplement that its verdict did not name.

No network search for another source was performed. The repository is
read-only, external access requires permission, and the held source was adequate
to produce a reviewable transcription. Consequently I could not establish an
independent witness or independently test Oxford's first-edition claim.

## Preparation

`prepare_dubois.py` asserts the 260-page source, boundary text, and the next
excluded leaf, then keeps source PDF pages 38–215 inclusive (178 pages). It drops
pages 1–37 and 216–260. The first retained leaf is the work's title; the last is
the After-Thought ending “THE END”; the next source leaf begins Appendix I.

No crop was applied. Ordinary running heads and folios are deterministically
excluded by geometry, while the chapter epigraphs and music occupy unusually
high and low regions; a blanket crop risked deleting authorial material.

The shared duplicate-leaf scanner asserted 178 prepared pages. Its planted copy
of page 7 was detected (one exact group and one fuzzy hit). The real scan covered
1,177 fuzzy comparisons across 174 evidence-bearing pages and found zero exact
groups and zero fuzzy candidates.

## Extraction and post-processing

`build_dubois.py` is the reproducible extraction/post-processing tool. Its
source-specific assertions cover page count, chapter page sequence, the exact
nineteen drawing pages, fourteen output chapters, nineteen image references,
151 source asterisk glyphs and their disposition, and exclusion of appendices
and explanatory notes. Its last run produced 400,921 characters, 431 paragraphs,
34 verse/epigraph blocks, and 19 music images.

`verify_dubois.py` independently checks conservation. It found an exact
normalized long-line anchor in the final text for every one of the 174
substantive work pages. It accounts separately for the title, dedication,
removed contents leaf, and blank leaf, then asserts fourteen chapters, the
opening title, final “THE END,” apparatus absence, and a one-to-one match between
nineteen unique references and nineteen files. This is a completeness check,
not character-level proofreading.

The figure audit first passed all its shipped controls. It then found 19 images
on disk and 19 distinct references, with no referenced-but-absent,
present-but-unreferenced, duplicate, or thumbnail candidates. Its reported reach
was only one of four witnesses: musical passages have no printed numbering
sequence, and the audit's source-artifact check does not inspect vector drawings
inside PDFs. I therefore also asserted the drawing-page inventory in the build
and visually inspected the complete contact sheet.

The controlled diagnostic triad passed: each checker rejected its planted
defect, then `lint-math.py`, `check-math.js`, and `check-raw-latex.js` returned
clean. There are zero math blocks, so this establishes Markdown/renderer hygiene
only. It says nothing about prose correctness or musical notation. The math
vocabulary census correctly reported that no Markdown text with math was found.

## Status and remaining limits

This is honestly proposable at `needs-review`, not complete. I did not change
`ocr_status`. Stage 4 has no mechanical acceptance test, and the whole prose was
not visually proofread against all 178 prepared pages. No `ESCALATION.md` is
present because no human decision is currently required to adopt the bounded,
machine-checked artifact for review.

Time went mainly to recovering structure the generic PDF extractor flattens and
to discovering, extracting, and visually checking the vector music. The source
is unusually favorable for prose, so character recovery itself was fast.

## Where this was harder than it needed to be

The route and apparatus rules required reading long, overlapping documents to
extract a few operative facts. The decisive PDF-native rule is easy to find;
the fact that its generic extractor collapses a publisher PDF's page-sized text
blocks into single paragraphs becomes clear only later, from a precedent under
an author-specific tool directory. I also looked for source identity as a
per-file command because the stage lists `check-source-identity.py`; the script
is instead a corpus-level command and rejects PDF/metadata arguments.

I had to build a geometry-aware prose and vector-music extractor. I expected the
PDF-native path to preserve paragraph structure, italics, verse, and non-image
page graphics, but the shipped extractor joins every line in a PDF block and
explicitly skips non-text blocks. I also had to build a conservation check for a
PDF-native prose book; the documented completeness command is specific to EPUB,
while the raw-page separator check is specific to OCR.

The ordering fought the run at recon: the clean PDF-native headline arrived
before any warning that nineteen pieces of meaningful notation existed only as
vector drawing commands. The generic image count was one and looked reassuring;
visual inspection of a chapter opening was what exposed the loss. The figure
audit was useful only after extraction and could compare the two lists I had
already produced, not discover PDF vector material lost from both.

The ambiguous choices were whether the three Du Bois appendices belonged to the
work, whether Oxford's asterisks were authorial marks, and whether music should
be transcribed semantically or preserved visually. I classified the appendices
as edition-added separate works because their brackets give independent
publication histories; classified the 145 Baskerville stars as navigation to
removed editorial notes while retaining the two spaced authorial asterisms; and
preserved all music as page-derived images because translating it into a music
encoding would introduce a new act of transcription.
