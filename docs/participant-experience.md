# Participant experience — the backwards design

Method: design and audit **from the last moment backwards**. Every moment
below states what the participant feels, what must exist for that moment to
happen, and how it breaks. Anything that no moment needs is cut; anything a
moment needs and we haven't built is a gap (see §Audit).

## The walk (T+1 week → 0:00)

### M10 — T+1 week, they retell it
**Feel:** "I watched an AI double-count revenue and caught it myself."
**Must exist:** the checklist in their bag (scoresheet back); a rerun-at-home
kit they can actually open (data + cards + recipe); a follow-up email.
**Breaks if:** the kit is a zip nobody can run, or the checklist never got
printed. → WP7 owns the kit; WP9 owns the email.

### M9 — 2:28, the one-word round
**Feel:** surprised, competent, out on time.
**Must exist:** every pair had ≥1 personal catch (their Arc-1 number vs the
envelope); hard stop at 2:30.
**Breaks if:** a pair never mismatched anything (they got lucky/naive) —
facilitator moves that pair's Q2 to the wall as "the biggest gap in the
room" so they still own a catch.

### M8 — 2:15, synthesis
**Feel:** three sentences crystallize.
**Must exist:** the three lessons said aloud while the scoreboard shows
their OWN two scores (raw vs governed) — the lessons cite their numbers,
not Spider 2.0.

### M7 — 1:50–2:15, they broke the machine
**Feel:** power — they wrote the trap, the AI fell (or honestly refused).
**Must exist:** wall cards + markers; C8; the transcription flow; and the
**edge playbook** for when the AI *survives* their trap: "Why did it
survive? What did the metric view carry for you? Now make it harder." — a
survived trap is a deeper lesson, not a dead end.
**Breaks if:** wall questions can't be transcribed (eval set lost) or the
room reads a survived trap as "see, it's fine."

### M6 — 1:25, THE MAGIC MOMENT (reveal of Arc 2)
**Feel:** the jump. 1.5/5 → ~4/5 on the scoreboard, caused by THEIR ticks.
**Must exist:** C6 runs first time for every pair (rehearse with the actual
model — this is the single most rehearsed step of the day); the re-run
questions actually change answers (view carries primary line + region —
**fixed after the audit**); envelope Q2 matches the default tick set
(**fixed after the audit**).
**Breaks if:** the view errors, or the re-run equals the naive run — then
the whole day's thesis collapses. Contingency: lead re-runs Q1' on the main
screen from the podium while roamers fix tables.

### M5 — 0:55, they declare
**Feel:** ownership — "ticks first, then paste."
**Must exist:** D1–D3 menus and the scoresheet tick boxes printed on the
same sheet, physically before the paste step.
**Breaks if:** any pair pastes C6 before ticking (the declare-order is the
lesson). Roamers enforce.

### M4 — 0:30, the first mismatch
**Feel:** intrigue — "my number is real, but finance's is different. Why?"
**Must exist:** C1 returns in < 1 min; the envelope mismatch is BIG
(86.3M naive vs 23.2M finance — by design); facilitator line: "you matched
the naive answer — the machine answered the question you literally asked."
**Breaks if:** the model over-governs (excludes cancelled unprompted) and
the naive answer never appears. Rehearsal watch-item; if seen, the C1 card
gains "do not exclude anything" wording.

### M3 — 0:12, the smoke test
**Feel:** "this just works."
**Must exist:** C0's "you should see" matches EXACTLY (16 tables + counts
**generated from manifest.json at print time** — never hand-typed, always
after the D-2 freeze); red/green cards; loaners warm.
**Breaks if:** WiFi/auth is touched in the room. While stragglers are
fixed, the rest of the room runs **C0.5** ("show me 5 cancelled orders") —
nobody watches a facilitator debug.

### M2 — 0:00, walking in
**Feel:** this is organized; I know what my hands will do.
**Must exist:** scoreboard, timer, deck per table, glossary, scoresheets,
the fictional company name on screen, poll questions ready.

### M1 — T-1 week, they chose to come
**Must exist:** a blurb promising three concrete take-homes (a number they
caught, a checklist, a rerun kit) — the registration page IS the first
experience.

## Experience contract (non-negotiables)

1. Nobody configures anything after 0:00.
2. Every participant mismatches an envelope at least once and understands
   why.
3. The score jump is caused by ticks the participant chose.
4. Every trap written in the room is photographed before the room empties.
5. Everyone leaves with the checklist physically and the rerun kit digitally.
6. Out at 2:30 sharp.

## Audit results (what working backwards changed)

| Finding | Fix |
|---|---|
| C6 view had no region/line attribution → re-run wouldn't fix the fan-out; the magic moment would have failed silently | C6 card rewritten: view must carry PRIMARY line + PRIMARY region columns |
| Envelope Q2 was gross of returns; attendees' default D2 tick is net → guaranteed reveal mismatch | Q2 keys + envelope recomputed to the default tick set; register names the ticks |
| No scoresheet existed — reveals had nothing physical to compare | `assets/scoresheet.md` print spec; D1–D3 tick-before-paste built into the sheet |
| Card counts could go stale vs the dataset (or the scale-0.2 rehearsal) | Generation rule added: print assets derive from `manifest.json` post-freeze |
| Rerun-at-home kit was promised in the take-homes but no WP owned building it | WP7 acceptance now includes the kit (DuckDB file + cards + checklist PDF) |
| Survived traps and naive-luck pairs had no script | Edge playbook lines added above (M7, M9) and to the facilitator pack (WP6) |

## Re-prioritized criticality (for the remaining WPs)

- **P0 — the moment dies without it:** C6/C7 rehearsal against the live
  model; scoresheets; envelopes; C0 counts from manifest; wall capture.
- **P1 — the day survives without it, barely:** DuckDB fallback; intern
  answers; loaner laptops.
- **P2 — polish:** slides, branding, follow-up email template.
