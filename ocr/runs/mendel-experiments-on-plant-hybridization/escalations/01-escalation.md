# HANDOFF — correct source required

Replace the supplied EPUB/PDF with a source for Gregor Mendel's *Experiments on Plant Hybridization*, then resume this run at stage 0.

Both current files are unambiguously the wrong work: Herbert F. Peyser's *Robert Schumann: Tone-Poet, Prophet and Critic*. The EPUB package metadata names Peyser, Schumann, and Project Gutenberg ebook 49378; the PDF's opening text and title page name the same work. The files in this workspace are byte-for-byte identical to those in the repository text directory, so there is no alternate local witness to use.

What turns on the replacement source:

- Recon and the extraction route cannot be chosen until the actual file is present. Run `0-recon/recon-epub.py` first if the replacement includes an EPUB, then `0-recon/recon-pdf.py` on any PDF.
- If an EPUB carries recoverable notation, use `2-extract/extract-epub.py --report`; otherwise route according to the new recon evidence.
- The current metadata describes the intended Mendel/Bateson text, but its edition details must be checked against the replacement's title page before processing.
- No page ranges, crop, or duplicate-leaf scan are reported because preparing the Schumann booklet would prepare the wrong work. If the replacement routes to OCR, stage 1 must perform and document all of those checks before the manual OCR handoff.

Reproduce the identity failure with:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 audit_source_identity.py
```

No network acquisition was attempted: external access requires permission, and a correct source supplied by the library owner also settles which edition/translation is intended.
