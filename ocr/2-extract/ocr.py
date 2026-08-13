#!/usr/bin/env python3
"""
Mistral OCR pipeline for Enchiridion text processing.
Converts scanned PDFs to markdown using Mistral's OCR API.

Usage:
  python ocr.py <pdf_path> [output_dir]

Writes <name>.md into the same directory as the PDF (or output_dir if given),
and saves extracted images to an images/ subfolder alongside the markdown.
<name> is the PDF's own filename with any `-prepared`, `-ocr-ready` or
`-cropped` suffix dropped, so the output name is predictable from the command
you typed.
"""

import sys
import os
import base64
import re
from pathlib import Path
from dotenv import load_dotenv
from mistralai.client import Mistral

# Load API key
load_dotenv(Path(__file__).resolve().parents[1] / ".env")
API_KEY = os.environ.get("MISTRAL_OCR_KEY")


def ocr_pdf(pdf_path: str, output_dir: str | None = None) -> str:
    """Run OCR on a PDF, extract images, and write markdown."""
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # The output name comes from the PDF ITSELF, with its preparation suffix
    # dropped -- `foo-prepared.pdf` writes `foo.md`.
    #
    # It used to come from the PDF's PARENT DIRECTORY, which is right only when
    # the layout happens to be `<text-id>/<anything>.pdf`. Two runs in one wave
    # had to read this file to find that out, and both wrote it into their
    # handoff: Dirac's said the output "will be named ... because ocr.py derives
    # its basename from the input PDF's parent directory", and Leibniz's warned
    # its raw output would land as `source.md` because the prepared file sat in
    # `workspace/source/`. A name nobody can predict from the command they typed
    # is a name they have to go and look up.
    text_id = re.sub(r"-(prepared|ocr-ready|cropped)$", "", pdf_path.stem)
    out_dir = Path(output_dir) if output_dir else pdf_path.parent
    md_path = out_dir / f"{text_id}.md"
    img_dir = out_dir / "images"

    print(f"Processing: {pdf_path.name} ({pdf_path.stat().st_size / 1024 / 1024:.1f} MB)")
    print(f"Output:     {md_path}")

    client = Mistral(api_key=API_KEY, timeout_ms=600_000)

    # Encode PDF as base64 data URI
    with open(pdf_path, "rb") as f:
        pdf_data = base64.b64encode(f.read()).decode("utf-8")

    data_uri = f"data:application/pdf;base64,{pdf_data}"

    print("Calling Mistral OCR API...")
    result = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": data_uri,
        },
        include_image_base64=True,
        extract_header=True,
        extract_footer=True,
    )

    # Extract images and collect page markdown
    pages = []
    image_count = 0

    for page in result.pages:
        md = page.markdown

        if page.images:
            for img in page.images:
                if hasattr(img, "image_base64") and img.image_base64:
                    # Save image file
                    img_dir.mkdir(exist_ok=True)
                    img_filename = img.id  # e.g. "img-0.jpeg"

                    # Strip data URI prefix if present
                    b64 = img.image_base64
                    if b64.startswith("data:"):
                        b64 = b64.split(",", 1)[1]

                    img_path = img_dir / img_filename
                    img_path.write_bytes(base64.b64decode(b64))
                    image_count += 1

                    # Rewrite image reference in markdown to use images/ path
                    md = md.replace(
                        f"({img_filename})",
                        f"(images/{img_filename})"
                    )

        pages.append(md)

    combined = "\n\n---\n\n".join(pages)

    # Write markdown
    md_path.write_text(combined, encoding="utf-8")

    print(f"Written: {md_path} ({len(pages)} pages, {len(combined)} chars, {image_count} images)")

    if hasattr(result, "usage_info") and result.usage_info:
        print(f"Usage: {result.usage_info}")

    return str(md_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ocr.py <pdf_path> [output_dir]")
        sys.exit(1)

    pdf = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    ocr_pdf(pdf, out)
