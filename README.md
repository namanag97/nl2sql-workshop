# NL2SQL Enterprise Workshop

Prep repository for a **2.5–3 hour hands-on workshop** where mid-level industry
folks (analysts, BI developers, data engineers, PMs — assumed **limited tech
proficiency**) drive **Codex against a Databricks lakehouse** and learn, by
measuring it themselves, why NL2SQL breaks in enterprises and what closes the
gap: **governed semantics, declared decisions, and auditor-grade verification.**

Thesis of the room: *the model writes the SQL; the human's job is to judge it.*
Frontier models score ~86–91% on academic text-to-SQL but 10–21% on
enterprise-scale problems (Spider 2.0), and ~16% on realistic multi-step data
analysis at launch (DABstep). Attendees reproduce that cliff on their own
laptop in 90 minutes, then close most of it with a governed metric view.

## Non-goals

- Not a prompt-engineering course.
- Not "build your own NL2SQL product."
- No live configuration in the room: everything is pre-authed, pre-loaded,
  printed on cards. Codex does the typing; attendees direct and judge.

## File map

| Path | What it is |
|---|---|
| `docs/participant-experience.md` | Backwards design from the participant's experience; the experience contract + audit |
| `docs/research-bibliography.md` | 35+ annotated sources mapped to packs: benchmarks, semantic-layer evidence, security, process mining, training design |
| `docs/wargame-findings.md` | Mock-run logs: 9+2 issues found and fixed, executed proofs, remaining live watch-items |
| `docs/workshop-run-of-show.md` | The centerpiece: minute-by-minute steps S1–S30, card system, contingencies |
| `app/index.html` | Hostable single-file app: **executive 90-min** and **operator 150-min** rooms, Teach/Stage talking points, pulses, packs, scores, 90-day decision record, facilitator dashboard (`?f=1`, `?stage=1`) |
| `docs/app-setup.md` | IA guide: participant screen-by-screen journey + facilitator setup/run/harvest manual |
| `docs/company-artifacts.md` | The realism layer: CFO email, stale wiki, Teams thread — documents that conflict with the data |
| `packs/` | Distributable per-problem handouts P1–P8 (participant section + facilitator cut) |
| `docs/problem-catalog.md` | 8 problems (P1–P8): story, planted quirks, tasks, floor/ceiling, keys |
| `docs/problem-packs.md` | Cold-run facilitator expansions of P1–P8 (verbatim prompts, hints, debriefs) |
| `docs/work-packages.md` | WP0–WP9 prep breakdown: steps, acceptance criteria, iteration protocol, countdown |
| `docs/environment-runbook.md` | Databricks + Codex/MCP setup, pre-flight checklist, offline fallback kit |
| `docs/attendee-pack.md` | Cheat sheet, glossary, trap checklist, printable prompt cards C0–C8 |
| `docs/facilitator-pack.md` | Roles, adjudication moves, failure-mode playbook, dry-run checklist |
| `data/README.md` | Dataset design: schema, sizes, planted-quirk register (quirk → axis → problem) |
| `eval/README.md` | Wall-of-pain capture + eval-case export format (the company's take-home) |
| `assets/` | Scoresheet spec, slide outline, registration blurb, follow-up email, printable card templates |

## Design principles

1. **15-minute rule** — setup must complete before the room arrives; nothing
   is configured live.
2. **Codex absorbs skill variance** — attendees never need to write SQL; every
   action is a numbered prompt card with "what you should see" printed on it.
3. **PIRA micro-loop** — Prompt → Inspect → React → Announce. The one skill we
   actually teach for driving agents.
4. **Evidence-anchored review** — a team's answer counts only against a
   precomputed numeric answer key + decision register, never "looks right."
5. **Scaffolds fade** — worked example → checklist only → open attack.
6. **≤20-minute production cadence** — no segment without a visible artifact.
7. **Everyone leaves with three things** — the trap checklist, a rerun-at-home
   recipe, and one story of catching the AI being confidently wrong.
8. **The workshop produces an eval set** — every trap question written in the
   room is exported as a test case for the company's product.

## Status

- [x] Coverage axes + meta-model agreed
- [x] Folder scaffolded, docs drafted
- [x] WP1 dataset + keys built; 18/18 quirk proofs; deterministic seed 42
- [x] WP4 DuckDB fallback built; key parity proven (5/5); **magic moment
      proven** (verify_arcs 3/3); rerun-at-home kit assembled + accepted
- [x] WP6 prep: intern-answers outage deck generated (W3 closed)
- [x] Simulated agent pass: all cards C0–C8 answerable + envelope-covered
- [x] One-command freeze pipeline (`scripts/rebuild_all.sh`, all gates green)
- [x] WP8 eval schema + 20 seeded cases
- [ ] WP2/WP3 live: Databricks workspace + Codex/ucode verified on a clean machine
- [x] WP7 print-asset generator (counts from manifest) + registration
      blurb, slides outline, follow-up email, scoresheet spec
- [x] WP2 load notebook + reset kit drafted
- [x] WP5 problem packs expanded (P1–P8 cold-runnable; P6 key computed
      with delay-concentration analysis: 74.3% of the late tail on
      dual-region reps carrying 43.3% of orders)
- [ ] WP2/WP3 live: Databricks workspace + Codex/ucode verified on a clean machine
- [ ] WP6 dry run within 150 ± 10 min (incl. C6 first-run success 100%)

Decisions and open questions are logged inline in `docs/work-packages.md`.

## Hosting the app

`app/index.html` is a single self-contained file — host on GitHub Pages,
Netlify (drag-and-drop), or any static server. No backend.

**Design:** enterprise-Swiss light — white ground, black ink, one red accent
(`#D8231F`), Helvetica-family type, hairline rules, numbered index rail,
tabular-numeral timer. Flat, no shadows; a print stylesheet turns any page
into a clean handout.

**Features:** email-only registration (localStorage session) · team join
codes (edit `EVENT.teams`) · live agenda clock with mm:ss countdown,
segment auto-detection and progress bar (started from the facilitator
dashboard) · Pilot/Copilot swap toggle · all 8 packs with tickable task
checklists and per-pack completion % · all 10 prompt cards with
copy-to-clipboard · company artifacts in-app · **auto-graded scoresheet**
(±0.5% against the envelopes, with per-match explanation text) · digital
wall of pain exporting schema-valid eval JSONL · facilitator dashboard
(`?f=1`): clock, team sync-code merge (scores + ticks + pack progress),
eval-set download.

**Honest limitation:** static hosting means no shared server state. Teams
hand the facilitator short sync codes; the physical scoreboard remains the
adjudicator of record. Keys are embedded for instant grading — fine for a
workshop; move grading server-side if prizes ever depend on it.
