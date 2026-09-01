# Workshop run-of-show — 150 minutes, step by step

Assumptions: 20–30 attendees in pairs, 3 facilitators (1 lead + 2 roamers),
1 visible timer, 1 scoreboard wall, printed card decks on every table.
Attendees are assumed to have **never used Codex or Databricks before**.

## The mechanics that make limited proficiency safe

**Card system (printed, one action per card):**

| Card | Meaning |
|---|---|
| `C0`–`C8` | Codex prompt cards: verbatim text to paste + "you should see" |
| `D1`–`D3` | Decision menus: tick-a-box choices that define a metric |
| Red / Green | Table status flags: red = stuck, green = done (no hand-raising ambiguity) |

**Roles inside each pair:** **Pilot** (reads the card aloud, makes the
decisions) and **Copilot** (drives the keyboard, pastes). Swap every question.
Nobody is a spectator.

**The PIRA micro-loop — the one skill we teach:**
1. **Prompt** — paste the card text.
2. **Inspect** — read what came back. Does it match "you should see"?
3. **React** — if wrong, say *what* is wrong to the agent (card back lists the hint).
4. **Announce** — write the number on the scoresheet.

**Facilitator rule:** never touch a pair's keyboard. Diagnose by asking the
Pilot to read the card and the screen aloud.

---

## Segment 0 — Before doors (T-60 to T-5)

| # | Step | Owner | Pass condition |
|---|---|---|---|
| F1 | Run pre-flight checklist (`environment-runbook.md` §Pre-flight): warehouse awake, catalog loaded, row counts match | Lead | checklist all green |
| F2 | Verify Codex↔Databricks on 2 "clean" laptops via `C0` smoke card | Roamer | result < 60s |
| F3 | Project scoreboard + timer; lay out card decks, scoresheets, glossaries | Roamer | every table has a deck |
| F4 | Decide fallback trigger: if ≥2 tables red after smoke test, switch room to offline DuckDB kit | Lead | decision made by T-5 |
| F5 | Envelopes with answer keys sealed and pinned to scoreboard (opened at reveals) | Lead | 7 envelopes (Q1–Q5, P6, P7) |

## Segment 1 — Welcome & contract (0:00–0:10)

| # | Time | Step | Detail |
|---|---|---|---|
| S1 | 0:00 | The promise | "In 2.5 hours you will: catch an AI confidently lying, fix it without writing SQL, and leave with a checklist you can use at work tomorrow." |
| S2 | 0:03 | Skill poll (hands up) | "Who can read SQL? Who has used Databricks? Who has used an AI coder?" Facilitators note counts → pair assignment. |
| S3 | 0:05 | Pair up | Each pair = one strong-ish + one new. **Pairing needs per-person data, not the aggregate poll:** each attendee gets badge dots at the door (blue = reads SQL, red = used Databricks, green = used an AI agent). Pair blue-with-plain, etc. Introduce Pilot/Copilot roles. |
| S4 | 0:08 | The dataset story | 2 min on the fictional company (Meridian Trading Co., order-to-cash, 16 tables). Hand out glossary + counts handout. Attendees never need domain knowledge beyond it. |

## Segment 2 — Smoke test (0:10–0:20)

| # | Time | Step | Pass condition |
|---|---|---|---|
| S5 | 0:10 | Open Codex (already authed; icon on desktop) | app opens |
| S6 | 0:12 | Paste card `C0` (smoke: "list tables in schema o2c and their row counts") | table list appears |
| S7 | 0:15 | Compare to "you should see" on card | 16 table names, exact counts |
| S8 | 0:16 | Red-card protocol: raise red if mismatch; roamers converge; **green tables start C0.5 (5 cancelled orders) so nobody watches us debug** | all reds resolved |
| S9 | 0:18 | **Gate:** all tables green. If ≥2 reds at 0:20 → fallback kit. **The switch is FINAL here** — after Arc 1 starts, a mid-session fallback means re-auth per laptop; if Databricks degrades later, finish Arc 1 and switch during the break. | green wall |

## Segment 3 — Arc 1: measure your own cliff (0:20–0:45)

Worked example first (Q1, fully guided), then Q2–Q5 self-serve on cards.
Every question is answerable by a single query, and every one has a planted
quirk (`data/README.md` quirk register). Raw score expected: 1–2 / 5.

| # | Time | Step | Detail |
|---|---|---|---|
| S10 | 0:20 | The story | Lead: "Three teams, three different revenue numbers, one warehouse. Your job: find out why." |
| S11 | 0:23 | Q1 worked together, on the big screen | Lead drives `C1` aloud; pairs mirror. PIRA on display. Subgoals printed on `C1`: (1) find revenue column, (2) run, (3) compare to envelope. |
| S12 | 0:30 | Reveal Q1 | Open envelope 1. Almost nobody matches. Ask Pilot of one pair: "what did the agent include that finance wouldn't?" (cancelled orders — quirk `QK-01`). |
| S13 | 0:32 | Q2–Q5 self-serve | Pairs run `C2`–`C5` at their pace. **Stagger the start by table groups (30 s apart)** — 15 pairs pasting simultaneously can trip agent rate limits. Roamers enforce PIRA (Inspect step, not just paste). Swaps at each question. Q5 is the cut-first question if the clock slips. |
| S14 | 0:43 | Score wall | Pairs post their 5 numbers vs keys on scoresheet → scoreboard. |
| S15 | 0:44 | Transition line | "Average room score so far: ~1.5/5. GPT-5 scores 94% on math olympiads. Same model. Remember that." |

## Segment 4 — Concept beat (0:45–0:55)

| # | Time | Step | Detail |
|---|---|---|---|
| S16 | 0:45 | The cliff slide | Spider 2.0: 86–91% academic → 10–21% enterprise. DABstep: 16% multi-step. Databricks' own guidance: constraints + metric views + example SQL beat prose. |
| S17 | 0:50 | Name what happened | "You didn't fail at SQL. The model didn't fail at SQL. The *schema* failed to carry the business rules." |
| S18 | 0:53 | The fix preview | "For the next 40 minutes we make the schema carry the rules — then re-run the same 5 questions." |

## Segment 5 — Arc 2: govern the estate (0:55–1:35)

The heart. Attendees make **declarations**, Codex writes the DDL.
Scaffolds fade: no subgoals on these cards, only the checklist.

| # | Time | Step | Detail |
|---|---|---|---|
| S19 | 0:55 | Decision menus `D1`–`D3` | Pairs tick: returns in revenue? cancelled orders? order-date vs invoice-date? This is the declared-decision moment — the first lesson made physical. |
| S20 | 1:00 | Card `C6`: Codex builds the metric view | Prompt includes the pair's D1–D3 choices. Codex writes + runs the `CREATE VIEW`. "You should see: view created." |
| S21 | 1:05 | Card `C7`: constraints + trusted examples | Codex declares PK/FKs and 3 example SQLs. **Teaching beat:** Databricks constraints are *informational* — they show the agent where joins belong but enforce nothing; "the view is the enforcement." Production upgrade path (30-second mention): Databricks metric views (YAML-defined, UC-registered, what Genie consumes) — same idea, platform-native. |
| S22 | 1:10 | Re-run against the governed view | `FROM o2c_team<N>.V_REVENUE_GOVERNED`. **Only Q1/Q2/Q5 change** — the view governs revenue; C3 (time) and C4 (identity) re-run unchanged and often stay wrong, which is the S24 segue. |
| S23 | 1:25 | The reveal | Open envelopes. Typical delta: 1.5 → 4/5. Celebrate the room's measured cliff. |
| S24 | 1:33 | Name the residuals | Q3/Q4 (time + identity) often still wrong → segue: "semantic layer isn't everything — that's what the extended problems cover." |

## Segment 6 — Break + wall of pain (1:35–1:50)

| # | Time | Step | Detail |
|---|---|---|---|
| S25 | 1:35 | Break (5 min) | Coffee. |
| S26 | 1:40 | Wall of pain | Each pair writes 2–3 questions designed to **break** the governed setup (tricky phrasing, cross-source, tiny segments, PII-adjacent). Pin to wall. Facilitators transcribe during Arc 3 — this becomes the eval set. |

## Segment 7 — Arc 3: adversarial (1:50–2:15)

| # | Time | Step | Detail |
|---|---|---|---|
| S27 | 1:50 | Trade traps | Swap wall cards with the neighbor team. Run their traps via PIRA. Record: refused / answered-with-assumptions / confidently wrong. |
| S28 | 2:00 | The monster (optional, card `C8`) | DABstep-style multi-step: "Which region's margin dropped most QoQ after the returns policy change, and by how much?" Nobody one-shots this; the lesson is composition, not cleverness. |
| S29 | 2:10 | Evidence harvest | Teams star the best trap per pair on the wall. Facilitators photograph + transcribe. |

## Segment 8 — Synthesis (2:15–2:30)

| # | Time | Step | Detail |
|---|---|---|---|
| S30 | 2:15 | Three lessons | (1) The question is ambiguous; resolve it into declared decisions. (2) Business context — constraints, metric views, examples — closes the gap, not model choice. (3) Verify like an auditor; a refusal with reasons is a correct answer. |
| S31 | 2:22 | Take-homes | Trap checklist handout + "steal this at work" recipe (the rerun-at-home kit). Company contact for the eval-set follow-up. |
| S32 | 2:28 | Close | One-word round: "name the thing that surprised you." Out at 2:30 sharp. |

---

## Contingencies

| Failure | Trigger | Response |
|---|---|---|
| Setup hell | ≥2 reds at S9 | Switch to offline DuckDB kit (`environment-runbook.md` §Fallback); arc structure unchanged |
| Model/agent outage | Codex errors room-wide | Hand out printed "intern answers" (pre-generated SQL outputs, some wrong) — the judging exercise survives intact |
| Running late | Arc 2 not done by 1:40 | Cut Q5 and `C8`; never cut the reveal or Segment 8 |
| Room too fast | Arc 2 done by 1:15 | Unleash ceiling prompts (`problem-catalog.md` per-problem ceiling); start wall of pain early |
| Energy slump | Arc 2 midpoint | Pull the reveal forward; competition beats slide |

## 180-minute extension variant

Insert as Segment 7.5: one extended problem pack — **P5 (who may see what)**
for governance-minded rooms, **P3 (as-of March)** for finance-heavy rooms.
Each is self-contained in `problem-catalog.md` with its own key envelope.
