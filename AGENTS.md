# AGENTS.md — for Codex / ZCode / Claude sessions working on prep

## Context

This repo preps a 2.5–3h NL2SQL workshop. Audience: mid-level industry folks
with **limited tech proficiency**. Tooling: **Codex (agent mode) connected to a
Databricks SQL warehouse** via MCP. Read `README.md` first, then
`docs/work-packages.md` for the current work package.

## Conventions

- **Problem IDs**: `P1`–`P8` (see `docs/problem-catalog.md`).
  **Questions**: `Q1`–`Q5` (the live spine). **Planted data quirks**: `QK-xx`
  (see `data/README.md`). **Prompt cards**: `C0`–`C8` (see
  `docs/attendee-pack.md`). Keep these identifiers stable across all docs —
  cross-references depend on them.
- **Answer keys are sacred**: every numeric key must be recomputable by an
  independent person from the dataset alone, and must ship with a *decision
  register* (the list of definitional choices that produce the number).
  A key without a register is invalid.
- **Limited-proficiency test**: any attendee-facing artifact (cards, cheat
  sheet) must be followable by a person who has never opened a notebook.
  One instruction per line; "what you should see" after every action.
- **Numbers are big and readable**: round to whole units; no floats with
  >2 decimals anywhere attendee-facing.
- **No filler**: docs state constraints and steps, not philosophy. If a
  sentence doesn't change what the reader does, delete it.

## Iteration protocol (per work package)

1. **Specify** — the WP's deliverables + acceptance criteria are already in
   `docs/work-packages.md`; do not invent scope.
2. **Build** — agent produces the artifact in the mapped path.
3. **Verify** — check each acceptance criterion explicitly; report pass/fail
   per criterion.
4. **Dogfood** — for attendee-facing artifacts, simulate a naive user (fresh
   context, only the artifact visible) and attempt the flow. Fix what the
   simulated novice trips on.
5. **Mark status** — update the WP checklist at the bottom of
   `docs/work-packages.md`.

## Hard rules

- Never edit generated answer-key numbers by hand to make a test pass —
  regenerate from the dataset and investigate the delta.
- Attendee-facing text assumes nothing about SQL, Databricks, or agents.
- The offline fallback (DuckDB mirror) must stay behaviorally identical to the
  Databricks path: same keys, same quirks.
- Everything attendee-facing must be printable in black and white.
