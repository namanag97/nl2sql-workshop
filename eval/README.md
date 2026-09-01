# Eval capture — the company's take-home

The wall of pain is not a souvenir; it is an eval set. Every trap question
written in the room becomes a regression case for the product.

## Capture flow (during workshop)

1. Roamer transcribes each pinned card verbatim into `eval/raw/capture.csv`
   (columns: `card_text, pair_id, wall_position, photo_ref`).
2. Photograph the wall as backup (`eval/raw/photos/`).
3. No triage in the room — capture only. Triage is WP9 (D+3).

## Triage (post-workshop)

For each raw card, classify and dedupe:

| Field | Values |
|---|---|
| `outcome` | `refused` / `answered_with_assumptions` / `confidently_wrong` / `unrun` |
| `trap_axes` | subset of A1–A10 (see `docs/problem-catalog.md` header) |
| `difficulty` | `easy` / `hard` (DABstep convention) |
| `duplicate_of` | id of an earlier equivalent case, if any |

## Case format (`eval/cases.schema.json`)

```json
{
  "id": "CASE-0007",
  "question": "verbatim from the wall",
  "expected": {"type": "number|table|refusal",
               "value": null,
               "refusal_reason": "ambiguous term 'active'"},
  "decision_register": ["exclude cancelled", "net of returns"],
  "trap_axes": ["A1", "A6"],
  "difficulty": "hard",
  "outcome_at_workshop": "confidently_wrong",
  "pair_id": "T3-P2",
  "notes": ""
}
```

## Acceptance (WP8)

- ≥ 30 deduped cases exported to `eval/cases.jsonl`.
- Every case has `trap_axes` filled and either an expected value or an
  explicit refusal reason.
- **Grading tolerance**: numeric expectations carry a `tolerance` field —
  exact integers compare exactly; computed ratios/percentages pass within
  ±0.5% unless the case says `exact`. Model nondeterminism is no excuse for
  a flaky grader.
- The export reruns: `cases.jsonl` can be replayed against the governed
  setup from `data/` to reproduce workshop outcomes (that's the regression
  harness — wrongness that is reproducible is fixable).

## Why this matters

Attendees leave with the checklist and the story; the company leaves with a
measured raw-vs-governed delta and a backlog of real failure cases. That
two-sided payoff is what makes the same 2.5 hours worth everyone's time.
