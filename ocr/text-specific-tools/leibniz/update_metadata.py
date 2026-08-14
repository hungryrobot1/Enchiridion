#!/usr/bin/env python3
"""Make the catalog title match Latta's printed title page, with assertions."""

import json
from pathlib import Path

PATH = Path("source/metadata.json")
OLD = "The Monadology and Other Writings"
NEW = "The Monadology and Other Philosophical Writings"

data = json.loads(PATH.read_text())
assert data["author"] == "Gottfried Wilhelm Leibniz"
assert data["translator"] == "Robert Latta"
assert data["year_translated"] == 1898
assert data["title"] in (OLD, NEW), data["title"]
data["title"] = NEW
PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
print(f"metadata title: {NEW}")
