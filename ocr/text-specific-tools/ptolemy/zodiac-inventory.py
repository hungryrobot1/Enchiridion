#!/usr/bin/env python3
r"""Inventory the tokens standing in for Ptolemy's zodiac signs.

Why not the census: the census reduces \COMMAND occurrences to context
signatures, so it cannot see a stand-in that is not a single command — bare "π",
"π₀", "Ṽ", "\mathfrak{m}\mathfrak{g}", "\pi_1". Those are exactly the forms the
m-shaped signs (Virgo ♍, Scorpius ♏) collapsed onto, so the family is
undercounted by the very instrument that found it.

A sign in Toomer is JUXTAPOSED with a longitude: "♈ 10°", "♏ 1¾°",
"♑ = 20;22°". Legitimate relations also sit in that slot (≈ 4;30°), and staring
at one occurrence never settles which it is. Two measurable discriminators,
neither needing the scan:

  SLOT RATIO   A relation appears all over a text; a sign appears ONLY before a
               longitude. The fraction of a token's uses falling in this slot
               separates them — the census's strays-vs-flat logic, applied to
               tokens instead of slots. Needs >=3 uses to mean anything.

  DEGREE RANGE A longitude within a sign spans 0-30 degrees, because that is
               what a sign is. A token followed by 45;30 is not a sign.

A sign is also a SINGLE symbol carrying no other meaning, so the candidate shape
excludes anything built out of \text/\mathrm/\angle/\arc — those are Toomer's
point labels and prose interjections, which sit in the same slot innocently.
"""
import json, re, sys, collections

DEG   = r'(?:\^\s*\\circ|\^\{\\circ\}|°)'
NUM   = r'\d+(?:[;,]\d+(?:,\d+)?)?(?:\\frac\{\d+\}\{\d+\}|[½⅓⅔¼¾⅙⅚⅛])?'
# A bare symbol: a command with no argument (+ optional subscript), a fraktur
# digraph, or a run of non-ASCII letters with combining marks / subscript digits.
SYMBOL = (r'\\mathfrak\{[a-z]\}(?:\\mathfrak\{[a-z]\})?'
          r'|\\[A-Za-z]+(?:_\{?[A-Za-z0-9]{1,3}\}?)?'
          r'|[^\x00-\x7F\s\d][\u0300-\u036f\u2080-\u2089]*[^\x00-\x7F\s\d]?')
SLOT  = re.compile(rf'({SYMBOL})\s*=?\s*({NUM})\s*{DEG}')
BANNED = re.compile(r'text|mathrm|mathbf|mathit|angle|arc|operatorname|quad|circ|frac|sqrt|begin|end|tag|cdot|times')

def main(text_id, min_uses=3):
    idx  = json.load(open('site/public/text-index.json'))
    path = next(t['path'] for t in idx['texts'] if t['id'] == text_id)
    body = open(path, encoding='utf-8').read()

    slot, inrange, samples = collections.Counter(), collections.Counter(), collections.defaultdict(list)
    for m in SLOT.finditer(body):
        tok, val = m.group(1), m.group(2)
        if BANNED.search(tok):
            continue
        slot[tok] += 1
        if int(re.match(r'\d+', val).group()) < 30:
            inrange[tok] += 1
        if len(samples[tok]) < 2:
            a, b = max(0, m.start() - 60), min(len(body), m.end() + 20)
            samples[tok].append(body[a:b].replace('\n', ' ⏎ '))

    rows = []
    for tok, n in slot.items():
        total = len(re.findall(re.escape(tok) + r'(?![A-Za-z])', body))
        rows.append((n / total if total else 0, n, total, tok))
    rows.sort(key=lambda r: (-r[0], -r[1]))

    print(f'{path}\n')
    print(f'{"token":26} {"slot":>5} {"total":>6} {"ratio":>6} {"0-30":>5}  verdict')
    print('-' * 68)
    signs, relations = [], []
    for ratio, n, total, tok in rows:
        if n < min_uses:
            continue
        if ratio > 0.75 and inrange[tok] == n:
            verdict, bucket = 'SIGN', signs
        elif ratio < 0.3:
            verdict, bucket = 'relation (leave)', relations
        else:
            verdict, bucket = 'ambiguous', None
        print(f'{tok:26} {n:5} {total:6} {ratio:6.2f} {inrange[tok]:5}  {verdict}')
        if bucket is not None:
            bucket.append((tok, n))

    print(f'\nSIGN-LIKE: {len(signs)} distinct tokens, {sum(n for _, n in signs)} occurrences')
    for tok, n in sorted(signs, key=lambda x: -x[1]):
        print(f'\n  {tok}  ({n})')
        for s in samples[tok]:
            print(f'      …{s}…')

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'ptolemy-almagest')
