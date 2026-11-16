---
type: rule
state: current
updated: 2026-11-16
area: repository
applies: always
summary: "What git tracks and what it doesn't, the data root, scratch, and how to clean up (archive tags, one-off scripts, macOS metadata)"
---

# Storage and hygiene

## Decision

| Path | Tracked? | Why |
|---|---|---|
| `notebooks/<slug>/` | Tracked, with outputs | Runs of record; notebooks that read restricted data are committed without outputs. |
| `output/figures/`, `tables/`, `documents/`, `presentations/` | Tracked | Citable deliverables. |
| any `restricted/` | Ignored | Figures and files that show restricted records. |
| `<data_root>/` (`data_nobackup/`) | Ignored | Raw and prepared data, derived caches, literature PDFs (`literature/<topic>/`). |
| `scratch_nobackup/` | Ignored | Disposable working files; location overridable by an environment variable, never `/tmp` on a shared cluster. |
| `*.local.yaml`, secrets | Ignored | Per-machine settings and credentials. |

The `.gitignore` baseline is in the template; carve exceptions back in with a commented `!`
line.

**Cleaning up:**

- **Tag before removing code** (`git tag -a archive/YYYY-MM-<what>`, pushed), and say in the
  commit which tag holds it.
- **Delete one-off scripts once they have run**; keep only tools that are run again, with tests.
- **Run `python scripts/docs.py check` after any cleanup that touches docs.**
- **macOS metadata:** copying a repository through a Mac network mount leaves `._*` files, also
  inside `.git/` (git reports them as garbage). They are 4 KB AppleDouble files (magic bytes
  `00 05 16 07`), safe to delete, and ignored by the baseline.

**License:** a `LICENSE` file chosen before the first commit with real content.

## Why

Bulk data never belongs in git. Without an archive tag, removed code is hard to find again;
without deleting one-off scripts, the next reader cannot tell which tools still matter.

## How

`.gitignore` and `LICENSE` come from the template.

## Per-project choices

- The license (copier asks: MIT, BSD-3-Clause, CC-BY-4.0 for written material, or none yet). If
  code and writing need different licenses, say so in the README.
- Whether a published output site exists (`output/webpage/` plus a publishing workflow).

## Checked by

`check-restricted.py` blocks data files and restricted paths at commit time.
