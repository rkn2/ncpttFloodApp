---
name: project-rag-pipeline
description: "Status and bugs found/fixed in floodAPp's RAG knowledge-base pipeline (build-kb.py)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 43b12481-0e79-4a85-a650-71e9fc61d011
---

Both blocking bugs in `build-kb.py` were found and fixed (commit 8dc6901):

1. `chunk()` had an infinite-loop bug: once the sliding window reached the final chunk, `start = end - OVERLAP` became a fixed point and looped forever, SIGKILL-ing every run via OOM. Fixed with a `break` when `end >= len(text)`.
2. `pdfplumber`/`pdfminer` produced 100% unreadable `cid:` glyph codes for `docs/secretary for interior.pdf` (custom font subset, no ToUnicode CMap). Switched to `pdftotext` (poppler) via subprocess — correctly decodes the body text.

**Why:** `knowledge-base.json` had never successfully been built before these fixes.

**How to apply:** `python3 build-kb.py` now completes in ~6 seconds and produces 490 usable chunks. Run from repo root (`/Users/becca/Code/floodAPp`). `knowledge-base.json` is gitignored (local build artifact).

**OCR fallback added (2026-06-25):** `build-kb.py` now extracts page-by-page and OCRs pages where `(cid:` ratio > 3% OR non-whitespace control chars > 3% of text. 62/148 secretary PDF pages OCR'd. Result: 513 chunks, 0 garbled. Deps: `tesseract` (brew) + `pytesseract`, `pdf2image` (pip).
