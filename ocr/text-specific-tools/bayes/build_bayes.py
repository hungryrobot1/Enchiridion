#!/usr/bin/env python3
"""Build reader-ready Bayes/Price markdown from the 49-page raw OCR.

Every non-generic repair is either licensed by internal evidence (long-s OCR,
duplicated catchwords, impossible word joins) or cites the printed page in the
nearby comment.  Exact counts make source drift fail loudly.
"""

from pathlib import Path
import re

RAW = Path("source/raw.md")
OUT = Path("bayes-essay-towards-solving-a-problem-in-doctrine-of-chances.md")


def replace_exact(s: str, old: str, new: str, count: int = 1) -> str:
    got = s.count(old)
    assert got == count, f"expected {count} occurrence(s), found {got}: {old[:90]!r}"
    return s.replace(old, new)


def sub_exact(s: str, pattern: str, replacement: str, count: int = 1) -> str:
    repl = replacement if callable(replacement) else (lambda _m: replacement)
    out, got = re.subn(pattern, repl, s, flags=re.S)
    assert got == count, f"expected {count} regex match(es), found {got}: {pattern[:90]!r}"
    return out


def main() -> None:
    pages = RAW.read_text(encoding="utf-8").split("\n\n---\n\n")
    assert len(pages) == 49, f"expected 49 OCR pages, found {len(pages)}"

    # Printed catchwords repeat the next leaf's opening; folios and signature
    # marks are page furniture. These are page-indexed so identical body text
    # elsewhere cannot be touched.
    tail_catchwords = {
        7: "Suppose", 9: "same", 12: "P R O P.", 13: "may", 15: "prop.",
        19: "culars", 21: "to", 23: "we", 27: "ner", 35: "In", 40: "An",
        42: "Let", 44: "throw", 46: "supposed", 51: "this", 54: "Suppose,",
        57: "drawn", 58: "that", 60: "and", 62: "By",
    }
    # Keys above are raw line-oriented page-boundary labels from the first
    # audit; translate the relevant PDF-page positions explicitly.
    page_catchwords = {
        7: "Suppose", 9: "same", 12: "P R O P.", 13: "may", 15: "prop.",
        19: "culars", 21: "to", 23: "we", 27: "ner", 35: "In", 40: "An",
        42: "Let", 44: "throw", 46: "supposed", 51: "this", 54: "Suppose,",
        57: "drawn", 58: "that", 60: "and", 62: "By",
    }
    # Actual 1-indexed PDF pages corresponding to those boundary catchwords.
    actual = {
        5: "Mr.", 7: "Suppose", 9: "same", 13: "may", 15: "prop.",
        19: "culars", 21: "to", 23: "we", 26: "ner", 31: "In", 34: "An",
        35: "Let", 37: "throw", 39: "supposed", 41: "this", 43: "Suppose,",
        44: "drawn", 45: "that", 46: "and", 47: "By",
    }
    del tail_catchwords, page_catchwords
    for number, word in actual.items():
        lines = pages[number - 1].rstrip().splitlines()
        while lines and not lines[-1].strip():
            lines.pop()
        assert lines[-1].strip() == word, (number, word, lines[-1] if lines else None)
        lines.pop()
        pages[number - 1] = "\n".join(lines).rstrip()
    # On p.381 the catchword sits above the two footnotes, not at page bottom.
    pages[11] = replace_exact(pages[11], "\n\nP R O P.\n\n", "\n\n")

    for number, furniture in {
        13: "# [382]", 15: "# [384]", 32: "# [ 401 ]",
        34: "# [ 403 ]", 43: "# [ 412 ]",
    }.items():
        pages[number - 1] = replace_exact(pages[number - 1], furniture + "\n\n", "")
    pages[44 - 1] = replace_exact(pages[44 - 1], "\n\nVOL. LIII.\n\nH h h", "")
    pages[46 - 1] = replace_exact(pages[46 - 1], "\n\nHhh 2", "")

    # Printed p.382: Price's dagger note continues from p.381 in the lower
    # band. OCR inserted its continuation after Prop. 6's first body paragraph.
    continuation = (
        "be accompanied with another to be determined at the same time? In this case, as one of "
        "the events is given, nothing can be due for the expectation of it; and, consequently, "
        "the value of an expectation depending on the happening of both events must be the same "
        "with the value of an expectation depending on the happening of one of them. In other "
        "words; the probability that, when one of two events happens, the other will, is the same "
        "with the probability of this other. Call $x$ then the probability of this other, and if "
        "$\\frac{b}{N}$ be the probability of the given event, and $\\frac{p}{N}$ the probability "
        "of both, because $\\frac{p}{N} = \\frac{b}{N} \\times x$, $x = \\frac{p}{b} =$ the "
        "probability mentioned in these propositions."
    )
    pages[12] = replace_exact(pages[12], "\n\n" + continuation, "")
    pages[11] = pages[11].rstrip() + " " + continuation + "\n"

    # Printed p.381: the mark after P/b is the dagger introducing Price's note,
    # not a plus sign in the numerator.
    pages[11] = replace_exact(pages[11], "$$\\frac{P+}{b}$$", "$\\frac{P}{b}$†")

    # Printed p.384, Prop. 7: all instances are E a^p b^q and the binomial is
    # (a+b)^(p+q). OCR repeatedly read superscript letters as b/c.
    pages[14] = replace_exact(pages[14], "$E a^b$", "$E a^p b^q$")
    pages[14] = replace_exact(pages[14], "$a^b b^c$", "$a^p b^q$", 5)
    pages[14] = replace_exact(
        pages[14], "$\\overline{a+b}|^{b+q}$", "$(a+b)^{p+q}$"
    )
    pages[14] = replace_exact(
        pages[14], "$\\overline{a+b}|^{p+q}$", "$(a+b)^{p+q}$"
    )

    # Reconcile each physical page boundary after catchwords are gone.
    joined = pages[0].rstrip()
    for nxt in pages[1:]:
        nxt = nxt.lstrip()
        if joined.endswith("-") and nxt and nxt[0].islower():
            joined = joined[:-1] + nxt
        else:
            # A lowercase opener or an unfinished clause continues the same
            # paragraph. Otherwise retain a paragraph boundary.
            prev = joined.rstrip()
            first = nxt[0] if nxt else ""
            if first.islower() or (prev and prev[-1] in ",—"):
                joined = prev + " " + nxt
            else:
                joined = prev + "\n\n" + nxt
    s = joined

    # Printed p.398, articles 4–5. OCR built one enormous display containing
    # prose and left its delimiters unbalanced. Re-state the same page layout as
    # prose with inline formulas. The ratios and exponents are read from p.398.
    article4 = (
        "4. If E be the coefficient of that term of the binomial $(a+b)^{p+q}$ expanded in which "
        "occurs $a^p b^q$, the ratio of the whole figure ACFH to HO is "
        "$\\frac{1}{n+1} \\times \\frac{1}{E}$, $n$ being $=p+q$. For, when $Af=AH$, "
        "$x=1$, $r=0$. Wherefore, all the terms of the series set down in Art. 2 as expressing "
        "the ratio of ACf to HO will vanish except the last, and that becomes "
        "$\\frac{1}{n+1} \\times \\frac{q}{p+1} \\times \\frac{q-1}{p+2} \\times \\&c. "
        "\\times \\frac{1}{n}$. But E being the coefficient of that term in the binomial "
        "$(a+b)^n$ expanded in which occurs $a^p b^q$ is equal to "
        "$\\frac{p+1}{q} \\times \\frac{p+2}{q-1} \\times \\&c. \\times \\frac{n}{1}$. "
        "And, because $Af$ is supposed to become $=AH$, $ACf=ACH$. From whence this article is plain."
    )
    s = sub_exact(s, r"4\. If E be the coefficient.*?From whence this article is plain\.\}?\$\$", article4)
    s = replace_exact(s, "difference between between the two series", "difference between the two series")

    # Printed p.399, Rule 1. This formula carries the operative ratio. OCR left
    # most variables as prose and changed multiplication signs to the letter x.
    rule1 = (
        "If nothing is known concerning an event but that it has happened $p$ times and failed $q$ "
        "in $p+q$ or $n$ trials, and from hence I guess that the probability of its happening in a "
        "single trial lies somewhere between any two degrees of probability as $X$ and $x$, the "
        "chance I am in the right in my guess is $(n+1) \\times E \\times d$ into the difference "
        "between the series\n\n"
        "$$\\frac{X^{p+1}}{p+1} - q\\frac{X^{p+2}}{p+2} + q \\times \\frac{q-1}{2} "
        "\\times \\frac{X^{p+3}}{p+3} - \\&c.$$\n\n"
        "and the series\n\n"
        "$$\\frac{x^{p+1}}{p+1} - q\\frac{x^{p+2}}{p+2} + q \\times \\frac{q-1}{2} "
        "\\times \\frac{x^{p+3}}{p+3} - \\&c.$$\n\n"
        "$E$ being the coefficient of $a^p b^q$ when $(a+b)^n$ is expanded."
    )
    s = sub_exact(
        s,
        r"If nothing is known concerning an event but that it has happened p times.*?when a\^1 \+ b\^1\^n is expanded\.",
        lambda _m: rule1,
    )

    # Printed pp.395–397. OCR flattened the displayed derivation and repeatedly
    # read superscripts p+1, p+2, … as fractional exponents. This bounded
    # replacement follows the pages; notably, the edition itself prints q-3 in
    # the last term of the fluxion footnote, which is retained here.
    derivation = r"""which purpose, suppose $AH=1$ and $HO$, the square upon $AH$, likewise $=1$, and $Cf=y$, and $Af=x$, and $Hf=r$, because $y$, $x$ and $r$ denote the ratios of $Cf$, $Af$, and $Hf$ respectively to $AH$. And by the equation of the curve $y=x^p r^q$ and (because $Af+fH=AH$) $r+x=1$. Wherefore

$$y=x^p(1-x)^q=x^p-qx^{p+1}+q\times\frac{q-1}{2}\times x^{p+2}-q\times\frac{q-1}{2}\times\frac{q-2}{3}\times x^{p+3}+\&c.$$

Now the abscissa being $x$ and the ordinate $x^p$, the correspondent area is $\frac{x^{p+1}}{p+1}$ (by prop. 10. cas. 1. Quadrat. Newt.)* and the ordinate being $qx^{p+1}$ the area is $\frac{qx^{p+2}}{p+2}$; and in like manner of the rest. Wherefore, the abscissa being $x$ and the ordinate $y$, or $x^p-qx^{p+1}+\&c.$, the correspondent area is

$$\frac{x^{p+1}}{p+1}-q\times\frac{x^{p+2}}{p+2}+q\times\frac{q-1}{2}\times\frac{x^{p+3}}{p+3}-q\times\frac{q-1}{2}\times\frac{q-2}{3}\times\frac{x^{p+4}}{p+4}+\&c.$$

Wherefore, if $x=Af=\frac{Af}{AH}$ and $y=Cf=\frac{Cf}{AH}$, then

$$ACf=\frac{ACf}{HO}=\frac{x^{p+1}}{p+1}-q\times\frac{x^{p+2}}{p+2}+q\times\frac{q-1}{2}\times\frac{x^{p+3}}{p+3}-\&c.$$

From which equation, if $q$ be a small number, it is easy to find the value of the ratio of $ACf$ to $HO$. And in like manner as that was found out, it will appear that the ratio of $HCf$ to $HO$ is

$$\frac{r^{q+1}}{q+1}-p\times\frac{r^{q+2}}{q+2}+p\times\frac{p-1}{2}\times\frac{r^{q+3}}{q+3}-p\times\frac{p-1}{2}\times\frac{p-2}{3}\times\frac{r^{q+4}}{q+4}+\&c.$$

which series will consist of few terms and therefore is to be used when $p$ is small.

2. The same things supposed as before, the ratio of $ACf$ to $HO$ is

$$\frac{x^{p+1}r^q}{p+1}+\frac{q}{p+1}\times\frac{x^{p+2}r^{q-1}}{p+2}+\frac{q}{p+1}\times\frac{q-1}{p+2}\times\frac{x^{p+3}r^{q-2}}{p+3}+\frac{q}{p+1}\times\frac{q-1}{p+2}\times\frac{q-2}{p+3}\times\frac{x^{p+4}r^{q-3}}{p+4}+\&c.$$

$$+\frac{x^{n+1}}{n+1}\times\frac{q}{p+1}\times\frac{q-1}{p+2}\times\&c.\times\frac{1}{n},$$

where $n=p+q$. For this series is the same with $\frac{x^{p+1}}{p+1}-q\times\frac{x^{p+2}}{p+2}+\&c.$ set down in Art. 1st as the value of the ratio of $ACf$ to $HO$; as will easily be seen by putting in the former instead of $r$ its value $1-x$, and expanding the terms and ordering them according to the powers of $x$. Or, more readily, by comparing the fluxions of the two series, and in the former instead of $\dot r$ substituting $-\dot x$.*

* This is very evident here, without having recourse to Sir Isaac Newton, that the fluxion of the area $ACf$ being

$$y\dot x=x^p\dot x-qx^{p+1}\dot x+q\times\frac{q-1}{2}x^{p+2}\dot x+\&c.,$$

the fluent or area itself is

$$\frac{x^{p+1}}{p+1}-q\times\frac{x^{p+2}}{p+2}+q\times\frac{q-1}{2}\times\frac{x^{p+3}}{p+3}+\&c.$$

The fluxion of the first series is

$$x^p r^q\dot x+\frac{q x^{p+1}r^{q-1}\dot r}{p+1}+\frac{q x^{p+1}r^{q-1}\dot x}{p+1}+q\times\frac{q-1}{p+1}\times\frac{x^{p+2}r^{q-2}\dot r}{p+2}+q\times\frac{q-1}{p+1}\times\frac{x^{p+2}r^{q-2}\dot x}{p+2}+q\times\frac{q-1}{p+1}\times\frac{q-3}{p+2}\times\frac{x^{p+3}r^{q-3}\dot r}{p+3}+\&c.$$

or, substituting $-\dot x$ for $\dot r$,

$$x^p r^q\dot x-\frac{q x^{p+1}r^{q-1}\dot x}{p+1}+\frac{q x^{p+1}r^{q-1}\dot x}{p+1}-q\times\frac{q-1}{p+1}\times\frac{x^{p+2}r^{q-2}\dot x}{p+2}+q\times\frac{q-1}{p+1}\times\frac{x^{p+2}r^{q-2}\dot x}{p+2}+\&c.,$$

which, as all the terms after the first destroy one another, is equal to $x^p r^q\dot x=x^p(1-x)^q\dot x=x^p\dot x\left(1-qx+q\frac{q-1}{2}x^2+\&c.\right)=x^p\dot x-qx^{p+1}\dot x+q\frac{q-1}{2}x^{p+2}\dot x+\&c.$, the fluxion of the latter series, or of $\frac{x^{p+1}}{p+1}-q\frac{x^{p+2}}{p+2}+\&c.$ The two series therefore are the same."""
    s = sub_exact(s, r"which purpose, suppose AH = 1.*?The two series therefore are the same\.", derivation)

    # Internal-evidence repairs: long-s glyphs and unambiguous English words.
    s = s.replace("ſ", "s")
    long_s_words = {
        "abfurd":"absurd", "absciffe":"abscisse", "afferted":"asserted",
        "alfo":"also", "becaufe":"because", "cafes":"cases",
        "confequently":"consequently", "demonftrated":"demonstrated",
        "difcovered":"discovered", "expreffion":"expression", "exprefs":"express",
        "fame":"same", "fay":"say", "feems":"seems", "feries":"series",
        "fhew":"shew", "fhould":"should", "fignify":"signify",
        "fimilar":"similar", "fince":"since", "fingle":"single",
        "firft":"first", "fomewhere":"somewhere", "fubfequent":"subsequent",
        "fufficient":"sufficient", "fum":"sum", "fuppofed":"supposed",
        "fuppofing":"supposing", "fuppofition":"supposition", "guefs":"guess",
        "infcribing":"inscribing", "laft":"last", "lefs":"less",
        "muft":"must", "nearnefs":"nearness", "neceffary":"necessary",
        "obfervation":"observation", "refpect":"respect", "reinfated":"reinstated",
        "Simpfon":"Simpson", "thefe":"these", "ufe":"use", "whofe":"whose",
        "exactnefs":"exactness", "conféquent":"consequent",
    }
    for old, new in long_s_words.items():
        s = re.sub(rf"\b{re.escape(old)}\b", new, s)

    for old, new, count in [
        ("those a remuch mistaken", "those are much mistaken", 1),
        ("every every valuable blessing", "every valuable blessing", 1),
        ("in so many differentials, is in reality", "in so many different trials, is in reality", 1),
        ("noticeof mathematicians", "notice of mathematicians", 1),
        ("b1 and mz", "$b$ and $mz$", 1),
        ("depending pending on", "depending on", 1),
        ("the 2d event event has happened", "the 2d event has happened", 1),
        ("shall rest rest somewhere", "shall rest somewhere", 1),
        ("is is the ratio", "is the ratio", 1),
        ("being the the coefficient", "being the coefficient", 1),
        ("in Eee 2 the the right", "in the right", 1),
        ("first rule, rule, is", "first rule is", 1),
        ("under the same\n\ncircumcircumstances", "under the same circumstances", 1),
    ]:
        s = replace_exact(s, old, new, count)
    assert len(re.findall(r"\b1ft\b", s)) == 6
    s = re.sub(r"\b1ft\b", "1st", s)

    # Printed p.388, Prop. 8: restore the four exponent/ratio expressions that
    # OCR flattened into ordinary spaced letters.
    s = replace_exact(
        s,
        "and E being the coefficient of the term in which occurs a p b q when the binomial a + b p + q is expanded) y = E x p r q.",
        "and $E$ being the coefficient of the term in which occurs $a^p b^q$ when the binomial $(a+b)^{p+q}$ is expanded) $y=Ex^p r^q$.",
    )

    # Printed pp.405–406: the page-bottom note was inserted between the two
    # halves of Price's next paragraph. Move it behind the paragraph it annotates.
    note405 = "* There can, I suppose, be no reason for observing that on this subject unity is always made to stand for certainty, and $$\\frac{1}{2}$$ for an even chance."
    s = replace_exact(s, "\n\n" + note405 + " enquiry to be", " enquiry to be")
    marker405 = "odds that it is somewhat more than an even chance that it will happen on a second trial *."
    s = replace_exact(s, marker405, marker405 + "\n\n" + note405)
    # Printed exponent 11, p.406.
    s = replace_exact(s, "\\frac{16}{17}'' - \\frac{2}{3}''", "(\\frac{16}{17})^{11} - (\\frac{2}{3})^{11}")

    # Printed pp.407–408: ratios whose one-digit denominators OCR dropped.
    s = replace_exact(s, "$\\frac{1.600000}{1.600000}$", "$\\frac{1,600,000}{1,600,001}$")
    s = replace_exact(s, "equal to 1400000 raised", "equal to $\\frac{1,400,000}{1,400,001}$ raised")

    # Printed pp.413–414: join the body across the footnote band, then place the
    # note after the completed paragraph rather than inside it.
    note413 = re.search(r"\* I suppose no attentive person.*?separately unlikely\.", s)
    assert note413, "p.413 footnote not found"
    note413_text = note413.group(0)
    s = s[:note413.start()] + s[note413.end():]
    s = replace_exact(s, "same with that of the number of blanks\n\n drawn", "same with that of the number of blanks drawn")
    marker413 = "they are all separately unlikely."
    # The note was removed, so attach it after the completed paragraph ending
    # with the lottery-wheel comparison on printed p.414.
    end414 = "there were in the wheel about so many more blanks than prizes."
    s = replace_exact(s, end414, end414 + "\n\n" + note413_text)

    # Printed pp.415–417: page-verified approximation ratios and intervals.
    s = replace_exact(
        s,
        "$\\frac{2\\Sigma}{1-2Ea^p b^q + 2Ea^p b^q}$",
        "$\\frac{2\\Sigma}{1-2Ea^p b^q + \\frac{2Ea^p b^q}{n}}$",
    )
    s = replace_exact(
        s,
        "$\\frac{2 \\Sigma}{1-2 \\operatorname{E} a^p b^q - 2 \\operatorname{E} a^p b_q}$",
        "$\\frac{2\\Sigma}{1-2Ea^p b^q - \\frac{2Ea^p b^q}{n}}$",
    )
    s = replace_exact(s, "\\operatorname{E} a^p p^q", "E a^p b^q")
    s = replace_exact(s, "$\\frac{1}{112} = z", "$\\frac{1}{110} = z")
    s = replace_exact(s, "\\frac{m^5 z}{5}", "\\frac{m^5 z^5}{5}")
    s = replace_exact(s, "$\\frac{0}{10}$", "$\\frac{9}{10}$")
    s = replace_exact(s, "$z = \\frac{1}{22}$", "$z = \\frac{1}{55}$")
    s = replace_exact(s, "\\frac{10}{11} + \\frac{1}{22}", "\\frac{10}{11} + \\frac{1}{55}")
    s = replace_exact(s, "\\frac{10}{11} - \\frac{1}{22}", "\\frac{10}{11} - \\frac{1}{55}")
    # Printed p.415: first two terms of each series.
    s = replace_exact(s, "\\frac{X^{p+1}}{p+2}", "\\frac{X^{p+1}}{p+1}")
    s = replace_exact(s, "\\frac{qX^{p+1}}{p+2}", "\\frac{qX^{p+2}}{p+2}")

    # Printed p.400, Rule 2, and p.401 continuation.
    s = replace_exact(s, "$m^2 = \\frac{n^2}{pq} a", "$m^2 = \\frac{n^3}{pq}$, $a")
    s = replace_exact(s, "$mz - \\frac{m^2 z^2}{3}", "$mz - \\frac{m^3 z^3}{3}")
    s = replace_exact(s, "\\text{E} a_p b^q", "\\text{E} a^p b^q")
    s = replace_exact(s, "E aᵖ bᵗ", "$E a^p b^q$", 2)
    s = replace_exact(s, "$E a^p b^q$ will be equal to $$\\frac{\\sqrt{n}}{2\\sqrt{Kpq}} \\times$$ by the ratio", "$E a^p b^q$ will be equal to $\\frac{b\\sqrt{n}}{2\\sqrt{Kpq}}$, $b$ being the ratio")
    # The page groups each Bernoulli correction before multiplying it.
    s = replace_exact(
        s,
        "$$\\frac{1}{12} \\times \\frac{1}{n} - \\frac{1}{p} - \\frac{1}{q} - \\frac{1}{360} \\times \\frac{1}{n^3} - \\frac{1}{p^3}$$\n$$\\frac{1}{q^3} + \\frac{1}{1260} \\times \\frac{1}{n^5} - \\frac{1}{p^5} - \\frac{1}{q^5} - \\frac{1}{1680} \\times \\frac{1}{n^7} - \\frac{1}{p^7} - \\frac{1}{q^7} + \\frac{1}{1188} \\times \\frac{1}{n^9} - \\frac{1}{p^9} - \\frac{1}{q^9}$$",
        "$\\frac{1}{12}(\\frac{1}{n}-\\frac{1}{p}-\\frac{1}{q})-\\frac{1}{360}(\\frac{1}{n^3}-\\frac{1}{p^3}-\\frac{1}{q^3})+\\frac{1}{1260}(\\frac{1}{n^5}-\\frac{1}{p^5}-\\frac{1}{q^5})-\\frac{1}{1680}(\\frac{1}{n^7}-\\frac{1}{p^7}-\\frac{1}{q^7})+\\frac{1}{1188}(\\frac{1}{n^9}-\\frac{1}{p^9}-\\frac{1}{q^9})$",
    )

    # Printed pp.372–373: Price's note belongs to the sentence carrying its
    # asterisk, not between the two halves of the page-turn sentence.
    note372 = "* See his Doctrine of Chances, p. 252, &c."
    s = replace_exact(s, "\n\n" + note372 + " the effect", " the effect")
    end372 = "and not from any of the irregularities of chance."
    s = replace_exact(s, end372, end372 + "\n\n" + note372)

    # Printed pp.402–403. These are not plausibility repairs: every exponent,
    # factor, and ratio below was read from the page images. OCR had flattened
    # the powers into adjacent numerals and put fraction bars around the wrong
    # groups. Keep Price's Simpson footnote, but move it after the uninterrupted
    # series it annotates.
    approximation_bounds = r"""greater or less than the series

$$\frac{Hn}{n+1}\times\frac{\sqrt K}{\sqrt 2}
-\frac{n}{n+2}\times\frac{\left(1-\frac{2m^2z^2}{n}\right)^{\frac n2+1}}{2mz}
+\frac{n^2}{n+2}\times\frac{\left(1-\frac{2m^2z^2}{n}\right)^{\frac n2+2}}{(n+4)\times4m^3z^3}$$

$$+\frac{3n^3}{n+2}\times\frac{\left(1-\frac{2m^2z^2}{n}\right)^{\frac n2+3}}{(n+4)(n+6)\times8m^5z^5}
+\frac{3\times5\times n^4}{n+2}\times\frac{\left(1-\frac{2m^2z^2}{n}\right)^{\frac n2+4}}{(n+4)(n+6)(n+8)\times16m^7z^7}-\&c.,$$

continued to any number of terms, according as the last term has a positive or a negative sign before it.

* This method of finding these coefficients I have deduced from the demonstration of the third lemma at the end of Mr. Simpson's Treatise on the Nature and Laws of Chance."""
    s = sub_exact(
        s,
        r"greater or less than the series .*?continued to any number of terms, according as the last term has a positive or a negative sign before it\.",
        approximation_bounds,
    )

    rule3 = r"""# R U L E 3.

If nothing is known of an event but that it has happened p times and failed q in p+q or n trials, and from hence I judge that the probability of it's happening in a single trial lies between $\frac{p}{n}+z$ and $\frac{p}{n}-z$, my chance to be right is greater than

$$\frac{\sqrt{Kpq}\times b}{2\sqrt{Kpq}+bn^{\frac12}+bn^{-\frac12}}\times\left(2H-\frac{\sqrt2}{\sqrt K}\times\frac{n+1}{n+2}\times\frac{1}{mz}\times\left(1-\frac{2m^2z^2}{n}\right)^{\frac n2+1}\right),$$

and less than

$$\frac{\sqrt{Kpq}\times b}{2\sqrt{Kpq}-bn^{\frac12}-bn^{-\frac12}}$$

multiplied by the 3 terms

$$2H-\frac{\sqrt2}{\sqrt K}\times\frac{n+1}{n+2}\times\frac{1}{mz}\times\left(1-\frac{2m^2z^2}{n}\right)^{\frac n2+1}
+\frac{\sqrt2}{\sqrt K}\times\frac{n}{n+2}\times\frac{n+1}{n+4}\times\frac{1}{2m^3z^3}\times\left(1-\frac{2m^2z^2}{n}\right)^{\frac n2+2},$$

where $m^2$, K, b and H stand for the quantities already explained."""
    s = sub_exact(
        s,
        r"# R U L E 3\.\n\nIf nothing is known of an event but that it has happened p times.*?and H stand for the quantities already explained\.",
        rule3,
    )
    s = replace_exact(
        s,
        "From substituting these values of E at $b$ and $mz$",
        "From substituting these values of $Ea^p b^q$ and $mz$",
    )
    s = replace_exact(s, "\\frac{m^2z^3}{3}", "\\frac{m^3z^3}{3}")

    # Printed p.414 note belongs after the completed paragraph on p.414, not
    # before the continuation of the next paragraph on p.415.
    note414 = "* See Mr. De Moivre's Doctrine of Chances, pag. 250."
    s = replace_exact(s, "\n\n" + note414 + " that the proportion", " that the proportion")
    end_note414 = "what this chance would be in some higher cases."
    s = replace_exact(s, end_note414, end_note414 + "\n\n" + note414)
    s = replace_exact(s, "a direction a direction to our judgment", "a direction to our judgment")

    # Printed p.418, Price's added improvement: the last divisor term is /n.
    s = replace_exact(
        s,
        "$\\frac{2 \\Sigma}{1 + 2 E a^p b^q + 2 E a^p b^q}$",
        "$\\frac{2\\Sigma}{1+2Ea^p b^q+\\frac{2Ea^p b^q}{n}}$",
    )
    for old, new, count in [
        ("For if not; ist let", "For if not; 1st let", 1),
        ("brought forth into this, world", "brought forth into this world", 1),
        ("&cc.", "&c.", 2),
        ("notice of mathematicians. 462", "notice of mathematicians.", 1),
    ]:
        s = replace_exact(s, old, new, count)

    answer415 = r"""The answer, according to the second rule, is that this chance is greater than $\frac{2\Sigma}{1-2Ea^p b^q + \frac{2Ea^p b^q}{n}}$ and less than $\frac{2\Sigma}{1-2Ea^p b^q - \frac{2Ea^p b^q}{n}}$, $E$ being

$$\frac{n+1}{n}\times\frac{\sqrt{2pq}}{\sqrt n}\times Ea^p b^q\times\left(mz-\frac{m^3z^3}{3}+\frac{n-2}{2n}\times\frac{m^5z^5}{5}+\&c.\right).$$

By making here $1000=p$, $100=q$, $1100=n$,

$$\frac{1}{110}=z,\qquad m=\frac{\sqrt{n^3}}{\sqrt{pq}}=1.048808,\qquad Ea^p b^q=\frac{b}{2}\times\frac{\sqrt n}{\sqrt{Kpq}},$$

$b$ being the ratio whose hyperbolic logarithm is"""
    s = sub_exact(
        s,
        r"The answer, according to the second rule, is that this chance is greater than.*?being the ratio whose hyperbolic logarithm is",
        answer415,
    )

    # Reader structure and explicit attribution. Price's letter and appendix
    # are integral to article LII, per the resolved text-specific decision.
    opening = "LII. An Essay towards solving a Problem in the Doctrine of Chances. By the late Rev. Mr. Bayes, F. R. S. communicated by Mr. Price, in a Letter to John Canton, A. M. F. R. S."
    s = replace_exact(
        s, opening,
        "# AN ESSAY TOWARDS SOLVING A PROBLEM IN THE DOCTRINE OF CHANCES\n\n"
        "## RICHARD PRICE — COVERING LETTER\n\n" + opening,
    )
    s = replace_exact(s, "# P R O B L E M.", "## THOMAS BAYES — ESSAY\n\n### PROBLEM")
    s = replace_exact(s, "# An APPENDIX.\n\n# CONTAINING\n\nAn Application of the foregoing Rules to some particular Cases.",
        "## RICHARD PRICE — APPENDIX\n\n### AN APPLICATION OF THE FOREGOING RULES TO SOME PARTICULAR CASES")
    s = re.sub(r"^#\s+(?:P R O P\.|PROP\.)\s*(\d+)\.$", r"#### PROPOSITION \1", s, flags=re.M)
    s = replace_exact(s, "# S E C T I O N I.", "### SECTION I")
    s = replace_exact(s, "# SECTION II.", "### SECTION II")
    s = replace_exact(s, "# D E M O N S T R A T I O N.", "#### DEMONSTRATION")
    s = replace_exact(s, "# SCHOLIUM.", "#### SCHOLIUM")
    s = re.sub(r"^#{1,3}\s+R U L E\s+(\d+)\.$", r"#### RULE \1", s, flags=re.M)

    # Mistral often used display delimiters for formulas printed inline in
    # prose. Collapse every same-line pair only when non-math prose remains on
    # that line; true standalone displays are untouched.
    inline_display = re.compile(r"\$\$([^$\n]+?)\$\$")
    collapsed = 0
    fixed_lines = []
    for line in s.splitlines():
        spans = list(inline_display.finditer(line))
        outside = inline_display.sub("", line).strip()
        if spans and outside:
            line, n = inline_display.subn(lambda m: "$" + m.group(1) + "$", line)
            collapsed += n
        fixed_lines.append(line)
    assert collapsed == 56, f"expected 56 inline display collapses, found {collapsed}"
    s = "\n".join(fixed_lines)

    # Outside math this is an ampersand abbreviation, not a LaTeX command.
    s = replace_exact(s, " .9405 \\&c.", " .9405 &c.")

    OUT.write_text(s.rstrip() + "\n", encoding="utf-8")
    print(f"built {OUT}: {len(s):,} chars from 49 OCR pages")


if __name__ == "__main__":
    main()
