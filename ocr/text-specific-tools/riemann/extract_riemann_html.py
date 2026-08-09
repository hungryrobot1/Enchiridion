#!/usr/bin/env python3
"""Extract Riemann's geometry lecture from the supplied saved HTML.

The HTML is a structured transcription, not a printed witness.  Its five
formula GIFs carry the strings used to set them in ``alt`` attributes, so this
converter reads those strings directly rather than OCRing the pixels.  It keeps
the complete lecture and its closing synopsis, removes the one bibliographic
source note, and asserts the source structure and notation inventory.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from lxml import html


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source" / "On the Hypotheses which lie at the Bases of Geometry..html"
OUTPUT = ROOT / "riemann.raw.md"


def clean_space(value: str) -> str:
    value = value.replace("\u00ad", "").replace("\xa0", " ")
    value = re.sub(r"[ \t\r\f\v]+", " ", value)
    value = re.sub(r" *\n *", " ", value)
    value = re.sub(r" +([,.;:?!])", r"\1", value)
    return value.strip()


class InlineRenderer:
    def __init__(self) -> None:
        self.math: list[str] = []
        self.subs: list[str] = []
        self.sups: list[str] = []
        self.formulas: list[str] = []

    @staticmethod
    def _token(kind: str, index: int) -> str:
        return f"@@{kind}{index}@@"

    def node(self, element) -> str:
        tag = element.tag.lower() if isinstance(element.tag, str) else ""
        if tag == "br":
            return "@@BR@@"
        if tag == "img":
            alt = element.get("alt")
            assert alt and alt.startswith("\\"), "formula image lacks LaTeX alt text"
            self.formulas.append(alt.strip())
            return self._token("F", len(self.formulas) - 1)
        if tag == "i":
            value = clean_space(element.text_content())
            assert value in {"n", "x", "dx", "ds", "s"}, value
            self.math.append(value)
            return self._token("M", len(self.math) - 1)
        if tag in {"sub", "sup"}:
            value = clean_space(element.text_content())
            assert value in {"0", "1", "2", "3", "n"}, value
            target = self.subs if tag == "sub" else self.sups
            target.append(value)
            return self._token("S" if tag == "sub" else "U", len(target) - 1)

        value = element.text or ""
        for child in element:
            value += self.node(child)
            value += child.tail or ""
        if tag == "em":
            value = f"*{value.strip()}*"
        return value

    def finish(self, value: str) -> str:
        # Join a variable with any immediately following HTML sub/superscripts
        # before introducing Markdown math delimiters.
        pattern = re.compile(r"@@M(\d+)@@((?:@@[SU]\d+@@)*)")

        def variable(match: re.Match[str]) -> str:
            base = self.math[int(match.group(1))]
            suffix = ""
            for kind, number in re.findall(r"@@([SU])(\d+)@@", match.group(2)):
                values = self.subs if kind == "S" else self.sups
                suffix += ("_{" if kind == "S" else "^{") + values[int(number)] + "}"
            return f"${base}{suffix}$"

        value = pattern.sub(variable, value)
        for index, formula in enumerate(self.formulas):
            value = value.replace(self._token("F", index), f"${formula}$")
        assert not re.search(r"@@[MSUF]\d+@@", value), value
        return value

    def content(self, element) -> str:
        value = element.text or ""
        for child in element:
            value += self.node(child)
            value += child.tail or ""
        return self.finish(value)


def paragraphs(value: str) -> list[str]:
    # Two HTML breaks delimit synopsis items; a lone break is merely a space.
    value = re.sub(r"(?:\s*@@BR@@\s*){2,}", "\n\n", value)
    value = value.replace("@@BR@@", " ")
    return [clean_space(part) for part in value.split("\n\n") if clean_space(part)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("cp1252")
    assert source_text.count("§") == 22
    assert source_text.count("½") == 8
    root = html.fromstring(source_bytes)
    body = root.xpath("//body")[0]

    headings = [clean_space(x.text_content()) for x in body.xpath("./h1|./h2")]
    assert headings == [
        "On the Hypotheses which lie at the Bases of Geometry.",
        "Bernhard Riemann Translated by William Kingdon Clifford",
        "Plan of the Investigation.",
        "I. Notion of an n-ply extended magnitude.",
        "II. Measure-relations of which a manifoldness of n dimensions is capable on the assumption that lines have a length independent of position, and consequently that every line may be measured by every other.",
        "III. Application to Space.",
        "Synopsis.",
    ], headings

    images = body.xpath(".//img")
    assert len(images) == 6
    assert len({x.get("src") for x in images}) == 5
    for image in images:
        path = (SOURCE.parent / image.get("src")).resolve()
        assert path.is_file(), f"missing source asset: {image.get('src')}"
    assert [x.get("alt") for x in images] == [
        r"\sqrt{ \sum (dx)^2 }",
        r"\sqrt{ \sum dx^2 }",
        r"\sum dx^2",
        r"\sum dx^2",
        r"\alpha",
        r"\frac{1}{1 + \frac{1}{4} \alpha \sum x^2} \sqrt{\textstyle \sum dx^2 }.",
    ]

    publication_notes = body.xpath(
        './p[starts-with(normalize-space(string(.)), "[Nature,")]'
    )
    assert len(publication_notes) == 1

    renderer = InlineRenderer()
    out = [
        "# On the Hypotheses which lie at the Bases of Geometry.",
        "*Translated by William Kingdon Clifford*",
    ]
    loose = ""

    def flush_loose() -> None:
        nonlocal loose
        if loose.strip():
            out.extend(paragraphs(renderer.finish(loose)))
        loose = ""

    for index, element in enumerate(body):
        tag = element.tag.lower() if isinstance(element.tag, str) else ""
        if index in {0, 1} or element in publication_notes:
            pass
        elif tag == "h2":
            flush_loose()
            label = clean_space(renderer.content(element))
            if label.startswith("*") and label.endswith("*"):
                label = label[1:-1]
            out.append(f"## {label}")
        elif tag == "p":
            flush_loose()
            content = renderer.content(element)
            out.extend(paragraphs(content))
        elif tag == "blockquote":
            flush_loose()
            content = renderer.content(element)
            parts = paragraphs(content)
            if len(parts) == 1 and re.fullmatch(r"\$.*\$", parts[0]):
                formula = parts[0][1:-1]
                out.append(f"$$\n{formula}\n$$")
            else:
                out.extend(parts)
        elif tag in {"br", "hr"}:
            flush_loose()
        else:
            loose += renderer.node(element)
        loose += element.tail or ""
    flush_loose()

    result = "\n\n".join(x for x in out if x.strip()) + "\n"
    assert result.count("## ") == 5
    assert result.count("$\\sqrt") == 2
    assert result.count("$\\sum dx^2$") == 2
    assert "Nature, Vol." not in result
    assert "## Synopsis." in result
    assert result.endswith("Connection of this question with the interpretation of nature.\n")
    args.output.write_text(result, encoding="utf-8")
    print(f"wrote {args.output}: {len(result):,} chars, {len(result.split()):,} whitespace tokens")
    print("source assertions: 7 headings, 6 formula uses/5 assets, 22 section signs")
    print("removed: 1 bibliographic publication note; retained: full synopsis")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
