#!/usr/bin/env python3
"""Convert Gutenberg 15114's generating TeX to reader Markdown.

This is a source-specific, fail-closed converter.  The TeX is the extraction
source; the PDF generated from it is only the rendered witness.  Exact anchors
and source/output inventories make upstream changes refuse silent conversion.
"""
from __future__ import annotations

import argparse
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source" / "15114-t.tex"
OUTPUT = ROOT / "boole-investigation-of-the-laws-of-thought.md"

START = r"\chapter[NATURE AND DESIGN OF THIS WORK]"
END = r"\begin{text}"
PREFACE = r"\chapter[PREFACE.]{}"
CONTENTS = r"\chapter[CONTENTS.]{}"
NOTE = r"\chapter[]{}"
DEDICATION = "TO\\\\\n\\bigskip"

MATH_ENVS = {
    "equation", "equation*", "eqnarray", "eqnarray*", "align*", "alignat*",
    "gather", "gather*", "multline", "multline*",
}
NESTED_MATH_ENVS = {"aligned", "array", "split", "gathered", "minipage"}
SKIP = {
    "noindent", "smallskip", "medskip", "bigskip", "newpage", "clearpage",
    "hfill", "dotfill", "normalsize", "small", "large", "Huge", "centering",
    "displaystyle", "textstyle", "upshape", "it", "sc", "quad", "qquad",
    "newline", "raggedright", "raggedleft",
    "mainmatter",
}

GREEK_MAP = {
    "bajud'inhc": "βαθυδίνης",                         # printed p. 20
    "p'ajos": "πάθος",                                 # printed p. 103
    "d'unamis": "δύναμις",                             # printed p. 103
    "<'exis": "ἕξις",                                  # printed p. 103
    r"t`o m'eson \dots pr`os >hm": "τὸ μέσον … πρὸς ἡμ", # printed p. 103; ᾶς follows in math
    "a>i'wnia d'ikaia": "αἰώνια δίκαια",               # printed p. 106
    r'''t`hn 'up`er `hm<'ac 'aret`hn `hrw"ik'hn tina kai jeian''':
        "τὴν ὑπὲρ ἡμᾶς ἀρετὴν ἡρωϊκὴν τινα καὶ θείαν",  # printed p. 106
    "t`o po>'n": "τὸ ποῦ",                             # printed p. 135
    "p'ojen t`o kak`on": "πόθεν τὸ κακόν",              # printed p. 159
}


def strip_comments(text: str) -> str:
    rows = []
    for line in text.splitlines():
        if line.lstrip().startswith("%"):
            continue
        cut = len(line)
        for i, ch in enumerate(line):
            if ch != "%":
                continue
            n = 0
            j = i - 1
            while j >= 0 and line[j] == "\\":
                n += 1; j -= 1
            if n % 2 == 0:
                cut = i; break
        rows.append(line[:cut])
    return "\n".join(rows)


def command_at(text: str, pos: int) -> tuple[str, int]:
    assert text[pos] == "\\"
    if pos + 1 >= len(text): return "", pos + 1
    if text[pos + 1].isalpha() or text[pos + 1] == "@":
        m = re.match(r"\\([A-Za-z@]+)", text[pos:]); assert m
        return m.group(1), pos + len(m.group(0))
    return text[pos + 1], pos + 2


def group(text: str, pos: int) -> tuple[str, int]:
    while pos < len(text) and text[pos].isspace(): pos += 1
    if pos >= len(text) or text[pos] != "{":
        raise ValueError(f"expected group at {pos}: {text[pos:pos+50]!r}")
    depth, i, start = 1, pos + 1, pos + 1
    while i < len(text):
        if text[i] == "\\": i += 2; continue
        if text[i] == "{": depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0: return text[start:i], i + 1
        i += 1
    raise ValueError(f"unclosed group at {pos}")


def optional(text: str, pos: int) -> tuple[str | None, int]:
    while pos < len(text) and text[pos].isspace(): pos += 1
    if pos >= len(text) or text[pos] != "[": return None, pos
    end = text.find("]", pos + 1)
    if end < 0: raise ValueError("unclosed optional argument")
    return text[pos + 1:end], end + 1


def environment(text: str, pos: int, env: str) -> tuple[str, int]:
    """Read an environment, respecting nested environments of the same name."""
    depth, cursor = 1, pos
    token = re.compile(r"\\(begin|end)\{" + re.escape(env) + r"\}")
    while True:
        m = token.search(text, cursor)
        if not m: raise ValueError(f"unclosed environment {env}")
        depth += 1 if m.group(1) == "begin" else -1
        if depth == 0: return text[pos:m.start()], m.end()
        cursor = m.end()


def replace_command(text: str, opening: str, replacement: str) -> str:
    """Replace one grouped command selected by an asserted opening anchor."""
    assert text.count(opening) == 1, opening
    start = text.index(opening)
    command = opening[:opening.index("{")]
    _, end = group(text, start + len(command))
    return text[:start] + replacement + text[end:]


def accent(mark: str, body: str) -> str:
    base = body.replace(r"\i", "ı").strip("{}")
    combining = {"'": "\u0301", "`": "\u0300", "^": "\u0302", '"': "\u0308", "~": "\u0303"}[mark]
    return unicodedata.normalize("NFC", base + combining)


def accent_arg(text: str, pos: int) -> tuple[str, int]:
    """Read TeX's braced or single-token accent argument."""
    if pos < len(text) and text[pos] == "{":
        return group(text, pos)
    if pos < len(text) and text[pos] == "\\":
        name, end = command_at(text, pos)
        if name == "i": return "ı", end
        return "\\" + name, end
    if pos < len(text): return text[pos], pos + 1
    raise ValueError("accent without argument")


def normalize_math(tex: str) -> str:
    # Dollar pairs inside a math environment are TeX's way of temporarily
    # returning to math from \text/\mathrm. Close and reopen the text span in
    # KaTeX instead of nesting dollar delimiters.
    dollar_open = True
    while "$" in tex:
        tex = tex.replace("$", "}" if dollar_open else r"\text{", 1)
        dollar_open = not dollar_open
    if not dollar_open:
        raise ValueError("odd nested dollar count in math environment")
    tex = re.sub(r"\\label\s*\{[^{}]*\}", "", tex)
    tex = tex.replace(r"\textrm", r"\mathrm")
    tex = tex.replace(r"\dfrac", r"\frac").replace(r"\tfrac", r"\frac")
    tex = tex.replace(r"\dotsc", r"\dots").replace(r"\dotso", r"\dots")
    tex = tex.replace(r"\nonumber", "")
    tex = tex.replace(r"\hfill", "")
    tex = tex.replace(r"\dotfill", r"\dots")
    tex = re.sub(r"\\textsc\{([^{}]*)\}", r"\1", tex)
    tex = tex.replace(r"{\sc ", "{")
    tex = tex.replace(r"\lefteqn", r"\mathrlap")
    tex = re.sub(r"\\setcounter\{equation\}\{\d+\}", "", tex)
    tex = re.sub(r"@\{\\hspace\{[^{}]*\}\}", "", tex)
    tex = re.sub(r"\\multispan(?:\{\d+\}|\d+)", "", tex)
    tex = re.sub(r"\\intertext\{([^{}]*)\}", r"\\\\ \\text{\1} \\\\", tex)
    tex = re.sub(r"&\s*(\\tag\{)", r"\1", tex)
    tex = tex.replace(
        r"\text{\raisebox{-1.5ex}{}\genfrac{}{}{0pt}{}"
        r"{\text{(sum of other con-}}{\text{stituents),}}\text{}}",
        r"\substack{\text{(sum of other con-}\\\text{stituents),}}",
    )
    tex = re.sub(r"\n\s*\n+", "\n", tex)
    tex = re.sub(r"\\begin\{minipage\}\{[^{}]*\}", r"\\begin{aligned}\\text{", tex)
    tex = tex.replace(r"\end{minipage}", r"}\end{aligned}")
    return tex.strip()


@dataclass
class Converter:
    notes: list[str] = field(default_factory=list)
    unknown: set[str] = field(default_factory=set)
    chapter: int = 0
    equation: int = 0
    inline_count: int = 0
    display_count: int = 0
    greek_mapped: int = 0
    greek_unresolved: list[str] = field(default_factory=list)

    def note(self, raw: str) -> str:
        self.notes.append(self.convert(raw).strip())
        return f"<sup>{len(self.notes)}</sup>"

    def number_math(self, env: str, raw: str) -> str:
        raw = raw.replace(r"\nonumber", "@@BOOLE-NONUMBER@@")
        raw = normalize_math(raw)
        if env.endswith("*"):
            return raw
        if env in {"equation", "gather", "multline"}:
            self.equation += 1
            if r"\tag" not in raw: raw += rf"\tag{{{self.equation}}}"
            return raw
        # eqnarray: each row is separately numbered unless \nonumber occurs.
        rows = re.split(r"(\\\\)", raw)
        for i in range(0, len(rows), 2):
            row = rows[i]
            if not row.strip(): continue
            if "@@BOOLE-NONUMBER@@" in row:
                rows[i] = row.replace("@@BOOLE-NONUMBER@@", "")
            else:
                self.equation += 1
                if r"\tag" not in row: rows[i] = row.rstrip() + rf"\tag{{{self.equation}}}"
        return "".join(rows)

    def math_environment(self, env: str, raw: str) -> str:
        self.display_count += 1
        suffix = ""
        # A few authorial notes occur syntactically inside equation environments.
        # Move only their markers outside the display; retain their bodies in the
        # same global note ledger as prose footnotes.
        while r"\footnote" in raw:
            p = raw.index(r"\footnote")
            if raw.startswith(r"\footnotemark", p):
                raw = raw[:p] + raw[p + len(r"\footnotemark"):]
                suffix += f"<sup>{len(self.notes)+1}</sup>"
                continue
            if raw.startswith(r"\footnotetext", p):
                body, end = group(raw, p + len(r"\footnotetext"))
                self.notes.append(self.convert(body).strip())
                raw = raw[:p] + raw[end:]
                continue
            body, end = group(raw, p + len(r"\footnote"))
            suffix += self.note(body)
            raw = raw[:p] + raw[end:]
        content = self.number_math(env, raw)
        if env.startswith("eqnarray") or env.startswith("align"):
            content = re.sub(r"\\tag\{([^{}]+)\}", r"\\qquad\\text{(\1)}", content)
            content = r"\begin{aligned}" + "\n" + content + "\n" + r"\end{aligned}"
        elif env.startswith("gather"):
            content = re.sub(r"\\tag\{([^{}]+)\}", r"\\qquad\\text{(\1)}", content)
            content = r"\begin{gathered}" + "\n" + content + "\n" + r"\end{gathered}"
        return "\n\n$$\n" + content + "\n$$\n" + suffix + "\n\n"

    def convert_environment(self, env: str, raw: str, arg: str | None = None) -> str:
        if env in MATH_ENVS: return self.math_environment(env, raw)
        if env in {"center", "quote", "verse", "Proposition"}:
            body = self.convert(raw).strip()
            if env == "quote": return "\n\n" + "\n> ".join(["> " + x for x in body.splitlines()]) + "\n\n"
            if env == "verse": return "\n\n" + body.replace("\n", "  \n") + "\n\n"
            if env == "Proposition": return "\n\n**Proposition.** " + body + "\n\n"
            return "\n\n" + body + "\n\n"
        if env == "itemize":
            parts = re.split(r"\\item(?:\[[^]]*\])?", raw)[1:]
            return "\n\n" + "\n".join("- " + tidy_fragment(self.convert(x)) for x in parts) + "\n\n"
        if env == "tabular":
            rows = []
            for row in re.split(r"\\\\", raw):
                cells = [tidy_fragment(self.convert(c)) for c in re.split(r"(?<!\\)&", row)]
                line = " ".join(c for c in cells if c)
                if line: rows.append(line)
            return "\n\n" + "  \n".join(rows) + "\n\n"
        if env == "tabbing":
            body = raw.replace(r"\=", " ").replace(r"\>", " ").replace(r"\kill", "")
            return "\n\n" + self.convert(body).strip() + "\n\n"
        self.unknown.add(f"begin{{{env}}}")
        return f"\\begin{{{env}}}{raw}\\end{{{env}}}"

    def convert(self, text: str) -> str:
        out: list[str] = []
        i = 0
        while i < len(text):
            if text.startswith(r"\[", i):
                end = text.find(r"\]", i + 2)
                if end < 0: raise ValueError("unclosed display math")
                self.display_count += 1
                raw_math = text[i+2:end]
                suffix = ""
                if r"\footnote" in raw_math:
                    p = raw_math.index(r"\footnote")
                    note_body, after = group(raw_math, p + len(r"\footnote"))
                    suffix = self.note(note_body)
                    raw_math = raw_math[:p] + raw_math[after:]
                out.append("\n\n$$\n" + normalize_math(raw_math) + "\n$$\n" + suffix + "\n\n")
                i = end + 2; continue
            if text[i] == "$":
                end = i + 1
                while True:
                    end = text.find("$", end)
                    if end < 0: raise ValueError(f"unclosed inline math at {i}")
                    if text[end - 1] != "\\": break
                    end += 1
                self.inline_count += 1
                out.append("$" + normalize_math(text[i+1:end]) + "$")
                i = end + 1; continue
            if text[i] == "{":
                body, i = group(text, i); out.append(self.convert(body)); continue
            if text[i] != "\\":
                out.append(" " if text[i] == "~" else text[i]); i += 1; continue
            name, pos = command_at(text, i)
            if name == "\\": out.append("\n"); i = pos; continue
            if name in {"textit", "emph"}:
                body, i = group(text, pos)
                converted = self.convert(body).strip()
                out.append((converted + "\n\n") if "$$" in converted else "*" + converted + "*")
                continue
            if name == "textbf":
                body, i = group(text, pos); out.append("**" + self.convert(body).strip() + "**"); continue
            if name == "textsc":
                body, i = group(text, pos); out.append(self.convert(body).upper()); continue
            if name in {"textrm", "mathrm", "text", "mbox", "centerline"}:
                body, i = group(text, pos); out.append(self.convert(body)); continue
            if name == "multicolumn":
                _, p = group(text, pos); _, p = group(text, p); body, i = group(text, p)
                out.append(self.convert(body)); continue
            if name == "footnote":
                body, i = group(text, pos); out.append(self.note(body)); continue
            if name == "footnotemark":
                out.append(f"<sup>{len(self.notes)+1}</sup>"); i = pos; continue
            if name == "footnotetext":
                body, i = group(text, pos); self.notes.append(self.convert(body).strip()); continue
            if name == "chapter":
                short, p = optional(text, pos)
                title, i = group(text, p)
                if short == "PREFACE.":
                    out.append("\n\n## PREFACE\n\n"); continue
                if short == "":
                    out.append("\n\n## NOTE\n\n"); continue
                self.chapter += 1; self.equation = 0
                clean = tidy_fragment(self.convert(title)).upper().rstrip(".")
                out.append(f"\n\n## CHAPTER {roman(self.chapter)}\n\n### {clean}\n\n"); continue
            if name == "section":
                title, i = group(text, pos); out.append("\n\n### " + tidy_fragment(self.convert(title)) + "\n\n"); continue
            if name == "begin":
                env, p = group(text, pos)
                arg = None
                if env == "tabular":
                    _, p = optional(text, p)
                    arg, p = group(text, p)
                elif env == "minipage": arg, p = group(text, p)
                raw, i = environment(text, p, env)
                out.append(self.convert_environment(env, raw, arg)); continue
            if name == "setcounter":
                counter, p = group(text, pos); value, i = group(text, p)
                if counter == "equation": self.equation = int(value)
                continue
            if name in {"label", "vspace", "hspace"}:
                _, i = group(text, pos); continue
            if name == "addcontentsline":
                _, p = group(text, pos); _, p = group(text, p); _, i = group(text, p); continue
            if name in SKIP: i = pos; continue
            if name == "par": out.append("\n\n"); i = pos; continue
            if name in {"&", "$", "%", "#", "_", "{", "}"}: out.append(name); i = pos; continue
            if name == " ": out.append(" "); i = pos; continue
            if name in {",", ";", ":"}: out.append(" "); i = pos; continue
            if name == "\n": out.append(" "); i = pos; continue
            if name in {"ae", "AE"}: out.append("æ" if name == "ae" else "Æ"); i = pos; continue
            if name in {"lq", "rq"}: out.append("‘" if name == "lq" else "’"); i = pos; continue
            if name in {"ldots", "dots"}: out.append("…"); i = pos; continue
            if name in {"'", "`", "^", '"', "~"}:
                body, i = accent_arg(text, pos); out.append(accent(name, body)); continue
            if name == "textgreek":
                body, i = group(text, pos)
                key = re.sub(r"\s+", " ", body).strip()
                if key in GREEK_MAP:
                    self.greek_mapped += 1
                    out.append(GREEK_MAP[key]); continue
                # Preserve the source's transliteration visibly pending printed-page
                # adjudication; never silently discard an unsupported script command.
                body = body.replace(r"\dots", "...").replace(r"\~", "~")
                key = re.sub(r"\s+", " ", body).strip()
                self.greek_unresolved.append(key)
                out.append("*[Greek: " + key + "]*"); continue
            self.unknown.add(name); out.append("\\" + name); i = pos
        return "".join(out)


def roman(n: int) -> str:
    vals = [(10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")]
    out = ""
    for v,s in vals:
        while n >= v: out += s; n -= v
    return out


def tidy_fragment(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def tidy(text: str) -> str:
    protected: list[str] = []
    def hold(m: re.Match[str]) -> str:
        protected.append(m.group(0)); return f"@@BOOLEMATH{len(protected)-1}@@"
    text = re.sub(r"\$\$[\s\S]*?\$\$|\$[^$\n]+\$", hold, text)
    text = text.replace("``", "“").replace("''", "”").replace("---", "—").replace("--", "–")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    blocks = []
    for block in text.split("\n\n"):
        block = block.strip()
        if not block: continue
        if block.startswith(("#", "$$", ">", "- ")) or "  \n" in block:
            blocks.append(block)
        else: blocks.append(re.sub(r"\s*\n\s*", " ", block))
    text = "\n\n".join(blocks)
    text = re.sub(r" +([,.;:?!])", r"\1", text)
    for i, value in enumerate(protected): text = text.replace(f"@@BOOLEMATH{i}@@", value)
    return text.strip() + "\n"


def build() -> tuple[str, Converter, dict[str, int]]:
    raw = SOURCE.read_text(encoding="latin-1")
    for anchor in (START, END, PREFACE, CONTENTS, NOTE, DEDICATION):
        assert raw.count(anchor) == 1, anchor
    assert not re.search(r"\\includegraphics|\\begin\{figure", raw)
    dedication_start = raw.index(DEDICATION)
    dedication_end = raw.index(r"\end{center}", dedication_start)
    dedication = raw[dedication_start:dedication_end]
    preface_start = raw.index(PREFACE)
    contents_start = raw.index(CONTENTS, preface_start)
    note_start = raw.index(NOTE, contents_start)
    end = raw.index(END, note_start)
    body = ("## DEDICATION\n\n" + dedication + "\n\n" +
            raw[preface_start:contents_start] + raw[note_start:end])
    body = replace_command(
        body,
        r"\footnote{Original text was \lq\lq probabibilities",
        "",
    )
    body = replace_command(
        body,
        r"\footnote{The following footnote was in the original text",
        r"\footnotemark",
    )
    body = replace_command(
        body,
        r"\footnote{The numerator was originally",
        "",
    )
    body = strip_comments(body)
    # TeX splits a few very long Greek formulas as adjacent math runs. Joining
    # the close/open delimiters restores the single expression they typeset.
    body = re.sub(r"(?<!\\)\$\s+(?<!\\)\$", " ", body)
    # One marker/note pair is explicitly Distributed Proofreaders apparatus,
    # identifying an already-applied correction rather than Boole's note.
    marker = r"and\footnotemark\ so on"
    assert body.count(marker) == 1
    body = body.replace(marker, "and so on")
    dp = r"\footnotetext{The original text was"
    assert body.count(dp) == 1
    p = body.index(dp)
    note_body, after = group(body, p + len(r"\footnotetext"))
    assert "corrected here by Distributed Proofreaders" in note_body
    body = body[:p] + body[after:]
    source_env = {e: len(re.findall(r"\\begin\{" + re.escape(e) + r"\}", body)) for e in MATH_ENVS}
    conv = Converter()
    markdown = tidy("# AN INVESTIGATION OF THE LAWS OF THOUGHT\n\n" + conv.convert(body))
    assert conv.chapter == 22, conv.chapter
    assert len(conv.notes) == 54, len(conv.notes)
    notes = ("\n\n## AUTHORIAL NOTES\n\n" +
             "\n\n".join(f"{i}. {tidy(x).strip()}" for i,x in enumerate(conv.notes,1)) + "\n")
    markdown = markdown.rstrip() + notes
    assert markdown.count("PREFACE.\n\n—$\\diamond$—") == 1
    markdown = markdown.replace("PREFACE.\n\n—$\\diamond$—\n\n", "")
    assert markdown.count("## NOTE\n\nNOTE.\n\n") == 1
    markdown = markdown.replace("## NOTE\n\nNOTE.\n\n", "## NOTE\n\n")
    broken = ("substituted in the expression of any constituent for\n\n"
              "each of the symbols")
    assert markdown.count(broken) == 1
    markdown = markdown.replace(broken, "substituted in the expression of any constituent for each of the symbols")
    assert markdown.count("## CHAPTER ") == 22
    assert markdown.count("## PREFACE") == 1 and markdown.count("## NOTE") == 1
    assert conv.display_count == sum(source_env.values()) + body.count(r"\[")
    assert "@@BOOLE-NONUMBER@@" not in markdown
    assert body.count(r"\nonumber") == 15
    assert conv.greek_mapped == 9, conv.greek_mapped
    assert len(conv.greek_unresolved) == 4, len(conv.greek_unresolved)
    return markdown, conv, source_env


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    markdown, conv, envs = build()
    print(f"chapters=22 notes={len(conv.notes)} inline_math={conv.inline_count} displays={conv.display_count}")
    print(f"textgreek mapped={conv.greek_mapped} unresolved={len(conv.greek_unresolved)}")
    print("source math environments:", ", ".join(f"{k}={v}" for k,v in sorted(envs.items())))
    print("unknown prose commands:", ", ".join(sorted(conv.unknown)) or "none")
    print(f"output bytes={len(markdown.encode())}")
    if conv.unknown:
        raise SystemExit("refusing output with unknown prose commands")
    if args.apply:
        OUTPUT.write_text(markdown, encoding="utf-8")
        print(f"wrote {OUTPUT.name}")


if __name__ == "__main__": main()
