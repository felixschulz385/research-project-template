#!/usr/bin/env python3
"""Pre-commit check: block Stata licence details in staged notebook outputs.

Inspects only staged content (``git show :<path>``) of staged ``.ipynb`` files and blocks the
commit if any cell output text contains ``Serial number:`` or ``Licensed to:`` (case-insensitive).
Stdlib only.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections.abc import Iterator

LICENSE_RE = re.compile(r"(?:Serial number:|Licensed to:)", re.IGNORECASE)


def _git(*args: str) -> bytes:
    return subprocess.run(["git", *args], capture_output=True, check=True).stdout


def staged_notebooks() -> list[str]:
    out = _git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").decode()
    return [p for p in out.split("\0") if p.endswith(".ipynb")]


def _iter_strings(value: object) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                yield item


def iter_output_text(nb: dict) -> Iterator[str]:
    """Yield every text chunk from cell outputs in a parsed notebook."""
    for cell in nb.get("cells", []):
        for out in cell.get("outputs", []):
            if not isinstance(out, dict):
                continue
            yield from _iter_strings(out.get("text"))
            data = out.get("data")
            if isinstance(data, dict):
                for val in data.values():
                    yield from _iter_strings(val)
            yield from _iter_strings(out.get("evalue"))
            yield from _iter_strings(out.get("traceback"))


def has_stata_license(nb: dict) -> bool:
    """Return True if any cell output text matches Stata's licence banner lines."""
    return any(LICENSE_RE.search(chunk) for chunk in iter_output_text(nb))


def main() -> int:
    bad: list[str] = []
    for path in staged_notebooks():
        try:
            nb = json.loads(_git("show", f":{path}"))
        except json.JSONDecodeError:
            continue
        if has_stata_license(nb):
            bad.append(path)
    if not bad:
        return 0
    print("\nCommit blocked: staged notebook(s) contain Stata licence details in cell outputs.\n", file=sys.stderr)
    for path in sorted(bad):
        print(f"  {path}", file=sys.stderr)
        print(f"  Fix: python .githooks/scrub-stata-license.py {path}", file=sys.stderr)
    print("\nThen git add the scrubbed notebook(s) and commit again. Bypass once: git commit --no-verify\n",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
