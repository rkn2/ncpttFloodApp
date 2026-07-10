# v3 Plan — Computer Vision Photo Assist (for Becca)

*Companion to `overnight/v3-cv-build/PROTOCOL.md` (the full hypothesis-tested build plan)
and `HYPOTHESES.json` (the falsifiable claims). This is the short human version.*

---

## What's being built

Two photo features for the homeowner flow, both **assistive, never automatic**:

1. **"Take a photo of the front of your building"** on the Building Information step.
   Claude vision suggests Building Type, Construction Material, and Age band (and
   Architectural Style in the assessor's Full Assessment), each with a confidence badge
   and a one-line reason ("brick coursing and stone lintels visible → Masonry"). The
   user taps **Apply** to fill the form — or ignores it entirely. Historic designation
   is deliberately *not* suggested: you can't see a National Register listing in a photo,
   and pretending otherwise would undermine the tool's credibility.

2. **"Take a photo of the damage"** on the Flood Damage step. Claude suggests a
   severity (None / Minor / Moderate / Severe) for whichever of the 9 damage categories
   are actually visible in the photo, plus the affected areas — and explicitly declines
   the categories it can't see. Multiple photos accumulate.

Every suggestion is double-checked by a second, adversarial "critic" AI pass against the
same photo before it's trusted — this comes straight from your llmDamage research, where
the critic caught real errors the model's own confidence rating missed. If the critic
flags a field, it shows a warning and is unchecked by default.

This mirrors what the app already does with citations: never show an AI-derived value
without showing *why* to trust it.

## Why this architecture (and why not the chat pattern)

The chat feature makes users paste their own Groq key into the browser — its own code
comment calls a backend proxy "the production-grade fix," and we've already had one key
leak from the client-side pattern. The CV feature is where that fix finally gets built:

- A tiny **Python serverless function** (`/api/vision-assess`, deployed on Vercel)
  holds the real Anthropic API key as a platform environment variable. The key never
  reaches the browser, never enters the repo.
  *(Note: this was originally scoped for Netlify, but Netlify Functions only support
  JavaScript and Go — no Python. You said to use Python for the CV part, so this moved
  to Vercel, which has first-class Python function support and links to the same
  GitHub repo just as easily.)*
- The browser sends only a photo and a task name; **all prompts live server-side**, so
  the endpoint can't be repurposed as a free general-purpose AI proxy.
- Photos are never stored — image in, JSON out, stateless.
- One new dependency, scoped to the function only: the official `anthropic` Python
  package (`api/requirements.txt`). The app itself stays a single HTML file.
- Model: **claude-sonnet-5** (current Sonnet, vision-capable).
- Offline (the app's core scenario): the photo button simply doesn't appear, exactly
  like the chat's offline behavior today. Everything stays fillable by hand.

## The cost story (grant-credible numbers)

claude-sonnet-5 pricing: $3 per million input tokens / $15 per million output tokens
(intro pricing $2/$10 through Aug 2026). Photos are downscaled in the browser before
upload, which keeps each image around 1,600 tokens.

| Call | Est. cost |
|---|---|
| Facade analysis (1 photo) | ~$0.012 |
| Damage analysis (per photo) | ~$0.012–0.015 |
| Critic check (per photo) | ~$0.015 |
| **Typical assessment** (1 facade + 2 damage photos + critics) | **≈ $0.07** |
| Worst case (5 photos, all critiqued) | ≈ $0.20–0.30 |

So ~500 fully CV-assisted assessments ≈ **$35–50**. These are estimates; the build
measures actual token usage on every test call (hypothesis H6) and the final report will
replace this table with measured numbers. A monthly spend cap on the Anthropic account
(see your to-do list below) makes the worst case bounded no matter what.

## How the build is run (the hypothesis discipline)

Every risky assumption is written down as a falsifiable hypothesis with a cheap test
*before* anything is built on top of it — same loop convention as the v2 overnight
build. The two that matter most:

- **Phase 0 tests the scariest unknown first:** can a bare Netlify function, with no
  dependencies and no Netlify CLI, be invoked locally and successfully round-trip a real
  Claude vision call in under Netlify's ~10-second limit? No UI gets built until this
  passes.
- **The damage feature is honestly labeled an extrapolation.** Your research validated
  whole-building 0–4 damage from before+after photo pairs; the app needs per-category
  severity from a single "after" photo. Hypothesis H3 tests that gap against your
  Montpelier reference photos with a hard safety bar: zero tolerance for calling truly
  severe damage "none." If it can't clear the bar, the feature degrades to something
  weaker but honest (affected areas + water-line height) rather than shipping
  overconfident.

Everything cut or scaled back gets recorded with the measured numbers, so decisions are
revisitable rather than silent.

## What YOU need to do (the agent can't do these)

1. **Create a fresh Anthropic API key** — ideally in its own workspace — and add it in
   the **Vercel dashboard**: Project Settings → Environment Variables →
   `ANTHROPIC_API_KEY`. This is the same class of action as "revoke the Groq key" from
   the v2 handoff: only you have the dashboard access.
2. **Set a monthly spend limit** on that Anthropic workspace. The endpoint is public;
   this cap is the real backstop.
3. **Deploy via Vercel.** The repo already has a GitHub remote
   (`github.com/rkn2/ncpttFloodApp.git`) — on vercel.com, "Add New Project" → import
   this repo. Vercel auto-detects the Python function in `api/` and serves the rest of
   the repo as static files; no build command or extra config needed. After deploying:
   `curl -X POST https://<your-site>/api/vision-assess` should return a JSON error
   (good — the function exists), not a 404.
4. **(Optional but helpful)** drop an `ANTHROPIC_API_KEY` into the local environment
   before the overnight run so the accuracy tests (H2/H3/H4) can run live instead of
   being marked "pending key."
5. **Still open from v2:** revoke the leaked Groq key.
6. If `deploy/` is already live on Netlify from v2, that's fine to keep — it doesn't
   need the Python function. Only the new CV feature needs Vercel. Consolidating onto
   one platform later is a reasonable v3.1 cleanup, not something done tonight.

## Things found while planning (worth 30 seconds of your attention)

- **`deploy/index.html` is out of date** — yesterday's chat-button/mobile fix landed in
  `floodapp.html` but the deployed copy wasn't synced. The v3 build will sync it, but
  the manual-sync convention is fragile; a git-linked Netlify deploy would remove this
  whole class of drift.
- Your llmDamage validation ran on the previous Sonnet model (4.6, via Vertex); carrying
  the results to sonnet-5 is reasonable but is re-verified rather than assumed.
- **Deliberately not tonight:** migrating the chat feature onto this same proxy (right
  move, but it touches a working feature — clean v3.1 follow-up), photo storage of any
  kind, Esri/Street View auto-capture, and per-IP rate limiting (needs a datastore; the
  spend cap covers the risk honestly).
