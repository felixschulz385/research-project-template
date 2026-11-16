---
type: rule
state: current
updated: 2026-11-16
area: workflow
applies: always
summary: "AGENTS.md holds rules and pointers for coding agents; its state table is generated; CLAUDE.md imports it"
---

# Agent instructions

## Decision

The instructions for coding agents live in **`AGENTS.md`**, read by several tools. **`CLAUDE.md`**
holds one line, `@AGENTS.md`, which Claude Code resolves as an import. The file is loaded into
every session, so it holds rules and pointers only:

| Section | Content |
|---|---|
| State | a **generated** table of the lines of work, and two or three standing pointers |
| Hard rules | restricted data, pre-specification, commit and branch policy |
| Environment | machines, network limits, the environment, the data root |
| Data pipeline | how a source is added, the CLI, cross-source rules |
| Analysis | the specification module, one module per line, notebooks |
| Docs conventions | a pointer to `docs/conventions.md` and the rules agents most often need |

What stays out: status and results (in charters and results pages), estimates, session history
(commit messages, dated notes), and anything a module docstring can say.

If the agent keeps its own memory outside the repository, it holds what the repository cannot:
the user's preferences and decisions about how to work, and pointers.

## Why

A hand-written status table in the instructions drifted within days in the source project, and
an instructions file tied to one tool's name does not serve the next tool.

## How

`AGENTS.md` and `CLAUDE.md` are in the template. `AGENTS.md` is listed under `extra` in
`docs/docs.toml`, so its links are checked and its State table regenerated.

## Per-project choices

- The hard rules that apply (restricted data, if any) and the environment notes.

## Checked by

`scripts/docs.py check` (links, the generated State table).
