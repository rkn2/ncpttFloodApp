# Round 02 — Phases 2/3/4/5: client wiring, critic, degradation, deploy sync

## MEASURE
Starting state: proxy function structurally verified (H0a/H1/H0c pass), pushed to
`v3-computer-vision`. No client UI existed yet.

## HYPOTHESIZE
Cheapest-to-falsify next, key-independent: the client wiring itself (does it render,
does it fail gracefully) and H5 (offline/error degradation) — all fully testable via
the repo's established headless-browser pattern without any live Claude calls. H2/H3/H4
accuracy remain gated on a key and stay pending-key; building their UI scaffolding is
still worthwhile because it's independently useful (structurally correct regardless of
what the eventual live numbers turn out to be) and is exactly what the advisor
recommended avoiding *over-polishing*, not avoiding building at all.

**Critique asked:** is the per-field checkbox + critic-badge UI proportionate, or
over-built for a night with no live validation? Decision: keep it — the checkbox
default (unchecked for low-confidence, checked for medium/high) and the critic-flag
override are cheap to build now and directly implement the plan's stated safety
posture ("never a silent fill", flagged fields default unchecked). Cutting them would
mean re-adding them later specifically once real accuracy data existed, which is
backwards — the safety scaffolding shouldn't wait on the accuracy data being good.

## EXECUTE
- Added the CV client module to `floodapp.html` (after `ARCH_STYLES`, before `APP
  STATE`): `downscaleImageFile()` (canvas resize to long edge ≤1568px, JPEG q0.85 —
  matches H0c's tested parameters exactly), `callVisionAssess()` (fetch wrapper to
  `/api/vision-assess`), facade and damage handlers (`handleFacadePhoto`,
  `handleDamagePhoto`), suggestion renderers with per-field checkboxes defaulting
  checked/unchecked by confidence, `applyFacadeSuggestions`/`applyDamageSuggestions`
  (write into `state.hw` via the existing fields, then re-render the step — same
  pattern `saveHwStep0`/`setSev` already use), critic wiring (`runFacadeCritic`/
  `runDamageCritic`, fires in parallel with the user reading suggestions, annotates
  each field with ✓/⚠/`(unverified)`), and offline gating (`cvOfflineNoteHtml`,
  checked via `navigator.onLine` exactly like `sendChat()`).
- Scoped to homeowner mode only tonight (Building Information + Flood Damage steps) —
  assessor mode's `archStyle`/`RAPID_DAMAGE_CATS` are not wired up; noted as a
  follow-on, not silently dropped.
- Added `.cv-*` CSS next to the existing severity-button mobile styles.
- Inserted `facadePhotoAssistHtml()` into `showHwStep0()` and `damagePhotoAssistHtml()`
  into `showHwStep1()`.

## VERIFY
Headless-browser walkthroughs (Playwright, same pattern as commit 87b3936):

**Online, panels render (desktop 1280px):**
```
FACADE PANEL HTML: <label class="cv-upload-btn" ...>📷 Take or upload a photo...
DAMAGE PANEL HTML: <label class="cv-upload-btn" ...>📷 Take or upload a photo...
CONSOLE ERRORS (online): ["...404... fetching the script."]   # pre-existing sw.js-in-dev
                                                                 non-issue, not CV-related
```
Screenshots confirm both panels sit cleanly in the existing form flow with no layout
breakage (`overnight/v3-cv-build/artifacts/` — see chat transcript for the two
screenshots reviewed).

**Offline (H5, first half):** `context.setOffline(true)` before entering the wizard.
```
FACADE AREA (offline): shows offline note (no upload button)
OFFLINE: reached results page manually: true
CONSOLE ERRORS (offline walkthrough): ["...404... fetching the script."]  # same
                                                                             pre-existing non-issue
```
Full Building Information → Flood Damage → Results walkthrough completed by manually
selecting radios/checkboxes/severities, exactly as a real offline user would, with zero
CV code executing.

**Online but function unreachable (H5, second half — the actual current real-world
state, since nothing is deployed to Vercel yet):** uploaded a real 1×1 JPEG via
`setInputFiles`. The local Python dev server has no route for `/api/vision-assess`
(and rejects POST outright — no JSON API to hit locally without deploying), so the
fetch failed with HTTP 501:
```
FACADE PANEL AFTER FAILED CALL: <p class="cv-error">Couldn't analyze that photo
(HTTP 501). You can still fill the form in manually.</p>
Manual form still usable: true
```
Non-blocking, no crash, no dangling "Analyzing…" state, manual radio/checkbox inputs
stayed enabled the whole time. **H5: PASS**, both halves.

**Deploy sync:** `diff floodapp.html deploy/index.html` before this round showed
`deploy/index.html` was 299 lines shorter (stale since before yesterday's chat-FAB fix
and before all of tonight's work). Diffed to confirm `deploy/index.html` had no
deploy-specific content of its own (every difference was strictly older/superseded
content, not a customization) before overwriting with `cp floodapp.html
deploy/index.html`. Bumped `CACHE_VERSION` in `deploy/sw.js` (`v1` → `v2`) so returning
PWA users actually get the update instead of being stuck on the stale cached shell.
Confirmed by reading `deploy/sw.js`'s fetch handler directly: it only intercepts
same-origin **GET** requests (`if (req.method !== 'GET' || url.origin !==
self.location.origin) return;`) — the vision-assess calls are same-origin POSTs, so
they pass through the service worker untouched, exactly as the plan assumed.

Secret scan (`pipeline/scan_secrets.py`) run on all touched files: clean.

## LOG+PERSIST
- `HYPOTHESES.json`: H5 → pass, with evidence.
- This round's commit bundles Phases 2–5's client work + deploy sync together (the
  client UI isn't independently meaningful without the offline/error handling that
  makes it safe to ship, so they land as one reviewable unit).

## What's left (see FINAL_REPORT.md for the full handoff)
Everything requiring a live Claude call — H0b, H2, H3, H4, H6 — is built and ready to
run but cannot be validated without `ANTHROPIC_API_KEY`. This is the honest stopping
point for tonight: the scaffolding is solid and tested end-to-end on every path that
doesn't need a key; the actual "does this work well" question is unanswered and must
not be assumed answered.
