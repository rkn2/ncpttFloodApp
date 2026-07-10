# floodApp v3 — Computer Vision Build: Final Report & Handoff

**Campaign:** 2 build rounds, hypothesis-gated (planned by Fable, executed by Sonnet),
each deliverable validated by an automated test recorded in a round file. **Result: the
full structural scaffolding is built and verified end-to-end on every path that doesn't
require a live Claude call. The actual accuracy questions (does this work well) are
unanswered and explicitly marked pending — not assumed.**

---

## 🔴 DO THESE FIRST (only you can — I can't)

1. **Create a fresh Anthropic API key** (a dedicated workspace is recommended) and set
   it as `ANTHROPIC_API_KEY` in the **Vercel dashboard** (Project Settings →
   Environment Variables). It must never be written to the repo or sent to the browser
   — the whole point of tonight's build is that it isn't.
2. **Set a monthly spend limit** on that Anthropic workspace. The endpoint will be
   public; this cap is the real abuse backstop (the code's own origin-check is honestly
   documented as a soft deterrent only — spoofable outside a browser).
3. **Deploy via Vercel**, git-linked to the existing GitHub remote
   (`github.com/rkn2/ncpttFloodApp.git`) — on vercel.com, "Add New Project" → import
   this repo, branch `v3-computer-vision` (or merge to main first, your call). Vercel
   auto-detects `api/vision-assess.py` as a Python function and serves the rest of the
   repo as static files — no build command needed. After deploying:
   `curl -X POST https://<your-site>/api/vision-assess` should return a JSON error
   body (confirms the function exists), not a 404.
4. **Once deployed (or with a local key), run the live tests** that couldn't run
   tonight — this is the actual validation step, not optional polish:
   ```
   cd /path/to/floodAPp
   python3 -m venv .venv && source .venv/bin/activate && pip install anthropic
   ANTHROPIC_API_KEY=sk-... python3 overnight/v3-cv-build/artifacts/test_function_local.py --live
   ```
   That runs H0b against 2–3 reference photos. H2/H3/H4 (the real accuracy questions —
   see below) need a slightly larger, hand-labeled test that wasn't built tonight
   (would need real accuracy data to be worth automating) — see "What to do next."
5. **If `deploy/` is already live on Netlify from v2**, that's fine to leave as-is —
   it doesn't need the Python function, only the new CV feature does. The Netlify
   deploy and the Vercel deploy can coexist; consolidating onto one platform is a
   reasonable v3.1 cleanup, not tonight's problem.
6. **Still outstanding from v2:** revoke the leaked Groq key. This wasn't touched
   tonight (explicitly out of scope — see PROTOCOL.md).

---

## The mid-build pivot (why this isn't what was originally planned)

You said "you should just be using python for the computer vision" partway through.
I verified (via the docs, not assumption) that Netlify Functions — the originally
planned host — only supports JavaScript/TypeScript and Go, no Python. Vercel Python
Functions are first-class and documented, and link to the same GitHub repo just as
easily. So the whole proxy moved from a Netlify JS function to a **Vercel Python
function**, using the official `anthropic` SDK instead of hand-rolled `fetch`. The
core architecture decision from earlier in the night — server-side proxy, never a
client-side key, fixed server-side prompts, structured JSON output, progressive
enhancement, critic pass — is unchanged. Full reasoning trail:
`overnight/v3-cv-build/HYPOTHESES.json` → `architecture_pivot` key.

---

## What was built and verified

### Phase 0/1 — The proxy (`api/vision-assess.py`)
A stateless Python function: image in, structured JSON out, nothing logged or
persisted. Routes on a fixed `task` enum (`facade | damage | critic`) — the client
never sends prompt text, which is what stops the endpoint from being repurposed as a
free general-purpose Claude proxy. Uses `claude-sonnet-5` with `thinking: disabled`
and `output_config.format` (json_schema) for guaranteed-valid structured output — no
regex JSON extraction needed, an improvement over the sibling llmDamagev3 research
repo's approach (which predates structured outputs on this scale).

- **H0a (local invocability):** PASS — 14/14 mock assertions, no deploy needed to test.
- **H1 (request validation):** PASS — every rejection path (bad task, oversized
  payload, missing/wrong-type image, missing critic fields, missing API key) returns
  the right status and never reaches the Anthropic API.
- **H0c (payload size):** PASS — client-side downscale (long edge ≤1568px, JPEG q0.85)
  turns even an oversized synthetic 3.75MB source photo into a 335KB base64 payload,
  well under the function's own 2MB cap.
- **H0b (live latency/schema):** PENDING-KEY — harness is written and ready
  (`test_function_local.py --live`), just needs a key to actually run.

### Phase 2/3 — Client UI (facade + damage suggestions in `floodapp.html`)
Photo upload in the Building Information step (suggests building type, construction
material, age band) and the Flood Damage step (suggests severity per category, only
for categories actually visible in the photo — never guesses at what it can't see).
Every suggestion shows a confidence badge and a one-line reason, with a checkbox
(default-checked for medium/high confidence, unchecked for low) — nothing auto-fills
without the user applying it. This mirrors the app's existing citation-hover pattern:
show *why* to trust a value, never just the value.

- **H2 (facade accuracy)** and **H3 (damage accuracy)**: PENDING-KEY. The UI and
  prompts are built; **accuracy is genuinely unvalidated** — H3 in particular is an
  honest extrapolation beyond what the sibling research validated (whole-building
  0–4 from before+after photo pairs, not per-category severity from a single
  after-only photo). Treat this as the single most important open question before
  telling anyone the damage-photo feature works.
- Scoped to homeowner mode only tonight. Assessor mode (`archStyle`, rapid-triage
  categories) isn't wired up — a straightforward follow-on.

### Phase 4 — Critic pass (`task: 'critic'`)
A second, separate model call reviews the same photo against the fields about to be
applied and flags contradictions — directly reusing the strongest finding from the
llmDamagev3 research (self-reported confidence alone wasn't a reliable trust signal;
a critic pass caught real errors). Runs in parallel with the user reading the
suggestions; on failure or timeout, suggestions stay usable and are labeled
"unverified" rather than blocking anything.

- **H4 (critic effectiveness):** PENDING-KEY. Structurally wired (parallel call,
  ✓/⚠/unverified badges, unchecks flagged fields) but not yet tested against seeded
  errors.

### Phase 5 — Degradation + deploy sync
- **H5 (progressive enhancement):** **PASS.** Verified via headless-browser
  walkthrough, not just code review: offline, the upload button is replaced by an
  "available online" note and the entire wizard remains completable by hand with zero
  CV code executing. Online-but-unreachable (the actual current state, since nothing
  is deployed yet), a real photo upload fails cleanly with a non-blocking error
  message and the manual form inputs stay fully usable throughout. Confirmed the
  service worker's fetch handler only intercepts same-origin GETs, so it never
  interferes with the POST calls.
- **`deploy/index.html` synced** from `floodapp.html` (was 299 lines stale — predates
  even yesterday's chat-FAB fix). `CACHE_VERSION` bumped `v1` → `v2` in `deploy/sw.js`
  so returning PWA users actually get the update.
- Secret scan (`pipeline/scan_secrets.py`) clean on every touched file, every round.

---

## What's NOT done (and why)

- **Live accuracy validation (H0b, H2, H3, H4, H6)** — needs `ANTHROPIC_API_KEY`,
  which doesn't exist in this environment. This is the most important remaining work
  and is explicitly *not* claimed to be validated anywhere in the code or UI copy.
- **Before/after photo comparison** — homeowners won't have pre-flood photos on hand;
  the sibling research's before-set was a research luxury, not a product reality.
- **Migrating the chat feature onto this same proxy** — the obviously-correct
  long-term move (same server-side-key pattern fixes the chat feature's own leaked-key
  history too), but it changes a working feature and doubles tonight's blast radius.
  Clean v3.1 follow-up.
- **Assessor-mode wiring** (`archStyle`, rapid triage categories) — straightforward,
  not done tonight to keep the diff reviewable.
- **Photo storage, per-IP rate limiting, Esri/Street View integration, i18n of the new
  UI strings** — all explicitly out of scope; see PROTOCOL.md for the reasoning on
  each.

## What to do next (in order)

1. Do the 6 PENDING-HUMAN items above (key, spend cap, deploy, live-test).
2. Run `test_function_local.py --live` against a handful of real photos and read the
   output by eye — is the reasoning sensible, are the confidence levels calibrated.
3. If that looks reasonable, do the fuller H2/H3/H4 tests from PROTOCOL.md (8–10
   hand-labeled facade photos, 5 hand-labeled damage photo sets, 5 seeded-error critic
   tests) — these need a human to hand-label ground truth, which is why they weren't
   automated tonight.
4. Update `HYPOTHESES.json` with the real results. If H3 (damage accuracy) doesn't
   clear its bar — especially the "zero severe called none" safety criterion — the
   plan's own fallback is to degrade that feature to affected-areas + estimated
   water-line height rather than ship an overconfident severity call. That's a
   legitimate outcome, not a failure of the night's work.
5. Only after real numbers exist, update the cost table in `V3_CV_PLAN.md` (currently
   clearly labeled as estimates) with measured `usage` data.

Everything in this campaign is designed so that "the accuracy turned out to be
mediocre" is a normal, recoverable outcome with a pre-agreed fallback — not a surprise
that requires re-architecting anything.
