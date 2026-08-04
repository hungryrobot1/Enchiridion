# Escalation: authorized OCR is blocked by the execution environment

The acquisition decision is resolved: do **not** search the network, and use the
paid Mistral OCR API on the prepared PDF. I followed that answer.

The repository command failed before any upload or API response:

```text
Calling Mistral OCR API...
httpcore.ConnectError: [Errno 8] nodename nor servname provided, or not known
```

This session has no outbound DNS/network access and exposes no approved Mistral
OCR connector. Therefore:

- prepared PDF pages: **146**;
- pages sent to Mistral: **0**;
- API page failures: **none** (the request never reached the service);
- API charge from this attempt: **none expected**;
- raw markdown/images produced: **none**.

I need one of the following execution remedies:

1. Resume this run in an environment that permits outbound HTTPS/DNS access to
   the Mistral API; or
2. Run the following already-authorized command outside this restricted session
   and re-sync its `raw/pdfs.md` plus any `raw/images/` output into the workspace:

   ```sh
   mkdir -p raw
   /Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
     /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/ocr.py \
     tmp/pdfs/anselm-prepared.pdf raw
   ```

What turns on this: stage 3 requires the stage-2 markdown. There is no honest
post-processing, diagnostic-triad, source-page repair, or `PROPOSED.md` work to
perform until that output exists. The prepared PDF and asserted preparation
scripts remain ready and unchanged. No network acquisition was attempted.
