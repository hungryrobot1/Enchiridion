# §8 Modern Era II — rights audit, slice B (mcluhan-understanding-media onward)

Audited all 35 texts in the slice. Opened the source PDF/HTML front matter for 32
of them (three — `weil-gravity-and-grace`, `rumelhart-hinton-williams-...`, and
`wilkes-microprogramming` — are scanned-image PDFs with no text layer at all;
`pymupdf` and `pdftotext` both return empty, so those were read from their
already-transcribed `.md` companions instead, which quote the title/copyright
page verbatim). Two were already `metadata.withheld.json` before I started
(`turing-on-computable-numbers`, `watson-crick-...`) and two were named already
BLOCKED in the task brief (`vaswani-shazeer-...`, `wilkins-stokes-wilson-...`);
I recorded all four as settled rather than re-deriving them, per instructions.
Biggest surprises: `oconnor-the-geranium`'s source is not O'Connor's published
book at all but her 1947 University of Iowa MFA thesis, sourced from Wikisource;
`stepanov-mcjones-elements-of-programming`'s file names Pearson Education 2009
copyright explicitly, correcting the vague "in print" note in `RIGHTS.md`; and
`ortega-gasset-the-public-and-its-problems` — Ortega's 1930 Spanish original is
clear, but the 1932 Norton translation was renewed in 1960 (found via web
search, renewal claimant Teresa Carey, translator J. R. Carey), so it stays
encumbered until 1 Jan 2028, not PD now as `RIGHTS.md`'s "almost certainly
open" framing might suggest.

## copyrighted

Mankiewicz and Wachowski, The Matrix (Screenplay), copyrighted — studio-held, no authorised published text, per task brief and `RIGHTS.md`
McLuhan, Understanding Media, copyrighted — Marshall McLuhan, 1964, in print; file confirms 1964 first edition, no PD claim possible
O'Connor, The Geranium: A Collection of Short Stories, copyrighted — source is O'Connor's 1947 University of Iowa MFA thesis (unpublished at the time), sourced from Wikisource; unpublished-work term is life+70, O'Connor d. 1964, so protected until 2034 regardless of publication history
Rumelhart, Hinton, and Williams, Learning Internal Representations by Error Propagation, copyrighted — the source file (`Chap8_PDP86.pdf`) is Chapter 8 of MIT Press's *Parallel Distributed Processing* (1986), still in print, not the shorter 1986 *Nature* letter our title implies; flag this as a sourcing mismatch as well as a rights one
Stepanov and McJones, Elements of Programming, copyrighted — title page states "Copyright © 2009 Pearson Education, Inc. Portions Copyright © 2019 Alexander Stepanov and Paul McJones. All rights reserved."; this Semigroup Press printing is not a freely-licensed release
Strauss, Historicism and Modern Relativism, copyrighted — title page: "© 2016 Estate of Leo Strauss. All Rights Reserved." (Leo Strauss Transcript Project, University of Chicago)
Strauss, Natural Right, copyrighted — same project; explicit "© 2022 Estate of Leo Strauss. All Rights Reserved." found in the file text
Turing, Computing Machinery and Intelligence, copyrighted — *Mind* 59 (1950), Oxford University Press for the Mind Association; a foreign 1950 work, restored under URAA (still under UK copyright as of the 1996 URAA date), running 95 years from publication to roughly 2046 — same shape as the already-withheld 1936 paper, just a different clock
Turing, On Computable Numbers, copyrighted — already `metadata.withheld.json`; settled per `SOURCING.md`, not re-derived
Vaswani, Shazeer, et al., Attention Is All You Need, copyrighted (blocked) — already determined: arXiv's default licence grants arXiv distribution, not us; settled, not re-derived
Watson and Crick, Molecular Structure of Nucleic Acids, copyrighted — already `metadata.withheld.json`; settled per `WITHHELD.md`, not re-derived
Wilkins, Stokes, and Wilson, Molecular Structure of Deoxypentose Nucleic Acids, copyrighted (blocked) — file's own text layer reads "© Nature Publishing Group 1953"; settled per task brief, not re-derived

## translation needed

Ortega y Gasset, The Revolt of the Masses (misfiled as "the-public-and-its-problems" — that title is Dewey's, not Ortega's; see `RIGHTS.md`), translation needed — Spanish original 1930, public domain; the 1932 Norton "authorized translation" (translator withheld at the time, later identified as J. R. Carey) was renewed in 1960 (US copyright renewal, claimant Teresa Carey), so it runs the full 95 years and stays in copyright until 1 Jan 2028 — do not treat as an open translation yet, and a fresh translation from the PD Spanish text is the durable fix in the meantime

## public domain

Trump, Inaugural Address (2017), public domain — already recorded: 17 U.S.C. 105, US government work, verified 2026-08-10
United Nations General Assembly, Universal Declaration of Human Rights, public domain — UN administrative instruction ST/AI/189/Add.9/Rev.1 (1985): "Official Records, United Nations documents and public information material are in the public domain"; the UDHR is GA Resolution 217 A (III), squarely a compilation-of-resolutions official record, not the separately-illustrated commercial edition (whose YAK artwork is copyrighted but irrelevant to our plain-text source)
von Neumann, First Draft of a Report on the EDVAC, public domain — the 1945 Moore School typescript itself is treated as public domain by every archive that hosts it (Smithsonian's own copy is marked CC0); it was circulated as an Army Ordnance contract report without a copyright notice under the 1909 Act, which forfeits protection. Caveat: our specific PDF is Michael D. Godfrey's 2003–2017 annotated edition, which adds his own introduction, corrections, and bracketed material "with copyright permission granted by the APS (2017)" — that editorial layer is not obviously covered by the same PD reasoning as von Neumann's original text, though it is a small fraction of the document
Weber, The Protestant Ethic and the Spirit of Capitalism, public domain — already VERIFIED: Parsons 1930 translation, term expired 1 Jan 2026; recorded in metadata and `RIGHTS.md`

## undetermined

McCulloch and Pitts, A Logical Calculus of the Ideas Immanent in Nervous Activity, undetermined — original is Bulletin of Mathematical Biophysics 5 (1943); our actual file is a 1990 Pergamon Press / Society for Mathematical Biology reprint (Bulletin of Mathematical Biology 52) carrying its own 1990 copyright line — settle both (a) whether the 1943 original was renewed in 1970–71, and (b) whether this reprint's 1990 notice covers only new editorial matter or the whole text
Minsky, Steps Toward Artificial Intelligence, undetermined — Proceedings of the IRE, 1961; needs a renewal check (renewal would have fallen due ~1988–89) or confirmation from IEEE, successor to IRE in 1963
Mullis, The Polymerase Chain Reaction (Nobel Lecture), undetermined — Nobel Foundation publishes lectures on nobelprize.org but asserts copyright there; check the Foundation's actual terms of use for lecture text specifically before assuming open access equals a licence
Nagel, What Is It Like to Be a Bat?, undetermined — Philosophical Review 83 (1974), Duke University Press; needs an individual renewal/rights check, per `RIGHTS.md`'s Journals list
Nirenberg and Matthaei, The Dependence of Cell-Free Protein Synthesis..., undetermined — PNAS 47 (1961); PNAS/National Academy of Sciences rights for papers of this era need checking directly, not assumed
Ritchie, The Development of the C Programming Language, undetermined — Bell Labs / ACM, 1993 (History of Programming Languages II); per `RIGHTS.md`'s ACM list, author-agreement terms of the period vary and need checking
Ritchie and Thompson, The UNIX Time-Sharing System, undetermined — Communications of the ACM 17:7 (1974); our copy is "electronic version recreated by Eric A. Brewer, UC Berkeley," which changes nothing about the underlying ACM copyright — needs the same individual check as the rest of `RIGHTS.md`'s ACM list
Rivest, Shamir, and Adleman, A Method for Obtaining Digital Signatures and Public-Key Cryptosystems, undetermined — Communications of the ACM 21:2 (1978); per `RIGHTS.md`'s ACM list
Sanger, Nicklen, and Coulson, DNA Sequencing with Chain-Terminating Inhibitors, undetermined — PNAS 74 (1977); same PNAS-era question as Nirenberg/Matthaei and Woese/Fox
Searle, Minds, Brains, and Programs, undetermined — The Behavioral and Brain Sciences 3 (1980), Cambridge University Press; per `RIGHTS.md`'s Journals list, needs individual check
Shannon, A Mathematical Theory of Communication, undetermined — BSTJ 1948; already checked in `RIGHTS.md` and confirmed the non-renewal argument does not hold up (Online Books Page's negative result is not proof of non-renewal, and Nokia now licenses the BSTJ archive through IEEE); settled as undetermined, not re-derived
Shannon, A Symbolic Analysis of Relay and Switching Circuits, undetermined — BSTJ 1937; same issue as above, already checked per `RIGHTS.md`, still undetermined
Wadler, Propositions as Types, undetermined — 2015; no explicit licence statement found in the file itself (checked reference list and surrounding text); the author's own web posting of the PDF is not a licence per the charter — need to find and check the original publication venue's copyright terms
Weil, Gravity and Grace, undetermined — the English text we hold (G. P. Putnam's Sons, 1952) is credited on its own title page to ARTHUR WILLS, not "Emma Crawford" as `metadata.json` states, and carries an explicit "COPYRIGHT, 1952, BY G. P. PUTNAM'S SONS. All rights reserved." — this translation is definitely encumbered. What is unresolved is whether the French original (*La Pesanteur et la Grâce*, compiled and published posthumously in 1947; Weil d. 1943) is itself still under US copyright: if restored under URAA at life+70, it would already be PD (2013); if restored at 95-years-from-publication, it runs to 2042. Resolve that calculation to know whether this is `translation needed` or simply `copyrighted`
Wilkes and Stringer, Micro-programming and the Design of the Control Circuits in an Electronic Digital Computer, undetermined — Proceedings of the Cambridge Philosophical Society 49 (1953), a UK venue; a foreign work of this vintage is a URAA-restoration candidate (Wilkes d. 2010, so almost certainly still under UK copyright as of the 1996 URAA date), which would put US expiry around 2048, but this needs confirming rather than assuming
Wilkes, Slave Memories and Dynamic Storage Allocation, undetermined — IEEE Transactions on Electronic Computers, 1965; per `RIGHTS.md`'s IEEE list, needs individual check
Woese and Fox, Phylogenetic Structure of the Prokaryotic Domain, undetermined — PNAS 74 (1977); same PNAS-era question as Nirenberg/Matthaei and Sanger et al.
Woese, Kandler, and Wheelis, Towards a Natural System of Organisms, undetermined — PNAS 87 (1990); well within the modern PNAS regime, no PD argument available, needs a direct rights check with PNAS/NAS

## Metadata corrections

- `weil-gravity-and-grace/metadata.json` — `translator` reads "Emma Crawford"; the file's own title page credits "TRANSLATED BY ARTHUR WILLS" (G. P. Putnam's Sons, 1952). These are two different people; the metadata translator field is wrong.
- `ortega-gasset-the-public-and-its-problems/metadata.json` — `translator` is null; the 1932 Norton "authorized translation" is now identifiable as J. R. Carey (per the 1960 US copyright renewal record, claimant Teresa Carey), which is also what settles this text's rights status.
- `stepanov-mcjones-elements-of-programming` — `RIGHTS.md` names the publisher as "Addison-Wesley 2009"; the file's own copyright page says "Pearson Education, Inc." (Addison-Wesley's parent/imprint owner) with "Portions Copyright © 2019 Alexander Stepanov and Paul McJones" for this particular Semigroup Press printing — not a contradiction, but worth recording precisely since two different entities hold rights in the same file.
