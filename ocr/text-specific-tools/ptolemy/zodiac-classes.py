#!/usr/bin/env python3
r"""Group zodiac-slot occurrences into equivalence classes by restated position.

Why classes and not a lookup table. The corruption is many-to-many: one printed
glyph fails into several tokens (Pisces -> \aleph, U+264B, U+2611), and one token
stands in for several glyphs (Toomer's own legend shows Psi covering EIGHT signs
and Xi covering two). So a token is EVIDENCE, not a key, and any global
substitution is unsafe until the token is shown to be unequivocal.

What is reliable in this text is that Ptolemy restates positions. The same
longitude appears within a passage as he computes with it, and a restatement is
the same position however the glyph happened to fail that time. So: connect two
occurrences carrying the same value close together in the text, take connected
components, and each component is one sign -- identity still unknown, but ONE
page read now settles every occurrence in it.

The payoff is the equivocality check that falls out for free. A token appearing
in two different components cannot be bulk-replaced, and we learn that without
reading anything.

Guards against false merges: only distinctive values (a minutes part or a
fraction -- bare round degrees like "10 deg" recur everywhere by chance), and
only within a proximity window. Every merge is printed with its evidence.
"""
import json, re, sys, collections

DEG    = r'(?:\^\s*\\circ|\^\{\\circ\}|°)'
NUM    = r'\d+(?:[;,]\d+(?:,\d+)?)?(?:\\frac\{\d+\}\{\d+\}|[½⅓⅔¼¾⅙⅚⅛])?'
SYMBOL = (r'\\mathfrak\{[a-z]\}(?:\\mathfrak\{[a-z]\})?'
          r'|\\[A-Za-z]+(?:_\{?[A-Za-z0-9]{1,3}\}?)?'
          r'|[^\x00-\x7F\s\d][\u0300-\u036f\u2080-\u2089]*[^\x00-\x7F\s\d]?')
SLOT   = re.compile(rf'({SYMBOL})\s*=?\s*({NUM})\s*{DEG}')
BANNED = re.compile(r'text|mathrm|mathbf|mathit|angle|arc|operatorname|quad|circ'
                    r'|frac|sqrt|begin|end|tag|cdot|times|Theta|approx|simeq|pm\b')
WINDOW = 1200   # chars; a restatement lives in the same argument

FRAC = {'½':';30','⅓':';20','⅔':';40','¼':';15','¾':';45','⅙':';10','⅚':';50','⅛':';7,30'}

def norm(v):
    """Canonical value, so 5 1/2 and 5;30 and 5;30,0 compare equal."""
    v = re.sub(r'\\frac\{(\d+)\}\{(\d+)\}', lambda m: FRAC.get(
        {('1','2'):'½',('1','3'):'⅓',('2','3'):'⅔',('1','4'):'¼',('3','4'):'¾',
         ('1','6'):'⅙',('5','6'):'⅚',('1','8'):'⅛'}.get((m.group(1),m.group(2)),''), ''), v)
    for f, s in FRAC.items():
        v = v.replace(f, s)
    parts = re.split(r'[;,]', v)
    while len(parts) > 1 and parts[-1] in ('0', ''):
        parts.pop()
    return ';'.join(parts)

def distinctive(v):
    return ';' in v            # has a minutes part after normalisation

class DSU(dict):
    def find(self, x):
        self.setdefault(x, x)
        while self[x] != x:
            self[x] = self[self[x]]; x = self[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb: self[ra] = rb

def main(text_id='ptolemy-almagest'):
    idx  = json.load(open('site/public/text-index.json'))
    path = next(t['path'] for t in idx['texts'] if t['id'] == text_id)
    body = open(path, encoding='utf-8').read()

    occ = []
    for m in SLOT.finditer(body):
        tok, raw = m.group(1), m.group(2)
        if BANNED.search(tok): continue
        if int(re.match(r'\d+', raw).group()) >= 30: continue
        occ.append(dict(i=len(occ), tok=tok, val=norm(raw), raw=raw, pos=m.start(),
                        ctx=body[max(0, m.start()-70):m.end()+18].replace('\n', ' ⏎ ')))
    print(f'{path}\n{len(occ)} sign-slot occurrences, '
          f'{len({o["tok"] for o in occ})} distinct tokens\n')

    dsu, merges = DSU(), []
    byval = collections.defaultdict(list)
    for o in occ:
        if distinctive(o['val']): byval[o['val']].append(o)
    for val, group in byval.items():
        group.sort(key=lambda o: o['pos'])
        for a, b in zip(group, group[1:]):
            if b['pos'] - a['pos'] <= WINDOW:
                dsu.union(a['i'], b['i'])
                if a['tok'] != b['tok']:
                    merges.append((val, a, b))

    comps = collections.defaultdict(list)
    for o in occ: comps[dsu.find(o['i'])].append(o)
    multi = {r: g for r, g in comps.items() if len({o['tok'] for o in g}) > 1}

    print(f'CROSS-TOKEN MERGES — differently-corrupted tokens, one position: {len(merges)}')
    for val, a, b in merges:
        print(f'\n  {val}   {a["tok"]}  ==  {b["tok"]}   (gap {b["pos"]-a["pos"]} chars)')
        print(f'      …{a["ctx"][-78:]}…')
        print(f'      …{b["ctx"][-78:]}…')

    tok_comps = collections.defaultdict(set)
    for r, g in comps.items():
        for o in g: tok_comps[o['tok']].add(r)
    equivocal = {t: c for t, c in tok_comps.items() if len(c) > 1}
    print(f'\n\nEQUIVOCAL TOKENS (appear in >1 class — UNSAFE to bulk-replace): {len(equivocal)}')
    for t, c in sorted(equivocal.items(), key=lambda x: -len(x[1]))[:14]:
        print(f'   {t:24} {len(c)} distinct classes')
    print(f'\nClasses containing >1 token: {len(multi)}  '
          f'(each needs ONE page read, not one per token)')

if __name__ == '__main__':
    main(*sys.argv[1:])
