# Wargame findings — mock run of the full workshop (WP6 prep)

Method: stepped through the run-of-show minute by minute, playing three
personas — **Jordan** (analyst, never used Codex), **Priya** (BI dev, used
Genie, skeptical), and a **straggler** whose auth fails at 0:12 — plus the
facilitator and the environment. Every friction point was logged, then
either fixed in the repo (✅) or assigned a watch-item for the live
rehearsal (⏳).

## Issues found and fixed

| # | Where | What broke in the simulation | Fix |
|---|---|---|---|
| 1 | S7, C0, runbook, README, slides | "12 table names" — the estate has **16** tables. First smoke test would have failed its own "you should see" | All mentions corrected to 16; generated C0 card derives from manifest so it can't drift again |
| 2 | C1 card | Agent could sum `invoice_amount` instead of `line_amount` — a *plausible, different* answer (73.9M booked vs 86.3M naive) the envelope didn't cover | C1 pins the column; envelope Q1 now carries the booked number with a facilitator line: "also a decision, just a different one" |
| 3 | C2 card | The result is ~384 rows (6 months × 8 regions × 8 lines). Attendees cannot SUM that by hand; the scoresheet asked them to | C2 now requests the grand total as part of the card |
| 4 | C6/C7 cards + permissions | Attendees are read-only on `o2c` (by design) — but the cards said "create a view" there. And 12 teams creating the *same* view name with *different* ticks = silent collisions | Cards now create the view in the team scratch schema (`o2c_team<N>`), which runbook grants; re-run FROM paths updated |
| 5 | S22 wording | "Re-run C1–C5 against the governed view" is wrong for Q3/Q4 — the view governs revenue only | S22 now says only Q1/Q2/Q5 change; C3/C4 staying wrong IS the S24 segue |
| 6 | S3 pairing | The hands-up poll produces three aggregate numbers — you cannot pair individuals from aggregates | Badge-dot protocol: dot per person at the door (blue=SQL, red=Databricks, green=agent); pair across dots |
| 7 | S9 → fallback | Switching a mid-arc room to DuckDB means re-auth per laptop — 5+ min each | Fallback is FINAL at the S9 gate; later degradation = finish Arc 1, switch at the break |
| 8 | S13 | 15 pairs pasting simultaneously can trip Codex rate limits / seat caps | Staggered start by table group (30 s apart); ops check for seats added to runbook D-2 |
| 9 | F5 | "5 envelopes" — there are 7 (Q1–Q5, P6, P7) | Corrected |

## Watch-items for the live rehearsal (cannot be resolved on paper)

| # | Item | What would prove it |
|---|---|---|
| W1 | **C6 first-run success** — the magic moment dies if the view build errors | ≥3 rehearsal runs, 100% first-pass |
| W2 | Model over-governing on C1: if the agent excludes cancelled orders unprompted, the naive-vs-finance mismatch (the hook of Arc 1) never appears | F1.7 variance probe (3× C1/C2); if seen, C1 gains "do not exclude anything" |
| W3 | "Intern answers" outage deck doesn't exist yet | Print at WP6 from the frozen dataset; some outputs deliberately wrong |
| W4 | MCP handshake latency at 0:10 (first query can take 20–30 s) — a full room staring | C0.5 card absorbs it; verify it reads well |
| W5 | Rerun-at-home kit (promised in take-homes) | WP7 build; acceptance = runs offline on a machine that never saw Databricks |
| W6 | Q3 reveal: 236-now vs 236-as-of will look "broken" to sharp attendees | Pack P3 facilitator note covers it; rehearse the line |

## Wargame round 2 — executed proofs (no live model needed)

Instead of only stepping through prose, this round **built the things and
ran them**:

| Check | Result |
|---|---|
| **Magic moment, numerically**: built `V_REVENUE_GOVERNED` in a team schema exactly as card C6 instructs (default ticks, primary line/region columns), re-ran Q1'/Q2'/Q5' | ✅ `data/fallback/verify_arcs.py`: 3/3 — view output = envelope, all 8 regions match |
| **Q5 tick-alignment bug** (caught by the verifier above) | The envelope's governed AOV was gross of returns (16,321) while the default D2 tick nets them (16,173) — teams following their own ticks would have failed the reveal. Same bug class as round-1 issue 2, missed for Q5. Fixed in `compute_keys`, `build_duckdb` parity, and the envelope |
| **Intern-answers deck (W3)** built and generated from the live data: `scripts/gen_intern_answers.py` → `assets/print/intern-answers.md`; Table 1/2 & 5/6 get the naive variant, Table 3/4 the booked variant (73.9M) so reveals stay varied | ✅ closed |
| **Rerun-at-home kit (W5)** built: `scripts/build_kit.py` → `kit/` (duckdb + offline cards + checklist + recipe). Acceptance run on a fresh connection: 16 tables, orders 4,833, C1 revenue 86,296,983 | ✅ closed |
| **Team-scratch-schema parity offline**: `meridian.duckdb` now pre-creates `o2c_team1..6`; offline mode = one DB copy per table (duckdb has no grants — copy, don't share) | runbook §D updated |

Remaining watch-items are all genuinely live: W1 (model executes C6
correctly), W2 (over-governing on C1), W4 (MCP handshake), W6 (reveal
line). Everything checkable offline has been checked.

## Wargame round 3 — simulated agent + one-command freeze

| Check | Result |
|---|---|
| **Simulated agent pass** (`scripts/simulate_agent.py`): canonical SQL a competent agent would emit for every card C0–C8, run against the real DB | ✅ all cards answerable and envelope-covered (C0 counts, C1 pinned basis, C3 both definitions, C4 naive code, C5 naive, C6 view, C8 EAST) |
| **W7 (new watch-item)**: a *strong* agent may self-dedupe on C2/C5 — the Arc-1 cliff may be smaller for teams whose agent is well-trained | Envelope covers both outcomes (62.5M fan-out / 27.5M governed); reveal line: "your agent was lucky or good — which rule made it right?" |
| **One-command freeze** (`scripts/rebuild_all.sh`): generate → keys → 18/18 checks → duckdb+parity → magic moment → agent sim → intern deck → print assets → kit | ✅ ALL GATES GREEN, exit 0 — the D-2 procedure is now one command |
| **WP8 head start**: `eval/cases.schema.json` + 20 seeded cases (`eval/cases.seed.jsonl`, schema-validated) — 3 refusal cases, numeric tolerances, all 10 axes covered | The ≥30 acceptance needs only ~10 wall cases on the day |

## Wargame round 4 — IA walk + auto-assignment

**Fixed from the user's own report:** the redesigned app shipped without its
initial `render()` call — a blank page behind a passing syntax check. Root
cause: syntax-only verification. Fix + permanent runtime harness
(`scripts/app_runtime_test.js`) that renders every route with a stub DOM.
Second catch from the harness: `pack-*` routes were never wired into the
router (pack pages silently fell back to home).

**Auto team assignment:** static hosting cannot count registrations across
devices, so assignment is by **deep link**: each table card carries
`…/index.html#join=MARS` (QR + code). Opening it reserves the seat
("Seat reserved — Team Mars"); the participant types only email + name.
Bad codes show the valid list instead of dying silently.

**New in the app, all harness-tested:**
- deep-link seat reservation + invalid-code banner
- participant setup checklist on home (open Codex → paste C0 → check counts)
- presence check-in codes → facilitator roster (name × team)
- capacity display (EVENT.capacity) at registration

**IA dead-ends checked and cleared:** clock-not-started (explicit banner),
unregistered visitor on every route (register prompt), wall with zero traps
(empty state), facilitator route hidden without `?f=1`, re-render after
every state change.

## Persona verdicts (post-fix walk)

- **Jordan:** smoke → C1 → reveal works with zero typing beyond paste; the
  384-row moment (issue 3) was the one that would have lost them.
- **Priya:** the S21 "declaration ≠ enforcement" beat and the C8
  decomposition are what keep her from checking her phone; the wargame
  confirmed C8 must stay optional-pacing, not mandatory.
- **Straggler:** red card at 0:12 → loaner swap in ~3 min; C0.5 keeps their
  partner productive; if the straggler rate exceeds the loaner count, merge
  pairs (facilitator playbook covers it).
