# Resource Library Research — Round Protocol

**Goal:** Find every authoritative, publicly available document relevant to flood recovery for historic buildings and districts that should be in the floodAPp knowledge base. Priority: documents that mention historic buildings, historic districts, preservation standards, or culturally significant properties in the context of disaster/flood response. Deliverable: a verified list of downloadable PDFs/documents with URLs, descriptions, and relevance notes — ready to drop into docs/. Budget: ~$1.00.

Current KB has: NAIC Post-Disaster Claims Guide, FEMA Treatment of Flood-Damaged Historic Buildings, Secretary of Interior Standards (NPS). We likely have gaps in: state-specific SHPO guidance, FEMA historic-specific policy docs, insurance for historic properties, ACHP guidance, National Trust resources, SBA disaster loan guidance for historic properties, and community/district-level recovery docs.

Every wakeup runs **exactly one round** following steps in order.

## The metric
Decision confidence on coverage completeness:
- LOW: <5 distinct authoritative sources found
- MEDIUM: 5–12 sources found across multiple agencies/organizations  
- HIGH: 12+ sources, covering FEMA/NPS/ACHP/National Trust/SHPO/insurance domains, verified accessible

Target: HIGH. Stop when frontier is exhausted or budget hit.

## Baseline / known sources already in KB
- `secretary for interior.pdf` — NPS Secretary of Interior Standards
- `treatment of flood damaged hist buildings.pdf` — FEMA/NPS joint guide
- `post-disaster-claims-guide.pdf` — NAIC general insurance claims guide

## Hard safety rails
1. **Never add to docs/ during research** — research only; final download list goes in FINAL_REPORT.md. Becca decides what to add.
2. **Budget guard.** Cap: **$1.00**. Check STATE.budget before each paid subagent call.
3. **Evidence before claims.** A source is only listed if the URL is verified accessible (200 OK or PDF confirmed). No dead links.
4. **No silent error sinks.** Log 404s and dead links honestly.
5. **Subagent models explicit.** `model: "opus"` for gate; `model: "sonnet"` for workers.

## Round steps
1. **MEASURE.** Read STATE.json + prior round files. Count verified sources found so far. Assess coverage completeness.
2. **HYPOTHESIZE — Opus gate.** Pruned frontier → 3 diverse hypotheses → ranked rec.
3. **SELECT.** Pick investigation angle. Record rationale.
4. **EXECUTE.** Research subagent searches the selected domain. Verifies URLs. Returns source list.
5. **VERIFY.** Cross-check: is each source actually accessible? Is it relevant to historic buildings + flood/disaster?
6. **LOG + PERSIST.** Update HYPOTHESES.json, append to LOG.md, update STATE.json, write round file.
7. **SCHEDULE.** If HIGH confidence + frontier exhausted, write FINAL_REPORT.md and end. Otherwise loop.

## Stop conditions
- Coverage HIGH AND frontier empty/exhausted.
- `budget.spent_usd_est >= 1.00`.
- 3 consecutive rounds with no new verified sources.
