# PROTOCOL — floodApp v3 Computer Vision Build Campaign

## North-star goal
Add two photo-driven assist features to the Historic Flood Recovery Tool, on branch
`v3-computer-vision`:

1. **Facade photo → building suggestion** — auto-suggests Building Information fields
   (`buildingType`, `materials[]`, `age`; plus `archStyle` in assessor Full Assessment).
2. **Damage photo → severity suggestion** — auto-suggests per-category severity
   (`none|minor|moderate|severe`) for the 9 `DAMAGE_CATEGORIES` in the Flood Damage step.

Both are **progressive enhancement**: the app must work exactly as today with no photo,
no network, and no API key. Every AI-derived value is shown with confidence + reasoning
and requires an explicit user "Apply" — never a silent fill (this follows the app's
existing citation/provenance precedent: show *why* to trust a value, not just the value).

Approach validated by the sibling research repo `rkn2/llmDamagev3`: single-shot Claude
vision calls (image + fixed rubric in the system prompt) returning structured JSON with
`confidence` + `reasoning`, PLUS a second adversarial **critic** pass over the same
photo, because self-reported confidence alone was NOT reliable there — the critic caught
real errors even on medium-confidence fields.

## Architecture decision (settled — do not re-litigate)
**Server-side proxy, not bring-your-own-key.** `api/vision-assess.py` holds the real
`ANTHROPIC_API_KEY` as a platform environment variable. The browser POSTs
`{task, imageBase64, mediaType, fields?}` to its own-origin path `/api/vision-assess`
and gets structured JSON back.

> **PIVOT (mid-build):** this was originally planned as a Netlify function in
> JavaScript. Becca explicitly directed "just use python for the computer vision."
> Verified via WebFetch against Netlify's own docs (Functions overview + Lambda
> compatibility page) that Netlify Functions supports only JavaScript/TypeScript and
> Go — no Python runtime exists there. Verified via WebFetch against Vercel's docs that
> Vercel Python Functions are first-class and well documented (`api/*.py` →
> `handler(BaseHTTPRequestHandler)`, deps via `requirements.txt`, git-linked deploy to
> the same GitHub repo). Moved the whole proxy to **Vercel, in Python**. Every mention
> of Netlify/`.mjs`/`netlify.toml` below is historical — the actual deliverable is
> `api/vision-assess.py` + `api/requirements.txt`, deployed on Vercel.

- Python, using the **official `anthropic` SDK** (`pip install anthropic` via
  `api/requirements.txt`) — not raw HTTP. The original Netlify plan avoided the SDK
  specifically to dodge adding a JS build step to a zero-build-step repo; that
  constraint doesn't apply to Python (pip install at Vercel build time is normal), and
  the claude-api skill's own guidance is to prefer the official SDK over raw HTTP
  whenever one exists. This also removes llmDamagev3's regex-based JSON re-parsing
  entirely (see below).
- Model: `claude-sonnet-5` — vision-capable, high-res up to 2576px long edge,
  $3/$15 per MTok (intro $2/$10 through 2026-08-31). API notes that constrain the
  design: adaptive thinking is ON by default when `thinking` is omitted (we send
  `thinking: {type:"disabled"}` for latency-predictable extraction — H0b tests this);
  `temperature` is rejected (omit); structured outputs via `output_config.format`
  (json_schema) guarantee schema-valid JSON, no regex extraction needed.
- **Prompts live server-side.** The client sends a `task` enum
  (`facade | damage | critic`), never free-form prompt text. This is what stops the
  proxy from being a free general-purpose Claude endpoint. The chat feature's
  bring-your-own-key pattern (its own comment: "A backend proxy is the production-grade
  fix") is explicitly NOT copied — this function is the first instance of that fix.

## Why this is riskier than it looks (drives phase order)
- The repo has **no Netlify infrastructure at all** — no package.json, no netlify.toml,
  no functions dir. Whether a bare function invokes and deploys correctly is the
  riskiest unknown → Phase 0, before any UI.
- llmDamagev3 validated **whole-building 0–4 damage** (HAZUS-style) from **before+after
  photo pairs** on `claude-sonnet-4-6` via Vertex. This app needs **per-category
  none/minor/moderate/severe** from a **single after-only phone photo** on
  `claude-sonnet-5`. That is an extrapolation, not a validated result — H3 exists to
  test it, and its failure is survivable (feature ships as "suggestions for visible
  categories only" or is cut).
- Netlify synchronous functions: ~10 s default execution budget and ~6 MB request
  payload (Lambda limits). Raw phone photos are 3–12 MB and base64 inflates ×1.33 —
  client-side canvas downscale is **mandatory**, not an optimization (H0c).

## Discrepancies found while reading the code (trust the code)
1. **`deploy/index.html` is stale.** Commit `87b3936` (chat FAB / severity-button fix)
   edited only `floodapp.html`; the deployed copy still has the old markup. The
   floodapp.html → deploy/index.html sync is manual and was missed. v3 must include a
   sync step (Phase 5) and flag the existing drift to Becca.
2. **Deployment mechanism is unverified — but a git remote DOES exist.** Correction to an
   earlier draft of this plan (and to stale project memory): `git remote -v` shows
   `origin` = `https://github.com/rkn2/ncpttFloodApp.git`, reachable. There is no
   `netlify.toml`, so whether Netlify is currently git-linked to this repo (vs. an
   earlier drag-and-drop deploy that's since gone stale) is still unverified — but a
   git-linked deploy is one step away (Netlify → "Import from Git" → pick this repo) and
   is the actual recommended path now, not a distant follow-up. If the site is deployed
   by drag-and-drop instead, **functions will not ship** — Netlify Drop does not deploy
   functions. Flagged as a pending human action either way.
3. **llmDamagev3 runs `claude-sonnet-4-6` on Vertex** (`vision_client.py` line 16), not
   `claude-sonnet-5`. Its validation results carry over as *supporting evidence*, not
   proof, for the newer model.
4. **Damage scales don't match.** `damage_scale.py` is whole-building 0–4;
   `DAMAGE_CATEGORIES` is 9 categories × 4 levels keyed by water-line height per
   category. A new per-category rubric must be authored (Phase 3), reusing the
   water-line framing of the 0–4 scale descriptions.
5. **Exact enum strings matter.** Auto-fill must emit the app's literal values,
   en-dashes included (e.g. `"1870–1940"`, `"Masonry (brick / stone)"`,
   `"Commercial / mixed-use"`). Structured-output enums pin this.
6. **`designations[]` is excluded from auto-fill.** National Register status is not
   visually inferable from a facade photo; suggesting it would be fabrication.
7. **No `ANTHROPIC_API_KEY` in the local environment** and no `ant` CLI. Live-call
   hypotheses (H0b, H2, H3, H4) require a key; without one, only structural halves run
   and the live halves are recorded as PENDING-KEY, not passed.

## Metric (BUILD loop)
`readiness = (# deliverables with a PASSING automated acceptance test) / (# deliverables defined)`.
A deliverable counts ONLY when its acceptance test passes and is recorded in the round
file with the actual command + output. No partial credit. Hypotheses blocked on the
missing API key are recorded as PENDING-KEY in `LEDGER.md` — visibly incomplete, never
silently assumed true.

## Hard safety rails
1. **Never write a real API key into any file.** The function reads
   `process.env.ANTHROPIC_API_KEY` only. `scan_secrets.py` (from v2-build) must pass on
   every round.
2. **Photos are never persisted server-side.** The function is stateless: image in,
   JSON out. No logging of image bytes.
3. **App-source edits are additive & reversible.** Keep a pre-edit copy of any touched
   file in `overnight/v3-cv-build/artifacts/originals/`. Never delete user content.
   Never `git commit` or push — the orchestrating agent commits after review.
4. **No silent error sinks.** Every catch surfaces a user-visible, non-blocking message
   AND a `console.error` with the real cause. CV failure must never block manual entry.
5. **Evidence before claims** (per `~/.claude/CLAUDE.md`): state the hypothesis, run the
   test, log output, then build on it. A failed round is a valid round.
6. **CV output is a suggestion, never an assertion.** UI copy must say "suggested from
   photo — please verify"; user applies explicitly; applied values remain editable.

## Budget
Anthropic spend for testing: expected < $2 total (dozens of small vision calls at
~$0.01–0.02 each), and $0 if no key is available (structural tests only). Track actual
`usage` fields from every live response in the round files — these numbers also feed
the cost table in `V3_CV_PLAN.md` (H6).

## Round contract
MEASURE → HYPOTHESIZE (which H is cheapest to falsify next; ≥1 critique per round asking
whether we're building the right thing) → EXECUTE (additive) → VERIFY (acceptance test,
real command + output) → LOG+PERSIST (round file, LEDGER.md, HYPOTHESES.json write-back)
→ next.

---

## Phases (ordered by risk, each gated on the previous)

### Phase 0 — Proxy viability spike (riskiest unknown first; NO UI work before this passes)
Build `netlify/functions/vision-assess.mjs` as a bare handler using the modern Netlify
Functions signature (`export default async (req) => Response`, web-standard
Request/Response — directly invokable from a plain Node script, no Netlify CLI needed;
`netlify` CLI is not installed locally, confirmed).

- **H0a (structural):** The handler can be imported and invoked locally by a plain Node
  test script (`overnight/v3-cv-build/artifacts/test_function_local.mjs`) that
  constructs a `Request` and asserts on the `Response` — with the Anthropic call stubbed.
  - *Test:* `node test_function_local.mjs --mock` → asserts 200 + JSON schema for a
    valid request; 4xx for bad task / oversized payload / missing image.
  - *Pass:* all assertions green. *Fail / falsified by:* handler signature can't run
    outside Netlify's runtime → fall back to legacy `exports.handler` CJS signature and
    re-test; if that also fails, the no-CLI local-test premise is wrong and Phase 0
    escalates to installing Netlify CLI (`npx netlify-cli dev`) before proceeding.
- **H0b (live):** The same handler, given a real `ANTHROPIC_API_KEY` in env, calls
  `POST https://api.anthropic.com/v1/messages` with `claude-sonnet-5`, one test image,
  `thinking: {type:"disabled"}`, `output_config.format` (json_schema), `max_tokens` ≤ 1024,
  and returns schema-valid JSON in **< 8 s** (buffer under Netlify's ~10 s sync budget).
  - *Test:* `ANTHROPIC_API_KEY=... node test_function_local.mjs --live` against 2–3
    photos from the llmDamagev3 `ref_photos/` set; log wall-clock latency and `usage`.
  - *Pass:* valid JSON, all latencies < 8 s. *Fail:* latency ≥ 8 s → reduce max_tokens /
    image size, re-test; if still failing, redesign to Netlify background functions or
    client-direct-with-different-auth is NOT on the table — instead split critic into a
    separate invocation (already planned) and accept per-call scope reduction.
    *If no key available:* record PENDING-KEY; Phases 1–5 may still build against the
    mock, but the campaign's FINAL_REPORT must state H0b unverified.
- **H0c (payload):** A representative large photo (≥ 8 MB source), downscaled via the
  same canvas parameters the client will use (long edge ≤ 1568 px, JPEG q≈0.85),
  produces a base64 body ≤ 1.5 MB — far under the ~6 MB function payload cap — and
  ~1.6k image tokens (not the ~4.8k high-res cost).
  - *Test:* Node script with `sharp`? No — no deps. Use a browser-context check via the
    existing headless-browser walkthrough pattern (commit 87b3936 precedent), or a
    plain `sips`/`ImageMagick` resize locally to the same dimensions and measure bytes.
  - *Pass:* ≤ 1.5 MB base64. *Fail:* raise JPEG compression / drop long edge to 1200 px.

### Phase 1 — Function contract & abuse resistance
Harden the Phase 0 spike into the real function. Fixed server-side prompts per `task`
(`facade | damage | critic`); client never supplies prompt text.

- **H1:** Cheap request validation blocks the obvious misuse paths: unknown `task` →
  400; body > 2 MB → 413; missing or non-image payload → 400; `Origin`/`Referer` not in
  the site's own origin allowlist → 403 (note honestly in code comments: origin headers
  are spoofable outside browsers — this deters drive-by browser abuse only; the real
  backstop is the Anthropic workspace spend cap, a Becca action).
  - *Test:* extend `test_function_local.mjs` with one case per rejection path.
  - *Pass:* every bad request rejected with the right status, no Anthropic call made
    (assert stub not called). *Fail:* any path reaches the API → fix before Phase 2.
- Deliverable: `netlify.toml` with `[build] publish = "deploy"` and
  `functions = "netlify/functions"` so a git-linked or CLI deploy ships both.

### Phase 2 — Facade feature (Building Information auto-fill)
Client: photo `<input type="file" accept="image/*" capture="environment">` in the
Building Information step → canvas downscale → POST `task:"facade"` → suggestion panel
(value + confidence badge + one-line reasoning per field) → "Apply suggestions" writes
into the existing form inputs (checks the radio/checkboxes; `saveHwStep0()` unchanged).
Server prompt returns a json_schema-constrained object whose enums are the app's exact
strings for `buildingType`, `materials`, `age`, `archStyle` (from `ARCH_STYLES`), each
with `confidence: high|medium|low` and `reasoning`, and `null` when not inferable.

- **H2:** `claude-sonnet-5` maps facade photos to the app's exact enums with usable
  accuracy — modeled on llmDamagev3's `analyze_visual_attributes.py`, which did this
  successfully for cladding/stories/roof on Street View shots (on sonnet-4-6; carrying
  to sonnet-5 is assumed favorable but is part of what this tests).
  - *Test:* run the live function against ~8–10 photos (llmDamagev3
    `ref_photos/`/`building_details/` + a few Street View captures), hand-label the
    truth, score.
  - *Pass:* 100% schema/enum validity (guaranteed by structured outputs — assert it
    anyway) AND ≥ 7/10 correct on `materials` and `buildingType`; `age`/`archStyle`
    ≥ 5/10 with wrong answers accompanied by low/medium confidence.
  - *Fail / falsified by:* systematic enum misses (e.g. always "Mixed" materials) →
    tighten rubric with per-enum visual criteria; if age/style stays unreliable at high
    confidence, drop those fields from auto-fill and ship materials+type only.
- Explicitly NOT auto-filled: `designations[]` (not visual), `state`/`address` (typed).

### Phase 3 — Damage feature (Flood Damage auto-fill)
Client: photo input in the Flood Damage step → POST `task:"damage"` → per-category
suggestion rows → "Apply" calls the same state path `setSev()` uses (set
`state.hw.damage[key]` and re-render, so UI and state can't diverge).
Server prompt: NEW per-category rubric — for each of the 9 `DAMAGE_CATEGORIES` keys,
`{severity: none|minor|moderate|severe|not_assessable, confidence, reasoning}` —
authored by adapting `damage_scale.py`'s water-line anchors (below-floor / joist-height /
mid-wall / full-story) to each category. One photo rarely shows all 9 categories:
**only categories the model marks assessable are suggested; the rest stay untouched.**
Multiple photos accumulate (later photos may fill more categories; conflicts surface to
the user, higher-confidence wins the default).

- **H3 (the honest extrapolation):** single after-only photos support per-category
  severity suggestions at suggestion-grade accuracy. This is NOT what llmDamagev3
  validated (whole-building 0–4, before+after pairs) — treat as unproven.
  - *Test:* run against llmDamagev3 `ref_photos/after/` (5 Montpelier buildings),
    hand-label visible categories per photo, score only assessable-marked categories.
  - *Pass:* ≥ 70% exact-level agreement on assessable categories AND zero cases of
    `severe` truth suggested as `none` (the dangerous miss); over-flagging categories
    as assessable that aren't visible < 20%.
  - *Fail / falsified by:* systematic over-assessment (claiming to see interior/mold
    from an exterior shot) → rubric gets an explicit "only what is visibly in frame"
    gate + critic focus; if accuracy stays below the bar after one rubric iteration,
    ship the feature as "affected areas + water-line height estimate" only (weaker but
    honest) and record the cut.
- `affectedAreas[]` (basement/first floor/upper/exterior) is also suggested — it falls
  out of the water-line reasoning nearly for free.

### Phase 4 — Critic pass (the llmDamagev3 lesson, adapted for interactive use)
**Decision, with reason (not by default): the critic IS included**, as a second,
separate function invocation (`task:"critic"`), because (a) llmDamagev3 showed
self-reported confidence is not a sufficient trust signal — the critic caught real
errors on medium-confidence fields (`critic.py`, `critic_findings.json`), and (b) the
cost/latency math works for a single-user interactive flow: one extra ~$0.015 / ~4–6 s
call per photo, running while the user is already reading the suggestions. What is NOT
carried over: llmDamagev3's rule-based checks (geometry/collision rules don't apply
here) and its batch-all-fields sweep — the critic here reviews only the fields about to
be applied, against the same single photo.

Flow: assess call returns suggestions → UI renders them immediately marked "checking…"
→ critic call fires in parallel with the user reading → critic verdicts annotate each
field (✓ consistent / ⚠ flagged: reason) → flagged fields default to unchecked in the
Apply panel. If the critic call fails or times out, suggestions remain usable but
labeled "unverified" — the critic degrades, it never blocks.

- **H4:** the critic catches seeded errors at acceptable interactive cost.
  - *Test:* take 5 photos with known truth, deliberately corrupt 2 fields per photo
    (e.g. claim "Masonry" on a clapboard facade, claim `severe` structural on a
    water-stained-siding photo), send through `task:"critic"`, score detection.
  - *Pass:* ≥ 8/10 seeded errors flagged, ≤ 2 false flags on correct fields, latency
    < 8 s per call.
  - *Fail / falsified by:* detection < 6/10 → the critic adds latency without trust and
    is CUT for v3 (recorded, with the numbers, so the decision is revisitable); the UI
    then shows raw confidence only, with more conservative default-unchecked behavior
    for medium/low confidence.

### Phase 5 — Degradation, sync, and handoff
- Offline gate mirroring `sendChat()`: if `!navigator.onLine`, the photo-assist UI
  renders a one-line "available online" note instead of the button; nothing else
  changes. Proxy-error path: non-blocking inline message, manual entry untouched.
  - **H5 test:** headless-browser walkthrough (the repo's established verification
    pattern) with network disabled: both steps fully completable manually, no console
    errors, no CV UI. *Pass:* walkthrough clean. *Fail:* any blocked path is a P0 bug.
- Sync `floodapp.html` → `deploy/index.html` (and note the pre-existing 87b3936 drift);
  update `deploy/sw.js` `CACHE_VERSION`; confirm the service worker ignores the
  function path (it only handles same-origin **GET**s — verified in `deploy/sw.js`; the
  function is POST, so it passes through untouched — assert this in the walkthrough).
- Write `FINAL_REPORT.md` with the PENDING-HUMAN list (below) at the top, v2-style.

---

## Explicitly OUT of scope tonight (each with the reason)
- **Before/after photo comparison** — homeowners won't have pre-flood photos in hand;
  llmDamagev3's before-set was a research luxury. Single-photo is the product reality.
- **Migrating the chat feature onto the proxy** — right long-term move (same pattern,
  same key), but it changes a working feature and doubles blast radius tonight. Noted
  as the obvious v3.1 follow-up in the plan.
- **Photo storage / server-side history** — privacy + statelessness; photos are
  transient request payloads only.
- **Street View / Esri auto-capture, geocoding** — external partnership dependency
  (same reason v2 excluded P3).
- **Rate limiting with state (per-IP quotas)** — needs a datastore; the spend-cap +
  origin-check + payload-cap combination is the honest tonight-sized mitigation, and
  the residual risk is documented rather than hidden.
- **Fine-tuning / local models** — the single-shot + critic pattern is the validated
  approach; anything else is research, not a build.
- **i18n of the new CV UI beyond routing strings through `t()`** — Spanish table entries
  deferred with the rest of D2.3.

## Stop conditions
- All phases' deliverables pass (or are PENDING-KEY with everything else green).
- H0a fails in both handler styles → campaign stops at an infrastructure report.
- H2 AND H3 both fail their fallbacks → CV is not suggestion-grade; write up the
  negative result honestly (that is a valid research outcome for this grant).
- 3 consecutive rounds without a new passing deliverable or viable hypothesis.

## PENDING-HUMAN (Becca) — cannot be done by the agent, flagged v2-style
(Updated for the Netlify → Vercel/Python pivot above.)
1. **Create a fresh Anthropic API key** (dedicated workspace recommended) and set it as
   `ANTHROPIC_API_KEY` in the **Vercel dashboard** (Project Settings → Environment
   Variables). It is never written to the repo or the browser.
2. **Set a monthly spend limit** on that Anthropic workspace — this is the real abuse
   backstop for a public endpoint.
3. **Deploy via Vercel**, git-linked to the existing GitHub remote
   (`origin` → `github.com/rkn2/ncpttFloodApp.git`) — Vercel → "Add New Project" →
   import this repo. Vercel auto-detects `api/*.py` as Python functions and serves the
   rest of the repo as static files; no build command needed. Verify after deploy:
   `curl -X POST https://<site>/api/vision-assess` returns a 4xx JSON error (not 404).
4. (Optional, unblocks live testing pre-deploy) provide `ANTHROPIC_API_KEY` in the local
   build environment so H0b/H2/H3/H4/H6 can run live instead of PENDING-KEY.
5. Still outstanding from v2: **revoke the leaked Groq key**.
6. **Netlify vs. Vercel:** if `deploy/` (the offline-PWA build) is already live on
   Netlify from v2, that can stay as-is — it doesn't need the Python function. Only the
   CV proxy needs Vercel. If simplifying to one platform is preferred long-term, that's
   a v3.1-scale decision, not tonight's.
