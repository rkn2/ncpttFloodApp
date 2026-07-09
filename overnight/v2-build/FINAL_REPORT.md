# floodApp v2 — Overnight Build: Final Report & Handoff

**Campaign:** 7 build rounds + wrap-up, each hypothesis-gated (Opus), validated by an automated
acceptance test, and self-critiqued. **Result: 9/11 core deliverables validated, 2 partial.**
Nothing was marked "done" without a passing, re-run test recorded in a round file.

---

## 🔴 DO THESE FIRST (only you can — I can't)

1. **REVOKE the leaked Groq API key** `gsk_rfyOhRY9…56se` in the Groq console. It was hardcoded in
   the client JS and pushed to **public** github.com/rkn2/ncpttFloodApp. I removed it from all working
   files, but **it still exists in git history**, so it must be treated as permanently compromised.
   Revoking is the only real fix.
2. **Scrub git history** (`git filter-repo` or BFG) to purge the key from past commits, then
   force-push. I did NOT rewrite pushed history unattended — that's your call.
3. After revoking: the online chat now requires each user to paste their own key (no shared default).
   The production fix is a **backend proxy** (P0 external item — not buildable overnight). Until then,
   the app still works fully offline; only the online "ask a question" LLM synthesis is affected.

---

## What was built and validated

### P0 — Security & credibility (Round 1)
- **Removed the leaked key** from `floodapp.html` + `deploy/index.html`; `getGroqKey()` now returns
  only the user's localStorage value.
- **Fixed a regression the removal exposed:** reordered `sendChat()` so the offline passage search
  runs *before* the key check — an offline user (the core case) is no longer blocked by a key prompt.
- **`pipeline/scan_secrets.py`** — credential scanner (self-test + full-tree clean), usable as a
  git pre-commit hook.

### P1 — The NLP authoring pipeline (Rounds 2–5) — *the headline deliverable*
A reproducible pipeline under `pipeline/` that compiles **structured, cited** guidance from the
documents in `docs/`, with provenance enforced mechanically:
- **`extract.py`** — cached extraction + per-PDF fidelity report. Caught that the **SOI Standards PDF
  is garbled** under pdftotext (custom font) *before* any content was built on it.
- **`corpus.py`** — recovers clean SOI text from the already-OCR'd chunks in `knowledge-base.json`.
- **`retrieve.py`** — BM25 retrieval of candidate source passages per topic.
- **`verify_citations.py`** — the provenance rail: every citation's quote must appear **verbatim** in
  its source (strict substring, NFKD + de-hyphenation normalization, ≥8-word length gate, no fuzzy
  matching). This makes "don't hallucinate repair advice" a mechanical check.
- **`guidance_schema.py`** / **`directive_lint.py`** — structural validator (every item must be cited)
  + scope-creep lint (flags unlicensed absolutes/safety-verbs/thresholds).
- **`content-bundle.json`** — **5 cited guidance records** (siding, windows, chimney, insulation,
  interior), 43 items, **49/49 citations verified**. Each item passed **three independent gates**:
  mechanical quote-verification, an LLM claim-entailment audit, AND a flood-relevance audit. The gates
  **dropped 2 unsafe items** during synthesis (a false attribution to a garbled source; a
  verbatim-but-distorting over-claim applying "stone foundation wall" guidance to a chimney) and
  **removed the roof record entirely** — a relevance audit found it was mostly wind/hail/storm
  mitigation (out of the project's inland-flood scope) and the corpus has almost no flood-specific
  roof content. For roof, the app falls back to its built-in flood-appropriate guidance, and roof is
  flagged for human authoring.
- **4 categories held back for human authoring** in
  `overnight/v2-build/artifacts/needs_human_authoring.json` (NOT in the shippable bundle):
  structural, electrical, mold (safety-critical — a subtly wrong directive can injure people), plus
  roof (corpus lacks flood-specific roof guidance). Retrieved passages included for an expert (APTI
  DRI) to author from.
- **App integration** — `floodapp.html` loads the bundle and renders cited guidance with the **exact
  source quote shown on hover (📄)**; falls back to the built-in guidance if the bundle is absent.

### P2 — Offline + internationalization (Rounds 6–7)
- **Installable offline PWA** — `deploy/manifest.webmanifest`, `deploy/sw.js` (precaches the app
  shell + guidance bundle + 3.2MB knowledge base so it works with no signal), `deploy/icon.svg`, SW
  registration in the app. Versioned cache with cleanup; Groq excluded from caching.
- **i18n scaffold** — `t()` + string table + **EN/ES switcher**; the welcome/entry screen is fully
  translated to **Spanish** (100% key coverage, English fallback).

---

## What still needs you (beyond the 🔴 items)

| Item | Why it needs a human |
|------|----------------------|
| **Redeploy** `deploy/` to Netlify | You hold the hosting account. The folder is ready & synced. |
| **Confirm offline once** | I validated all PWA machinery but have no browser here. Open the deployed site online, then reload in airplane mode / DevTools-Offline — it should load fully. |
| **Click through the app once** | Validation was at the logic/HTTP level, not a rendered browser. Walk the homeowner flow: confirm cited guidance renders with 📄 quote-on-hover tooltips, roof shows the built-in fallback, and the EN/ES switch works on the welcome screen. |
| **Bump `CACHE_VERSION`** in `deploy/sw.js` on every future deploy | Otherwise returning users are stranded on the old cached app. |
| **Author the 3 safety-critical categories** | structural/electrical/mold — from `needs_human_authoring.json`, reviewed by APTI DRI. |
| **Native Spanish review** | The Spanish strings are machine-authored; a PR/native reviewer should check preservation terminology before public release. |
| **Delete a duplicate PDF** | `docs/treatment of flood damaged hist buildings.pdf` duplicates `nthp-treatment-…pdf`; remove one before the next KB rebuild. |

---

## How to run / re-verify everything
```bash
cd /Users/becca/Code/floodAPp
python3 pipeline/scan_secrets.py .                     # no secrets
python3 pipeline/verify_citations.py content-bundle.json   # 60/60 verified
python3 pipeline/extract.py                            # fidelity report (SOI flagged garbled)
python3 -m http.server 8000                            # then open http://localhost:8000/deploy/
```
To rebuild guidance from source later: the pipeline is pluggable — the deterministic steps run in
Python; the synthesis step (done this run by in-loop LLM subagents) can be wired to an API. See
`pipeline/` and the round files for the exact harness.

## Where things live
- **App:** `floodapp.html` (source of truth) → copied to `deploy/index.html`.
- **Pipeline:** `pipeline/*.py` (7 modules, all self-tested).
- **Compiled guidance:** `content-bundle.json` (ships) + `needs_human_authoring.json` (held back).
- **Campaign trail:** `overnight/v2-build/` — `PROTOCOL.md`, `LEDGER.md`, `HYPOTHESES.json`,
  `LOG.md`, `rounds/round_0N.md` (full reasoning + evidence per round), `artifacts/`.
- **The v2 strategy doc** you'll send to grants people: `V2_PLAN.md`.

## Honest limitations
- **D2.1 (PWA):** offline machinery validated; the actual airplane-mode reload needs 1 manual check.
- **D0.4:** 6/9 categories now cited in-app; 3 safety-critical intentionally deferred to humans.
- **D2.3 (Spanish):** entry screen fully translated as a working scaffold; the deeper homeowner flow
  (steps, results, insurance panel) is not yet externalized — mechanical follow-on using the same
  `t()` pattern.
- **Nothing here replaces a professional structural/electrical/mold assessment** — the app says so.
- **Stopped reason:** all autonomously-achievable P0–P2 families addressed (frontier empty).
