---
type: rule
state: current
updated: 2026-11-23
area: workflow
applies: always
summary: "Recurring task procedures live as Agent Skills in .agents/skills/, symlinked from .claude/skills, in short tool-neutral prose"
---

# Agent skills

## Decision

Step-by-step procedures for recurring repository tasks live as **Agent Skills** (the open
`SKILL.md` format):

- **Rules vs procedures.** Hard rules (pre-specification, restricted data, commit policy) and
  standing pointers stay in `AGENTS.md` ([`agent-instructions.md`](agent-instructions.md)), which
  every agent loads into every session. Skills hold step-by-step procedures only and point to the
  project's own docs (`AGENTS.md`, `docs/conventions.md`, `docs/templates/`) rather than repeating
  them.
- **Canonical location:** `.agents/skills/<name>/SKILL.md`, one flat level (no nested groups).
- **Claude Code compatibility:** `.claude/skills` is a relative symlink to `../.agents/skills`,
  checked into git (carved back into `.gitignore` with `!.claude/skills`).
- **Front matter:** only `name` (lowercase, hyphenated, matching the folder name) and `description`
  (what the skill does and when to use it, under 1024 characters).
- **Tool-neutral, short prose:** aim for under ~80 lines per `SKILL.md` and avoid agent-specific
  tool names; write plain actions ("ask the user", "run", "search").

The template ships skills matched to the project's options:

| Skill | Covers | Included when |
|---|---|---|
| `start-line` | New line charter, branch, indexes, initial planning doc | always |
| `write-prespec` | Drafting and confirming a step's pre-spec | research profile |
| `add-source` | Data source module, registry, config, doc page, verification | pipeline projects |
| `end-line` | Finalizing record and charter, indexes, merge prep | always |
| `tidy-repo` | Archive tag, one-off scripts, macOS metadata, hygiene checks | always |

## Why

Putting multi-step checklists in `AGENTS.md` bloats every session's context with procedures only
needed occasionally; leaving them out means agents reconstruct the steps unevenly from memory.
One canonical folder under `.agents/skills/` with a relative symlink at `.claude/skills` serves
both Antigravity and Claude Code without duplicating files.

## How

The template ships `.agents/skills/` (with Jinja-conditional skill folders for `doc_profile` and
`pipeline`) and the `.claude/skills` symlink. `copier.yml` sets `_preserve_symlinks: true` so the
symlink is preserved on render, and `.gitignore` ignores `.claude/*` while keeping
`!.claude/skills` tracked.

## Per-project choices

- Additional project-specific skills under `.agents/skills/` (for example, domain-specific build
  or submission procedures).

## Checked by

Template CI renders both configurations (`research-pipeline-hpc` and `software-minimal`); review
checks skill scope and tool-neutral wording.
