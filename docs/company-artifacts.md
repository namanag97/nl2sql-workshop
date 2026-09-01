# Company artifacts — the realism layer

The packs stop feeling like exercises when the ambiguity arrives the way it
arrives at work: **in documents, not in schemas**. Three artifacts are baked
into the app (`app/index.html` → "Company Artifacts") and printed below.
Attendees must reconcile *documents vs data vs the question being asked* —
that reconciliation is the most realistic enterprise skill in the whole day.

## The three artifacts

| Artifact | Seeds | Undermines | Used by |
|---|---|---|---|
| 📧 **CFO email** (Mon 07:42): "ONE number. Invoice-basis, net of returns, cancelled isn't revenue, no European entities. Fix the stale wiki." | The authoritative ask | Naive answers; the stale wiki | P1, P2 |
| 📄 **Wiki "Metric definitions"** (edited Jan 2026): revenue = all lines, fiscal, order-date; active = ordered in trailing 90d; region = see table | The stale authority | Anyone who trusts documentation over the ask | P1, P3 |
| 💬 **Teams #data-help thread**: sales-ops sees 62.5M vs finance 27.5M; data-eng: "they're both right — check your line join and the two-region reps"; CFO-office: "one number, declared rules, no vibes" | The room's exact dilemma, in the company's own voice | The idea that one of two numbers is simply "wrong" | P2, P8 |

## How packs use them

- **P1** tasks now include: *read the artifacts; the CFO email and the wiki
  disagree — who wins, and what would you tell the board?* The envelope
  numbers correspond to the CFO email's rules (invoice-basis, net, USD):
  attendees can literally grade the CFO against the warehouse.
- **P2**: the Teams thread IS the room's situation, pre-told. Sales-ops's
  62.5M is the actual naive fan-out total — attendees can verify the thread
  against the data.
- **P3**: the CFO email's postscript ("fix or delete the wiki") is why the
  restatements happened — documents explain the data's transaction-time
  story.
- **P8**: the traps are phrased as questions *real colleagues asked*, and
  the correct move is often "the wiki is stale, refuse and confirm with
  the CFO's definition."

## Realism upgrade plan (v2 options — require a full pipeline rerun)

Ordered by realism-per-effort; the pipeline makes each a one-command rebuild:

1. **Dirty column names** (`cust_ref`, `ord_dt`, `amt_usd`) — schema stops
   looking synthetic. Effort: rename in generator + DDL + all key SQL.
2. **A decoy table** (`orders_old`, 2019–2024, similar shape) — agents and
   humans must notice the period. Effort: one table + one quirk check.
3. **Late-arriving fact feed**: a small `invoices_restatements` table that
   changes Q1 answers when included — makes "which tables did you use?" a
   real lineage question. Effort: moderate.
4. **Mixed currencies stored natively** (EUR amounts in EUR) — forces the
   FX-date decision to bite in the base question, not just the ceiling.
5. **A second, contradicting "official" dashboard spec** exported as CSV —
   the artifact that is *provably wrong* against the data.

Adopted so far in v1: the artifact layer above. 1–2 are recommended before
the next workshop cohort; 3–5 are diminishing returns for a 2.5h format.
