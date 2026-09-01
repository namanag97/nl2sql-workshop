# Environment runbook — Databricks + Codex, plus the offline fallback

Two hard rules: **(1)** nothing is configured while attendees watch;
**(2)** the room must survive total auth/network failure via the DuckDB kit.

## A. Databricks side (prep, D-10)

1. **Workspace + catalog**: dedicated workspace; catalog `nl2sql_ws`, schema
   `o2c`. Grant attendees **read** on catalog, **write only** on their own
   scratch schema (`o2c_team<N>`).
2. **SQL warehouse**: Serverless, size Small, auto-stop 30 min. Pin its ID —
   the MCP config references it explicitly (no "default warehouse" guessing).
3. **Load**: run `data/load/load_notebook.py`; verify the row-count table it
   prints matches `data/README.md`.
4. **Constraints pass** (Arc 2 needs raw → governed): raw tables have NO PK/FK
   metadata; the governed metric view `v_revenue_governed` is created live by
   attendees via `C6` — the prep creates only its *definition* in a helper
   table so any team can rebuild it.

## B. Codex side (prep, D-10)

1. **Auth**: Databricks MCP via `ucode` (documented Codex path — no OAuth
   app, client ID or secret needed):
   ```
   uv tool install git+https://github.com/databricks/ucode
   databricks auth login            # prerequisite: CLI + uv installed
   ucode mcp add --agents codex --services <catalog>.<schema>.<service>
   ucode codex                      # writes config, refreshes OAuth tokens
   ```
   Pin the service to the workshop catalog explicitly (the documented
   failure mode is profile/host mis-binding → "cannot register MCP server").
2. **Smoke**: run card `C0` twice; must return the table list in < 60 s.
   If MCP works in Inspector but not Codex, the fault is client config —
   re-run `ucode mcp add`. (PAT auth exists but only suits short-term
   testing; the room standard is the ucode OAuth flow.)
3. **Guardrails**: attendees get READ on `o2c` and WRITE **only on their
   team scratch schema** (`o2c_team1`..`o2c_team6`, one per table of two
   pairs) — cards C6/C7 create the governed view and notes there. No
   catalog-level DDL. **Ops check (D-2):** confirm Codex seat count and
   rate limits cover ~15 simultaneous agent sessions; plan the S13
   staggered start if not.
4. **Loaners**: 4 pre-authed spare laptops for pairs whose own machines fail.

## C. Pre-flight checklist (T-60, lead + 1 roamer)

| # | Check | Pass |
|---|---|---|
| F1.1 | Warehouse awake (ping via C0) | < 10 s response |
| F1.2 | Row counts match README | 16/16 tables |
| F1.3 | Codex smoke on 2 clean laptops | < 60 s |
| F1.4 | Scoreboard/timer/cards physically in place | per table |
| F1.5 | Key envelopes sealed (Q1–Q5 + reveal) | 6 envelopes |
| F1.6 | **Fallback decision point** at T-5 | go/fallback decided |
| F1.7 | Variance probe: run C1 + C2 three times | note answer variance on the run sheet |

## D. Fallback kit (offline, DuckDB)

Trigger: ≥ 2 tables red at S9, or network loss at any point before Arc 2.

1. **Artifact**: `data/fallback/meridian.duckdb` built by the same generator
   (identical keys — proven: 5/5 parity + 3/3 magic-moment checks in
   `data/fallback/verify_arcs.py`). **One DB copy per table** — duckdb has
   no grants; team views live in each copy's own `o2c_team<N>` schema
   (pre-created by the build script).
2. **Switch**: Codex config on each laptop points at the local file; cards
   are unchanged except `FROM` paths (printed on the reverse of each card).
3. **Tradeoff accepted**: no Unity Catalog governance objects in DuckDB —
   Arc 2's metric view becomes a plain view (same numbers, same lesson);
   constraints become comments in the schema file.
4. **Rehearsal duty**: WP4 acceptance requires running full Arc 1 + Arc 2 on
   the fallback once, keys diffed against `keys.json`.

## E. Reset kit (between rehearsals / sessions)

- `data/load/reset.sql` — drop scratch schemas + governed view, restore raw
  state. Run after every rehearsal; verify with `C0`.
- Loaner laptops: re-run auth smoke, clear chat history.

## F. Known failure modes (from field reports)

| Symptom | Cause | Fix |
|---|---|---|
| "Couldn't register with the MCP server's sign-in" | profile/host mis-binding | re-run `ucode` bind with explicit profile; see runbook §B.1 |
| Codex answers from memory, not data | agent didn't query | cards force "you should see <table> <count>"; PIRA Inspect step |
| Warehouse auto-stopped mid-arc | 30-min idle | lead pings at every segment boundary |
| Venue blocks OAuth ports | corporate network | switch to fallback kit; report to venue (do not debug live) |
