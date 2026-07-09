# Deliverables Ledger — floodApp v2 Build

A deliverable counts as DONE only with a passing automated acceptance test recorded in a round file.

| ID | Phase | Deliverable | Acceptance test | Status | Round | Evidence |
|----|-------|-------------|-----------------|--------|-------|----------|
| D0.1 | P0 | Leaked Groq key removed from all working files | real key `gsk_rfyOhRY9…` absent from working tree (excl git history) | **DONE** | 1 | round_01.md |
| D0.2 | P0 | Chat uses only user-supplied key (no default) | `getGroqKey()` = localStorage `\|\| ''`, no fallback; +offline-first reorder | **DONE** | 1 | round_01.md |
| D0.3 | P0 | Secret-scan guard script | `scan_secrets.py --self-test` PASS; full-tree scan CLEAN | **DONE** | 1 | round_01.md |
| D0.4 | P0 | Citations added to existing hardcoded guidance | 6/9 categories now render verified citations via bundle; 3 safety-critical deferred to human authoring | PARTIAL | 5 | round_05.md |
| D1.1 | P1 | Deterministic pipeline (extract+retrieve+schema) | extract.py+retrieve.py+guidance_schema.py all self-test PASS; SOI garbled resolved via corpus.py | **DONE** | 3 | round_03.md |
| D1.1b | P1 | Extraction + per-PDF fidelity precheck | `extract.py` caches text + flags garbled PDFs (found SOI garbled) | **DONE** | 2 | round_02.md |
| D1.2 | P1 | Citation verifier | `verify_citations.py` self-test PASS + end-to-end PASS on real PDF | **DONE** | 2 | round_02.md |
| D1.3 | P1 | content-bundle.json (first real cited bundle) | 5 records (43 items, 49/49 citations) through 3 gates (verify+entailment+flood-relevance); 4 held for human authoring | **DONE** | 4,8 | round_04.md, round_08.md |
| D1.4 | P1 | App reads content-bundle (graceful) | JS syntax OK; node logic test PASS (cited render + fallback); HTTP serves bundle | **DONE** | 5 | round_05.md |
| D2.1 | P2 | PWA manifest + service worker | manifest+sw valid; SHELL covers all fetches; all assets 200; *1 manual browser offline-check pending | **DONE*** | 6 | round_06.md |
| D2.2 | P2 | i18n string externalization + switcher | t()+I18N table+switcher; node test PASS (100% coverage, en fallback, es renders) | **DONE** | 7 | round_07.md |
| D2.3 | P2 | Spanish (homeowner flow) | entry/welcome screen fully renders in es (verified); deeper flow externalization = follow-on | PARTIAL | 7 | round_07.md |

Readiness: 9 / 11 core = 0.82  (+1 bonus D1.1b; D0.4 & D2.3 partial)  (updated round 7)
