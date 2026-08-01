#!/usr/bin/env python3
"""Convert Gutenberg's TeX source of Dedekind's Essays to reader markdown.

The supplied PDF was generated from ``source/21016-t.tex``.  The TeX is the
best extraction source: it preserves the mathematical tokens which the PDF
text layer flattens or corrupts.  The PDF remains the layout witness.

Scope (the library's text-only apparatus policy):
  KEEP  both essays, Dedekind's two prefaces to the second essay, all 22
        sections, all 172 numbered propositions/definitions, and all 25
        authorial notes.
  DROP  Gutenberg header/license, transcriber's note, publisher title matter,
        advertisements, and Gutenberg's correction appendix.  The appendix's
        two corrections are already applied in the TeX body.

This is deliberately a small converter for the TeX vocabulary in this file,
not a general LaTeX parser.  Unknown commands survive into the output and make
the raw-LaTeX diagnostic fail.  Structural counts and exact source anchors are
asserted so that a changed source cannot be converted silently.

Dry-run prints the report.  ``--apply`` writes the markdown, toc, and metadata.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "source" / "21016-t.tex"
OUT = ROOT / "dedekind-essays-on-theory-of-numbers.md"
TOC = ROOT / "toc.json"
METADATA = ROOT / "metadata.json"

START = r"\mychap{I}{CONTINUITY AND IRRATIONAL NUMBERS}"
SECOND = r"\mychap{II}{THE NATURE AND MEANING OF NUMBERS}"
END = "% [File: 121.png]"

PAGE_REFS = {
    "EISIII": "4",
    "EISIV": "6",
    "EISViv": "9",
    "EISVI": "10",
    "Ind132": "47",
}

SKIP_COMMANDS = {
    "newpage", "smallskip", "medskip", "bigskip", "nopagebreak",
    "noindent", "normalsize", "small", "large", "Large", "footnotesize",
    "scriptsize", "thispagestyle", "pagestyle", "null", "hfill", "vfill",
    "quad", "qquad",
}


def strip_comments(text: str) -> str:
    """Remove unescaped TeX comments without joining the adjacent lines."""
    out = []
    for line in text.splitlines():
        if line.lstrip().startswith("%"):
            continue
        cut = len(line)
        for i, char in enumerate(line):
            if char == "%":
                nslash = 0
                j = i - 1
                while j >= 0 and line[j] == "\\":
                    nslash += 1
                    j -= 1
                if nslash % 2 == 0:
                    cut = i
                    break
        out.append(line[:cut])
    return "\n".join(out)


def group(text: str, pos: int) -> tuple[str, int]:
    """Return balanced-brace contents and the first position after it."""
    while pos < len(text) and text[pos].isspace():
        pos += 1
    if pos >= len(text) or text[pos] != "{":
        raise ValueError(f"expected group at offset {pos}: {text[pos:pos+40]!r}")
    depth = 1
    i = pos + 1
    start = i
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start:i], i + 1
        i += 1
    raise ValueError(f"unclosed group at offset {pos}")


def command_at(text: str, pos: int) -> tuple[str, int]:
    assert text[pos] == "\\"
    if pos + 1 >= len(text):
        return "", pos + 1
    if text[pos + 1].isalpha() or text[pos + 1] == "@":
        m = re.match(r"\\([A-Za-z@]+)", text[pos:])
        assert m
        return m.group(1), pos + len(m.group(0))
    return text[pos + 1], pos + 2


def normalize_math(tex: str, *, display: bool = False) -> str:
    tex = re.sub(r"\\label\s*\{[^{}]*\}", "", tex)
    tex = tex.replace(r"\partof", r"\mathrel{\mathfrak{3}}")
    # The TeX defines \wholeof as a reflected \partof. KaTeX has no
    # \reflectbox; its trusted HTML extension preserves that one use.
    tex = tex.replace(
        r"\wholeof",
        r"\mathrel{\htmlStyle{display:inline-block;transform:scaleX(-1)}{\mathfrak{3}}}",
    )
    tex = tex.replace(r"\@", "")
    tex = re.sub(r"\\tag\s*\{\$([^$]+)\$\}", r"\\tag{\1}", tex)
    tex = re.sub(r"\\rlap\s*\{\$([^$]+)\$\}", r"\\rlap{\1}", tex)
    tex = re.sub(r"\\rlap\s*\{([^{}]*)\}", r"\1", tex)
    tex = re.sub(r"\\shortintertext\s*\{([^{}]*)\}",
                 r"\\\\ &\\text{\1} \\\\", tex)
    if not display:
        tex = tex.replace(r"\\ ", " ")
    return tex.strip()


@dataclass
class Converter:
    prefix: str
    notes: list[str] = field(default_factory=list)
    unknown: set[str] = field(default_factory=set)

    def note(self, body: str) -> str:
        number = len(self.notes) + 1
        converted = self.convert(body).strip()
        converted = re.sub(r"\s+", " ", converted)
        self.notes.append(converted)
        return (f'<sup id="fnref-{self.prefix}-{number}">'
                f'<a href="#fn-{self.prefix}-{number}">{number}</a></sup>')

    def environment(self, env: str, raw: str) -> str:
        if env in {"align*", "gather*", "eqnarray*"}:
            target = "gathered" if env == "gather*" else "aligned"
            return ("\n\n$$\n\\begin{" + target + "}\n" +
                    normalize_math(raw, display=True) + "\n\\end{" + target + "}\n$$\n\n")
        if env == "quote":
            body = self.convert(raw).strip()
            return "\n\n" + "\n>\n".join(
                "> " + re.sub(r"\s+", " ", p.strip())
                for p in re.split(r"\n\s*\n", body) if p.strip()
            ) + "\n\n"
        if env == "itemize":
            items = re.split(r"\\item(?:\[[^]]*\])?", raw)[1:]
            return "\n\n" + "\n".join(
                "- " + re.sub(r"\s+", " ", self.convert(x).strip())
                for x in items
            ) + "\n\n"
        if env == "tabular":
            rows = []
            for row in re.split(r"\\\\", raw):
                row = row.strip().rstrip(",")
                if not row:
                    continue
                cells = [self.convert(x).strip() for x in row.split("&")]
                line = "".join(cells[:2])
                if len(cells) > 2:
                    line += " " + " ".join(cells[2:])
                rows.append(re.sub(r"\s+", " ", line).strip())
            return "\n\n" + "\n\n".join(rows) + "\n\n"
        if env in {"center", "flushright"}:
            body = re.sub(r"\s+", " ", self.convert(raw)).strip()
            if body in {"PREFACE TO THE FIRST EDITION.",
                        "PREFACE TO THE SECOND EDITION."}:
                return f"\n\n## {body}\n\n"
            if body == "THE NATURE AND MEANING OF NUMBERS.":
                return "\n\n"
            return f"\n\n{body}\n\n"
        self.unknown.add(f"begin{{{env}}}")
        return f"\\begin{{{env}}}{raw}\\end{{{env}}}"

    def convert(self, text: str) -> str:
        out: list[str] = []
        i = 0
        while i < len(text):
            if text.startswith("\\[", i):
                end = text.find("\\]", i + 2)
                if end < 0:
                    raise ValueError("unclosed display math")
                out.append("\n\n$$\n" + normalize_math(text[i + 2:end], display=True) + "\n$$\n\n")
                i = end + 2
                continue
            if text[i] == "$":
                end = i + 1
                while True:
                    end = text.find("$", end)
                    if end < 0:
                        raise ValueError(f"unclosed inline math at {i}")
                    if text[end - 1] != "\\":
                        break
                    end += 1
                out.append("$" + normalize_math(text[i + 1:end]) + "$")
                i = end + 1
                continue
            if text[i] == "{":
                body, i = group(text, i)
                out.append(self.convert(body))
                continue
            if text[i] != "\\":
                out.append(" " if text[i] == "~" else text[i])
                i += 1
                continue

            name, pos = command_at(text, i)
            if name == "\\":
                out.append("\n")
                i = pos
                continue
            if name in {"textit", "emph"}:
                body, i = group(text, pos)
                out.append("*" + self.convert(body).strip() + "*")
                continue
            if name == "mbox" and (pos >= len(text) or text[pos:].lstrip()[:1] != "{"):
                i = pos
                continue
            if name in {"textsc", "mbox", "mathrm", "text", "rlap"}:
                body, i = group(text, pos)
                out.append(self.convert(body))
                continue
            if name == "textgreek":
                body, i = group(text, pos)
                expected = r"\as e\ig{} \oR{} \asa njrwpos \as rijmht\ia zai"
                if re.sub(r"\s+", " ", body.strip()) != expected:
                    raise ValueError(f"unexpected Teubner Greek: {body!r}")
                out.append("ἀεὶ ὁ ἄνθρωπος ἀριθμητίζει")
                continue
            if name == "footnote":
                body, i = group(text, pos)
                out.append(self.note(body))
                continue
            if name == "mychap":
                _, pos2 = group(text, pos)
                title, i = group(text, pos2)
                out.append(f"\n\n# {self.convert(title).strip()}\n\n")
                continue
            if name == "mysect":
                _, pos2 = group(text, pos)
                roman, pos3 = group(text, pos2)
                title, i = group(text, pos3)
                out.append(f"\n\n## {roman}. {self.convert(title).upper().strip()}\n\n")
                continue
            if name == "mypara":
                number, i = group(text, pos)
                out.append(f"**{number.strip()}**")
                continue
            if name == "begin":
                env, after_env = group(text, pos)
                content_start = after_env
                if env == "tabular":
                    while content_start < len(text) and text[content_start].isspace():
                        content_start += 1
                    if content_start < len(text) and text[content_start] == "[":
                        close = text.find("]", content_start)
                        if close < 0:
                            raise ValueError("unclosed tabular option")
                        content_start = close + 1
                    _, content_start = group(text, content_start)  # column spec
                marker = f"\\end{{{env}}}"
                end = text.find(marker, content_start)
                if end < 0:
                    raise ValueError(f"unclosed environment {env}")
                out.append(self.environment(env, text[content_start:end]))
                i = end + len(marker)
                continue
            if name == "addcontentsline":
                _, p2 = group(text, pos)
                _, p3 = group(text, p2)
                _, i = group(text, p3)
                continue
            if name == "label":
                _, i = group(text, pos)
                continue
            if name == "pageref":
                label, i = group(text, pos)
                if label not in PAGE_REFS:
                    raise ValueError(f"unresolved page reference {label}")
                out.append(PAGE_REFS[label])
                continue
            if name in SKIP_COMMANDS:
                # thispagestyle/pagestyle take an argument in this source
                i = pos
                if name in {"thispagestyle", "pagestyle"}:
                    _, i = group(text, pos)
                continue
            if name in {"par"}:
                out.append("\n\n")
                i = pos
                continue
            if name in {"@"}:
                i = pos
                continue
            if name == "\n":
                out.append(" ")
                i = pos
                continue
            if name in {"&", "$", "%", "#", "_", "{" , "}"}:
                out.append(name)
                i = pos
                continue
            if name == " ":
                out.append(" ")
                i = pos
                continue
            if name == "ldots":
                out.append("…")
                i = pos
                continue
            self.unknown.add(name)
            out.append("\\" + name)
            i = pos
        return "".join(out)

    def notes_block(self) -> str:
        if not self.notes:
            return ""
        rows = []
        for i, body in enumerate(self.notes, 1):
            rows.append(
                f'{i}. <span id="fn-{self.prefix}-{i}">{body}</span> '
                f'[↩](#fnref-{self.prefix}-{i})'
            )
        return "\n\n## NOTES\n\n" + "\n\n".join(rows) + "\n"


def tidy(text: str) -> str:
    math: list[str] = []

    def protect(match: re.Match[str]) -> str:
        token = f"@@DEDEKINDMATH{len(math)}@@"
        math.append(match.group(0))
        return token

    # Typography substitutions below are prose-only. In particular, TeX's
    # ``n''`` primes must not become Unicode quotation marks inside math.
    text = re.sub(r"\$\$[\s\S]*?\$\$|\$[^$\n]+\$", protect, text)
    text = text.replace("``", "“").replace("''", "”")
    text = text.replace("---", "—").replace("--", "–")
    text = re.sub(r"\\([,;:!])", r"\\\1", text)  # retain math spacing
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    blocks = []
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block:
            continue
        if block.startswith(("#", "$$", ">", "- ")) or "  \n" in block:
            blocks.append(block)
        else:
            blocks.append(re.sub(r"\s*\n\s*", " ", block))
    text = "\n\n".join(blocks)
    text = re.sub(r" +([,.;:?!])", r"\1", text)
    for i, block in enumerate(math):
        text = text.replace(f"@@DEDEKINDMATH{i}@@", block)
    return text.strip() + "\n"


def build() -> tuple[str, dict, dict, set[str]]:
    raw = SOURCE.read_text(encoding="latin-1")
    assert raw.count(START) == 1, "first essay anchor changed"
    assert raw.count(SECOND) == 1, "second essay anchor changed"
    assert raw.count(END) == 1, "end-of-text anchor changed"
    body = raw[raw.index(START):raw.index(END)]
    body = strip_comments(body)
    split = body.index(SECOND)

    first = Converter("e1")
    second = Converter("e2")
    first_md = tidy(first.convert(body[:split]) + first.notes_block())
    second_md = tidy(second.convert(body[split:]) + second.notes_block())
    markdown = first_md.rstrip() + "\n\n" + second_md

    headings = re.findall(r"^(#{1,2}) (.+)$", markdown, re.M)
    numbered = [int(x) for x in re.findall(r"^\*\*(\d+)\.\*\*", markdown, re.M)]
    assert len([h for h in headings if h[0] == "#"]) == 2
    assert len([h for h in headings if h[0] == "##" and h[1] != "NOTES"]) == 23
    assert numbered == list(range(1, 173)), "numbered units are not 1..172"
    assert len(first.notes) == 3, f"expected 3 first-essay notes, got {len(first.notes)}"
    assert len(second.notes) == 22, f"expected 22 second-essay notes, got {len(second.notes)}"
    source_dollars = len(re.findall(r"(?<!\\)\$", body)) // 2
    nested_layout_math = len(re.findall(r"\\(?:tag|rlap)\s*\{\$[^$]+\$\}", body))
    output_displays = len(re.findall(r"\$\$[\s\S]*?\$\$", markdown))
    output_without_displays = re.sub(r"\$\$[\s\S]*?\$\$", "", markdown)
    output_inlines = len(re.findall(r"\$[^$\n]+\$", output_without_displays))
    source_displays = (body.count(r"\[") +
                       len(re.findall(r"\\begin\{(?:align\*|gather\*|eqnarray\*)\}", body)))
    assert output_inlines == source_dollars - nested_layout_math
    assert output_displays == source_displays
    assert markdown.count(r"\mathrel{\mathfrak{3}}") == body.count(r"\partof")
    assert markdown.count("ἀεὶ ὁ ἄνθρωπος ἀριθμητίζει") == 1

    toc = {
        "title": "Essays on the Theory of Numbers",
        "sections": [
            {"title": title, "page": page}
            for title, page in [
                ("CONTINUITY AND IRRATIONAL NUMBERS", 1),
                ("I. PROPERTIES OF RATIONAL NUMBERS", 2),
                ("II. COMPARISON OF THE RATIONAL NUMBERS WITH THE POINTS OF A STRAIGHT LINE", 3),
                ("III. CONTINUITY OF THE STRAIGHT LINE", 4),
                ("IV. CREATION OF IRRATIONAL NUMBERS", 6),
                ("V. CONTINUITY OF THE DOMAIN OF REAL NUMBERS", 9),
                ("VI. OPERATIONS WITH REAL NUMBERS", 10),
                ("VII. INFINITESIMAL ANALYSIS", 12),
                ("THE NATURE AND MEANING OF NUMBERS", 14),
                ("PREFACE TO THE FIRST EDITION.", 14),
                ("PREFACE TO THE SECOND EDITION.", 19),
                ("I. SYSTEMS OF ELEMENTS", 21),
                ("II. TRANSFORMATION OF A SYSTEM", 24),
                ("III. SIMILARITY OF A TRANSFORMATION. SIMILAR SYSTEMS", 25),
                ("IV. TRANSFORMATION OF A SYSTEM IN ITSELF", 27),
                ("V. THE FINITE AND INFINITE", 31),
                ("VI. SIMPLY INFINITE SYSTEMS. SERIES OF NATURAL NUMBERS", 33),
                ("VII. GREATER AND LESS NUMBERS", 34),
                ("VIII. FINITE AND INFINITE PARTS OF THE NUMBER-SERIES", 40),
                ("IX. DEFINITION OF A TRANSFORMATION OF THE NUMBER-SERIES BY INDUCTION", 42),
                ("X. THE CLASS OF SIMPLY INFINITE SYSTEMS", 46),
                ("XI. ADDITION OF NUMBERS", 48),
                ("XII. MULTIPLICATION OF NUMBERS", 51),
                ("XIII. INVOLUTION OF NUMBERS", 53),
                ("XIV. NUMBER OF THE ELEMENTS OF A FINITE SYSTEM", 54),
            ]
        ],
    }

    metadata = json.loads((ROOT / "source" / "metadata.json").read_text())
    metadata["format"] = "markdown"
    metadata["filename"] = OUT.name
    metadata["description"] = (
        "Constructions of the real numbers through cuts and of the natural "
        "numbers through systems, transformations, and induction"
    )
    # Stage 4 has no independent witness: do not silently claim completion.
    metadata["ocr_status"] = "pending"
    return markdown, toc, metadata, first.unknown | second.unknown


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    markdown, toc, metadata, unknown = build()
    math_blocks = len(re.findall(r"\$\$[\s\S]*?\$\$|\$[^$\n]+\$", markdown))
    print(f"output: {len(markdown):,} chars, {math_blocks} math blocks")
    print(f"structure: 2 essays, 23 subordinate headings, 172 numbered units, 25 notes")
    print("inventory: source and output agree on inline/display math and 234 part signs")
    print("unknown commands:", ", ".join(sorted(unknown)) if unknown else "none")
    if args.apply:
        OUT.write_text(markdown)
        TOC.write_text(json.dumps(toc, indent=2, ensure_ascii=False) + "\n")
        METADATA.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")
        print(f"wrote {OUT.name}, {TOC.name}, {METADATA.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
