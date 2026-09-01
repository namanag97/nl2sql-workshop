# Work packages — WP0–WP9

Each WP is sized for one agent session (≤ half-day of agent work) plus a
human verification pass. Build order follows dependencies. Every WP ends with
the **iteration protocol** from `AGENTS.md` (specify → build → verify against
acceptance criteria → dogfood as a naive user → tick the checklist).

## WP0 — Foundation ✅
Folder scaffold, README, AGENTS, this doc set. **Done in initial commit.**

## WP1 — Dataset + answer keys ✅
1. ✅ `data/ddl/o2c_ddl.sql` — 16 tables, Databricks dialect (loads in DuckDB).
2. ✅ `data/gen/generate.py` — seed 42, stdlib-only, plants QK-01..QK-18;
   **deterministic** (two fresh runs byte-identical), runs in < 1 s.
3. ✅ `data/keys/compute_keys.py` — SQLite-based independent recomputation;
   emits `keys.json` + 6 printable envelopes.
4. ✅ `data/keys/quirk_checks.sql` + `run_checks.py` — **18/18 proofs pass**.
- **Accept:** ✅ generator < 60s · ✅ keys derived from CSVs only · ✅ every
  quirk provable · teaching gaps verified (Q5 AOV delta ≈ $1,500; Q3
  236-now vs 198-at-close; fan-out 2.25×; Q4 Acme merge lands #1 with decoy
  at #2).
- Known follow-up: two-seat recompute of keys by a human (WP6 rehearsal).

## WP2 — Databricks environment (artifacts drafted; live acceptance pending)
1. ✅ `data/load/load_notebook.py` — COMMAND-cell notebook: widget-driven
   catalog/volume params, typed CSV→Delta loads, manifest drift assertion
   (fails loudly), facilitator baseline probe.
2. ✅ `data/load/reset.sql` — drops governed view + team scratch schemas +
   C7 constraints, verifies raw counts against manifest.
3. ⏳ Pre-flight executable checklist — needs a live workspace to bind.
- **Accept (pending live run):** cold-start to "C0 smoke card passes"
  < 15 min on a clean workspace, executed by a non-expert.

## WP3 — Codex wiring
1. MCP/`ucode` setup per runbook; pin the Databricks profile/host binding
   (known failure mode).
2. Smoke prompt set `C0`; pre-auth instructions for the loaner laptops.
- **Accept:** fresh laptop → first query result < 5 min, twice in a row.

## WP4 — Offline fallback kit ✅
1. ✅ `data/fallback/build_duckdb.py` — builds `meridian.duckdb` from the
   same CSVs + DDL; **parity proven: 5/5 key comparisons identical** to
   `keys.json` (16/16 tables + 6 team scratch schemas).
2. ✅ `data/fallback/verify_arcs.py` — **magic moment proven**: the C6 view
   built per the card's instructions reproduces the envelope on
   Q1'/Q2'/Q5' (3/3). Caught and fixed the Q5 tick-alignment bug en route.
3. ✅ `scripts/build_kit.py` — rerun-at-home kit assembled; acceptance run
   offline on a fresh connection (16 tables, orders 4,833, C1 86.3M).
- **Accept:** ✅ keys identical to WP1 · ✅ C0/C1 runnable offline ·
  ⏳ full Arc 1 + Arc 2 flow walked at the WP6 rehearsal (formality).

## WP5 — Problem packs (P1–P8 fully expanded) ✅
1. ✅ `docs/problem-packs.md` — all 8 packs: runs-on state, facilitator
   prep, tasks, verbatim floor prompts + React hints, ceiling, key +
   register pointer, trap note, debrief line, cold-run rule.
2. ✅ Coverage back-fill: quirk × pack matrix complete (P6 gained the
   delay-concentration analysis — QK-06 now has a P6 role too);
   `keys.P6` computed (buckets, late tail, validity ledger).
- **Accept:** ✅ each pack runnable cold from the doc + cards + envelope +
  keys.json · ✅ coverage matrix complete · ⏳ timing validated per pack at
  the WP6 rehearsal.

## WP6 — Facilitator pack + dry run
1. Expand `docs/facilitator-pack.md`: role scripts, reveal mechanics,
   failure-mode playbook, scoreboard template.
2. Add the **edge-experience playbook** lines from
   `docs/participant-experience.md` (M7 survived traps, M9 lucky pairs).
3. Produce the printed **"intern answers"** fallback deck (pre-generated
   outputs from the frozen dataset, some deliberately wrong) — WP8 key
   format, graded the same way.
4. Full dress rehearsal with 2 stand-ins playing naive attendees; rehearse
   C6/C7 against the live model ≥ 3 times (the magic moment).
- **Accept:** rehearsal fits 150 ± 10 min; every contingency in the
   run-of-show triggered at least once deliberately; C6 first-run success
   100% across rehearsal pairs.

## WP7 — Attendee pack (print assets)
1. Expand `docs/attendee-pack.md` → printable: cheat sheet (PIRA), glossary,
   trap checklist, cards `C0`–`C8` + `D1`–`D3`.
2. Print scoresheets from `assets/scoresheet.md` spec.
3. **Generate all printed counts from `data/out/manifest.json`** after the
   D-2 freeze (cards, C0 "you should see", handout) — never hand-typed;
   regenerate at scale 0.2 for rehearsals.
4. Slide skeleton (≤ 10 slides) from `assets/slides-outline.md`.
5. Build the **rerun-at-home kit**: DuckDB file + card PDFs + checklist +
   one-page recipe, downloadable via the follow-up email.
6. Registration blurb (`assets/registration-blurb.md`) to events/whatever
   page; follow-up email template (`assets/followup-email.md`) wired to
   WP9's room scores.
- **Accept:** a non-expert follows floor prompts unaided in dogfood mode;
   everything legible in black-and-white print; kit opens and runs C0/C1
   offline on a machine that never saw Databricks.

## WP8 — Eval capture (schema + seeds done; live capture at the workshop)
1. ✅ `eval/cases.schema.json` — grader tolerance field, refusal cases as
   first-class, wall-capture fields.
2. ✅ `eval/cases.seed.jsonl` — 20 schema-validated seed cases derived from
   the planted quirks (3 refusals; every axis A1–A10 covered). The ≥30
   acceptance needs only ~10 wall cases on the day.
3. ⏳ Post-workshop capture flow + triage — runs on the day (WP9).
- **Accept (partial):** ✅ export format live · ⏳ ≥30 deduped cases after
  the workshop.

## WP9 — Day-zero + post
1. Day-of checklist (who owns what, timeline T-60 → T+1 week).
2. Retro template; harvest eval cases; update THIS repo with actuals.

---

## Countdown plan (2 weeks out)

| When | Milestone |
|---|---|
| D-14 | WP1 dataset + keys frozen |
| D-10 | WP2 + WP3 verified on clean laptops |
| D-7 | WP5 packs + WP7 print files to review |
| D-5 | WP4 fallback tested; WP6 rehearsal |
| D-2 | Freeze; print everything; envelopes sealed |
| D-0 | Run |
| D+3 | WP9 eval harvest + retro |

## Decisions log

| Date | Decision | Rationale |
|---|---|---|
| 2026-08-29 | Standalone repo (not inside san/ or san-analytics) | Workshop is external-facing; san repos have strict boundary/allowlist hygiene |
| 2026-08-29 | O2C single-estate dataset, 5 spine questions | One story beats several; 5 fits 25-min arc |
| 2026-08-29 | Keys auto-graded, DABstep-style | Enables wall scoreboard + company eval export |
| 2026-08-29 | DuckDB offline fallback mandatory | Auth/MCP is the #1 venue-kill risk |
| 2026-08-29 | Backwards-experience audit folded in (`docs/participant-experience.md`) | C6 rewritten (attribution columns), Q2 keys aligned to default ticks, scoresheet spec added, rerun-kit + edge playbook assigned to WP6/WP7 |
| 2026-08-29 | Research pass 2: Databricks PK/FK constraints are **informational, not enforced** (RELY = optimizer permission only) | C7 card + S21 teaching beat now say "declaration ≠ enforcement; the view is the enforcement" |
| 2026-08-29 | Research pass 2: Codex wiring pinned to `ucode mcp add --agents codex` (needs `uv` + authed CLI); metric views are YAML-defined UC objects consumed by Genie | Runbook §B has exact commands; S21 mentions metric views as the production upgrade path; workshop stays on plain views for first-run reliability |
| 2026-08-29 | Wargame pass: 9 issues fixed (table counts 12→16, C1 basis pinned, C2 grand total, team-schema views, S22 scope, badge-dot pairing, fallback-finality, S13 stagger, envelope count); log in `docs/wargame-findings.md` | All attendee-facing cards now survive a naive-user simulation; 6 watch-items assigned to the live rehearsal |
| 2026-08-29 | Packs split into distributable handouts `packs/P1..P8.md` with facilitator-only cut lines | Participants get participant-facing pages; keys never leave the facilitator section |
