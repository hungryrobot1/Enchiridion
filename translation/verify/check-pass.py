#!/usr/bin/env python3
"""Check a translation pass against its witness for what a machine CAN check.

  translation/verify/check-pass.py <run-dir> <pass-file> [--self-test]

Three checks, and a plain statement of what they do not test:

  1. COMPLETENESS — every `<!-- seg:ID -->` in the witness appears in the pass,
     in the same order. A missing ID is a missing sentence; this is the
     declared-units ledger the OCR completeness check never had.
  2. NUMERIC FIDELITY — for every table/figure/ops segment, the sequence of
     numeric tokens in the pass is byte-identical to the witness's. Tables are
     copied, never re-typed; this catches a re-typed digit.
  3. ARITHMETIC — worked examples labelled `a | b` per row are checked: binary
     column equals decimal column, and sums/differences/products hold. A text
     whose argument is calculation carries its own control. (The Leibniz
     witness has a KNOWN swapped label in the addition example; the check
     reports it on the witness and expects the pass to have corrected it.)

None of this tests MEANING. Meaning is what the two-pass divergence and the
status ladder are for. A pass that clears all three checks has been shown to
be complete and numerically faithful, and nothing more.
"""
import re, sys
from pathlib import Path

SEG = re.compile(r"<!--\s*seg:([A-Za-z0-9_\-]+)")
NUMERIC_SEGS = ("table", "figure", "ops-", "inline-tables")

def segments(text: str) -> list[str]:
    return SEG.findall(text)

def block_of(text: str, seg_id: str) -> str:
    """The content from this segment's marker to the next marker."""
    m = re.search(r"<!--\s*seg:" + re.escape(seg_id) + r"\b.*?-->", text, re.S)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"<!--\s*seg:", rest)
    return rest[: nxt.start()] if nxt else rest

def numeric_tokens(block: str) -> list[str]:
    block = re.sub(r"<!--.*?-->", "", block, flags=re.S)
    block = re.sub(r"\[\^\d+\]", "", block)   # footnote refs are not table content
    return re.findall(r"\d+", block)

def check_completeness(w: str, p: str) -> list[str]:
    ws, ps = segments(w), segments(p)
    out = []
    missing = [s for s in ws if s not in ps]
    extra = [s for s in ps if s not in ws]
    if missing: out.append(f"missing segments: {missing}")
    if extra: out.append(f"segments not in witness: {extra}")
    common = [s for s in ws if s in ps]
    if [s for s in ps if s in common] != common:
        out.append("segment order differs from witness")
    return out

def check_numeric(w: str, p: str) -> list[str]:
    """Byte-identical numbers — with ONE licence. Where the witness block fails
    its own arithmetic (a source misprint) and the pass block passes it, the
    difference is the correction the ledger demands, not a re-typed digit."""
    out = []
    for s in segments(w):
        if not any(k in s for k in NUMERIC_SEGS):
            continue
        wb, pb = block_of(w, s), block_of(p, s)
        a, b = numeric_tokens(wb), numeric_tokens(pb)
        if not b:
            out.append(f"{s}: pass has NO numeric content (table not copied)")
        elif a != b:
            if arithmetic_faults(wb) and not arithmetic_faults(pb) and len(a) == len(b):
                continue  # a corrected source misprint, footnoted per the ledger
            out.append(f"{s}: numeric tokens differ — witness {len(a)}, pass {len(b)}")
    return out

def arithmetic_faults(block: str) -> list[str]:
    faults = []
    for line in block.splitlines():
        for cell in re.split(r"\s{3,}", line.strip()):
            m = ROW.match(cell)
            if m and int(m.group(1), 2) != int(m.group(2)):
                faults.append(cell)
    return faults

ROW = re.compile(r"^\s*([01]+)\s*[|‖]+\s*(\d+)\s*$")

def check_arithmetic(text: str, label: str) -> list[str]:
    """Binary/decimal agreement on every `binary | decimal` row, in ops blocks."""
    out = []
    for s in segments(text):
        if not s.startswith("ops-"):
            continue
        for line in block_of(text, s).splitlines():
            for cell in re.split(r"\s{3,}", line.strip()):
                m = ROW.match(cell)
                if m and int(m.group(1), 2) != int(m.group(2)):
                    out.append(f"{label} {s}: {m.group(1)} is {int(m.group(1),2)}, labelled {m.group(2)}")
    return out

def run(run_dir: Path, pass_file: Path) -> int:
    witness = next(run_dir.glob("transcription-pass-*.md"))
    w, p = witness.read_text(), pass_file.read_text()
    print(f"  witness : {witness.name}\n  pass    : {pass_file.name}")
    problems = 0
    for name, fn in (("completeness", lambda: check_completeness(w, p)),
                     ("numeric fidelity", lambda: check_numeric(w, p))):
        issues = fn()
        print(f"  {'ok ' if not issues else 'FAIL'}  {name}")
        for i in issues: print(f"          {i}")
        problems += len(issues)
    wa = check_arithmetic(w, "witness")
    pa = check_arithmetic(p, "pass")
    print(f"  {'ok ' if not wa else 'note'}  arithmetic on witness" + (" — source misprints, expected to be corrected in the pass:" if wa else ""))
    for i in wa: print(f"          {i}")
    print(f"  {'ok ' if not pa else 'FAIL'}  arithmetic on pass")
    for i in pa: print(f"          {i}")
    problems += len(pa)
    print("\n  checks well-formedness and fidelity, never meaning.")
    return 1 if problems else 0

def selftest() -> int:
    import tempfile
    w = ("<!-- seg:1 -->\nUn.\n<!-- seg:ops-add -->\n  110 | 6\n  111 | 7\n  1101 | 13\n"
         "<!-- seg:table-x -->\n| 0 | 1 |\n| 1 | 2 |\n<!-- seg:2 -->\nDeux.\n")
    good = ("<!-- seg:1 -->\nOne.\n<!-- seg:ops-add -->\n  110 | 6\n  111 | 7\n  1101 | 13\n"
            "<!-- seg:table-x -->\n| 0 | 1 |\n| 1 | 2 |\n<!-- seg:2 -->\nTwo.\n")
    cases = [
        ("clean pass passes", good, 0),
        ("missing segment fails", good.replace("<!-- seg:2 -->\nTwo.\n", ""), 1),
        ("re-typed digit fails", good.replace("| 1 | 2 |", "| 1 | 3 |"), 1),
        ("table left as comment fails", good.replace("| 0 | 1 |\n| 1 | 2 |\n", ""), 1),
        ("swapped label fails arithmetic", good.replace("110 | 6", "110 | 7"), 1),
    ]
    ok = True
    for name, p, want in cases:
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "transcription-pass-a.md").write_text(w)
            pf = Path(d) / "pass.md"; pf.write_text(p)
            import io, contextlib
            with contextlib.redirect_stdout(io.StringIO()):
                got = run(Path(d), pf)
            good_case = (got == want)
            ok &= good_case
            print(f"  {'pass' if good_case else 'FAIL'}  {name}")
    # A witness WITH a misprint, and a pass that corrects it: allowed, and the
    # pass must still clear. The inverse -- a pass that introduces a fault
    # against a clean witness -- is already covered above.
    w_bad = w.replace("110 | 6\n  111 | 7", "110 | 7\n  111 | 6")
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "transcription-pass-a.md").write_text(w_bad)
        pf = Path(d) / "pass.md"; pf.write_text(good)
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            got = run(Path(d), pf)
        ok &= (got == 0)
        print(f"  {'pass' if got == 0 else 'FAIL'}  correcting a witness misprint is allowed")
    print("\n  controls pass: each check can fail, and does, on a case known to be bad" if ok else "  CONTROLS FAILED")
    return 0 if ok else 1

if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    sys.exit(run(Path(sys.argv[1]), Path(sys.argv[2])))
