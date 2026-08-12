#!/usr/bin/env python3
"""The extraction route as a computed verdict, with the conditions that flip it.

    from route import Facts, decide, render
    print(render(decide(facts)))

WHY THIS EXISTS. Every run in wave 4 -- five for five, on five different source
shapes -- reported the same thing: the operative route rule is four lines and
perfectly clear, and confirming that no later qualification reverses it means
reading the dispatch charter, the README, and two STAGE documents. 97 lines
across five files touch the route, and it is asserted normatively in two of
them. The runs were not complaining about verbosity. They were correctly
detecting that there is no single authoritative statement, and the only safe
response to that is to read everything.

So the route stops being a rule a worker derives from prose and becomes a
verdict recon computes from facts it already holds. The prose stays, to explain
the verdict and to hold the reasoning; it is no longer the thing that produces
the answer.

THE `would_flip` FIELD IS THE POINT. What the runs were actually asking was not
"what is the route" but "have I read enough to be sure?" More prose cannot
answer that. Naming the conditions under which the verdict changes can: a worker
whose case is not listed is done reading.

WHAT THIS MUST BE ALLOWED TO DO IS REFUSE. A computed route is a static
detection procedure, and static detection misses true positives -- Riemann's
lecture returned a clean recon verdict while every formula sat in plain sight in
an alt attribute. If this prints a confident answer and workers stop looking,
that is WORSE than four prose documents, because it converts a slow correct
process into a fast wrong one. So UNDETERMINED is a first-class verdict and the
honest one whenever the facts do not decide. A route function that always
produces an answer is a route function that cannot be trusted.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Producers that mean "this PDF was generated from something else", so the
# something else is the source and rendering it to pixels is a pure loss.
# Lavoisier's PDF is `calibre 9.5.0` + Ghostscript, a render of the EPUB beside
# it, and stage 2's tool table read as "OCR this". It nearly cost a lossy
# transcription of a text that then extracted at 99.96% token agreement.
RENDER_PRODUCERS = ("CALIBRE", "GHOSTSCRIPT", "PDFTEX", "XETEX", "LUATEX",
                    "MICROSOFT WORD", "LIBREOFFICE", "WKHTMLTOPDF")

# Producers that mean a human pointed OCR software at photographs.
OCR_PRODUCERS = ("ABBYY", "FINEREADER", "LURATECH", "LURADOCUMENT",
                 "TESSERACT", "OMNIPAGE")


@dataclass
class Facts:
    """What recon observed. Every field is something a tool already computes."""

    # A structured source sitting beside the PDF, if any: "epub", "tex", "html".
    structured: str | None = None
    # Which notation convention its formulas are stored in, if any.
    notation: str | None = None
    notation_count: int = 0
    # Formulas whose notation is present but NOT recoverable (MathSpeak).
    unrecoverable_count: int = 0
    # Images carrying no notation at all. Ambiguous by nature: a diagram and a
    # picture of a formula are the same fact to every tool we have.
    plain_images: int = 0

    # The PDF, if there is one. "none" | "born-digital" | "ocr-layer"
    text_layer: str | None = None
    producer: str = ""

    def producer_says_rendered(self) -> bool:
        return any(k in self.producer.upper() for k in RENDER_PRODUCERS)

    def producer_says_ocr(self) -> bool:
        return any(k in self.producer.upper() for k in OCR_PRODUCERS)


@dataclass
class Route:
    decision: str                       # source-native | pdf-native | OCR | UNDETERMINED
    because: list[str] = field(default_factory=list)
    not_taken: list[tuple[str, str]] = field(default_factory=list)
    would_flip: list[str] = field(default_factory=list)


def decide(f: Facts) -> Route:
    """Facts in, verdict out. Refuses when the facts do not settle it."""

    # --- A structured source is present. It is the source unless it cannot be.
    if f.structured:
        if f.notation and f.notation != "mathspeak-title":
            r = Route("source-native")
            r.because.append(
                f"{f.notation_count} formula(s) carry recoverable LaTeX "
                f"({f.notation}) in the {f.structured}")
            r.not_taken.append(
                ("OCR", "the strings are already here; rendering them to pixels "
                        "so OCR can guess them back is a pure loss"))
            r.would_flip.append(
                "if the notation were mathspeak-title — a SPOKEN description of "
                "the formula, not the string it was set from, and ambiguous as "
                "soon as an expression nests")
            r.would_flip.append(
                "this settles the ROUTE, not correctness: it is the same "
                "transcription either way, so stage 4 still wants the page")
            return r

        if f.unrecoverable_count:
            r = Route("OCR")
            r.because.append(
                f"{f.unrecoverable_count} formula(s) carry only their SPOKEN "
                f"form (mathspeak-title) — a description made for the formula, "
                f"not the string it was set from")
            r.not_taken.append(
                ("source-native", "the notation is marked up but not recoverable"))
            r.would_flip.append(
                "if any formula also carries data-tex, mediawiki-alt or bare "
                "LaTeX in an alt attribute — check the CONVENTION, not one "
                "attribute")
            r.would_flip.append(
                "keep the spoken forms regardless: they are a cheap way to FLAG "
                "disagreements with OCR output, though they cannot settle one")
            return r

        if f.plain_images:
            # THE CASE THIS MODULE EXISTS TO STOP GUESSING AT.
            # recon-epub.py used to route here to OCR, on the reasoning that
            # images without notation might be pictures of formulas. For
            # Huygens' Treatise on Light that was wrong: 53 of its images are
            # geometric diagrams, the prose is prose, and the correct route was
            # source-native. Nothing we can compute distinguishes a diagram from
            # a picture of an equation. So say so.
            r = Route("UNDETERMINED")
            r.because.append(
                f"{_an(f.structured)} {f.structured} source is present and its {f.plain_images} "
                f"image(s) carry no notation of any kind")
            r.because.append(
                "whether those images are ILLUSTRATIONS or PICTURES OF FORMULAS "
                "decides the route, and no tool here can tell the difference")
            r.not_taken.append(
                ("source-native", "correct IF the images are diagrams, plates or "
                                  "ornaments — extract directly and ship them"))
            r.not_taken.append(
                ("OCR", "correct IF they are set mathematics — only OCR reads a "
                        "picture of an equation"))
            r.would_flip.append(
                "OPEN THREE OF THEM. This is a minute of looking and it settles "
                "the route; a guess here costs a whole run")
            r.would_flip.append(
                "either way a text-only conversion DROPS these images silently — "
                "losing an illustration is visible, losing a formula leaves "
                "fluent prose with holes in it")
            return r

        r = Route("source-native")
        r.because.append(f"{_an(f.structured)} {f.structured} source is present and carries no "
                         f"images at all: this is prose")
        r.not_taken.append(
            ("OCR", "the PDF round trip buys nothing and costs an OCR pass"))
        r.would_flip.append(
            "if images turn up that this survey missed — it counts <img>, so "
            "anything drawn by other means is invisible to it")
        return r

    # --- No structured source. The PDF is all we have.
    if f.text_layer == "none":
        r = Route("OCR")
        r.because.append("the PDF carries no extractable text: it is a scan")
        r.not_taken.append(
            ("pdf-native", "there is no text layer to extract"))
        r.not_taken.append(
            ("source-native", "no structured source is present"))
        r.would_flip.append(
            "if a structured source exists elsewhere — Project Gutenberg "
            "publishes .tex for texts typeset from it, and the address has to "
            "be tried rather than looked up. That is acquisition work, needs "
            "network access, and a dispatched worker cannot do it")
        r.would_flip.append(
            "the page images are a real printed witness, so stage 4 applies here")
        return r

    if f.text_layer == "ocr-layer":
        r = Route("OCR")
        r.because.append(
            f"a scan with an embedded OCR layer (producer: {f.producer or 'unknown'})")
        r.because.append(
            "its characters are guesses and its errors are already in the file")
        r.not_taken.append(
            ("pdf-native", "the layer was produced by OCR over photographs "
                           "rather than typeset — it is not a born-digital source"))
        r.would_flip.append(
            "judge the layer before trusting OR discarding it: render a page and "
            "compare. A shredded-looking layer over tabular content may be "
            "describing columns of numbers correctly")
        return r

    if f.text_layer == "reconstruction":
        # OCR software produced this, but the pages are not rasters: somebody
        # re-typeset OCR output and threw the photographs away. Extractable, and
        # uncheckable — re-OCRing it only re-reads the reconstruction.
        r = Route("pdf-native")
        r.because.append(
            f"the producer is OCR software ({f.producer or 'unknown'}) but the "
            f"pages are not mostly rasters: this is a RECONSTRUCTION")
        r.not_taken.append(
            ("OCR", "there are no page images to read; re-OCRing this would "
                    "only re-read somebody else's OCR"))
        r.would_flip.append(
            "nothing flips it, and that is the problem: this file is its own "
            "only witness. Extract it, STATE THE CEILING in NOTES.md, and "
            "expect needs-review rather than complete")
        r.would_flip.append(
            "if a scan of the same edition can be found, that is a real printed "
            "witness and stage 4 becomes possible again")
        return r

    if f.text_layer == "born-digital":
        if f.producer_says_rendered():
            r = Route("UNDETERMINED")
            r.because.append(
                f"born-digital text layer, but the producer is {f.producer!r} — "
                f"this PDF was GENERATED from something else")
            r.not_taken.append(
                ("pdf-native", "workable, but it extracts a rendering rather "
                               "than the source that produced it"))
            r.not_taken.append(
                ("OCR", "never appropriate here: there is a text layer. "
                        "'Not this tool' never means 'OCR'"))
            r.would_flip.append(
                "FIND THE THING IT WAS RENDERED FROM. Look for an .epub or .tex "
                "in the same directory, then upstream. Dedekind's PDF yielded "
                "zero mathematical expressions; its LaTeX yielded 3,262")
            return r
        r = Route("pdf-native")
        r.because.append(
            f"a born-digital text layer (producer: {f.producer or 'unknown'})")
        r.not_taken.append(
            ("OCR", "there is a usable text layer. OCR is only ever for a scan"))
        r.would_flip.append(
            "for MATHEMATICS specifically, OCR is still the reliable route in a "
            "PDF — encoding varies by producer and rasterising is what "
            "normalises it. This is the one place the rule inverts")
        return r

    r = Route("UNDETERMINED")
    r.because.append("not enough was observed to decide: no structured source "
                     "found and the PDF's text layer was not characterised")
    r.would_flip.append("run recon-pdf.py on the PDF, and recon-epub.py or "
                        "recon-html.py on any structured source beside it")
    return r


LABEL_W = 16

# A refusal that does not say what to do next is not finished. Boole's run hit
# UNDETERMINED and then went hunting through four documents for "the material
# needed to establish that UNDETERMINED meant stop" -- so the verdict that was
# supposed to save reading caused reading. The exit has to travel WITH the
# refusal, every time, which is why this is a constant and not prose in a
# stage document that the worker would have to go and find.
UNDETERMINED_PROTOCOL = [
    "UNDETERMINED means STOP. It does not mean 'pick the likely one'.",
    "1. Do the check under `would flip` above. It is written to be cheap "
    "and it usually settles the route in a minute.",
    "2. If it settles: you have your route. Record the fact you observed "
    "and the route it gave in NOTES.md, and carry on. This needs no "
    "permission and is not an escalation.",
    "3. If it does not settle: write ESCALATION.md and STOP. Do not "
    "extract on a guess.",
    "Escalating here is a SUCCESS. Boole's run escalated on UNDETERMINED, "
    "and the generating LaTeX turned out to exist -- 3,232 math lines that "
    "a guess would have thrown away.",
]


def render(r: Route, indent: str = "  ", width: int = 78) -> str:
    """The verdict as the four-part block a worker reads instead of four docs."""
    out = [f"{indent}ROUTE: {r.decision}"]
    for line in r.because:
        out.append(_row("because", line, indent, width))
    for alt, why in r.not_taken:
        out.append(_row(f"not {alt}", why, indent, width))
    for line in r.would_flip:
        out.append(_row("would flip", line, indent, width))
    if r.decision == "UNDETERMINED":
        out.append(_row("what to do", UNDETERMINED_PROTOCOL[0], indent, width))
        for line in UNDETERMINED_PROTOCOL[1:]:
            out.append(_row("", line, indent, width))
    return "\n".join(out)


def _row(label: str, body: str, indent: str, width: int) -> str:
    """One labelled row, wrapped with a hanging indent under the label column.

    A label longer than the column gets its own line rather than being sliced
    through the middle -- the first version cut `not source-native` into
    `not source-na tive`, which is exactly the kind of small ugliness that makes
    a report look untrustworthy.
    """
    import textwrap

    pad = indent + " " * LABEL_W
    wrapped = textwrap.fill(body, width=width, initial_indent=pad,
                            subsequent_indent=pad)
    if not label:
        return wrapped
    if len(label) <= LABEL_W - 1:
        return indent + label.ljust(LABEL_W) + wrapped[len(pad):]
    return f"{indent}{label}\n{wrapped}"


def _an(word: str) -> str:
    return "an" if word[:1].lower() in "aeiou" else "a"


# The verdicts that matter are the ones that previously fooled us. A control set
# of easy cases proves only that the easy cases are easy -- so Lavoisier (the
# producer-string near-miss), Riemann (the bare-alt miss) and Huygens (the
# images-without-notation misroute) are all here, and each must come out right.
CONTROLS = [
    ("Hilbert — 248 formulas, all data-tex, the lucky case",
     Facts(structured="epub", notation="data-tex", notation_count=248),
     "source-native"),
    ("Riemann — bare LaTeX in alt, no marker; recon once returned clean",
     Facts(structured="html", notation="bare-alt", notation_count=6),
     "source-native"),
    ("Lavoisier — born-digital PDF whose producer says it is a RENDER",
     Facts(text_layer="born-digital", producer="calibre 9.5.0; GPL Ghostscript"),
     "UNDETERMINED"),
    ("Huygens — EPUB whose images carry no notation but ARE the argument",
     Facts(structured="epub", plain_images=65),
     "UNDETERMINED"),
    ("Einstein Relativity — notation present as SPOKEN form only",
     Facts(structured="epub", notation="mathspeak-title", unrecoverable_count=225),
     "OCR"),
    ("Mill — prose EPUB, no images at all",
     Facts(structured="epub"),
     "source-native"),
    ("Napier — IA scan with a LuraDocument OCR layer",
     Facts(text_layer="ocr-layer", producer="Recoded by LuraDocument PDF v2.28"),
     "OCR"),
    ("a PDF with no text layer at all",
     Facts(text_layer="none"),
     "OCR"),
    ("a plain born-digital PDF with no structured source",
     Facts(text_layer="born-digital", producer="Acrobat Distiller 8.1.0"),
     "pdf-native"),
    ("NEGATIVE: nothing observed must not produce a confident answer",
     Facts(),
     "UNDETERMINED"),
]


def self_test() -> int:
    bad = 0
    for name, facts, want in CONTROLS:
        got = decide(facts).decision
        ok = got == want
        bad += not ok
        print(f"  {'pass' if ok else 'FAIL'}  {got:<14} want {want:<14} {name}")

    # Every refusal must carry its exit. A verdict that says "stop" without
    # saying what stopping looks like sends the worker back into the documents,
    # which is the cost this module exists to remove.
    undecided = [(n, f) for n, f, w in CONTROLS if w == "UNDETERMINED"]
    assert undecided, "controls must include at least one UNDETERMINED case"
    for name, facts in undecided:
        text = render(decide(facts))
        for want in ("what to do", "ESCALATION.md", "means STOP"):
            if want not in text:
                print(f"  FAIL  UNDETERMINED without {want!r}: {name}")
                bad += 1
    # ... and a decided route must NOT carry it, or it is noise on every run.
    decided = next(f for _, f, w in CONTROLS if w == "source-native")
    if "what to do" in render(decide(decided)):
        print("  FAIL  the stop protocol printed on a DECIDED route")
        bad += 1

    if bad:
        print(f"\n  {bad} CONTROL(S) FAILED — the route verdict cannot be trusted.")
        return 2
    print("\n  controls pass: it routes the three cases that previously fooled "
          "us, and refuses when the facts do not decide")
    return 0


if __name__ == "__main__":
    import sys
    if "--show" in sys.argv:
        for name, facts, _ in CONTROLS:
            print(f"\n── {name}")
            print(render(decide(facts)))
        sys.exit(0)
    sys.exit(self_test())
