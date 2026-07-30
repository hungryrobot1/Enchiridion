#!/usr/bin/env python3
r"""Score one run against a CONSENSUS of stronger runs over the same pages.

This is not a measure of accuracy. There is no ground truth here short of a
human reading every page, and if we had that we would not need the harness. What
it measures is agreement with a control population -- the readings that two
independent strong runs both produced -- which is the same move used to validate
the parts/degrees repair against the text's own established parts population.

That distinction matters for how the result may be used. A cheap model scoring
well means it agrees with the expensive one, which licenses substituting it. It
does not mean either is right, and a reading both models share is exactly the
kind of error this method cannot see.

Two numbers, and they carry very different weight:

  RECALL        of the consensus readings, how many did this run also find.
                A miss is cheap -- it survives to the next pass.
  CONTRADICTION this run found the same slot and read it as a DIFFERENT sign.
                A contradiction is expensive: one of the two writes a wrong
                sign into the text, and nothing downstream would catch it.

A cheap model with mediocre recall and zero contradictions is usable. A cheap
model with excellent recall and a handful of contradictions is not, and the
headline percentage will hide that, which is why they are reported separately.

  ocr/proofreading/score-against.py <run> --consensus <batch-a> <batch-b>
"""
import argparse, importlib.util, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    'compare_runs', os.path.join(HERE, 'compare-runs.py'))
cr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cr)


def sign_map(batch, by_page=False):
    """{spot: {readings}} for zodiac claims only.

    by_page defaults to FALSE, which is not the obvious choice and was not the
    original one. Runs disagree about which page a finding sits on -- a weaker
    model put a whole page's findings on its neighbour -- and a page-bearing key
    turns every one of those into a miss AND a spurious extra. Measured on the
    first cheap-model comparison, including the page reported 45% recall with 2
    contradictions where the true figures were 82% and 4. It flattered the model
    on the number that matters and punished it on the number that does not.
    """
    path = os.path.join(batch, 'result.json')
    if not os.path.exists(path):
        sys.exit(f'no result.json in {batch}')
    out = {}
    for f in cr.findings(path):
        r = cr.reading(f)
        if not r.startswith('SIGN:'):
            continue
        md = re.sub(r'\s+', '', (f.get('markdown') or '')).lower()
        key = (f.get('page'), md) if by_page else (md or 'AT:' + (f.get('quote') or '')[:32])
        out.setdefault(key, set()).add(r)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('run')
    ap.add_argument('--consensus', nargs=2, required=True,
                    help='two batches whose AGREEING readings form the control')
    ap.add_argument('--by-page', action='store_true',
                    help='include the reported page in the key; see sign_map -- '
                         'runs disagree about page attribution and this distorts both numbers')
    args = ap.parse_args()

    a, b = (sign_map(x, args.by_page) for x in args.consensus)
    control = {k: a[k] for k in a if k in b and a[k] == b[k]}
    run = sign_map(args.run, args.by_page)

    found = [k for k in control if k in run]
    contra = [(k, control[k], run[k]) for k in found if run[k] != control[k]]
    missed = [k for k in control if k not in run]
    extra = [k for k in run if k not in control]

    print(f'{os.path.basename(args.run)}  vs consensus of '
          f'{os.path.basename(args.consensus[0])} + {os.path.basename(args.consensus[1])}')
    print(f'  consensus readings   : {len(control)}')
    pct = 100 * len(found) / len(control) if control else 0
    print(f'  found by this run    : {len(found)}  ({pct:.0f}% recall)')
    print(f'  CONTRADICTIONS       : {len(contra)}')
    print(f'  missed               : {len(missed)}')
    print(f'  claims outside the consensus : {len(extra)}'
          '   (unjudged — may be real finds the strong runs missed)')

    for k, want, got in contra:
        print(f'\n  CONTRADICTION at {k}')
        print(f'      consensus: {sorted(want)}')
        print(f'      this run : {sorted(got)}')
    if missed:
        print('\n  missed:')
        for k in missed:
            print(f'      {k}  {sorted(control[k])[0]}')


if __name__ == '__main__':
    main()
