# Escalation: OCR permission granted, but runner network is disabled

The paid Mistral OCR permission was applied exactly as answered, using:

```sh
/Users/zacharygrunenberg/Projects/Enchiridion/ocr/.venv/bin/python3 \
  /Users/zacharygrunenberg/Projects/Enchiridion/ocr/2-extract/ocr.py \
  source/alberunisindiaac01biru-split.pdf source
```

The call failed before connecting to Mistral with
`httpcore.ConnectError: [Errno 8] nodename nor servname provided, or not known`.
This runner has network/DNS disabled. The API received **zero of the 408
prepared pages**, no page-level failures were returned, and no output Markdown
was created. The available tool inventory contains no Mistral/OCR connector that
can accept the local PDF instead.

No new editorial judgment is needed. Please resume this run in an environment
where the authorized command can reach the Mistral API (while retaining access
to `ocr/.env`), or arrange for the same command to be run and resync its
Markdown/images output into `source/`.

What turns on this: stage 2 has no viable local substitute. The supplied PDF
layer was already adjudicated unusable, and using it merely to avoid the network
block would silently reverse the accepted recon decision. Postprocessing,
positive-controlled verification, and a `needs-review` proposal all depend on
the missing OCR output.
