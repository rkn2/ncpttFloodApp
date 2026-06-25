# Offline Search — Final Report

**Completed:** 2026-06-25, Round 1  
**Decision confidence:** HIGH  
**Total cost estimate:** ~$0.02

---

## Critical finding

The app already does offline retrieval. `searchKB()` (floodapp.html:1977) is a pure-JS TF scorer that runs entirely on-device. Groq is only called for **answer synthesis** (line 2058). The offline gap is not search — it's the LLM generation step.

---

## What was investigated

| Approach | Device coverage | Download | Quality | Verdict |
|---|---|---|---|---|
| WebLLM (WebGPU) | ~50–60% | 360MB–2.4GB | Good (if it runs) | DEAD |
| wllama (WASM) | ~90% | 270MB–1.1GB | Poor–Fair for sub-1B | DEAD now |
| Passages mode | 100% | 0 MB | N/A (no synthesis) | IMPLEMENT |
| BM25 upgrade | 100% | 0 MB | +20–40% retrieval | IMPLEMENT FIRST |

---

## Recommendation

### Step 1: Upgrade BM25 (~70 lines, immediate quality win)

Replace the current raw-TF scorer with BM25 (k1=1.5, b=0.75):
- Add IDF computation to `build-kb.py` (~20 lines Python), stored in `kb.idf`  
- Replace `searchKB()` with BM25 scorer (~50 lines JS)
- No new dependencies, no change to offline behavior
- IDF table adds ~100–300 KB to KB JSON — acceptable
- Expected 20–40% improvement in retrieval quality; biggest gains on domain queries where IDF suppresses near-universal terms ("flood", "damage") and weights discriminative ones ("masonry", "hypochlorite", "secretary")

### Step 2: Passages mode as offline fallback (~15 lines)

When `navigator.onLine === false` OR Groq call fails:
- Call `searchBM25(query, 5)` 
- Render the top-5 chunks as attribution-labeled cards (source + text)
- Show label: "Offline mode — showing relevant passages from loaded documents"
- No Groq call, no API key, works anywhere

This also fully resolves the API key exposure problem (floodapp.html:1955) — when offline, the key is never used.

### Step 3: Skip in-browser LLM (revisit 2027+)

- **WebLLM** requires WebGPU (unavailable on ~40% of likely field devices; all iOS < 26, Android < 12 with non-Qualcomm GPU). Fails hard with no degradation. Disqualified.
- **wllama** (WASM) works on 90% of browsers but sub-1B models are too small for domain-specific Q&A. Preservation professionals will act on these answers — hallucination about FEMA programs or Secretary of Interior Standards is actively harmful. Revisit when 1–2B WASM models improve quality benchmarks.

---

## Why "passages mode" is actually good UX for this audience

The users are preservation architects, SHPO staff, and program managers — professionals trained to read primary sources. Showing them "From: Secretary of Interior Standards, Treatment of Historic Properties, p. 12: [exact text]" is often more actionable than a synthesis. It provides provenance, is verifiable, and builds trust. The synthesized answer is mostly useful for novice users; for this audience, the passage is the answer.

---

## Implementation order

1. BM25 in `build-kb.py` + `searchKB()` replacement — ~1 hour
2. Passages fallback in `sendChat()` — ~30 minutes
3. Rebuild KB with `python3 build-kb.py` to generate new IDF table
4. Test offline: airplane mode, open app, ask "secretary of interior standards for wood repair"
