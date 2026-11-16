# Agent instructions (CLAUDE.md)

Projects are worked on with coding agents. Their instructions file (`CLAUDE.md`, or
`AGENTS.md`) is loaded into every session, so it must be short, current and free of anything
that goes stale. Start from [`../scaffold/CLAUDE.md`](../scaffold/CLAUDE.md).

## What goes in

| Section | Content |
|---|---|
| State | a **generated** table of the lines of work (`<!-- docs:begin lines -->`), plus two or three standing pointers (how to start a session, how new work starts, archive tags) |
| Hard rules | restricted data, pre-specification discipline, commit and branch policy |
| Environment | cluster, network limits (where downloads run), Python environment, data root |
| Data pipeline | how a source is added, the CLI, cross-source rules |
| Analysis | the specification module, one module per line, where notebooks live |
| Docs conventions | a pointer to `docs/conventions.md` and the three rules agents most often need |

## What stays out

- **Status and results.** They live in the charters and results pages; the State table is
  generated from them. A hand-written status table in the instructions drifts within days.
- **Estimates.** Numbers belong in the results page.
- **History.** What happened in a session belongs in a commit message or a dated note.
- **Anything a module docstring can say.** File-local reasoning stays next to the code.

## Keeping it current

Update the instructions in the same commit as any change to the layout or the rules they state.
The docs checker regenerates the State table and checks the file's links (it is listed under
`extra` in `docs/docs.toml`).

## Agent memory

If the agent keeps its own memory outside the repository, it should hold what the repository
cannot: the user's preferences and decisions about how to work, and pointers. It should not
duplicate results or status, which the repository records.
