# Round 04 — SYNTHESIS (the headline payoff): cited content-bundle.json

## MEASURE
Start 5/11. Frontier [H4,H5,H6,H7]. Move: H4 synthesis (highest drift risk → gate first).

## HYPOTHESIZE (Opus gate)
Gate identified **case (b)** as the real threat: a VERBATIM quote wrapped in a distorting frame
passes quote-match but the advice is wrong — the mechanical check is blind to it. Recommendations
(all adopted):
- Split: auto-synthesize only the 6 NON-safety-critical categories; hold structural/electrical/mold
  for human authoring (a subtly wrong directive there injures people).
- Add a **claim-entailment gate** (independent LLM: "is this claim entailed by this passage?").
- Add a **deterministic directive-scope lint** (absolutes/safety-verbs/thresholds).
- Flag thin retrieval coverage; store quote context for review.

## SELECT / EXECUTE
- `directive_lint.py` (self-test PASS). Retrieval briefs for all 9 categories — coverage solid
  (top scores 15–36, no thin flags).
- 6 synthesis subagents (sonnet), each given ONLY its category's 8 passages, told to quote VERBATIM
  ≥8 words. Returned 6 schema-valid records.
- Assembled `bundle_draft.json`; ran the gates:
  1. **schema** — 0 errors.
  2. **verify_citations (mechanical)** — 62/63; **caught 1** false attribution (chimney: an
     nps quote not verbatim in source — real text was in a garbled SOI OCR region; subagent had
     "cleaned it up"). Diagnosed to root cause, DROPPED the item (rail: never ship unverified cite).
  3. **directive_lint** — 2 warnings, both conditional/hedge phrasing ("not all", "if…must"),
     not scope-creep; reviewed acceptable.
  4. **claim-entailment audit (opus, independent)** — 53 items, **caught 1 case-(b) over-claim**
     (chimney/do: quotes about "stone FOUNDATION walls" reframed as chimney advice). DROPPED it.
     Two borderline items judged entailed with minor notes (kept).
- Finalized: `content-bundle.json` (6 verified records, 52 items, 60/60 citations) +
  `needs_human_authoring.json` (structural/electrical/mold — retrieved passages only, NO shippable
  advice, so they can never reach a user unreviewed).

## VERIFY (acceptance — re-run, captured)
- **D1.3 PASS** — `verify_citations.py content-bundle.json` → 60/60 verified (exit 0). 0 schema errors.
  9 topics addressed (6 shippable + 3 quarantined). Two independent gates dropped 2 unsafe items.
- Fixed 2 bugs found during finalization: verify_bundle CLI wasn't traversing do/dont item citations
  (reported 0/0); schema required summary before the needs_human_authoring early-return. Both fixed;
  schema + verifier self-tests still PASS.

## Metric delta
5/11 → 6/11 (D1.3 DONE).

## CRITIQUE / carry-forward
- The two-gate design (mechanical + semantic) demonstrably works: quote-match caught a false
  attribution; entailment caught a verbatim-but-distorting over-claim. Neither alone was sufficient.
  This is the provenance story for the grant, and it's real, not claimed.
- 2/9 categories' auto-drafts lost an item to the gates — expected and healthy (the system refuses to
  ship unverifiable/over-reaching advice). The garbled SOI region around masonry repointing is a
  known soft spot; those claims are better human-authored.
- Next: D1.4 — wire floodapp.html to load content-bundle.json when present (graceful fallback to the
  hardcoded REPAIR_GUIDANCE). Then P2 (PWA + i18n).
