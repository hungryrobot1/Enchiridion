# Escalation: OCR authorized but outbound network is unavailable

## What happened

The source was prepared as authorized and the Mistral key is configured. I then
invoked the repository's `ocr/2-extract/ocr.py` with the 184-page prepared PDF.
The Mistral client failed while opening its network connection:

```text
httpx.ConnectError: [Errno 8] nodename nor servname provided, or not known
```

The failure occurred before an HTTP connection or API response. Pages prepared:
184. Pages accepted/sent for OCR: 0. OCR result pages: 0. No markdown or image
assets were written, and this attempt should not have incurred an API charge.

## What I need

Either:

1. resume this workspace in an execution environment with outbound DNS/network
   access to the Mistral OCR API, retaining the configured
   `MISTRAL_OCR_KEY`; or
2. run the repository command below in a network-enabled environment and
   re-sync its `source.md` plus `images/` output into this workspace:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/ocr.py \
  source/The_Optics_of_Ibn_Al-Haytham_Books_I-split.pdf .
```

The command must be run from this workspace so its explicit output directory
(`.`) produces `source.md` and `images/` here.

## What turns on it

All remaining work consumes the Mistral result: figure reconciliation,
apparatus removal, paragraph and heading repair, diagnostic controls, notation
census, page-witnessed repairs, and the proposed reader markdown. Substituting
the scan's ABBYY text layer would reverse the answered stage-0 decision and is
not an honest workaround.

## Stage 1 is complete

- `1-prepare/split.py` materialized source PDF pages 5-188.
- `qpdf --show-npages` and PyMuPDF both report exactly 184 prepared pages.
- Rendered boundary inspection confirms prepared page 1 is the Book I division
  leaf and prepared page 184 ends with paragraph 289 and “End of the Third
  Book.”
- `scripts/duplicate_leaf_scan.py` demonstrated its positive control by matching
  prepared page 2 with itself (`sha256_equal=True`, fuzzy ratio `1.000`). It then
  found 0 exact duplicate groups and 0 fuzzy candidates in 1,230 comparisons at
  offsets 1-6 and 16.

