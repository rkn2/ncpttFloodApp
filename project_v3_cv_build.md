---
name: project-v3-cv-build
description: "floodApp v3 computer vision — PIVOTING away from the Claude-vision proxy to non-LLM Python CV; original LLM proxy status (Vercel/API key) below is superseded, see project-v3-nonllm-cv"
metadata:
  type: project
  originSessionId: 068ccfb5-c8ea-4e77-9996-ba29d67774ce
---

🔴 SUPERSEDED (2026-07-10): Becca decided against using an LLM for the CV
feature at all — "don't want you to use LLM for the CV, just use my python
scripts." The Vercel/ANTHROPIC_API_KEY plan below is on hold pending that
pivot. See [[project-v3-nonllm-cv]] for the replacement approach and status.

Overnight autonomous build on branch `v3-computer-vision` (pushed to origin), adding
two photo-based AI suggestion features to the homeowner flow: facade photo → building
type/materials/age, and damage photo → per-category severity. Full trail:
`overnight/v3-cv-build/` (PROTOCOL.md, HYPOTHESES.json, rounds/round_0N.md,
FINAL_REPORT.md).

## 🔴 URGENT human actions (could not do these unattended)
- **Create an Anthropic API key**, set as `ANTHROPIC_API_KEY` in the **Vercel**
  dashboard (Project Settings → Environment Variables) — never in the repo/browser.
- **Set a monthly spend limit** on that Anthropic workspace (the real abuse backstop
  for a public endpoint — the code's own origin-check is an honest soft deterrent only).
- **Deploy via Vercel**, git-linked to `github.com/rkn2/ncpttFloodApp.git`. Vercel
  auto-detects `api/vision-assess.py` as a Python function; no build config needed.
- **Run the live accuracy tests** (H0b/H2/H3/H4/H6 in HYPOTHESES.json) — none of these
  could run without a key. This is the actual "does it work" validation, not done yet.
- Still open from v2: **revoke the leaked Groq key**.

## Architecture — and a mid-build pivot worth remembering
Server-side proxy (never bring-your-own-key): `api/vision-assess.py` holds the real
key, routes on a fixed `task` enum (facade|damage|critic), prompts live server-side
only, structured JSON output via `output_config.format`. Model: `claude-sonnet-5`.

**Originally planned for Netlify (JS).** Becca said "just use python for the computer
vision" mid-build. Verified via WebFetch that Netlify Functions only support JS/TS/Go
— no Python runtime exists there. Moved the whole proxy to **Vercel Python
Functions** (`api/*.py`, `handler(BaseHTTPRequestHandler)`, deps via
`api/requirements.txt`), using the official `anthropic` Python SDK. See
[[feedback-verify-platform-before-committing]].

## What's built and verified (structural — no live key needed)
- H0a (local invocability, no deploy needed), H1 (request validation blocks bad input
  before it reaches the API), H0c (client-side downscale to ≤1568px/q0.85 keeps
  payloads ~335KB, well under limits) — all PASS with evidence in round_01.md.
- H5 (progressive enhancement: offline → no CV UI, wizard fully manual; online but
  proxy unreachable → non-blocking error, manual entry stays usable) — PASS, verified
  via the same headless-Playwright pattern established for the UI-fix commit.
- Client UI: photo upload + suggestion panels with confidence badges, per-field
  checkboxes (default-unchecked for low confidence), and a parallel "critic" call that
  flags contradictions before suggestions are trusted — reusing the strongest finding
  from the sibling `rkn2/llmDamagev3` research repo (self-reported confidence alone
  wasn't reliable there).
- `deploy/index.html` synced from `floodapp.html` (was 299 lines stale) and
  `CACHE_VERSION` bumped in `deploy/sw.js`.
- Scoped to homeowner mode only; assessor mode (`archStyle`, rapid triage) not wired.

## What's NOT validated — treat as unknown, not assumed-good
H0b (live latency/schema), H2 (facade accuracy), H3 (damage accuracy — an **honest
extrapolation**: the sibling research validated whole-building 0-4 from before+after
photo pairs, not per-category severity from a single after-only photo), H4 (critic
effectiveness), H6 (real cost) are all PENDING-KEY. Do not tell anyone the CV feature
"works" until these run for real. H3 in particular has a hard safety bar in its plan
(zero tolerance for calling true-severe damage "none") that hasn't been tested yet.

Also came out of this build: a UI bug fix (floating chat button was overlapping
content; severity buttons overflowed on mobile) — committed separately, see
[[project-v2-build]] for that lineage. And a corrected discrepancy: earlier project
memory said "no GitHub remote yet" — that was stale; the repo has had
`origin → github.com/rkn2/ncpttFloodApp.git` for a while.

See also [[project-v2-build]] [[project-rag-pipeline]] [[project-structure]]
[[project-stakeholders]] [[feedback-verify-platform-before-committing]]
[[feedback-autonomous-authorization]].
