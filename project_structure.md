---
name: project-structure
description: "floodAPp codebase layout, key facts, and how to run the app locally"
metadata: 
  node_type: memory
  type: project
  originSessionId: 43b12481-0e79-4a85-a650-71e9fc61d011
---

**Repo:** `/Users/becca/Code/floodAPp` — "Historic Flood Recovery Tool" prototype, single `main` branch.

**Key files:**
- `floodapp.html` (~93KB) — the entire app, single-file. Homeowner mode (3 steps) + Assessor mode (Rapid Triage + Full Assessment). RAG chat widget at bottom-right (floating). JS functions: `loadKB()`, `searchKB()`, `buildSystemPrompt()`, `sendChat()` for the chat/RAG flow.
- `build-kb.py` — builds `knowledge-base.json` from files in `docs/`. Run: `python3 build-kb.py` from repo root. Deps: `pdftotext` (brew install poppler) + python-docx (pip). Output is gitignored.
- `docs/` — drop source PDFs/TXT/DOCX/MD here, then run build-kb.py. Currently contains two reference PDFs: "Secretary of the Interior's Standards for Rehabilitation" and "Treatment of Flood Damaged Historic Buildings".
- `requirements.txt` — only `python-docx` (pdfplumber was dropped in favor of pdftotext).
- `knowledge-base.json` — gitignored, built locally, 490 chunks from 2 docs (as of 2026-06-25).

**How to run locally:**
```bash
python3 build-kb.py          # rebuild KB (needed after changing docs/)
python3 -m http.server 8000  # serve app
# then open http://localhost:8000/floodapp.html
```
Note: must use HTTP (not file://) — browser blocks fetch() of local JSON under file:// protocol.

**GitHub remote:** `https://github.com/rkn2/ncpttFloodApp` — pushed 2026-06-25.

**GROQ_API_KEY** at `floodapp.html:1955` is a placeholder (`gsk_PASTE_YOUR_KEY_HERE`). Chat completions won't work until a real key is provided — but KB load and retrieval work fine without it.
