#!/usr/bin/env python3
r"""Compare two independent runs over the SAME pages, and report where they agree.

Why this exists. Most error families in this corpus have a structural licence --
something in the text itself that says whether a reading is right. A chord and
its arc check each other through Crd(theta) = 120*sin(theta/2); a doubled degree
sign is verifiable because the two-right-angles value is exactly twice the
four-right-angles one. Where such a licence exists, one run plus a verifier
beats two runs, and costs less.

The zodiac has no such licence. The glyphs failed essentially every time, and a
wrong sign leaves no arithmetic residue unless the text happens to state a
difference. So for this family the only detector available is DISAGREEMENT
BETWEEN RUNS -- which is worth paying for precisely because it is the only thing
that works here, and worth NOT paying for everywhere else.

The unit of comparison is (line, what-the-markdown-says), not the finding text.
Two runs describe the same defect in different words -- "the printed glyph is
Libra" and "LIBRA 6 degrees" are the same claim -- so comparing prose would
manufacture disagreement. Comparing the normalised TARGET of the claim does not.

Three outcomes, and the middle one is the point:

  AGREED      both runs found it and read it the same way. Apply.
  CONFLICT    both found it and read it DIFFERENTLY. Never apply; needs a page.
                This is the class that a single run reports with high confidence
                and gets wrong, which is the entire argument for double-running.
  SOLO        one run found it, the other did not. Not a contradiction -- recall
                is imperfect -- but not corroborated either. Held.

  ocr/proofreading/compare-runs.py <batch-a> <batch-b>
"""
import argparse, json, os, re, sys


def findings(path):
    """Locate the findings array wherever the schema nested it."""
    with open(path) as fh:
        doc = json.load(fh)

    def walk(node):
        if isinstance(node, list) and node and isinstance(node[0], dict) \
                and 'claim' in node[0]:
            return node
        if isinstance(node, dict):
            for value in node.values():
                found = walk(value)
                if found:
                    return found
        return None

    return walk(doc) or []


SIGNS = ("aries taurus gemini cancer leo virgo libra scorpius scorpio "
         "sagittarius capricorn capricornus aquarius pisces").split()


def reading(f):
    """The substance of the claim, stripped of how it was phrased.

    A sign name anywhere in the 'printed' field IS the reading -- the runs wrap
    it in different sentences but the name is the decision. Everything else
    falls back to a normalised form of the field.
    """
    printed = (f.get('printed') or '').lower()
    for s in SIGNS:
        if re.search(r'\b' + s + r'\b', printed):
            return 'SIGN:' + ('scorpius' if s.startswith('scorpi') else
                              'capricorn' if s.startswith('capricorn') else s)
    if 'raised roman p' in printed or 'parts' in printed:
        return 'PARTS'
    if 'doubled' in printed or 'two degree' in printed or 'second degree' in printed:
        return 'DOUBLED-DEGREE'
    return 'OTHER:' + re.sub(r'\s+', ' ', printed).strip()[:40]


def key(f):
    """Identify the SPOT, so the same defect from two runs collides.

    Keyed on the page and the OFFENDING MARKDOWN, not on the quote. Two runs
    locate the same defect with different surrounding context -- they choose
    different amounts of it, and start in different places -- so a quote prefix
    splits one shared finding into two apparent solos. Measured on the first
    pair: keying on a 48-character quote prefix reported 12 shared and 34 solo;
    keying on the markdown token reported 11 shared and 1 solo, over the same
    two files. The difference was entirely an artefact of the key.

    The quote is used only where the markdown is EMPTY -- the sign-left-no-trace
    class, which has no offending token to key on and is locatable only by
    position.
    """
    md = re.sub(r'\s+', '', (f.get('markdown') or '')).strip().lower()
    if md:
        return (f.get('page'), md[:24])
    quote = re.sub(r'\s+', ' ', (f.get('quote') or '')).strip().lower()
    return (f.get('page'), 'AT:' + quote[:32])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('batch_a')
    ap.add_argument('batch_b')
    ap.add_argument('--signs-only', action='store_true',
                    help='restrict to zodiac claims, the family this is for')
    args = ap.parse_args()

    runs = []
    for batch in (args.batch_a, args.batch_b):
        path = os.path.join(batch, 'result.json')
        if not os.path.exists(path):
            sys.exit(f'no result.json in {batch}')
        runs.append(findings(path))

    indexed = []
    for run in runs:
        table = {}
        for f in run:
            if args.signs_only and not reading(f).startswith('SIGN:'):
                continue
            table.setdefault(key(f), []).append(f)
        indexed.append(table)
    a, b = indexed

    agreed, conflict, solo_a, solo_b = [], [], [], []
    for k, fa in a.items():
        if k not in b:
            solo_a.extend(fa)
            continue
        ra = {reading(f) for f in fa}
        rb = {reading(f) for f in b[k]}
        (agreed if ra == rb else conflict).append((k, ra, rb, fa[0]))
    for k, fb in b.items():
        if k not in a:
            solo_b.extend(fb)

    print(f'{os.path.basename(args.batch_a)}  vs  {os.path.basename(args.batch_b)}')
    print(f'  findings: {len(runs[0])} and {len(runs[1])}'
          f'{"  (zodiac only)" if args.signs_only else ""}')
    both = len(agreed) + len(conflict)
    print(f'  found by both runs : {both}')
    if both:
        print(f'      agreed         : {len(agreed)}  ({100*len(agreed)/both:.0f}%)')
        print(f'      CONFLICTING    : {len(conflict)}')
    print(f'  seen by A only     : {len(solo_a)}')
    print(f'  seen by B only     : {len(solo_b)}')

    if conflict:
        print('\nCONFLICTS — two confident runs, two different readings. Do not apply:')
        for k, ra, rb, f in conflict:
            print(f'  p{k[0]}  md={f.get("markdown","")!r}')
            print(f'      A: {sorted(ra)}')
            print(f'      B: {sorted(rb)}')
            print(f'      quote: {f.get("quote","")[:70]}')

    if agreed:
        print('\nCORROBORATED (both runs, same reading):')
        for k, ra, _, f in sorted(agreed, key=lambda x: (x[0][0] or 0, x[0][1])):
            print(f'  p{k[0]}  {f.get("markdown","")!r:30} -> {sorted(ra)[0]}')


if __name__ == '__main__':
    main()
