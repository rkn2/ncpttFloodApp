# Offline Search for floodAPp — Research Protocol

**Goal:** Determine the best offline replacement for the Groq RAG pipeline in floodapp.html (a single-file HTML app). The app must work with ZERO internet/cell signal in flood zones. It currently uses Groq API for RAG chat over 513 knowledge-base chunks from flood damage assessment PDFs. Deliverable: a concrete, evidence-backed recommendation (with bundle-size numbers, cold-start times, result quality assessment) for which offline search approach to implement. Budget: ~$0.50.

Scope order: (1) BM25/keyword search in-browser, (2) local embeddings (transformers.js / ONNX), (3) hybrid approaches.

Every wakeup runs **exactly one round** following these steps in order.

## The metric (recompute every round)
This is a research task, not a code optimization task. The "metric" is **decision confidence**:
- LOW: only one option investigated
- MEDIUM: both options investigated with concrete numbers
- HIGH: concrete numbers + domain-specific quality assessment + clear winner

Target: HIGH confidence by round 2 or sooner. Stop when recommendation is evidence-backed.

## Baseline / known failure modes
- Current: Groq API (`floodapp.html:1955`) — requires internet, exposes API key client-side
- 513 chunks in `docs/knowledge_base.json` (built by `build-kb.py`)
- Domain: flood damage assessment (FEMA, NRHP, secretary of interior standards PDFs)
- Query types: "what are the secretary of interior standards for wood repair?" / "how do I assess flood damage to a masonry building?"

## Hard safety rails
1. **Never mutate source data.** `floodapp.html`, `docs/`, `build-kb.py` are READ-ONLY. All artifacts under `overnight/offline-search/`.
2. **Budget guard.** Before any paid subagent call, check `STATE.budget`. Cap: **$0.50**.
3. **Evidence before claims.** Cite specific bundle sizes, GitHub stars, npm download counts, benchmarks.
4. **No silent error sinks.** Log any failures honestly.
5. **Subagent models are explicit.** `model: "opus"` for gate; `model: "sonnet"` for workers.

## Round steps
1. **MEASURE.** Read STATE.json + latest outputs. Assess current decision confidence.
2. **HYPOTHESIZE — Opus gate.** Pruned frontier view → 3 diverse hypotheses → ranked rec.
3. **SELECT.** Pick one investigation angle from the frontier.
4. **EXECUTE.** Research the selected angle; write findings to rounds/round_NN.md.
5. **VERIFY.** Can the findings support a concrete recommendation? Document evidence.
6. **LOG + PERSIST.** Update HYPOTHESES.json, LOG.md, STATE.json.
7. **SCHEDULE.** If HIGH confidence reached, write FINAL_REPORT.md and end. Otherwise loop.

## Stop conditions
- Decision confidence reaches HIGH (concrete recommendation with supporting numbers).
- `budget.spent_usd_est >= 0.50`.
- 3 consecutive rounds with no new evidence (shouldn't happen for a research task).
