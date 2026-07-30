#!/usr/bin/env python3
r"""Build a self-contained proofreading batch for one page range.

The batch is everything a reader needs and nothing else: the printed pages as
images, the markdown that claims to transcribe them, the brief, and an empty
findings file. No repository access, no PDF library, no lookups.

That is deliberate. A worker that has to install PyMuPDF, locate the source,
and work out which markdown corresponds to its pages has four ways to fail
before it has looked at anything -- and every worker fails them differently,
which makes the results incomparable. Pre-rendering also means the batch is
identical whichever agent reads it, so a run can be repeated or handed to a
different model without rebuilding the inputs.

Findings come back as JSONL, one record per claim, and NEVER as edits. A
proofreader's judgment about a glyph and a safe transformation of a 1.4MB file
are different skills; keeping them apart means a bad run costs a discarded file
instead of a corrupted text. The repair scripts in text-specific-tools consume
these records with asserted match counts, which is where the safety actually
lives.

  python3 ocr/proofreading/prepare-batch.py ptolemy-almagest 179-184
"""
import argparse, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))

SCHEMA = """\
# One JSON object per line. Append only; do not edit or reorder.
#
# {"page": 182,                      printed page as labelled in THIS batch
#  "quote": "its mean position is",  short verbatim run from the markdown,
#                                    enough to locate the spot unambiguously
#  "markdown": "\\\\aleph 0;45",       what the markdown currently has
#  "printed": "PISCES 0;45",         what the PAGE actually shows, described
#                                    in words if you cannot type the glyph
#  "claim": "zodiac sign lost",      what kind of error this is
#  "confidence": "high",             high | medium | low
#  "evidence": "two arcs joined by a bar; matches Pisces"}
#
# If a page is clean, say so: {"page": 183, "claim": "clean"}
# If something is confusing, say that rather than guessing:
#   {"page": 184, "claim": "unsure", "evidence": "glyph too faint to read"}
"""


def parse_range(spec):
    m = re.fullmatch(r'(\d+)(?:-(\d+))?', spec)
    if not m:
        sys.exit(f'bad page range: {spec} (use 179-184 or 182)')
    a = int(m.group(1))
    b = int(m.group(2) or a)
    if b < a:
        sys.exit('page range runs backwards')
    return a, b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('text_id')
    ap.add_argument('pages', help='PDF page index range, e.g. 179-184')
    ap.add_argument('--pagemap', default=None)
    ap.add_argument('--out', default=None)
    ap.add_argument('--zoom', type=float, default=3.0,
                    help='render scale; 3.0 is ~216dpi, legible for footnotes')
    args = ap.parse_args()

    import pymupdf
    base = args.pagemap or os.path.join(HERE, args.text_id, 'pagemap.json')
    if not os.path.exists(base):
        sys.exit(f'no pagemap at {base} — run align-pages.py first')
    pm = json.load(open(base))
    first, last = parse_range(args.pages)

    out = args.out or os.path.join(HERE, args.text_id, 'batches', f'p{first:04d}-{last:04d}')
    os.makedirs(os.path.join(out, 'pages'), exist_ok=True)

    doc = pymupdf.open(os.path.join(os.path.dirname(pm['md']), pm['pdf']))
    if last >= doc.page_count:
        sys.exit(f'page {last} beyond document ({doc.page_count} pages)')

    mat = pymupdf.Matrix(args.zoom, args.zoom)
    for p in range(first, last + 1):
        doc[p].get_pixmap(matrix=mat).save(os.path.join(out, 'pages', f'p{p:04d}.png'))

    # The markdown slice. Anchors bracket the range; pad by one anchor on each
    # side so a passage straddling a page boundary is not cut in half.
    anchors = pm['anchors']
    inside = [a for a in anchors if first <= a['page'] <= last]
    if inside:
        lo = min(a['line'] for a in inside)
        hi = max(a['line'] for a in inside)
        after = [a['line'] for a in anchors if a['page'] > last]
        hi = min(after) if after else hi + 80
        lo = max(1, lo - 12)
    else:
        sys.exit(f'no anchored page in {first}-{last}; pick a range with prose '
                 f'(unresolved runs are tables or plates — see align-pages output)')

    lines = open(pm['md'], encoding='utf-8').read().split('\n')
    slice_path = os.path.join(out, 'markdown.md')
    with open(slice_path, 'w', encoding='utf-8') as f:
        f.write(f'<!-- {pm["md"]} lines {lo}-{hi}; '
                f'line numbers are the real file\'s, cite them in findings -->\n\n')
        for n in range(lo, min(hi, len(lines)) + 1):
            f.write(f'{n:>6}\N{VERTICAL LINE}{lines[n-1]}\n')

    brief_src = os.path.join(HERE, args.text_id, 'brief.md')
    if os.path.exists(brief_src):
        shutil.copy(brief_src, os.path.join(out, 'BRIEF.md'))
    with open(os.path.join(out, 'findings.jsonl'), 'w') as f:
        f.write(SCHEMA)
    json.dump({'text_id': args.text_id, 'pdf_pages': [first, last],
               'md': pm['md'], 'md_lines': [lo, hi],
               'printed_page_note': 'filenames use the PDF page index, not the '
                                    'printed folio; cite the filename'},
              open(os.path.join(out, 'MANIFEST.json'), 'w'), indent=1)

    n_img = last - first + 1
    size = sum(os.path.getsize(os.path.join(out, 'pages', f))
               for f in os.listdir(os.path.join(out, 'pages'))) // 1024
    print(f'{out}\n  pages/     {n_img} images, {size} KB')
    print(f'  markdown.md  lines {lo}-{hi} ({hi - lo + 1} lines)')
    print(f'  BRIEF.md, findings.jsonl, MANIFEST.json')


if __name__ == '__main__':
    main()
