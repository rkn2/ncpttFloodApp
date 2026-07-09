# Round 1 — Offline Search Investigation

**Date:** 2026-06-25  
**Node executed:** H1 (BM25), H2 (local embeddings), H3 (precomputed/hybrid) — full sweep  
**Decision confidence:** HIGH → triggering FINAL_REPORT

## Key revelation (Opus gate finding, confirmed by code inspection)

The app's `searchKB()` (floodapp.html:1977–1992) already does offline retrieval — a raw TF scorer over 513 chunks in KB JSON. Groq is ONLY used for LLM answer generation (line 2058). The true offline gap is **answer synthesis**, not retrieval.

## Evidence gathered

### WebLLM (H2 — local embeddings via WebGPU)
- Minimum viable model: Phi-3.5-mini at 2.4 GB (smaller models give poor domain Q&A quality)
- WebGPU gate: fails on ~40–50% of likely field devices (Android < 12, all iOS < 26)
- No graceful degradation — throws immediately if WebGPU unavailable
- Cannot be bundled in single-file HTML; weights must be fetched separately
- **Verdict: DEAD — device coverage gap is disqualifying**

### wllama (H2b — WASM llama.cpp)
- Browser-compatible (WASM, no GPU needed): Chrome 92+, Firefox 79+, Safari 15.2+
- Sub-1B models (270MB–1.1GB download): 2–5 tok/s on mobile, ~40–100s for a 200-word answer
- Sub-1B quality: hallucination risk on domain-specific Q&A (Secretary of Interior Standards, FEMA programs) that professionals will act on
- **Verdict: DEAD now — quality risk too high for this domain/audience**

### Passages mode (H3 — strip LLM, show chunks directly)
- ~15 lines of JS — just a UI branch in `sendChat()` 
- Works on 100% of devices, 0 MB download, sub-10ms response
- Preservation professionals are trained to read primary documents; source attribution is actually a feature
- Risk: compound questions ("what grant programs cover masonry after floods?") may need multiple passages
- **Verdict: PROMISING — implement as offline fallback when Groq fails/unavailable**

### BM25 upgrade (H1 — replace raw TF scorer)
- Current scorer: no IDF, no saturation, re-tokenizes every chunk per query
- BM25: ~50 lines runtime JS + ~20 lines Python in build-kb.py
- IDF table adds ~100–300 KB to KB JSON (5,000–15,000 unique terms)
- Expected 20–40% NDCG@5 improvement; largest on domain queries (IDF suppresses "flood"/"damage", boosts discriminative terms like "masonry"/"dendrochronology")
- **Verdict: PROMISING — highest ROI change, do first**

## Round spend estimate: $0.02 (two subagents)
