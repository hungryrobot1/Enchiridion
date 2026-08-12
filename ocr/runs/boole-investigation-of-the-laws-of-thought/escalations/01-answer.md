Acquired. The generating TeX exists and is now in your workspace at `source/15114-t.tex` (939,635 bytes), fetched from https://www.gutenberg.org/files/15114/15114-t/15114-t.tex — the PG convention you inferred from the associated-files directory was right.

Verified before handing it over: it declares `Title: An Investigation of the Laws of Thought` and `Author: George Boole`, carries 3,232 lines containing math, and 27 chapter/section commands. No \\includegraphics, so this text appears to have no figures — confirm that rather than assuming it.

**Route: source-native.** This is the Dedekind case exactly — the published PDF is a pdfTeX rendering of this file, and extraction cannot recover what generating it discarded. Dedekind yielded 0 math blocks from the publisher's PDF and 3,262 from the LaTeX it was generated from, and also rendered 227 instances of a set-relation symbol as the digit 3, silently, with every diagnostic passing. Your escalation avoided that; it was the right call and the reason recon returned UNDETERMINED rather than guessing.

Two things to carry forward. Your stage 1 work on the PDF is not wasted — keep `source/15114-pdf-split.pdf` as a **rendered witness**, the authority on how a passage should look and never on what it says. And your note about physical page 337 sharing Boole's final paragraph with the Gutenberg end marker still applies to the witness, though the TeX should make the content boundary unambiguous.

The .tex half of the source-native track has no tool — both texts done this way were handled by reading the LaTeX directly. If you build something reusable, say so in NOTES.md and it can be promoted.
