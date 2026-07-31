#!/usr/bin/env python3
r"""Map PDF pages to line ranges in the markdown, so a page range names a text range.

Proofreading a scan means holding the print and the markdown side by side, which
needs an answer to "which markdown covers page N". Our pipeline strips page
numbers (strip-page-numbers.py), so the markdown carries no marks to go by, and
telling each reader to "consult the table of contents" makes every one of them
redo the same fallible lookup.

A scanned PDF of this kind carries an invisible OCR text layer -- in Toomer's
Almagest the font is literally named GlyphLessFont, i.e. Tesseract. Its rendering
of the MATH is garbage, which is the problem we are chasing in the first place;
its rendering of ordinary PROSE is fine. So prose is the shared key: take a
distinctive sentence fragment from a page's text layer, find it in the markdown,
and the page is located.

Anchors must be long, alphabetic, and unique in BOTH documents, and matches are
required to advance monotonically -- a page's anchor has to land after the
previous page's. That is what throws out coincidental hits in running heads and
repeated table stubs. Whitespace is matched flexibly, because our post-processing
rewraps lines and the text layer breaks them at the column.

Pages with no trustworthy anchor are REPORTED, never guessed at. Expect the
front matter, the plates, and any run of pure tables to be unresolvable: they
have no prose to key on. A long unresolved run is a signal, not a bug -- in the
Almagest it is the star catalogue, which wants arithmetic checking rather than
proofreading anyway.

  python3 ocr/4-proofread/align-pages.py ptolemy-almagest -o pagemap.json
"""
import argparse, glob, json, os, re, sys


def anchor_candidates(page_text):
    """Longest prose runs on a page: words only, no digits or symbols."""
    out = []
    for line in page_text.split('\n'):
        for run in re.findall(r"[A-Za-z][A-Za-z',\- ]{28,}", line):
            r = re.sub(r'\s+', ' ', run).strip()
            if r.count(' ') >= 4:
                out.append(r)
    return sorted(set(out), key=len, reverse=True)[:8]


def flexible(anchor):
    """Match the anchor across any rewrapping of whitespace."""
    return re.compile(r'\s+'.join(re.escape(w) for w in anchor.split(' ')))


def align(md, doc):
    line_starts = [0]
    for m in re.finditer(r'\n', md):
        line_starts.append(m.end())

    def line_of(off):
        lo, hi = 0, len(line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if line_starts[mid] <= off:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1

    anchors, unresolved, cursor = [], [], 0
    for i in range(doc.page_count):
        found = None
        for cand in anchor_candidates(doc[i].get_text()):
            rx = flexible(cand)
            hits = [m.start() for m in rx.finditer(md)]
            if len(hits) != 1 or hits[0] < cursor:
                continue
            found = (cand, hits[0])
            break
        if found:
            off = found[1]
            anchors.append({'page': i, 'offset': off, 'line': line_of(off),
                            'anchor': found[0][:70]})
            cursor = off
        else:
            unresolved.append(i)
    return anchors, unresolved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('text_id')
    ap.add_argument('-o', '--out', help='write pagemap JSON here')
    args = ap.parse_args()

    import pymupdf
    idx = json.load(open('site/public/text-index.json'))
    rec = next((t for t in idx['texts'] if t['id'] == args.text_id), None)
    if rec is None:
        sys.exit(f'no such text: {args.text_id}')
    md = open(rec['path'], encoding='utf-8').read()
    pdfs = glob.glob(os.path.join(os.path.dirname(rec['path']), '*.pdf'))
    if not pdfs:
        sys.exit(f'no source PDF beside {rec["path"]}')
    doc = pymupdf.open(pdfs[0])

    anchors, unresolved = align(md, doc)
    pct = 100 * len(anchors) // doc.page_count if doc.page_count else 0
    print(f'{rec["path"]}\n{os.path.basename(pdfs[0])}: {doc.page_count} pages')
    print(f'anchored {len(anchors)} ({pct}%)   unresolved {len(unresolved)}')

    if len(anchors) > 1:
        gaps = sorted(b['line'] - a['line'] for a, b in zip(anchors, anchors[1:]))
        print(f'lines between anchored pages: median {gaps[len(gaps)//2]}, max {gaps[-1]}')
    # A long unresolved RUN means a structurally different stretch (tables,
    # plates) — worth naming, because it should probably be handled another way.
    runs, start = [], None
    for i in range(doc.page_count):
        if i in set(unresolved):
            start = i if start is None else start
        elif start is not None:
            if i - start >= 8:
                runs.append((start, i - 1))
            start = None
    if runs:
        print('\nlong unresolved runs (handle these arithmetically, not by eye):')
        for a, b in runs:
            print(f'   pages {a}-{b}  ({b - a + 1} pages)')

    if args.out:
        json.dump({'text_id': args.text_id, 'pdf': os.path.basename(pdfs[0]),
                   'md': rec['path'], 'pages': doc.page_count,
                   'anchors': anchors, 'unresolved': unresolved},
                  open(args.out, 'w'), indent=1)
        print(f'\nwrote {args.out}')


if __name__ == '__main__':
    main()
