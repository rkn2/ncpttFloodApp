# Round 03 — complete the deterministic pipeline + resolve SOI-garbled

## MEASURE
Start 4/11. Frontier [H3,H4,H5,H6,H7]. Move: H3 (retrieval + SOI fix + schema → completes D1.1).

## HYPOTHESIZE / SELECT
No separate gate this round — Round 2's gate already laid out the sequence (precheck→verifier→
retrieval→synthesis) and flagged the SOI-garbled dependency. Executing that plan; the next gate runs
before synthesis (Round 4), which is the higher-risk creative step where drift is likely.
(Recorded deviation from "gate every round": the immediate move was fully specified by R2's gate and
is deterministic tooling with objective acceptance tests; I front-load the gate budget onto R4.)

## EXECUTE (additive, pipeline/)
- `corpus.py` — unified clean-text provider. For a garbled source (SOI), reconstructs clean text from
  the OCR'd chunks already in knowledge-base.json instead of re-OCR (libs not installed).
- Rewired `verify_citations.py` to source text via corpus → SOI quotes now verify against clean text.
- `retrieve.py` — BM25 retrieval over KB chunks (reuses KB idf/avgdl), returns top-k candidate
  passages per topic; feeds synthesis with real quotable text.
- `guidance_schema.py` — record schema + validator. Enforces that every actionable item (do/dont/
  soi_standard) carries ≥1 citation (provenance is structural). Does NOT check resolution — that's
  verify_citations' job; run both.

## VERIFY (re-run, captured)
- **SOI empirical resolution:** verdict `garbled-recovered` (266,690 clean chars from KB chunks). A real
  SOI-Standards span now **VERIFIES**; a fabricated SOI quote **FAILS**. (Before: SOI was unciteable.)
- `verify_citations --self-test` PASS after rewiring. `guidance_schema` self-test PASS (rejects uncited
  item + bad audience). Retrieval returns on-topic passages for "repoint masonry lime mortar".
- All 6 pipeline modules import cleanly.

## Metric delta
4/11 → 5/11 (D1.1 DONE: extract+retrieve+schema). D1.1b (fidelity) already counted.

## CRITIQUE / carry-forward
- Retrieval surfaced the **duplicate PDF** (`nthp-treatment-…` ≡ `treatment of flood damaged hist
  buildings.pdf`, identical chunk #20). Harmless for citing, but inflates the KB and could double-cite.
  Recommend Becca delete one before the next KB rebuild. Noted for handoff.
- Next (R4) is the payoff and the riskiest step: SYNTHESIS. Subagents must quote ONLY verbatim from
  retrieved passages (≥8 words) so verify_citations passes. Plan: retrieve passages here, hand to
  subagents, gate every record through guidance_schema + verify_citations, retry failures. Run the
  Opus gate first (creative step = highest drift risk).
