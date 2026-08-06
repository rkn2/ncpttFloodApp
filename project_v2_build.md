---
name: project-v2-build
description: "floodApp v2 overnight build — what got built (P0-P2), the authoring pipeline, and URGENT human actions"
metadata: 
  node_type: memory
  type: project
  originSessionId: cbdae0b4-651a-4d2c-aeca-d2ce3a08782e
---

Overnight autonomous build (2026-07-08→09), hypothesis-gated loop. Full trail:
`overnight/v2-build/` (PROTOCOL, LEDGER, HYPOTHESES.json, LOG, rounds/round_0N.md, FINAL_REPORT.md).
Strategy doc for grants people: `V2_PLAN.md`. Result: **9/11 core deliverables validated, 2 partial.**

## Human actions
- ✅ **RESOLVED (2026-07-10): Groq key `gsk_rfyOhRY9…` revoked** — Becca handled this herself in the
  Groq console. Git history may still contain the old string but it's dead, so no longer urgent.
- Scrubbing git history (BFG/git-filter-repo) is now optional cleanup, not urgent — the key is dead.
- Redeploy `deploy/` to Netlify; confirm offline once in a browser (airplane-mode reload); bump
  `CACHE_VERSION` in `deploy/sw.js` every deploy.

## What's built (all validated by automated tests)
- **P0 security**: key removed; `getGroqKey()`→localStorage only; offline-first reorder in sendChat;
  `pipeline/scan_secrets.py` guard.
- **P1 NLP authoring pipeline** (`pipeline/`): extract.py (fidelity), corpus.py (SOI garbled →
  recovered from OCR'd KB chunks), retrieve.py (BM25), **verify_citations.py** (strict verbatim
  substring + ≥8-word gate = provenance rail), guidance_schema.py, directive_lint.py. Output
  **`content-bundle.json`**: 5 cited guidance records (siding/windows/chimney/insulation/interior),
  **49/49 citations verified** through THREE gates (quote-verify + entailment + flood-relevance).
- **4 categories held for human authoring** (`needs_human_authoring.json`): structural/electrical/mold
  (safety-critical) + roof (a flood-relevance gate found roof auto-content was mostly wind/hail, out of
  the inland-flood scope, and the corpus lacks flood roof guidance; app falls back to built-in roof text).
- App (`floodapp.html`) renders cited guidance with verbatim source quote on hover (📄), graceful
  fallback to built-in guidance.
- **P2**: offline PWA (`deploy/` manifest+sw.js precache shell+bundle+KB); i18n scaffold (t()+EN/ES
  switcher, Spanish entry screen).

## Partials / follow-on
- D0.4: 6/9 categories cited in-app; 3 safety-critical deferred to humans.
- D2.3: Spanish = entry screen only; full-flow externalization is mechanical (wrap strings in t()).
- D2.1: PWA machinery validated; 1 manual browser offline-check pending.
- Native Spanish review needed before PR public release. Delete duplicate PDF
  `docs/treatment of flood damaged hist buildings.pdf` (≡ nthp-treatment-…) before next KB rebuild.

## Not done (external deps, out of scope): P3 computer vision (Esri), P4 SHPO backend, chat backend proxy.

See also [[project-next-steps]] [[project-rag-pipeline]] [[project-structure]] [[project-stakeholders]].
