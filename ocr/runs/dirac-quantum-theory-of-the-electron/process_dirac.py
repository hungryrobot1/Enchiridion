#!/usr/bin/env python3
"""Derive the reader-ready Dirac text from the untouched Mistral extraction.

Every transformation has an asserted count. Stage-3 transformations here are
structural only: heading hierarchy, page-turn joins/rules, and visible unlinked
footnote markers. Stage-4 readings, when added, live in PAGE_REPAIRS and cite
the printed journal page that was inspected.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

RAW = Path("source/raw.md")
OUT = Path("dirac-quantum-theory-of-the-electron.md")
RAW_SHA256 = "fd732946bed3f189d60b7960adaa0cfacb8d47d54a0af04bccaccfe15e0df859"


def replace_exact(text: str, before: str, after: str, expected: int, label: str) -> str:
    found = text.count(before)
    assert found == expected, f"{label}: expected {expected}, found {found}"
    return text.replace(before, after)


def main() -> None:
    raw = RAW.read_text(encoding="utf-8")
    digest = hashlib.sha256(raw.encode()).hexdigest()
    assert digest == RAW_SHA256, f"raw extraction changed: {digest}"
    text = raw

    # At 36 KB the work stays under one title h1; numbered structure nests at h2.
    for number, title, old_prefix in (
        (1, "Previous Relativity Treatments.", "#"),
        (2, "The Hamiltonian for No Field.", "#"),
        (3, "Proof of Invariance under a Lorentz Transformation.", "###"),
        (4, "The Hamiltonian for an Arbitrary Field.", "#"),
        (5, "The Angular Momentum Integrals for Motion in a Central Field.", ""),
        (6, "The Energy Levels for Motion in a Central Field.", "#"),
    ):
        old = f"{old_prefix + ' ' if old_prefix else ''}§ {number}. {title}"
        new = f"## § {number}. {title}"
        text = replace_exact(text, old, new, 1, f"section {number} heading")

    # Leaf 4 ends mid-sentence; the other rules are extraction page boundaries,
    # not authorial divisions.
    text = replace_exact(
        text,
        "The wave function $\\psi$ must\n\n---\n\nnow be a function",
        "The wave function $\\psi$ must now be a function",
        1,
        "printed pp. 613-614 paragraph join",
    )
    text = replace_exact(text, "\n\n---\n\n", "\n\n", 13, "remaining page rules")

    # The source uses symbol footnotes. Keep both call and note visible, but do
    # not create in-page links (the Enchiridion router cannot support them).
    for before, after, expected in (
        ("Pauli,*", "Pauli,<sup>*</sup>", 1),
        ("Darwin,†", "Darwin,<sup>†</sup>", 1),
        ("Gordon*", "Gordon<sup>*</sup>", 1),
        ("Klein,†", "Klein,<sup>†</sup>", 1),
        ("developed‡", "developed<sup>‡</sup>", 1),
        ("introduced*", "introduced<sup>*</sup>", 1),
        ("anti-commutes*", "anti-commutes<sup>*</sup>", 1),
        ("h$.* Thus", "h$.<sup>*</sup> Thus", 1),
        ("\n* Pauli,", "\n<sup>*</sup> Pauli,", 2),
        ("\n* Gordon,", "\n<sup>*</sup> Gordon,", 1),
        ("\n* We say", "\n<sup>*</sup> We say", 1),
        ("\n* See", "\n<sup>*</sup> See", 1),
        ("\n† Darwin,", "\n<sup>†</sup> Darwin,", 1),
        ("\n† Klein,", "\n<sup>†</sup> Klein,", 1),
        ("\n‡ Jordan,", "\n<sup>‡</sup> Jordan,", 1),
    ):
        text = replace_exact(text, before, after, expected, f"footnote marker {before!r}")

    # Page-adjudicated readings are appended here; every entry must name the
    # printed page in its label and be recorded in NOTES.md.
    page_repairs: tuple[tuple[str, str, int, str], ...] = (
        (
            "i \\hbar \\frac{\\partial}{c} \\frac{\\partial}{\\partial t}",
            "\\frac{i \\hbar}{c} \\frac{\\partial}{\\partial t}",
            1,
            "printed p. 611, equation (1)",
        ),
        ("\\mathbf{A}_m \\psi_m", "\\mathbf{A} \\psi_m", 1, "printed p. 611, current I_mn"),
        ("transition m - n", "transition $m \\rightarrow n$", 1, "printed p. 611, transition arrow"),
        ("$\\rho_{\\infty}$", "$\\rho_{nn}$", 1, "printed p. 612, Gordon-Klein density"),
        ("$\\beta = \\alpha_3 mc$", "$\\beta = \\alpha_4 mc$", 1, "printed p. 613, definition before (6)"),
        (
            "\\alpha _ { \\mu } \\alpha _ { r } + \\alpha _ { r } \\alpha _ { \\mu }",
            "\\alpha _ { \\mu } \\alpha _ { \\nu } + \\alpha _ { \\nu } \\alpha _ { \\mu }",
            1,
            "printed p. 613, equation (6)",
        ),
        ("\\Sigma_\\zeta \\alpha_\\mu (\\zeta \\zeta')", "\\Sigma_{\\zeta'} \\alpha_\\mu (\\zeta \\zeta')", 1, "printed p. 614, matrix multiplication sum"),
        ("p_\\mu' = \\Sigma_\\mu a_{\\mu\\nu} p_{\\nu\\nu}", "p_\\mu' = \\Sigma_\\nu a_{\\mu\\nu} p_\\nu", 1, "printed p. 615, Lorentz transformation"),
        (
            "\\Sigma_\\mu a_{\\mu\\nu} a_{\\mu\\nu} = \\delta_{\\mu\\nu}, \\quad \\Sigma_\\nu a_{\\mu\\nu} a_{\\nu\\nu} = \\delta_{\\mu\\nu}",
            "\\Sigma_\\mu a_{\\mu\\nu} a_{\\mu\\rho} = \\delta_{\\nu\\rho}, \\quad \\Sigma_\\nu a_{\\mu\\nu} a_{\\rho\\nu} = \\delta_{\\mu\\rho}",
            1,
            "printed p. 615, orthogonality relations",
        ),
        ("\\gamma_\\mu' = \\Sigma_\\nu a_{\\mu\\nu} \\gamma_{\\nu\\nu}", "\\gamma_\\mu' = \\Sigma_\\nu a_{\\mu\\nu} \\gamma_\\nu", 1, "printed p. 615, transformed gamma"),
        (
            "\\gamma_\\nu \\gamma_\\nu + \\gamma_\\nu \\gamma_\\mu = 0",
            "\\gamma_\\mu \\gamma_\\nu + \\gamma_\\nu \\gamma_\\mu = 0",
            1,
            "printed p. 615, gamma anticommutation",
        ),
        (
            "\\Sigma_{\\nu\\lambda}a_{\\mu\\nu}a_{\\nu\\lambda}(\\gamma_{\\nu}\\gamma_{\\lambda} + \\gamma_{\\lambda}\\gamma_{\\nu}) \\\\ = 2\\Sigma_{\\nu\\lambda}a_{\\mu\\nu}a_{\\nu\\lambda}\\delta_{\\nu\\lambda} \\\\ = 2\\Sigma_{\\nu}a_{\\mu\\nu}a_{\\nu\\nu}",
            "\\Sigma_{\\kappa\\lambda}a_{\\mu\\kappa}a_{\\nu\\lambda}(\\gamma_{\\kappa}\\gamma_{\\lambda} + \\gamma_{\\lambda}\\gamma_{\\kappa}) \\\\ = 2\\Sigma_{\\kappa\\lambda}a_{\\mu\\kappa}a_{\\nu\\lambda}\\delta_{\\kappa\\lambda} \\\\ = 2\\Sigma_{\\kappa}a_{\\mu\\kappa}a_{\\nu\\kappa}",
            1,
            "printed p. 616, transformed gamma proof",
        ),
        ("\\gamma_{\\lambda}' = \\rho_{2}' \\quad \\quad \\quad \\gamma_{\\nu}' = \\rho_{2}'\\sigma_{\\nu}'", "\\gamma_{4}' = \\rho_{3}' \\quad \\quad \\quad \\gamma_{r}' = \\rho_{2}'\\sigma_{r}'", 1, "printed p. 616, primed analogue of (10)"),
        ("applies to $\\rho_{2}'$", "applies to $\\rho_{3}'$", 1, "printed p. 616, canonical transformation target"),
        ("\\rho_{1}'\\rho_{2}'(\\rho_{1}')^{-1} = -\\rho_{2}'\\rho_{1}'(\\rho_{1}')^{-1} = -\\rho_{2}'", "\\rho_{1}'\\rho_{3}'(\\rho_{1}')^{-1} = -\\rho_{3}'\\rho_{1}'(\\rho_{1}')^{-1} = -\\rho_{3}'", 1, "printed p. 616, canonical transformation"),
        ("\\Sigma_{r2}c_{r2}\\rho_{r}\\sigma_{r}", "\\Sigma_{rs}c_{rs}\\rho_{r}\\sigma_{s}", 1, "printed p. 616, equation (13)"),
        ("$c_{r2}$", "$c_{rs}$", 1, "printed p. 616, coefficients after (13)"),
        ("c_{21}\\rho_{3}\\sigma_{1}", "c_{31}\\rho_{3}\\sigma_{1}", 1, "printed p. 616, sigma-prime expansion"),
        ("a anticommutes with $\\delta$", "a anticommutes with b", 1, "printed p. 616, authorial footnote"),
        ("$(a_{21}/a_{12})^1$", "$(a_{21}/a_{12})^{1/2}$", 1, "printed p. 617, row multiplier"),
        ("$(a_{43}/a_{34})^1$", "$(a_{43}/a_{34})^{1/2}$", 1, "printed p. 617, row multiplier"),
        ("\\begin{cases}", "\\begin{Bmatrix}", 2, "printed p. 617, four-by-four brace matrices"),
        ("\\end{cases}", "\\end{Bmatrix}", 2, "printed p. 617, four-by-four brace matrices"),
        ("i\\sigma_2' = \\sigma_2'\\sigma_1'", "i\\sigma_2' = \\sigma_3'\\sigma_1'", 1, "printed p. 617, sigma relation"),
        ("\\sigma_{2}p_{2}-\\sigma_{3}p_{2}", "\\sigma_{2}p_{3}-\\sigma_{3}p_{2}", 1, "printed p. 620, m1 commutator"),
        ("\\sigma_{3}p_{2}-\\sigma_{2}p_{2}", "\\sigma_{3}p_{2}-\\sigma_{2}p_{3}", 1, "printed p. 620, sigma1 commutator"),
        ("m_3p_3 - m_3p_2 + p_2m_3 - p_3m_2", "m_2p_3 - m_3p_2 + p_2m_3 - p_3m_2", 1, "printed p. 621, anticommutator expansion"),
        (
            "Now a permissible definition of pᵣ is\n\nand from (21)\n\n$$(\\mathbf{x}, \\mathbf{p}) = rp_r + ih,$$",
            "Now a permissible definition of $p_r$ is\n\n$$(\\mathbf{x}, \\mathbf{p}) = rp_r + ih,$$\n\nand from (21)",
            1,
            "printed p. 621, equation order before (22)",
        ),
        ("rp_r + i\\rho_2 jh", "rp_r + i\\rho_3 jh", 1, "printed p. 622, equations (22)-(23) consequence"),
        ("i\\varepsilon p_2 jh/r", "i\\varepsilon\\rho_3 jh/r", 1, "printed p. 622, radial momentum identity"),
        ("i\\varepsilon\\rho_2 jh/r + \\rho_2 mc", "i\\varepsilon\\rho_3 jh/r + \\rho_3 mc", 1, "printed p. 622, equation (24)"),
        ("iερ₂ will now be of the form iρ₂ρ₂", "iερ₃ will now be of the form iρ₂ρ₃", 1, "printed p. 622, transformed matrices"),
        ("without changing ρ₂, and without changing any of the other variables", "without changing ρ₃, and without changing any of the other variables", 1, "printed p. 622, canonical transformation invariant"),
        ("- \\rho_1 jh/r + \\rho_2 mc", "- \\rho_1 jh/r + \\rho_3 mc", 1, "printed p. 622, transformed wave equation"),
        (
            "(F\\psi)_a \\equiv (p_0 + V)\\psi_a - h \\frac{\\partial}{\\partial r} \\psi_a - \\frac{jh}{r} \\psi_a + mc\\psi_a",
            "(F\\psi)_a \\equiv (p_0 + V)\\psi_a - h \\frac{\\partial}{\\partial r} \\psi_b - \\frac{jh}{r} \\psi_b + mc\\psi_a",
            1,
            "printed p. 622, first component equation",
        ),
        ("eliminate $\\psi_s$", "eliminate $\\psi_a$", 1, "printed p. 623, eliminated component"),
        ("\\psi_s", "\\psi_a", 5, "printed p. 623, component a in differentiated equations"),
        ("\\chi = B^{-1} \\chi_1", "\\chi = B^{-1/2} \\chi_1", 1, "printed p. 623, wave-function transformation"),
        ("$V = c^2/cr$", "$V = -e^2/cr$", 1, "printed p. 624, hydrogen potential"),
    )
    for before, after, expected, label in page_repairs:
        text = replace_exact(text, before, after, expected, label)

    assert text.count("\n# ") == 0, "unexpected secondary h1"
    assert text.count("\n## § ") == 6, "section sequence is incomplete"
    assert "\n\n---\n\n" not in text, "page rule survived"
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT}: {len(text)} chars, 6 sections, 0 page rules")


if __name__ == "__main__":
    main()
