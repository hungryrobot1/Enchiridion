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

  ocr/4-proofread/corroborate-fixes.py a.json b.json -o corroborated.json
"""
import argparse, json, re, sys


# Two runs that read the SAME defect off the SAME page still write the
# correction two ways, because the encoding is a choice and nobody told them
# which one. Measured on Book I pages 60-65: the runs touched 8 lines each,
# agreed on 7 of them, and corroboration scored 4 -- the losses were entirely
#
#     DB^2   vs  DB²                     LaTeX vs Unicode superscript
#     30^{\mathrm{p}}  vs  30ᵖ           raised unit letter, same two ways
#
# Scoring those as disagreement is wrong twice over: it discards real
# corroboration, and it does so most often in the mathematically dense pages
# where agreement matters most. So the key folds superscripts to one spelling
# before comparing. It deliberately does NOT fold anything that changes a
# VALUE -- ^2 and ^3 stay distinct, as do p and d -- because the whole point of
# corroboration is to catch two runs reading a glyph differently.
#
# This is the same lesson as the sign glyphs, in a new family: the encoding
# decision belongs to the script, never to the worker. See ledger.md.
SUPERSCRIPT = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5",
               "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
               "ᵖ": "p", "ᵈ": "d", "ʰ": "h", "ⁿ": "n", "ᵐ": "m", "ˢ": "s"}


def norm(s):
    s = s or ""
    s = "".join("^" + SUPERSCRIPT[c] if c in SUPERSCRIPT else c for c in s)
    # ^{\mathrm{p}} / ^\mathrm{p} / ^{p}  ->  ^p
    s = re.sub(r"\^\s*\{\s*\\(?:mathrm|text|rm)\s*\{\s*([A-Za-z0-9]+)\s*\}\s*\}", r"^\1", s)
    s = re.sub(r"\^\s*\\(?:mathrm|text|rm)\s*\{\s*([A-Za-z0-9]+)\s*\}", r"^\1", s)
    s = re.sub(r"\^\s*\{\s*([A-Za-z0-9]+)\s*\}", r"^\1", s)
    return re.sub(r"\s+", "", s)


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

    # Once the key folds spellings together, run A's record is kept by accident
    # of order -- and if A wrote the Unicode form, the Unicode form is what
    # gets applied. The corpus sets raised units and exponents as LaTeX
    # (`^{\mathrm{p}}`, `X^2`), so prefer whichever record already uses it.
    # A no-op on this run, where A used LaTeX for all 31; it exists so the
    # convention does not depend on which run happened to be first.
    UNICODE_SUP = re.compile(r"[⁰¹²³⁴⁵⁶⁷⁸⁹ᵖᵈʰⁿᵐˢ]")
    by_key_b = {key(f): f for f in fb}

    both, solo_a = [], []
    for f in fa:
        k = key(f)
        if k not in kb:
            solo_a.append(f)
            continue
        alt = by_key_b.get(k)
        if alt is not None and UNICODE_SUP.search(f.get('after') or '') \
                and not UNICODE_SUP.search(alt.get('after') or ''):
            f = alt
        both.append(f)
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
