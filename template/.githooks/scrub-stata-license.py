#!/usr/bin/env python3
"""Scrub Stata licence lines from Jupyter notebook cell outputs in place.

Removes lines starting with ``Stata license:``, ``Serial number:``, ``Licensed to:`` and up to two
indented licensee continuation lines immediately following ``Licensed to:``. Leaves the rest of the
banner (logo, StataCorp address, notes) and all other cell content untouched, and writes back with
nbformat's JSON layout (``indent=1, ensure_ascii=False`` plus a trailing newline). Stdlib only.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

LICENSE_LINE_RE = re.compile(r"^\s*(?:Stata license:|Serial number:|Licensed to:)", re.IGNORECASE)
LICENSED_TO_RE = re.compile(r"^\s*Licensed to:", re.IGNORECASE)
INDENTED_CONT_RE = re.compile(r"^[ \t]+\S")
MAX_LICENSEE_CONT_LINES = 2


def scrub_lines(lines: list[str]) -> tuple[list[str], int]:
    """Remove Stata licence lines from a sequence of text lines; return (kept, removed_count)."""
    kept: list[str] = []
    removed = 0
    cont_remaining = 0
    for line in lines:
        if LICENSE_LINE_RE.match(line):
            removed += 1
            cont_remaining = MAX_LICENSEE_CONT_LINES if LICENSED_TO_RE.match(line) else 0
            continue
        if cont_remaining > 0 and INDENTED_CONT_RE.match(line):
            removed += 1
            cont_remaining -= 1
            continue
        cont_remaining = 0
        kept.append(line)
    return kept, removed


def _scrub_field(value: object) -> tuple[object, int]:
    if isinstance(value, str):
        lines = value.splitlines(keepends=True)
        kept, removed = scrub_lines(lines)
        return ("".join(kept) if removed else value), removed
    if isinstance(value, list) and all(isinstance(x, str) for x in value):
        lines = "".join(value).splitlines(keepends=True)
        kept, removed = scrub_lines(lines)
        return (kept if removed else value), removed
    return value, 0


def scrub_notebook(nb: dict) -> int:
    """Scrub Stata licence lines from cell outputs in ``nb`` in place; return lines removed."""
    total = 0
    for cell in nb.get("cells", []):
        for out in cell.get("outputs", []):
            if not isinstance(out, dict):
                continue
            if "text" in out:
                new_val, n = _scrub_field(out["text"])
                if n:
                    out["text"] = new_val
                    total += n
            data = out.get("data")
            if isinstance(data, dict):
                for mime, val in list(data.items()):
                    new_val, n = _scrub_field(val)
                    if n:
                        data[mime] = new_val
                        total += n
    return total


def scrub_file(path: Path) -> int:
    """Scrub a notebook file on disk if needed; return the number of lines removed."""
    nb = json.loads(path.read_text(encoding="utf-8"))
    removed = scrub_notebook(nb)
    if removed:
        with path.open("w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return removed


def main(argv: list[str]) -> int:
    if not argv:
        print("Usage: python .githooks/scrub-stata-license.py <notebook>...", file=sys.stderr)
        return 2
    for arg in argv:
        path = Path(arg)
        removed = scrub_file(path)
        print(f"{path}: removed {removed} line(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
