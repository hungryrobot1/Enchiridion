#!/usr/bin/env python3
"""Convert John Walker's TeX of Einstein's 1905 paper to reader Markdown.

The supplied ``specrel.pdf`` was generated from ``source/specrel.tex``.  TeX is
the extraction source because it preserves mathematical semantics; the PDF is
the rendered witness for conversion and layout, not an independent edition.

Scope (the library's text-only apparatus policy):
  KEEP  Einstein's paper, its two parts and ten sections, all mathematics, and
        the nine numbered footnotes reproduced from the 1923 edition.
  DROP  Walker's six daggered editor notes and the final ``About this Document``
        apparatus.  The latter remains available in the source files.

This is deliberately a converter for this file's TeX vocabulary, not a general
LaTeX parser. Unknown commands survive into the output so ``check-raw-latex``
fails visibly instead of accepting a guess. Exact anchors and structural/math
counts make a changed source refuse silent conversion.

Dry-run prints a report. ``--apply`` writes the Markdown, ToC, and metadata.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "source" / "specrel.tex"
OUT = ROOT / "einstein-on-electrodynamics-of-moving-bodies.md"
TOC = ROOT / "toc.json"
METADATA = ROOT / "metadata.json"

START = "It is known that Maxwell's electrodynamics---as usually understood at"
END = "\\vfill\n\n\\vbox{\n\\begin{quotation}"
TITLE = "ON THE ELECTRODYNAMICS OF MOVING BODIES"

SKIP_COMMANDS = {
    "noindent", "bigskip", "centering", "@", "quad", "qquad",
    "smallskip", "medskip", "large", "Large", "small", "normalsize",
}


def strip_comments(text: str) -> str:
    """Remove unescaped TeX comments without joining adjacent lines."""
    out: list[str] = []
    for line in text.splitlines():
        if line.lstrip().startswith("%"):
            continue
        cut = len(line)
        for i, char in enumerate(line):
            if char != "%":
                continue
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
        raise ValueError(f"expected group at offset {pos}: {text[pos:pos+50]!r}")
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
        match = re.match(r"\\([A-Za-z@]+)", text[pos:])
        assert match
        return match.group(1), pos + len(match.group(0))
    return text[pos + 1], pos + 2


def strip_editor_notes(text: str) -> tuple[str, dict[str, int]]:
    """Remove note commands inside each edNote block, retaining main text.

    Walker sometimes opens an editor-note block around a whole corrected
    paragraph or equation. Only its footnote/footnotetext is apparatus; the
    surrounding main-text correction remains the edition's reading.
    """
    out: list[str] = []
    i = 0
    in_editor = False
    counts = {"blocks": 0, "notes": 0, "marks": 0, "setcounters": 0}
    while i < len(text):
        if text[i] != "\\":
            out.append(text[i])
            i += 1
            continue
        name, pos = command_at(text, i)
        if name == "edNoteBegin":
            assert not in_editor, "nested editor-note block"
            in_editor = True
            counts["blocks"] += 1
            i = pos
            continue
        if name == "edNoteEnd":
            assert in_editor, "editor-note end without begin"
            in_editor = False
            i = pos
            continue
        if in_editor and name in {"footnote", "footnotetext"}:
            _, i = group(text, pos)
            counts["notes"] += 1
            continue
        if in_editor and name == "footnotemark":
            counts["marks"] += 1
            i = pos
            continue
        if in_editor and name == "setcounter":
            _, p2 = group(text, pos)
            _, i = group(text, p2)
            counts["setcounters"] += 1
            continue
        out.append(text[i:pos])
        i = pos
    assert not in_editor, "unclosed editor-note block"
    assert counts == {"blocks": 6, "notes": 6, "marks": 1, "setcounters": 2}, counts
    result = "".join(out)
    assert "\\edNote" not in result
    assert "Editor's note" not in result
    assert "\\footnotetext" not in result and "\\footnotemark" not in result
    return result, counts


def expand_math_macros(tex: str) -> str:
    """Expand this source's three local macros using balanced arguments."""
    out: list[str] = []
    i = 0
    while i < len(tex):
        if tex[i] != "\\":
            out.append(tex[i])
            i += 1
            continue
        name, pos = command_at(tex, i)
        if name == "dd":
            numerator, p2 = group(tex, pos)
            denominator, i = group(tex, p2)
            out.append(
                "\\frac{\\partial " + expand_math_macros(numerator) + "}"
                "{\\partial " + expand_math_macros(denominator) + "}"
            )
            continue
        if name == "ic":
            out.append(r"\frac{1}{c}")
            i = pos
            continue
        if name == "pr":
            body, i = group(tex, pos)
            out.append(r"\mathrm{" + expand_math_macros(body) + "}'")
            continue
        if name == "multicolumn":
            columns, p2 = group(tex, pos)
            alignment, p3 = group(tex, p2)
            body, i = group(tex, p3)
            assert columns.strip() == "2" and alignment.strip() == "c"
            out.append(expand_math_macros(body))
            continue
        out.append(tex[i:pos])
        i = pos
    return "".join(out)


def normalize_math(tex: str, *, display: bool = False) -> str:
    tex = expand_math_macros(tex)
    tex = re.sub(r"\\label\s*\{[^{}]*\}", "", tex)
    tex = tex.replace(r"\@", "")
    if not display:
        tex = tex.replace(r"\ ", " ")
    return tex.strip()


@dataclass
class Converter:
    notes: list[str] = field(default_factory=list)
    unknown: set[str] = field(default_factory=set)
    inline_seen: int = 0
    displays_seen: int = 0

    def note(self, body: str) -> str:
        number = len(self.notes) + 1
        converted = self.convert(body).strip()
        converted = re.sub(r"\s+", " ", converted)
        self.notes.append(converted)
        return f"<sup>{number}</sup>"

    def environment(self, env: str, raw: str) -> str:
        if env == "eqnarray*":
            self.displays_seen += 1
            return (
                "\n\n$$\n\\begin{aligned}\n"
                + normalize_math(raw, display=True)
                + "\n\\end{aligned}\n$$\n\n"
            )
        if env == "center":
            return "\n\n" + self.convert(raw).strip() + "\n\n"
        if env == "raggedleft":
            # The sole instance is equation system (A), nested in a presentational
            # tabular. Preserve its mathematical content and express the printed
            # dot leaders / label as a semantic equation tag.
            assert raw.count(r"\begin{math}") == 1
            assert raw.count(r"\end{math}") == 1
            assert raw.count(r"({\rm A})") == 1
            start = raw.index(r"\begin{math}") + len(r"\begin{math}")
            end = raw.index(r"\end{math}", start)
            math = normalize_math(raw[start:end], display=True)
            self.displays_seen += 1
            return "\n\n$$\n" + math + r"\tag{A}" + "\n$$\n\n"
        self.unknown.add(f"begin{{{env}}}")
        return f"\\begin{{{env}}}{raw}\\end{{{env}}}"

    def styled_group(self, body: str) -> str:
        match = re.match(r"\s*\\(em|rm|sc|bf|sf|tt|Large|large|small)\b\s*", body)
        if not match:
            return self.convert(body)
        style = match.group(1)
        converted = self.convert(body[match.end():]).strip()
        if style == "em":
            return f"*{converted}*"
        return converted

    def convert(self, text: str) -> str:
        out: list[str] = []
        i = 0
        while i < len(text):
            if text.startswith(r"\[", i):
                end = text.find(r"\]", i + 2)
                if end < 0:
                    raise ValueError("unclosed display math")
                self.displays_seen += 1
                out.append(
                    "\n\n$$\n"
                    + normalize_math(text[i + 2:end], display=True)
                    + "\n$$\n\n"
                )
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
                self.inline_seen += 1
                out.append("$" + normalize_math(text[i + 1:end]) + "$")
                i = end + 1
                continue
            if text[i] == "{":
                body, i = group(text, i)
                out.append(self.styled_group(body))
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
            if name in {"mbox", "mathrm", "text"}:
                body, i = group(text, pos)
                out.append(self.convert(body))
                continue
            if name == "footnote":
                body, i = group(text, pos)
                out.append(self.note(body))
                continue
            if name in {"section", "subsection"}:
                p2 = pos
                if p2 < len(text) and text[p2] == "*":
                    p2 += 1
                title, i = group(text, p2)
                level = "##" if name == "section" else "###"
                title_text = re.sub(r"\s+", " ", self.convert(title)).strip()
                out.append(f"\n\n{level} {title_text}\n\n")
                continue
            if name == "begin":
                env, content_start = group(text, pos)
                marker = f"\\end{{{env}}}"
                end = text.find(marker, content_start)
                if end < 0:
                    raise ValueError(f"unclosed environment {env}")
                out.append(self.environment(env, text[content_start:end]))
                i = end + len(marker)
                continue
            if name == "pr":
                body, i = group(text, pos)
                self.inline_seen += 1
                out.append("$" + normalize_math(r"\mathrm{" + body + "}'") + "$")
                continue
            if name == "S":
                out.append("§")
                i = pos
                continue
            if name in SKIP_COMMANDS:
                i = pos
                continue
            if name in {"rm", "sc", "bf", "sf", "tt", "em"}:
                # Declaration forms are normally consumed by styled_group. If a
                # bare one remains, discard only the styling instruction.
                i = pos
                continue
            if name == "renewcommand":
                _, p2 = group(text, pos)
                _, i = group(text, p2)
                continue
            if name in {"&", "$", "%", "#", "_", "{", "}"}:
                out.append(name)
                i = pos
                continue
            if name == " ":
                out.append(" ")
                i = pos
                continue
            if name == "\n":
                out.append(" ")
                i = pos
                continue
            if name == "par":
                out.append("\n\n")
                i = pos
                continue
            self.unknown.add(name)
            out.append("\\" + name)
            i = pos
        return "".join(out)

    def notes_block(self) -> str:
        assert len(self.notes) == 9, len(self.notes)
        rows = [f"{i}. {body}" for i, body in enumerate(self.notes, 1)]
        return "\n\n## NOTES\n\n" + "\n\n".join(rows) + "\n"


def tidy(text: str) -> str:
    math: list[str] = []

    def protect(match: re.Match[str]) -> str:
        token = f"@@EINSTEINMATH{len(math)}@@"
        math.append(match.group(0))
        return token

    text = re.sub(r"\$\$[\s\S]*?\$\$|\$[^$\n]+\$", protect, text)
    text = text.replace("``", "“").replace("''", "”")
    text = text.replace("---", "—").replace("--", "–")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    blocks: list[str] = []
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block:
            continue
        if block.startswith(("#", "$$", ">", "- ")):
            blocks.append(block)
        else:
            blocks.append(re.sub(r"\s*\n\s*", " ", block))
    text = "\n\n".join(blocks)
    text = re.sub(r" +([,.;:?!])", r"\1", text)
    for i, block in enumerate(math):
        text = text.replace(f"@@EINSTEINMATH{i}@@", block)
    return text.strip() + "\n"


def build() -> tuple[str, dict, dict, set[str], dict[str, int]]:
    raw = SOURCE.read_text(encoding="latin-1")
    assert len(raw.splitlines()) == 1594
    assert len(re.findall(r"(?<!\\)\$", raw)) == 554
    assert raw.count(r"\begin{eqnarray*}") == 14
    assert raw.count(r"\title{ON THE ELECTRODYNAMICS OF MOVING BODIES}") == 1
    assert raw.count(START) == 1, "start anchor changed"
    assert raw.count(END) == 1, "end anchor changed"
    body = raw[raw.index(START):raw.index(END)]
    body = strip_comments(body)
    body, editor_counts = strip_editor_notes(body)
    assert body.count(r"\footnote{") == 9
    assert body.count(r"\section*") == 2
    assert body.count(r"\subsection*") == 10
    assert body.count(r"\begin{eqnarray*}") == 14
    assert body.count(r"\[") == 67 and body.count(r"\]") == 67

    converter = Converter()
    converted = converter.convert(body)
    markdown = tidy(
        f"# {TITLE}\n\n**By A. EINSTEIN**\n\nJune 30, 1905\n\n"
        + converted
        + converter.notes_block()
    )

    headings = re.findall(r"^(#{1,3}) (.+)$", markdown, re.M)
    assert len([h for h in headings if h[0] == "#"]) == 1
    assert len([h for h in headings if h[0] == "##" and h[1] != "NOTES"]) == 2
    assert len([h for h in headings if h[0] == "###"]) == 10
    assert markdown.count("<sup>") == 9
    assert markdown.count("Editor's note") == 0
    assert converter.displays_seen == 82, converter.displays_seen
    output_displays = len(re.findall(r"\$\$[\s\S]*?\$\$", markdown))
    output_without_displays = re.sub(r"\$\$[\s\S]*?\$\$", "", markdown)
    output_inlines = len(re.findall(r"\$[^$\n]+\$", output_without_displays))
    assert output_displays == converter.displays_seen
    assert output_inlines == converter.inline_seen

    toc = {
        "title": "On the Electrodynamics of Moving Bodies",
        "sections": [
            {"title": "I. KINEMATICAL PART", "page": 2},
            {"title": "§ 1. Definition of Simultaneity", "page": 2},
            {"title": "§ 2. On the Relativity of Lengths and Times", "page": 3},
            {"title": "§ 3. Theory of the Transformation of Co-ordinates and Times from a Stationary System to another System in Uniform Motion of Translation Relatively to the Former", "page": 5},
            {"title": "§ 4. Physical Meaning of the Equations Obtained in Respect to Moving Rigid Bodies and Moving Clocks", "page": 9},
            {"title": "§ 5. The Composition of Velocities", "page": 11},
            {"title": "II. ELECTRODYNAMICAL PART", "page": 12},
            {"title": "§ 6. Transformation of the Maxwell-Hertz Equations for Empty Space. On the Nature of the Electromotive Forces Occurring in a Magnetic Field During Motion", "page": 12},
            {"title": "§ 7. Theory of Doppler's Principle and of Aberration", "page": 15},
            {"title": "§ 8. Transformation of the Energy of Light Rays. Theory of the Pressure of Radiation Exerted on Perfect Reflectors", "page": 17},
            {"title": "§ 9. Transformation of the Maxwell-Hertz Equations when Convection-Currents are Taken into Account", "page": 19},
            {"title": "§ 10. Dynamics of the Slowly Accelerated Electron", "page": 20},
        ],
    }
    metadata = json.loads((ROOT / "source" / "metadata.json").read_text())
    metadata["format"] = "markdown"
    metadata["filename"] = OUT.name
    metadata["ocr_status"] = "pending"
    return markdown, toc, metadata, converter.unknown, editor_counts


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    markdown, toc, metadata, unknown, editor_counts = build()
    displays = len(re.findall(r"\$\$[\s\S]*?\$\$", markdown))
    no_displays = re.sub(r"\$\$[\s\S]*?\$\$", "", markdown)
    inlines = len(re.findall(r"\$[^$\n]+\$", no_displays))
    print(f"output: {len(markdown):,} chars, {inlines} inline + {displays} display math blocks")
    print("structure: 1 title, 2 parts, 10 sections, 9 numbered notes")
    print(f"editor apparatus removed: {editor_counts}")
    print("unknown commands:", ", ".join(sorted(unknown)) if unknown else "none")
    if args.apply:
        OUT.write_text(markdown, encoding="utf-8")
        TOC.write_text(json.dumps(toc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        METADATA.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {OUT.name}, {TOC.name}, {METADATA.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
