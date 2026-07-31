#!/usr/bin/env python3
r"""Keep only the fixes that two independent runs derived identically.

This sits between verify-batch.py, which turns one run's edited slice into
anchored fix candidates, and the text-specific applier, which writes them. It
exists because the applier was built to consume one run and we now have two, and
because a fix that only one run made is a different kind of object from a fix
both made.

## Why the diff and not the findings

Both channels come back from a run, and they answer different questions. The
findings say WHY -- which is what lets one decision settle a family later -- but
they locate a spot by quoting it, and two runs quote differently: they choose
different amounts of surrounding context and start in different places. The diff
locates mechanically. So corroboration is computed on the diff, and the findings
are what a human reads when adjudicating a conflict.

## Why the slice is not simply swapped in

The obvious use of a per-worker copy of the markdown is to take the corrected
copy back wholesale. That does not survive contact with the runs. Workers
RESTRUCTURE as they correct -- on one batch the two returned slices were 308 and
295 lines against a 288-line original, having moved content between lines and
reflowed display math. Swapping either in wholesale would import that
restructuring along with the corrections, silently and unreviewably.

Taking localised diff hunks keeps the original instinct -- corrections come back
as text, not as descriptions -- while discarding everything the worker did that
nobody asked for. A hunk that both runs produced identically is a correction. A
region where they differ is either a disagreement or a reflow, and neither
belongs in the text.

## The key

Matched on line number plus the exact before and after text. That is the
strictest available key, and on the first two batches it produced the HIGHEST
agreement of the three keys tried (63/74 and 68/75, against 60 and 61 for
content-only matching). Strictness costs nothing when both runs edit the same
pristine slice, so there is no reason to loosen it.

  ocr/proofreading/corroborate-fixes.py a.json b.json -o corroborated.json
"""
import argparse, json, re, sys


def norm(s):
    return re.sub(r'\s+', '', s or '')


def key(f):
    return (f['line'], norm(f['before']), norm(f['after']))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('run_a')
    ap.add_argument('run_b')
    ap.add_argument('-o', '--out', help='write the corroborated fix set here')
    ap.add_argument('--show-solo', action='store_true',
                    help='list the fixes only one run made')
    args = ap.parse_args()

    a, b = (json.load(open(p)) for p in (args.run_a, args.run_b))
    if a['md'] != b['md']:
        sys.exit(f"these runs cover different files:\n  {a['md']}\n  {b['md']}")

    fa, fb = a['fixes'], b['fixes']
    kb = {key(f) for f in fb}
    ka = {key(f) for f in fa}

    both, solo_a = [], []
    for f in fa:
        (both if key(f) in kb else solo_a).append(f)
    solo_b = [f for f in fb if key(f) not in ka]

    print(f"{args.run_a} ({len(fa)})  vs  {args.run_b} ({len(fb)})")
    print(f"  corroborated by both : {len(both)}")
    print(f"  only run A           : {len(solo_a)}")
    print(f"  only run B           : {len(solo_b)}")
    print("  (solo fixes are HELD, not rejected -- an uncorroborated fix may still"
          "\n   be right, and each costs only another pass to confirm)")

    if args.show_solo:
        for label, fixes in (('A only', solo_a), ('B only', solo_b)):
            if fixes:
                print(f'\n  {label}:')
                for f in fixes:
                    print(f"    L{f['line']}  {f['before'][:46]!r}")
                    print(f"         -> {f['after'][:46]!r}")

    if args.out:
        json.dump({'md': a['md'],
                   'batch': f"{a.get('batch')}+{b.get('batch')}",
                   'corroboration': 'two independent runs, identical diff hunk',
                   'held_uncorroborated': len(solo_a) + len(solo_b),
                   'fixes': both},
                  open(args.out, 'w'), indent=1)
        print(f'\n  wrote {args.out}  ({len(both)} fixes)')


if __name__ == '__main__':
    main()
