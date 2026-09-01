# Research bibliography — 25+ sources, mapped to the workshop

Every source states what it contributes and where it lands in the material.
New sources from the latest sweep are marked ★.

## A. The accuracy cliff — why the workshop exists

1. ★ [Spider 2.0 — enterprise text-to-SQL benchmark](https://spider2-sql.github.io/) — 632 real enterprise workflow problems; the 86–91% → 10–21% collapse is the workshop's headline number. Used: concept beat (S16), registration blurb.
2. ★ [The Text-to-SQL Accuracy Cliff (CoLrops)](https://colrows.com/blogs/text-to-sql-accuracy-cliff/) — analysis of the benchmark gap. Used: facilitator talking points.
3. ★ [Promethium — enterprise benchmark reality](https://promethium.ai/guides/enterprise-text-to-sql-accuracy-benchmarks-2/) — best real-platform accuracy ~59% (Snowflake), ~38% elsewhere. Used: "even the best deployments miss."
4. ★ [DABstep (Adyen) — multi-step data agent benchmark](https://arxiv.org/abs/2506.23719) — frontier agents ≈16% at launch on realistic multi-step analysis. Used: P7's framing; grading format.
5. ★ [DABstep blog + leaderboard](https://huggingface.co/blog/dabstep) — task design (short verifiable answers) adopted as the workshop's key format.
6. ★ [GPT-5: 94.6% on AIME, fails enterprise SQL (Tunguz)](https://www.linkedin.com/posts/tomasztunguz_gpt-5-achieves-946-accuracy-on-aime-2025-activity-7361540127786979328-hF_s) — reasoning doesn't transfer to schema grounding. Used: S15 transition line.
7. ★ [A Survey of Text-to-SQL in the Era of LLMs (arXiv)](https://arxiv.org/html/2408.05109v5) — dedicated error-analysis section; validates the failure taxonomy the packs teach. Used: pack design rationale.
8. ★ [ACM Survey: LLMs for Text-to-SQL (2025)](https://dl.acm.org/doi/10.1145/3737873) — peer-reviewed taxonomy of semantic/schema errors. Used: defense of the 8-pack coverage claim.
9. ★ [Awesome-LLM-based-Text2SQL (curated index, TKDE 2025)](https://github.com/DEEP-PolyU/Awesome-LLM-based-Text2SQL) — reference index for future pack updates.
10. ★ [EntSQL — grounding text-to-SQL in proprietary business documents](https://arxiv.org/html/2606.03363v2) — documents-as-context failure mode; supports the artifacts layer.

## B. The cure — semantics beats model choice

11. ★ [dbt: Semantic Layer vs Text-to-SQL 2026 benchmark](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026) — near-100% accuracy for metric-covered queries via MetricFlow. Used: Arc 2, "steal this at work."
12. ★ [Semantic layers make enterprise text-to-SQL safer (Data Lakehouse Hub)](https://datalakehousehub.com/blog/2026-05-semantic-layers-text-to-sql) — **~40% → 85–95% when grounded in a semantic layer**. The strongest quantified lift found; use in the concept beat.
13. ★ [HumainEETI — semantic layer architecture & tools](https://www.humaineeti.ai/resources/text-to-sql-semantic-layer) — naive enterprise text-to-SQL under 60%. Used: corroborates #12.
14. ★ [Cube — semantic layer for AI agents (2026)](https://cube.dev/articles/semantic-layer-for-ai-agents-2026) — vendor-neutral semantic-layer design for agents. Used: rerun-at-home kit references.
15. ★ [Databricks — curate an effective Genie agent](https://docs.databricks.com/aws/en/genie-agents/best-practices) — official guidance: SQL expressions + examples beat prose. Used: C7 card design.
16. ★ [Databricks — metric views (create + YAML reference)](https://docs.databricks.com/aws/en/uc-semantics/metric-views/create) — the platform-native upgrade path mentioned in S21.
17. ★ [Databricks as a semantic engine (community)](https://community.databricks.com/t5/get-started-discussions/databricks-as-a-semantic-engine-why-the-semantic-layer-was-never/td-p/165741) — raw-schema text-to-SQL plateaus below production grade. Used: S17.
18. ★ [Databricks — PK/FK constraints (informational, not enforced)](https://docs.databricks.com/aws/en/tables/constraints) + [RELY GA blog](https://www.databricks.com/blog/primary-key-and-foreign-key-constraints-are-ga-and-now-enable-faster-queries) — "declaration ≠ enforcement" beat in S21.
19. ★ [Databricks — connect coding agents via MCP/ucode](https://docs.databricks.com/aws/en/agents/mcp-tools/connect-clients) — exact workshop wiring.

## C. Packs' specialist evidence

20. ★ [NCSC — Prompt injection is not SQL injection (it may be worse)](https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection) — prompts have no instruction/data boundary, unlike parameterized queries. **Used: P5's core lesson has a national-security authority behind it.**
21. ★ [ICSE 2025 — Prompt-to-SQL injection attacks](https://dl.acm.org/doi/10.1109/ICSE55347.2025.00007) — academic proof LLM-integrated apps are attackable. Used: P5 attack exercises.
22. ★ [Cisco — guardrails aren't enough](https://blogs.cisco.com/ai/prompt-injection-is-the-new-sql-injection-and-guardrails-arent-enough) — agents must inherit user authorization at the data layer (row-level security). Used: P5 debrief.
23. ★ [Secure Code Warrior — agentic tool prompt-injection risks](https://www.securecodewarrior.com/blog/prompt-injection-and-the-security-risks-of-agentic-coding-tools) — real agent compromise story. Used: P5 facilitator color.
24. ★ [van der Aalst — OCPM divergence/convergence (foundational)](https://www.researchgate.net/publication/335698927) — why one-case-per-event logs distort reality. Used: P6 log design.
25. ★ [Springer — classification of data quality issues in object-centric event data (2024)](https://link.springer.com/chapter/10.1007/978-3-031-82225-4_23) — academic backing for P6's validity-check step (orphans, backdated events).
26. ★ [Celonis — what is object-centric process mining](https://www.celonis.com/blog/what-is-object-centric-process-mining-ocpm) + [Microsoft OCPM adoption](https://learn.microsoft.com/en-us/power-platform/release-plan/2025wave2/power-automate/analyze-processes-using-object-centric-process-mining) — industry legitimacy for P6's approach.
27. ★ [Tamr — CDP vs MDM: customer matching challenges](https://www.tamr.com/blog/cdp-vs-mdm-3-key-differences-for-customer-data) + [Semarchy MDM use cases](https://semarchy.com/blog/examples-of-master-data-management/) — duplicated records, siloed entities: exactly P4's QK-10/11/12. Used: P4 story grounding.
28. ★ [Panorama — MDM challenges are governance, not technology](https://www.panorama-consulting.com/avoiding-inconsistent-master-data-and-other-mdm-challenges/) — "identity is a governed asset" has a consulting-industry source. Used: P4 debrief.
29. ★ [Fast Company / Reltio-HBR — 82% of decision-makers expect data literacy; fewer than half trained](https://www.nojitter.com/data-management/3-numbers-on-the-state-of-data-literacy) + [Frontiers 2025 systematic review on literacy → decisions](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1485821/full) — marketing stats and the "worth it" evidence for the training format itself.
30. ★ [Enterprise MDM trends (EA Journals 2025)](https://eajournals.org/ejcsit/vol13-issue12-2025/enterprise-master-data-management-trends-and-solutions/) — academic survey; P4 background.

## D. Workshop design (from the earlier sweep)

31. [Nick Tune — captivating workshop ratios](https://medium.com/nick-tune-tech-strategy-blog/designing-captivating-workshops-41e77c076467) (60/25/15) · 32. [Britt Andreatta — 20-minute chunks](https://www.brittandreatta.com/5-best-practices-for-awesome-workshop-design-1-in-3-part-series/) · 33. [ACM TOCE — cognitive load in computing education](https://dl.acm.org/doi/10.1145/3483843) (worked examples beat exploration for novices) · 34. [UXDX — concept/activity alternation](https://uxdx.com/blog/10-tips-for-running-a-hybrid-workshop/) · 35. [Open Practice Library — visible timeboxing](https://openpracticelibrary.com/blog/facilitation-tips-for-remote-sessions/).

## E. Sources that changed the material

| Finding | Change made |
|---|---|
| Semantic layer lifts measured at 40–60% → 85–95% (#12, #13) | Concept beat now quotes a *range*, not just the cliff; "steal this at work" cites dbt/Cube/MetricFlow by name |
| NCSC + ICSE + Cisco on injection & data-layer authorization (#20–22) | P5 debrief upgraded from "good practice" to "national security agency + top-tier venue + vendor consensus" |
| Springer OCEL data-quality classification (#25) | P6's validity ledger (orphans, backdated events) is now academically grounded |
| Text-to-SQL error surveys (#7, #8) | The 8-pack failure taxonomy is defensible as coverage, not anecdote |
| DABstep format (#5) | Already adopted: short verifiable answers, easy/hard tiers |
