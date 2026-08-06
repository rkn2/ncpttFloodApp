---
name: project-next-steps
description: Prioritized checklist of remaining technical and strategic tasks for floodAPp
metadata: 
  node_type: memory
  type: project
  originSessionId: 43b12481-0e79-4a85-a650-71e9fc61d011
---

## Technical (code tasks, roughly prioritized)

**✅ DONE: Offline capability** — committed 4f6258a (2026-06-25). BM25 scorer (k1=1.5, b=0.75) replaces raw TF in `searchKB()`; `build-kb.py` now computes IDF table (4589 terms) stored in `knowledge-base.json`. `sendChat()` checks `navigator.onLine` and shows top-5 BM25 passages via `appendOfflinePassages()` when offline — no Groq call, no API key needed. In-browser LLM skipped: WebLLM disqualified by WebGPU device gap; wllama quality too poor for domain Q&A professionals act on. Full research: `overnight/offline-search/FINAL_REPORT.md`.

**🔴🔴 SUPERSEDED by v2 overnight build (2026-07-09) — see [[project-v2-build]].** The API-key exposure is FIXED in code (key removed; user-key-only) but Becca must still REVOKE the leaked key `gsk_rfyOhRY9…` in the Groq console + scrub git history (still leaked there). Redeploy `deploy/` to Netlify (now includes offline PWA + cited content-bundle.json). Full handoff: `overnight/v2-build/FINAL_REPORT.md`.

**✅ FIXED: OCR for garbled KB chunks** — `build-kb.py` now does page-by-page detection of two garbling types: `(cid:)` sequences and control chars (`ord < 32`). Falls back to tesseract OCR for bad pages. Result: 513 clean chunks (was 490), 0 garbled. Requires `brew install tesseract && pip3 install pytesseract pdf2image`.

**✅ FIXED: severity button toggle** — `sel-minor` wrongly applied for `'none'`; corrected to `sel-none` at lines 1482 (template) and 1516 (runtime `setRapidSev`) in `floodapp.html`.

**✅ DONE: Named saves + export** — committed cb948a7. localStorage saves by name, auto-saves on step transitions, JSON export download, base64 share link in URL hash (#share=). 💾 button appears bottom-left after mode selected.

**🔴 KB resource library expansion** — research complete (2026-06-25); 11 priority PDFs identified to download into docs/ and rebuild KB. Full list with URLs at `overnight/resource-research/FINAL_REPORT.md`. Top pick: NPS Flood Adaptation Guidelines 2021. Awaiting Becca's go-ahead to download all Tier 1.

**🟢 No backend/persistence** — forms output to Print only; no server, no database, no audit trail.

**🟢 Platform decision** — web vs iOS vs both (undecided per 6/24 notes).

## Non-code outreach (Simeon's team action items, from 5/1 meeting notes)
- Reconnect with Jen (VT SHPO) — position app as referral tool
- Intro: Simeon's team ↔ PR SHPO contact (Morrell) — PR SHPO received ~$1M NPS grant
- Simeon → reach out to Esri re: damage classification / metadata / auto-detection collaboration
- Review OpenPointGlide (Swedish 3D tooling, FedRAMP in progress) link when sent
- Consider flood-focused PhD student (former structural engineer) for PR summer fieldwork (Penn State salary timing)

**Why:** From 2026_6_24Notes.docx (vision/requirements) and 2026_5_1_modconvo.docx (strategic meeting notes).
