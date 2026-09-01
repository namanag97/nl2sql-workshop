# App setup & IA guide — hosting, running, harvesting

Everything about `app/index.html`: two rooms in one file.

## Two rooms

| | Executive / CXO | Operator / analyst |
|---|---|---|
| Length | 90 minutes | 150 minutes |
| Job | Refuse to sign an unformulated number | Catch the wrong query, then fix it |
| Hands | Votes, ticks, 90-day owners | Paste cards into Codex |
| Clock | `AGENDA_EXEC` | `AGENDA_LAB` |
| Projector | `?stage=1` | same, different beats |

Pick the role on the register screen. Switch later from Today. Frame to the room as **risk reduction, not training** (Think Insights 2026): protect Thursday's board, do not "learn SQL."

## What research is baked in

- Silent pulse **before** discussion (Workshop Weaver; Mentimeter teach → vote → discuss the split).
- Decision record with a single owner and a 90-day move (strategy-meeting literature).
- "AI drafts, human certifies" anything that hits a board deck (Basedash / Databox 2026).
- Vendor filter: live data vs estimates, semantic layer vs guess, ask vs guess, refuse vs bluff.
- Formulation first; **no unidentified causes** (P6 concentration is a hypothesis; P7 before/after is not a policy effect).

## Participant path

```
INVITE         table QR → …/index.html#join=MARS
                 │
01 REGISTER    role (CXO / operator) + email + name. No password.
                 │
02 HOME        clock-driven "do this now" + 3 setup ticks
                 │
   EXEC:  Teach (big number + pulse) → Documents → Decide → Monday
   LAB:   Teach → Exercises → Cards → Score → Wall → Decide
                 │
STAGE          projector: ?stage=1  (talking points, no rail)
FACILITATOR    ?f=1  (clock, say-this, roster, merge, parking lot)
```

## Facilitator setup (D-2 → D-0)

1. Edit `EVENT` (team codes, capacity). Duration follows the role, not that constant, for the exec clock (90).
2. Host the single file (Netlify Drop / GitHub Pages).
3. Print table QR cards: `…/index.html#join=MARS`.
4. Projector tab: `…/index.html?stage=1#stage`. Operator laptop: `…/index.html?f=1`.
5. Rehearse: `node scripts/app_runtime_test.js`.
6. **Do not start the clock until S1.**

## Running — executive 90

| Min | You | They |
|---|---|---|
| 0 | Start clock. Say the contract: risk, not training. | Welcome |
| 8 | Show 86.3M on stage. "Do not discuss. Vote." | Pulse on Teach |
| 18 | Read the split. Then: 86 vs 23 is mostly **scope**. Sensitivity table is on Score. | Documents: CFO vs wiki |
| 38 | 62.5 → 27.5. Conservation, not a join gotcha. | Pulse: ship the dashboard? |
| 55 | Break five minutes. | |
| 62 | Three ticks. Anyone who disputes the number disputes a tick. | Decide |
| 72 | Refuse pulse. Vendor questions on Monday. | |
| 82 | Metric owner, 90-day move, **what we will not claim**. | Download one-pager |
| 90 | Stop. | |

## Running — operator 150

Same as before: C0 smoke → C1 mismatch → C2–C5 → ticks + C6 → wall → P8-lite. Teach page follows the lab beats so you can put talking points on the projector without a slide deck.

## Harvest

Wall JSONL → `eval/`. Hand-off codes → board. Decision one-pagers stay with each table (they download `meridian-decision.txt`).

## Known constraints

Static hosting still has no shared live poll. Pulses lock on each phone; you read the room (hands or shouted counts) and type the split on `?f=1`. That is intentional: the split is a facilitation move, not a dashboard.
