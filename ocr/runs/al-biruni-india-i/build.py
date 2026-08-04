#!/usr/bin/env python3
"""Rebuild the proposed Volume I Markdown from the frozen OCR output."""

from __future__ import annotations

import subprocess
import sys


STEPS = [
    ("initialize_text.py", "--apply"),
    ("remove_editorial_apparatus.py", "--apply"),
    ("remove_residual_synopses.py", "--apply"),
    ("strip_page_furniture.py", "--apply"),
    ("repair_page_boundaries.py", "--apply"),
    ("repair_wraps.py",),
    ("normalize_headings.py",),
    ("repair_math_variants.py",),
    ("remove_translator_footnote.py",),
]


for step in STEPS:
    subprocess.run([sys.executable, *step], check=True)
print("rebuilt source/al-biruni-india-i.md")
