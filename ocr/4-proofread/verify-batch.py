#!/usr/bin/env python3
r"""Cross-check a returned batch, and derive anchored fixes from its diff.

A batch comes back through two channels that are supposed to agree:

  result.json    findings, each carrying the REASON for a change
  edit/slice.md  the same markdown, corrected in place

Neither alone is trustworthy. A finding can misquote its location — our second
run put prose ("The longitude has no zodiac sign") in a field that was supposed
to hold verbatim text, which makes it unmatchable. An edit can be made without
explanation, which is worse: it looks authoritative and carries no argument. But
the two together are checkable, and the checking is the point of this script:

  * every diff hunk should have a finding explaining it   -> else UNEXPLAINED
  * every finding claiming a change should show up as a hunk -> else NOT ENACTED
  * where they agree, the hunk gives us a mechanical anchor  -> FIX CANDIDATE

That last line is the real payoff. A hunk carries the exact before-text, the
exact after-text, and its surrounding context, which is precisely what an
asserted-anchor repair needs. So the fragile step — hoping a worker transcribed
a quote faithfully — disappears rather than being policed.

The pristine text is REGENERATED from the line range in MANIFEST.json rather
than kept as a second copy in the batch, so there is nothing here to corrupt and
nothing to drift. Tampering with the reference files is detected by comparing
recorded hashes, not prevented — the batch is disposable and gitignored, so
detection is enough.

Nothing is written to the real text. This reports; repairs are applied by the
text's own script under ocr/text-specific-tools/.

  python3 ocr/4-proofread/verify-batch.py ocr/4-proofread/<text>/batches/<batch>
"""
import argparse, difflib, hashlib, json, os, re, sys


def norm(s):
    """Loose key for matching a claim against a hunk: ignore whitespace and
    LaTeX bracing, which workers reformat without meaning to."""
    return re.sub(r'[\s{}$\\]+', '', s)


def load(batch):
    man = json.load(open(os.path.join(batch, 'MANIFEST.json')))
    lo, hi = man['md_lines']
    src = open(man['md'], encoding='utf-8').read().split('\n')
    pristine = '\n'.join(src[lo - 1:hi]) + '\n'
    edited_path = os.path.join(batch, 'edit', 'slice.md')
    edited = open(edited_path, encoding='utf-8').read() if os.path.exists(edited_path) else None
    res_path = os.path.join(batch, 'result.json')
    findings = json.load(open(res_path))['findings'] if os.path.exists(res_path) else []
    notes = None
    for name in ('notes.md', 'summary.md'):
        p = os.path.join(batch, name)
        if os.path.exists(p):
            notes = open(p, encoding='utf-8').read()
            break
    return man, pristine, edited, findings, notes


def hunks(pristine, edited, lo):
    """Changed regions, with the source line number each begins at."""
    a, b = pristine.split('\n'), edited.split('\n')
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if tag == 'equal':
            continue
        out.append({'tag': tag, 'line': lo + i1,
                    'before': '\n'.join(a[i1:i2]), 'after': '\n'.join(b[j1:j2])})
    return out


def word_diff(before, after):
    """The smallest changed spans inside a hunk — this is the anchor."""
    aw, bw = before.split(), after.split()
    spans = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, aw, bw).get_opcodes():
        if tag == 'equal':
            continue
        spans.append((' '.join(aw[i1:i2]), ' '.join(bw[j1:j2]),
                      ' '.join(aw[max(0, i1 - 4):i1]), ' '.join(aw[i2:i2 + 4])))
    return spans


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('batch')
    ap.add_argument('--fixes', help='write derived fix candidates as JSON here')
    args = ap.parse_args()
    batch = args.batch.rstrip('/')

    man, pristine, edited, findings, notes = load(batch)
    lo, hi = man['md_lines']
    prose_mode = not findings and notes is not None
    print(f'{os.path.basename(batch)}   {man["md"]} lines {lo}-{hi}'
          + ('   [prose mode]' if prose_mode else ''))

    # Tamper check on the reference copies.
    if 'slice_sha256' in man and edited is not None:
        if hashlib.sha256(pristine.encode()).hexdigest() != man['slice_sha256']:
            print('  !! the SOURCE has changed since this batch was prepared; '
                  'regenerate the batch before trusting the diff')

    # --- prose mode: the diff is the only mechanical channel, and the account is
    # for a human. There is nothing to cross-check, so do not pretend otherwise:
    # every hunk becomes a fix candidate and the notes are reported unjudged.
    if prose_mode:
        if edited is None:
            print('  no edit/slice.md — nothing to derive anchors from')
            return
        hs = hunks(pristine, edited, lo)
        fixes = []
        for h in hs:
            for before, after, pre, post in word_diff(h['before'], h['after']):
                fixes.append({'line': h['line'], 'before': before, 'after': after,
                              'context_before': pre, 'context_after': post,
                              'claim': None, 'verified_by': None, 'evidence': '',
                              'occurrences_in_source': None})
        whole = open(man['md'], encoding='utf-8').read()
        for fx in fixes:
            fx['occurrences_in_source'] = whole.count(fx['before']) if fx['before'] else 0
        print(f'  diff: {len(hs)} changed regions -> {len(fixes)} fix candidates')
        for fx in fixes[:14]:
            n = fx['occurrences_in_source']
            warn = '  <-- occurs elsewhere; anchor on context' if n > 1 else ''
            print(f'    L{fx["line"]}  {fx["before"][:34]!r} -> {fx["after"][:34]!r}  (x{n}){warn}')

        # The things the schema channel never produced. Whether prose elicits
        # them is the whole question this mode exists to answer, so count them
        # rather than eyeballing the file.
        # Match on the ASKING, not on punctuation. The first prose run wrote a
        # real question — a genuine ambiguity in the brief's scope — as a
        # paragraph beginning "QUESTION:" and ending in a full stop, and a
        # naive '?' search reported zero questions for a batch that asked one.
        q = [ln for ln in notes.split('\n')
             if '?' in ln or re.search(r'\b(question|unclear|ambiguous|should (we|it)|'
                                       r'not sure|cannot tell|which of|please (confirm|clarify))\b',
                                       ln, re.I)]
        print(f'\n  notes.md: {len(notes.split())} words, '
              f'{len([l for l in notes.split(chr(10)) if l.startswith("#")])} headings, '
              f'{len(q)} passages that ask or hedge')
        for ln in q[:8]:
            print(f'    ? {ln.strip()[:110]}')
        print('\n  READ notes.md IN FULL — in this mode it carries every reason, '
              'and nothing above has checked it.')
        if args.fixes:
            json.dump({'batch': os.path.basename(batch), 'md': man['md'],
                       'mode': 'prose', 'fixes': fixes}, open(args.fixes, 'w'), indent=1)
            print(f'  wrote {args.fixes}')
        return

    real = [f for f in findings if f.get('claim') not in ('clean', 'brief', 'unsure')]
    print(f'  findings: {len(findings)} total, {len(real)} claiming an error')

    # --- schema-beyond-schema checks: the things a JSON Schema cannot express
    bad = []
    for f in real:
        q, md = f.get('quote', ''), f.get('markdown', '')
        if q and norm(q) not in norm(pristine):
            bad.append((f, 'quote is not verbatim text from the slice'))
        elif md and norm(md) not in norm(pristine):
            bad.append((f, 'markdown field is not verbatim text from the slice'))
        elif len(q) < 12:
            bad.append((f, 'quote too short to locate'))
    if bad:
        print(f'\n  UNANCHORABLE FINDINGS ({len(bad)}) — cannot be applied as written:')
        for f, why in bad[:12]:
            print(f'    L{f.get("line")}  {why}')
            print(f'        quote={f.get("quote","")[:70]!r}')

    if edited is None:
        print('\n  no edit/slice.md returned — findings channel only, so nothing to '
              'cross-check. Anchors must come from the quotes above.')
        return

    hs = hunks(pristine, edited, lo)
    print(f'\n  diff: {len(hs)} changed regions')

    # --- match hunks to findings
    def as_line(v):
        """Findings from before the schema tightened carry `line` as a string,
        sometimes a comma-separated list. Take the first integer in it; return
        None when there is none, so such a finding simply cannot be matched."""
        if isinstance(v, int):
            return v
        m = re.search(r'\d+', str(v or ''))
        return int(m.group()) if m else None

    by_line = {}
    for f in real:
        by_line.setdefault(as_line(f.get('line')), []).append(f)

    fixes, unexplained, matched = [], [], set()
    for h in hs:
        near = [f for ln, fs in by_line.items() if ln and abs(ln - h['line']) <= 2 for f in fs]
        # A hunk often carries SEVERAL corrections — one line can hold six. So
        # credit every nearby finding the hunk accounts for, not just the first;
        # crediting one made 85 of 109 findings look un-enacted when they were
        # simply bundled into the same changed region.
        explained = None
        for f in near:
            if norm(f.get('markdown', '')) and norm(f['markdown']) in norm(h['before']):
                if explained is None:
                    explained = f
                matched.add(id(f))
        if explained is None and near:
            explained = near[0]
            matched.add(id(explained))
        if explained is None:
            unexplained.append(h)
            continue
        for before, after, pre, post in word_diff(h['before'], h['after']):
            fixes.append({'line': h['line'], 'before': before, 'after': after,
                          'context_before': pre, 'context_after': post,
                          'claim': explained.get('claim'),
                          'verified_by': explained.get('verified_by'),
                          'evidence': explained.get('evidence', '')[:200],
                          # what makes the fix safe: how many times this exact
                          # text occurs in the WHOLE source, asserted at apply time
                          'occurrences_in_source': None})

    not_enacted = [f for f in real if id(f) not in matched]
    print(f'    matched to a finding : {len(hs) - len(unexplained)}')
    print(f'    UNEXPLAINED edits    : {len(unexplained)}')
    print(f'    findings NOT enacted : {len(not_enacted)}')

    for h in unexplained[:6]:
        print(f'\n  UNEXPLAINED at L{h["line"]} ({h["tag"]}) — an edit with no argument:')
        print(f'      - {h["before"][:100]}')
        print(f'      + {h["after"][:100]}')

    # occurrence counts against the whole file, so a fix knows its own blast radius
    if fixes:
        whole = open(man['md'], encoding='utf-8').read()
        for fx in fixes:
            fx['occurrences_in_source'] = whole.count(fx['before']) if fx['before'] else 0
        print(f'\n  FIX CANDIDATES ({len(fixes)}), with source-wide occurrence counts:')
        for fx in fixes[:10]:
            n = fx['occurrences_in_source']
            warn = '  <-- occurs elsewhere; anchor on context' if n > 1 else ''
            print(f'    L{fx["line"]}  {fx["before"][:34]!r} -> {fx["after"][:34]!r}  (x{n}){warn}')

    if args.fixes:
        json.dump({'batch': os.path.basename(batch), 'md': man['md'],
                   'fixes': fixes, 'unexplained': len(unexplained),
                   'not_enacted': len(not_enacted)},
                  open(args.fixes, 'w'), indent=1)
        print(f'\n  wrote {args.fixes}')


if __name__ == '__main__':
    main()
